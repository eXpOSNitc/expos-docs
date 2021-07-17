---
title: 'Stage 26 : User Management (12 Hours)'
original_url: https://exposnitc.github.io/Roadmap.html
---
 
!!! note "Learning Objectives"
    -   Adding support in eXpOS to manage multiple users.
    -   Implementation of multi-user system calls.
    
!!! abstract "Pre-requisite Reading"
    -   It is **absolutely necessary** to read and understand **[multi-user management and implementation](../tutorials/multiuser-implementation.md)** documentation.
    -   Description of data structures- [User Table](../os-design/disk-ds.md#user-table)
    -   Description of special processes - [Init (Login) and Shell process](../os-spec/misc.md) .
    

  

In this stage, we will enable eXpOS to handle multiple users by implementing [multi-user system calls](../os-spec/systemcallinterface.md#multiuser-system-calls) . *Newusr* and *Remusr* system calls are implemented to create new users and delete existing users in the system. The data structure called [user table](../os-design/disk-ds.md#user-table) is maintained to store user name and encrypted password of each user in the system. The index of the user table entry for a user is the USERID for the user. Two special users called "kernel" (USERID = 0) and "root" (USERID = 1) are already initialized in the user table at the time of disk formatting (executing fdisk command in XFS-interface). Password of "kernel" is unspecified and "root" user is given default password "root" (The user table will store the encrypted form of the string "root"). System calls *Setpwd* , *Getuname* and *Getuid* are also implemented in this stage.

*Login* and *Logout* system calls are implemented to enable users to login into the system and logout from the system. From this stage onwards, we will modify the INIT process to work as a special **login process** , running with PID=1 and owned by the kernel (user id is set to 0). Login process enables users to login into the system with their user name and password. After a user logs into the system, the OS (the login system call) will schedule the shell process with PID=2. **The shell will run in the context of the logged in user** (that is, user id of the shell will be set to the user id of the logged in user). Note that the address space for the shell process would be already set up in the memory by the OS boot code. Hence the login process simply sets the shell process to ready state and invoke the scheduler to start its execution. The Shell program will be modified in this stage to support [built-in shell commands](../os-spec/shell-spec.md) .

  
**Interrupt routine 17**  
  

The *Login* system call is implemented in the interrupt routine 17. *Login* has system call number 27. From ExpL programs, this system call is called using [exposcall function](../os-spec/dynamicmemoryroutines.md) .

  

1.  ***Login* system call**

*Login* system call takes two arguments 1) a user name (string) and 2) an unencrypted password (string). ***Login* system call can only be invoked from the [login process](../os-design/misc.md#initlogin-process) (PID = 1).** The init process of eXpOS is called login process. Login process will ask the user to enter user name and password from the console and invokes *Login* system call with provided login credentials.

To login a user into the system, *Login* system call checks whether the user with given user name and password is present in the [user table](../os-design/disk-ds.md#user-table) or not. Note that the password given as input is unencrypted and should be encrypted (using [encrypt statement](../arch-spec/instruction-set.md) ) before comparing to ENCRYPTED PASSWORD field in the user table. *Login* system call fails if the user with given user name and password is not found.

When a user with given login credentials is found, *Login* system call makes the shell process (PID = 2) ready for execution by changing the STATE field in the [process table](../os-design/process-table.md) entry of shell process to CREATED. Although, login process does not explicitly invoke *Fork* and *Exec* system calls to create child, conceptually login process is considered as parent of shell process. So the PPID field in the process table entry of shell process is set to PID of login process (PID = 1). Also, login process must wait for shell process to terminate, so STATE of login process is changed to the tuple (WAIT\_PROCESS, PID of shell). Then, Scheduler is invoked in order to schedule shell process for execution.

Note that the shell process is already loaded into the address space in boot module so Login system call is not required to load shell process into the memory.

Implement *Login* system call using detailed algorithm provided [here](../os-design/multiusersyscalls.md#login) .

  

!!! note
    The implementation of ***Login*** system call is final.

  
**Interrupt routine 12**  
  

The *Logout* system call is implemented in the interrupt routine 12. *Logout* has system call number 28. From ExpL programs, this system call is called using [exposcall function](../os-spec/dynamicmemoryroutines.md) .

  

1.  ***Logout* system call**
  

![](../assets/img/roadmap/logout.png)  

Control flow for *Logout* system call

  
  

*Logout* system call is used to logout the current user from the system and does not take any arguments. ***Logout* system call can only be executed from the shell process (PID = 2).** Before leaving the system, all the non-terminated processes of the user should be terminated. As a consequence of terminating the processes, the resources acquired by these processes will be released. *Logout* system call invokes **Kill All** function of [process manager module](../modules/module-01.md) to terminate the processes. Recall that Kill All function terminates all processes in the system except idle, init (login) and the current process.

*Logout* system call changes the STATE of current process (shell) to TERMINATED. **The starting IP of the shell process is stored at first word of user stack of shell, so that the next time when a new user is logged in and shell process is scheduled for the first time in the context of the new user, shell will run as newly created process.** Login process (PID = 1) is made ready for execution and scheduler is invoked to schedule login process.

Implement *Logout* system call using detailed algorithm provided [here](../os-design/multiusersyscalls.md#logout) .

  

!!! note
    The implementation of ***Logout*** system call is final.

  
**Interrupt routine 16**  
  

The system calls *Newusr* , *Remusr* , *Setpwd* , *Getuname* and *Getuid* are implemented in the interrupt routine 16. *Newusr* , *Remusr* , *Setpwd* , *Getuname* and *Getuid* have system call numbers 22, 23, 24, 25, 26 respectively. From ExpL programs, these system calls are called using [exposcall function](../os-spec/dynamicmemoryroutines.md) .

  

1.  ***Newusr* system call**

A user name and an unencrypted text password are arguments to the *Newusr* system call. ***Newusr* system call can only be invoked from the shell process of the root user.**

*Newusr* finds a free entry for the new user in the [user table](../os-design/disk-ds.md#user-table) and initialize this entry with the provided user name and password. The password is encrypted (using [encrypt statement](../support-tools/spl.md) ) before storing it into the user table.

Implement *Newusr* system call using detailed algorithm provided [here](../os-design/multiusersyscalls.md#newusr) .

  
6.  ***Remusr* system call**

***Remusr*** system call takes the user name of the user to be removed as an argument. ***Remusr* system call can only be invoked from the shell process of the root user. A user can not be removed from the system if the user is the owner of one or more files in the system.** To remove a user from the system, *Remusr* system call invalidates the entry in the [user table](../os-design/disk-ds.md#user-table) corresponding to given username by storing -1 in the USERNAME and ENCRYPTED PASSWORD fields. Note that the special users "root" and "kernel" can not be removed using *Remusr* system call.

Implement *Remusr* system call using detailed algorithm provided [here](../os-design/multiusersyscalls.md#remusr) .

  
10.  ***Setpwd* system call**

***Setpwd*** changes the password of a user to newly provided password. It takes as arguments a user name and a new password from application program. *Setpwd* can only be executed by shell process. A user is permitted to change only its own password. The privileged user "root" has permission to change the password of any user. The "root" user is provided the default password "root". The password of root user can be changed later using *Setpwd* . *Setpwd* encrypts the provided password and replaces the ENCRYPTED PASSWORD field in the [user table](../os-design/disk-ds.md#user-table) entry corresponding to provided user name.

Implement *Setpwd* system call using detailed algorithm provided [here](../os-design/multiusersyscalls.md#setpwd) .

  
14.  ***Getuname* and *Getuid* system calls**

***Getuname*** takes as argument a USERID from user program. *Getuname* returns the user name of the given USERID from the [user table](../os-design/disk-ds.md#user-table) . ***Getuid*** takes a user name (string) as an argument from the user program. *Getuid* returns the USERID of the given user name. The system calls *Getuname* and *Getuid* can be executed from any process of any user.

Implement *Getuid* and *Getuname* system calls using detailed algorithms provided [here](../os-design/multiusersyscalls.md#getuid) .

  

!!! note
    The implementation of ***Newusr*** , ***Remusr*** , ***Setpwd*** , ***Getuname*** and ***Getuid*** system calls are final.

  
**Modification to *Shutdown* system call**  
  

There is a slight modification in *Shutdown* system call. *Shutdown* system call can only be invoked from shell process. Until this stage, shell process was loaded as init program with PID = 1, but now login process is loaded as init and shell is loaded with PID = 2. So in *Shutdown* system call, modify the condition to check whether current process is shell or not, by comparing current PID to 2 (instead of the previous value 1).

!!! note
    The implementation of ***Shutdown*** system call is final.

  
**Modifications to boot module and OS startup code**  
  

The boot module is modified to initialize the Shell process. Shell process has PID equal to 2. The process table entry and page table with index as 2 is initialized in the boot module for shell process. Heap, user stack and kernel stack pages are also allocated for the shell.

The boot module will set the shell process to TERMINATED state so that it will not be scheduled. The state of the shell process will be set to CREATED by the login system call when a valid user is logged in. This ensures that the shell process is scheduled only after a valid user is logged in.

  
`Implementation Note:`  
  

Since Idle, Shell and Login processes are system processes that does pre-defined functionality, it is easy to design ExpL programs for them so that 1) they require no heap pages 2) Idle and login (init) processes require only one user stack page each 3) Idle and login code will fit into just one code page each (shell will be hard to implement without two pages of code). Hence, we will modify the boot code so as to allocate only one stack page apart from the user area page and code pages for Idle and Login processes. Shell process will be allocated two stack pages.

Note that the [memory organization](../os-implementation.md) allocates two pages each for Idle and Login. Since the code for Idle and Login can fit into just one page, the second page can be allocated for their user stack. Kernel stack pages will have to be allocated in the free memory area. This leads to better memory utilization so that more concurrent processes may be run with the available memory. The page table entries for unallocated heap pages, stack page and code pages must be set to invalid.

  

**Steps to be done in the OS startup code to reflect the above changes are described below:**

-   Changes for idle process allocation

1.  Load only the first code page from disk to memory (instead of two code pages). See [disk/memory organization](../os-implementation.md) .
2.  Allocate second code page (70) as user stack page for idle (only one page for user stack is needed). Allocate memory page 76 for kernel stack of idle.
3.  Change the page table entries for stack and code pages according to above allocation. Also change the user area page number in the [process table](../os-design/process-table.md) entry of idle.
4.  Store the starting IP address from the header of the first code page on the top of new user stack as the user stack page number is changed now for idle.

  

**Steps to be done in the boot module to reflect the above changes are described below:**

-   Load shell process, int 16, int 12 (Logout), int 17 from disk to memory. See disk and memory organization [here](../os-implementation.md) .
-   Changes for init process allocation

1.  Load only the first code page from disk to memory (instead of two code pages). See [disk/memory organization](../os-implementation.md) .
2.  Allocate second code page (66) as user stack page for init (only one page for user stack is needed). Allocate memory page 77 for kernel stack of init.
3.  Invalidate the heap page entries in the page table of the INIT process. Change the page table entries for stack and code pages according to above allocation. Also change the user area page number in the [process table](../os-design/process-table.md) entry of init.
4.  Store the starting IP address from the header of the first code page on the top of new user stack as the user stack page number is changed now for init.
5.  Remove disk map table initialization for the init process as it is not needed any longer.

-   Shell process allocation

1.  Load two code pages from disk to memory. See [disk/memory organization](../os-implementation.md) .
2.  Allocate memory pages 78 and 79 for user stack of shell. Also allocate memory page 80 for kernel stack of shell.
3.  Set the library page entries to 63 and 64 in the page table of shell. Invalidate the heap page entries in the page table. Initialize the page table entries for stack and code pages according to above allocation. Also change the user area page number in the [process table](../os-design/process-table.md) entry of shell.
4.  Initialize the [process table](../os-design/process-table.md) entry of the shell process (PID = 2) as follows- Set the STATE field to TERMINATED. Store PID and PPID fields to 2 and 1 respectively. Store the kernel stack page number allocated above in the USER AREA PAGE NUMBER field. Set the KERNEL STACK POINTER field to 0 and USER STACK POINTER to 8\*512. Also initialize PTBR and PTLR fields for the shell process.
5.  Initialize the [disk map table](../os-design/process-table.md#per-process-disk-map-table) entry of the shell process (PID = 2) as follows - Store the block numbers of the two code pages in the disk map table entry of the shell. Invalidate all other entries of the disk map table entry by storing -1.
6.  Store the starting IP address from the header of the first code page on the top of user stack for the shell process.

Note that shell process is set up for execution but STATE of the shell process is set to TERMINATED in the boot module. The shell process will be made READY only upon successful login of the user.

-   Change the initialization of [memory free list](../os-design/mem-ds.md#memory-free-list) according to the memory pages allocated for idle, init and shell processes.
-   Update the MEM\_FREE\_COUNT in the [system status table](../os-design/mem-ds.md#system-status-table) to 47 as now 47 memory pages are available.

  
**Login program**  
  

Login program is run as the Init process from this stage onwards. This program asks user for a user name and a password to log into the system. Login process uses *Login* system call to log in the user into the system. This is repeated in a loop. Write login program using the pseudocode provided [here](../os-design/misc.md#initlogin-process) and load the XSM excutable as init program using [XFS-interface](../support-tools/xfs-interface.md) .

  
**Extended Shell program**  
  

Shell program is improvised to support the built-in shell commands and XSM executable commands/files according to the specification provided in [eXpOS shell specification](../os-spec/shell-spec.md) . An implementation of the ExpL shell program is given [here](../test-programs/index.md#test-program-7-extended-shell) . Compile and load this program as shell into the disk using [XFS-interface](../support-tools/xfs-interface.md) . This program will be run as shell when a user logs into the system.

Now that multiple user related system calls are supported in eXpOS, the shell commands - "lu" and "ru" can be implemented. Implement commands lu, ru as executable files according to the specification of [executable commands/files](../os-spec/shell-spec.md#executable-commandsfilenames) and load into the disk as executable files.

  
**Making things work**  
  

Compile and load the newly written/modified files to the disk using XFS-interface.

  
??? question "Q1. Why *Newusr* , *Remusr* and *Setpwd* system calls are permitted to execute only from shell program whereas *Getuid* and *Getuname* can be executed from any application program?"
    The system calls *Newusr* , *Remusr* and *Setpwd* modify the data related to users in the user table. *Getuid* and *Getuname* system calls only access data related to users. As application programs other than Shell are not allowed to modify the user related data, system calls *Newusr* , *Remusr* , *Setpwd* are only executed from shell process.
    
  
!!! assignment "Assignment 1"
    Test the system calls, login and shell process by performing following sequence of actions -  

    1. Login into the system as root user and change the password of root user using Setpwd command  
    2. Create new user using Newusr command  
    3. Log out from system  
    4. Login as newly created user  
    5. Create new files and perform file operations on them  
    6. List all users using "lu.xsm" executable file  
    7. Logout and again login as root user  
    8. Remove files owned by the new user using excutable file command "ru.xsm" from the shell of root. 
    
    You can further test the system by running all build-in shell commands and excutable files commands to make sure that implementation is correct.