---
title: eXpOS Process Management Implementation Tutorial
---

!!! note "Prerequisites"
    It is necessary to read the following documentations before starting with this tutorial.

    1. eXpOS process - <a href="../os_spec-files/processmodel.html" target="_blank">user level specification</a>.<br>
    2. <a href="../os_spec-files/systemcallinterface.html#processsystemcalls" target="_blank">Program level interface</a> to different process system calls.<br>
    3. eXpOS <a href="../abi.html" target="_blank">ABI</a>.<br>
    4. <a href="xsm_unprivileged_tutorial.html" target="_blank">XSM unprivileged</a> mode execution tutorial.<br>

When a program is loaded from the disk and executed by the ​<i>Exec</i>​ system call, the system call code loads the program into memory and sets up the ​<i>address space</i>​ for a process. A process in execution can spawn more processes using the ​<i>Fork</i>​ system call. A process is terminated using the ​<i>Exit</i>​ system call. This tutorial will focus on the data structures related to the implementation of these system calls.

In order to manage processes, the OS needs to arrange memory for two categories of data:

a)​ The space to store the process. Stated technically, the OS must allocate ​<b>physical memory pages</b>​ into which the logical address space of the process must be mapped into. The OS maintains a <b>per-process page table</b>​ for keeping track of the physical memory to logical memory mapping. The OS also allocates a ​<b>user area page</b>​ for each process to create space for a kernel stack for the process. (to be described below).

b)​ The space to store ​ metadata ​ related to each process. The data structures for meta-data are 1. ​<b>process table​</b>, 2.​ <b>per-process resource tables</b>​ and 3. ​<b>Per-process disk map tables​</b>. (Strictly speaking, per-process page tables contain metadata, and should have been listed here, but the explanation is easier with the present ordering.)

Before, getting to these data structures, we need to have a quick look into how an executable program is stored in the disk and how the OS maintains metadata of executable programs in the disk.

---

The OS maintains in the disk a global data structure called ​<a href="../os_design-files/disk_ds.html" target="_blank">Inode table</a>​ in which each file in the disk has an entry. The only way in which an executable file can be loaded into the eXpFS disk is to load it externally using ​<i>xfs-interface</i>. Hence, the Inode table entry for an executable file is set when the file is loaded into the disk by <i>xfs-interface</i>​ to the following values.


a)​ File type will be set to EXEC. 
b) Name of the file as given,
c) Size of the file calculated from the content size 
c) User Id of the owner of the file – will be set to 0 (Kernal), 
d) File permissions – will not be set (eXpOS does not permit application programsto modify/delete executable files using OS system calls)
e) Disk blocks into which xfs-interface places the contents of the file. The maximum number of blocks for an executable file is 4.<br>

The values of <i>file size</i>​ of the file and disk blocks containing the file are of relevance to process management.


Now we describe how the OS manages processes in memory.

### Physical Memory

An XEXE executable file will contain the ​<b>code</b>​ of the program (along with a small eight word <b>​header​</b> in the beginning). As noted above, the size of an executable file is limited to maximum 4 disk blocks. Hence, to load the contents of an executable file into memory, the OS will need to allocate a maximum 4 pages of physical memory.

To understand how memory allocation for a program is done, we look at the ​<b>Exec system call</b>.​ The ​<i>Exec</i>​ system call takes as argument an executable file’s name and allocates memory for loading the executable file. It then loads the program into the allocated memory and sets it up for execution.

When the loaded code is executed, the code will require more memory. Hence, each process is given a ​<b>memory address space</b>​ called the logical or virtual address space of the process. The eXpOS ABI stipulates that the address space of a process starts from logical address 0 and ends at logical address 5119 (10 pages – numbered logical page 0 to logical page 9 of the process.)


Physical pages are allocated using ​<i>GetFreePage</i> ​function of the ​<a href="../os_modules/Module_2.html" target="_blank">Memory Manager Module</a>. The memory pages allocated to a process need not be contiguous. Hence, ​<b>there must be a table for each process that describes the mapping of logical pages to physical pages</b>.​ This table is called the ​<b>per-process page table​</b>. The code of the executable program will contain reference to logical addresses, which has to be translated to physical addresses when the program is executed. This translation is done by the ​<a href="../arch_spec-files/paging_hardware.html" target="_blank">paging hardware​</a> of the XSM machine. This documentation assumes that the user is familiar with paging hardware (see <a href="../arch_spec.html" target="_blank">XSM tutorial</a> for more details). Hence, we will not describe page tables or the details of paging here. What is important here is the fact that the mapping of logical pages to physical pages is maintained in the per-process page table.

The OS expects that the application program logically divides the 10 page logical address space of a process into four parts a) ​<b>library</b>​ (logical pages 0 and 1), b) ​<b>heap</b> (logical pages 2, 3), c) ​<b>code</b>​ (or sometimes called “text” in OS jargon) (logical pages 4,5,6,7) and d) ​<b>stack</b>​ (logical pages 8,9). (These conventions are listed out in the <a href="../abi.html" target="_blank">ABI documentation</a> and application programs (or program compilers) are expected to follow these regulations when preparing the executable file).

The ​<i>Exec</i> system call uses the ​<i>DiskLoad</i> function of the ​<a href="../os_modules/Module_4.html" target="_blank">Device Manager Module</a>​ to load the contents of the executable file specified into logical pages 4,5,6 and 7. (That is, the disk blocks will be loaded to the physical pages corresponding to these logical pages). Logical pages 0 and 1 are mapped to the eXpOS ​<a href="../abi.html" target="_blank">run time library​</a>. The OS pre-loads the library into memory pages 63 and 64 at boot time. The ​<i>Exec</i> system call sets the page table entries for the logical pages 0 and 1 of each process to physical pages 63 and 64. Pages are allocated using the <i>GetFreePage</i>​ function of the ​Memory Manager Module​ for stack and heap regions of memory during program loading.

<figure style="text-align: center;">
                           <img src="../img/roadmap/exec3.png" style="display:block;margin-left:auto;margin-right:auto" >
                           <br>
                           <figcaption style="font-size: 16px">Control flow diagram for <i>Exec</i> system call</figcaption>
                           </figure>

In actual implementation, code and heap pages may not be allocated at the time of program loading, but may be allocated dynamically through a ​<b>lazy strategy on demand</b>. This makes use of the ​<a href="../os_design-files/exe_handler.html" target="_blank">exception handling mechanism​</a> provided by the machine, and will be introduced in the road-map at appropriate stages. For simplicity of exposition, we assume here that all pages are allocated at load time.

When a process invokes interrupt handlers, a separate stack (called the ​<b>kernel stack</b>​ of the process) is used for kernel mode handler execution. Interrupt handlers may invoke other kernel module functions. During such calls, the call addresses are stored in the kernel stack. To make space for the kernel stack, a separate page is allocated (this page is not part of the address space as this page is visible only to the kernel). This
page is called the ​<a href="../os_design-files/process_table.html#user_area" target="_blank">user-area page​</a> of the process. Since one page is more than sufficient for the kernel stack, some part of the user area page can be used for other purposes. Hence, the user area page is divided into two parts. One part is allocated for the ​<b>kernel stack</b> of the process. The other part stores the ​<b>per-process resource table</b>​ of the process (to be described below).



There are some issues that were left out in the above description. ​<i>Exec</i> system call can be run only by an existing process. The system call <a href="https://en.wikipedia.org/wiki/Exec_(system_call)" target="_blank">overlays</a> the existing program with the newly loaded program and continues to run with the same process id and user id. From an implementation point of view, this means that the newly loaded program uses the same process data structures - process table, page table, resource table and disk map table - of process that invokes ​<i>Exec</i>. Part of the contents of these tables that define attributes of the process like the process id and user id are also retained.


After completion of its work, ​<i>Exec</i>​ system call transfers control to the starting address newly loaded code, so that the newly loaded program begins execution immediately in the <a href="../os_design-files/process_table.html#state" target="_blank">RUNNING state</a>.

This summarizes how memory allocation for processes is carried out. Next we describe the data structures that store the metadata of each process.

### Process Table
The process table is a global data structure that has an entry for each process. Each process is assigned a unique ​<b>process id</b>​ (called PID). The PID of a process is the index of the process's entry in the process table. The fields of the process table entries include​ <b>user-id</b>​ of the user executing the process (the semantics of user-id will not be discussed here), pointer to the ​<b>page table</b> of the process, index of the <b>inode</b>​ of the executable file that is loaded as the process, index of the ​<b>user area page​</b> etc. The field ​<b>input-buffer</b>​ is a one word buffer used to store data read from terminal by the process. The field <b>tick</b>​ is used to keep track of “how long” the process has been in the memory (and will not be discussed here).

Most of the fields are self explanatory and are described <a href="../os_design-files/process_table.html" target="_blank">here</a>.

### Per Process Disk Map table
We have already seen that a process requires upto 11 pages of memory (10 page logical address space plus 1 user area page). Of these, the first two pages - corresponding to the library - will always remain loaded in memory. The OS may ​<b>swap out</b>​ heap, stack and user area pages into the swap area to make memory available for other processes. Similarly, the process may not maintain one or more code pages in memory. (There is no need to swap out code pages as the executable file is present in the disk.) The disk map table contains information about the disk block to which a page is stored when it is not present in the memory. Details of disk map table is given <a href="../os_design-files/process_table.html#disk_map_table" target="_blank">here</a>.

### Per Process Resource Table
A process may open files or semaphores using ​<i>Open</i> and <i>​Semget</i> system calls respectively. These system calls return a file/semaphore ​<b>descriptor</b>​ which is used to access the file/semaphore. Moreover, associated which each such descriptor, there is a <a href="../os_design-files/mem_ds.html" target="_blank">open file table entry</a> / <a href="../os_design-files/mem_ds.html#sem_table" target="_blank">semaphore table entry</a> whose index is maintained by the OS. The descriptors and open file table/semaphore table indices of files/semaphores opened/acquired by a process are stored in the <a href="../os_design-files/process_table.html#per_process_table" target="_blank">per process resource table</a>.

---

We now describe process creation - the ​<i>Fork</i>​ system call, which will clarify how these data structures are set up. ​<i>Fork</i>​ allocates a new process table entry for a process using the <i>​GetPCBEntry</i>​ function of the ​<a href="../os_modules/Module_1.html" target="_blank">Process Manager Module</a>. <i>GetPCBEntry</i> function copies the index of the new entry into the PID field of the process table.

The PTLR field indicates the size (number of pages) of the address space allocated for the process. eXpOS sets the address space size uniformly to 10 pages for all processes. Hence this field is set to 10 by the <i>GetPCBEntry</i> function. The value of PTLR is copied to the PTLR register of the machine when the process is scheduled for execution. The machine uses this value to generate an exception if a process tries to generate an address beyond its address space.

The start address of the <a href="../os_design-files/process_table.html#per_page_table" target="_blank">page table</a> of each process is fixed by eXpOS design. The ​<i>GetPCBEntry</i> function sets this value appropriately when it allocates a new process table entry.

A newly created process (called the ​<i>child</i> process in OS jargon) inherits the User-ID of the process which invoked ​<i>Fork</i>​ (called the ​<i>parent</i> process​). <b>The ​child shares parent's code and heap pages​</b>. Hence, <i>Fork</i> system call copies the page table entries corresponding to the heap and code pages of the parent into the corresponding page table entries of the child. The disk map table entries corresponding to these pages are also copied from the parent to the child.

<i>Fork</i>​ allocates new stack pages for the child (using the ​<i>GetFreePage</i> function of the Memory ​ Manager Module) and sets the page table entries for stack pages of the child process to the newly allocated pages. However, ​<i>Fork</i>​ then copies the contents of the parent's stack into the child's stack pages. Since the stack and the code pages are either same or identical, the child and the parent resumes execution from the same instruction in their code. (There are minor details of differences – to state one, the parent and the child differ in the return value stored in the stack by the ​<i>Fork</i>​ system call. We ignore the differences for now.) ​<i>Fork</i> allocates a new user area page for the child. Thus, the child gets its own kernel stack.

<b>The child process inherits all open file and semaphore descriptors of the parent.</b> Hence ​<i>Fork</i>​ copies the open file descriptors from the resource table of the parent to the child.

After initializing process meta-data in child’s process table and setting up the address space of the child, <b><i>Fork</i> sets the state of the child process as CREATED</b>​.

After completing the work, ​<i>Fork</i> returns to the parent and the parent process continues execution immediately. The OS scheduler will put the child to execution in due course of round robin scheduling.

<figure style="text-align: center;">
                           <img src="../img/roadmap/fork.png" style="display:block;margin-left:auto;margin-right:auto" >
                           <br>
                           <figcaption style="font-size: 16px">Control flow diagram for <i>Fork</i> system call</figcaption>
                           </figure>

                           


The ​<b>Exit system call</b> results in​ <b>termination</b>​ of a process. <i>Exit</i> calls the ​<i>Exit Process</i> function of the <a href="../os_modules/Module_1.html" target="_blank">process manager module</a> to release all the memory (and swap pages if any) pages allocated to the process and close all open file and semaphore instances. The data structures allocated to the process are also released. ​<i>Exit</i>​ finally invokes the scheduler to run other processes.

The first two processes - IDLE and INIT are hand created by the OS during boot loading. All further processes created through <i>Fork</i> operations from the INIT process and its descendent processes.
