---
title: 'eXpOS Abstractions'
original_url: 'http://eXpOSNitc.github.io/os_spec-files/expos_abstractions.html'
hide:
    - navigation
---

eXpOS provides the following fundamental abstractions to an application program:

1. The eXpFS logical file system
2. The process abstraction for programs in execution
3. Methods of resource sharing
4. Primitives for concurrent access control and process synchronization
5. The system call interface that specifies the interface through which application programs can invoke the system calls and access the OS services.
6. The extended eXpOS specification provides a user abstraction as discussed here.


### The eXpFS logical file system

The eXpOS kernal provides a hardware independent logical file system model (called the **experimental file system or eXpFS**) for application programs. The application program views files as being organized and stored in the eXpFS logical file system. Application programs are not permitted to access files directly. Instead, they must invoke the appropriate **file system call** for creating, modifying or accessing files. The OS routine implementing each system call internally translates the request into disk block operations, hiding the hardware details from the application program.


eXpFS support three kinds of files - **data files, program files**  (executable files) and a special file called the **root file.**  The root file is a meta-data file that contains the list of all files in the file system. A data file consists of a sequence of words. A program contains a header, a sequence of machine instructions called text and static data, if any. 


eXpOS does not provide any mechanisms for application programs to create **executable files**. Executable files have to be pre-loaded into the disk using some other external disk access mechanism before OS bootstrap. Since such mechanisms are implementation dependent, they are not part of the OS specification. For instance, the [XFS-Interface](../support-tools/xfs-interface.md) tool for eXpOS implementation on the XSM machine is one such mechanism. 


Executable files follow certain format called the **[experimental executable format or XEXE format](../abi.md#xexe)**. The OS will execute only program files stored in the file system in the XEXE format. Hence system programs like compilers that translate high level application programs must ensure that the executable files adhere to the XEXE format. 


Application programs can create, modify and delete data files using appropriate OS system calls. These are discussed [here](systemcallinterface.md).


A detailed discussion of the file system structure, file system calls and XEXE format is given in [Section 3](expfs.md).



### The eXpOS process Abstraction

It was noted earlier that at the end of bootstrap, eXpOS loads into memory a program stored in a pre-determined part of the disk and creates the first process called the INIT process. Once a process is created, it can spawn new processes using the **fork**  system call. When a process spawns a new process, the former is called the **parent process** and the later is called the **child process**. A process can decide to terminate itself using the **exit** system call. 


 * In the extended eXpOS specification, the INIT process is called the LOGIN process and is executed directly by the kernel. This process invokes the login system call to log a user in. Once a user is logged in, the shell process is created for the user and the original login process waits for the termination of the user shell, to log in the next user. 


Associated with each process, there is a (virtual) address space (or logical memory space). This address space is a sequence of memory locations, each of which can store a word. eXpOS logically divides the address space of a process into four regions - **(shared) library, code, stack and heap**. 


When a process is created using the fork system call, the OS creates a virtual address space for the new process. Each process is given a view that it has its own virtual address space containing its code, library, stack and heap. The virtual address space is a continuous address space starting from address 0 up to a maximum limit that is implementation dependent. Internally, the OS maps the virtual address space into the machine memory using hardware mechanisms available in the machine like paging/segmentation.( Check mapping implementation in XSM [here](../arch-spec/paging-hardware.md))


The code region of a process contains the machine instructions that are to be executed. This code consists of instructions stored in some executable file in the file system. When a new process is created using the fork system call, *the child process shares the library, code and heap with the parent*. This means that any modifications to memory words in these regions by one process will result in modification of the contents for both the processes. The stack region of the parent and the child will be separate. The parent and the child concurrently proceeds execution from the instruction immediately following the fork system call in the code. 


The stack region of a process stores the variables and stack frames during the execution of the program. Since our implementation of eXpOS does not explicitly provide an area for storing static data, they are stored on the stack. Dynamic memory allocation is normally done from the heap region. Variables to be shared between different processes could also be allocated in the heap. Finally all (standard) library code (which is typically shared by all applications) is mapped to the library region. 


A process can load an XEXE executable file from the file system into the virtual address space (of the calling process) using the **exec** system call. During loading, the original code and stack regions are overlayed by those of the newly loaded program. If the original process had shared its heap with its parent process (or any other process), the OS ensures that other processes do not lose their shared heap data. Finally, the (shared) library is common to every application. 


The OS expects that executable files respect the programming conventions laid down by the OS (defined in the **[Application Binary Interface-ABI](../abi.md)**) like the division of memory into stack, code, heap and library. Each XEXE executable file must have a header which specifies how much size must be allocated by the OS for each region when the program is loaded for execution. Application programs are typically written in high level languages like [ExpL](../support-tools/expl.md) and eXpOS expects the compiler to generate code respecting the ABI specification. 


It must be noted here that an application program is free to violate the ABI conventions and decide to use its virtual address space in its own way. It is only required that the executable file follows XEXE format in order to ensure that exec system call does not fail. As long as such a process operates within its own address space, the OS permits the process to execute. However, if at any point during its execution, the process generates a virtual address beyond its permitted virtual address space, a hardware exception will be generated and the OS routine handling the exception will terminate the process. 


### Access Control and Synchronization

Two concurrently executing processes sharing resources like files or memory (for example, parent and child processes sharing the heap) would like to ensure that only one of them execute critical section code that access/modify a resource that is shared between them. 


A classical solution to this problem is using [semaphores](http://en.wikipedia.org/wiki/Semaphore_%28programming%29). A process can acquire a semaphore using the **Semget** system call and share it with its child (or later generation) processes. A semaphore can be locked by any of these sharing processes using the **SemLock** system call and the execution of all other processes trying to lock the same semaphore subsequently will be suspended (**blocked**) by the OS until the locking process unlocks the semaphore using the **SemUnlock** system call. 


The **Wait** system call allows a process to suspend its own execution until another process wakes it up using the **Signal** system call. This primitive is useful when a process must be made to wait at a point during its execution until another related process signals it to continue.


### Resource Sharing in eXpOS


It was already noted that the child process shares the **heap** of the parent process. Hence memory allocated in the heap will be a **shared memory** between both the processes. However, if either the parent or the child process loads another program into its virtual address space using the exec system call, then the shared heap is detached from that process and the surviving process will have the heap intact. The file pointers handled by the parent process are also shared by the child process.


Thus, eXpOS does not support any explicit primitives for memory sharing, but instead allows related processes to share these resources implicitly using the fork system call semantics. 


The file sharing semantics between users in Multiuser extension to eXpOS is described [here](multiuser.md).


 

### System Calls

The eXpOS system calls are software interrupt routines of the eXpOS kernal which are loaded into the memory when the OS is bootstrapped. These routines define the services provided by the OS to application programs. These services include accessing files and semaphores, creating new processes , sending a signal to another process etc. 


Application programs are not permitted to directly access files/semaphores or create new processes. Instead they must invoke the corresponding system call routines. System calls are kernal routines and operate in **privileged or system mode**. Thus when an application program invokes a system call (by invoking the corresponding software interrupt), a change of mode from unprivileged mode to privileged mode occurs. The system call code checks whether the request is valid and the process has permission to the resources/actions requested and then perform the request. Upon completion of the interrupt service routine, control is transferred back to the user process with a switch back to the unprivileged mode. 


eXpOS system calls can be classified as file system calls, process system calls and system calls for access control and synchronization. The following table lists the system calls. A detailed specification can be found [here](systemcallinterface.md).


#### [File system calls](./systemcallinterface.md)

| Name   | Description                                                                                                               |
| ------ | ------------------------------------------------------------------------------------------------------------------------- |
| Create | Create an eXpFS file                                                                                                      |
| Delete | Delete an eXpFS file                                                                                                      |
| Open   | Open an eXpFS file and return a file handle to the calling process                                                        |
| Close  | Close an eXpFS file already opened by the calling process                                                                 |
| Read   | Read one word from the location pointed to by the file pointer and advance the file pointer to the next word in the file  |
| Write  | Write one word from the location pointed to by the file pointer and advance the file pointer to the next word in the file |
| Seek   | Change the position of the file pointer                                                                                   |



#### [Process system calls](./systemcallinterface.md)

| Name    | Description                                                                                      |
| ------- | ------------------------------------------------------------------------------------------------ |
| Fork    | Create a child process allocating a new address space.                                           |
| Exec    | Load and execute an eXpFS executable file into the virtual address space of the present process. |
| Exit    | Destroy the process invoking the call                                                            |
| Getpid  | Get the Process ID of the invoking process                                                       |
| Getppid | Get the process ID of the parent process of the invoking process.                                |


#### [System calls for access control and synchronization](./systemcallinterface.md)




| Name       | Description                                                                                        |
| ---------- | -------------------------------------------------------------------------------------------------- |
| Signal     | Send a signal to a process specified in the call.                                                  |
| Wait       | Suspend execution of the current process until the process specified sends a signal or terminates. |
| Semget     | Acquire a new semaphore                                                                            |
| Semrelease | Release a semaphore already acquired by the process                                                |
| SemLock    | Get exclusive access permission to semaphore specified. (Process blocks till lock is obtained.)    |
| SemUnLock  | Release the lock on a semaphore already acquired                                                   |




#### <span style="color:red">[System calls for Multiuser extension to eXpOS](./systemcallinterface.md)</span>

| Name     | Description                                                    |
| -------- | -------------------------------------------------------------- |
| Newusr   | Creates a new user with the specified user name and password   |
| Remusr   | Removes the user specified by the username                     |
| Setpwd   | Sets the password for the corresponding user                   |
| Getuid   | Returns the userid of the user with the corresponding username |
| Getuname | Returns the username of the user with the corresponding userid |
| Login    | Logs in a new user                                             |


