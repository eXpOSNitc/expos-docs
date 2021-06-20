---
title: 'Process Table (Process Control Block)'
original_url: 'http://eXpOSNitc.github.io/os_design-files/process_table.html'
hide:
    - navigation
---

The Process Table (PT) contains an entry for each [process](../os_spec-files/processmodel.html) present in the system. The entry is created when the process is created by a Fork system call. Each entry contains several fields that stores all the information pertaining to a single process. The maximum number of entries in PT (which is maximum number of processes allowed to exist at a single point of time in eXpOS) is MAX\_PROC\_NUM. In the current version of eXpOS, MAX\_PROC\_NUM = 16.


Each entry in the Process Table has a constant size, defined by the PT\_ENTRY\_SIZE. In this version of eXpOS, PT\_ENTRY\_SIZE is set to 16 words. Any entry of PT has the following fields:

<table class="table table-bordered" style="font-size:0.5rem">
<tbody><tr>
<td style="border: 1px solid black; background-color: #90EE90">Offset</td>
<td >0</td>
<td >1</td>
<td >2</td>
<td ><span style="color:red">3</span></td>
<td >4</td>
<td >6</td>                                                                
<td >7</td>
<td >8</td>
<td >9</td>
<td >10</td>
<td >11</td>
<td >12</td>
<td >13</td>                      
<td >14</td>
<td >15</td>
</tr>
<tr>
<td style="border: 1px solid black; background-color: #90EE90">Field Name</td>
<td >TICK</td>
<td >PID</td>
<td >PPID</td>
<td ><span style="color:red">USERID</span></td>
<td >STATE</td>
<td >SWAP FLAG</td>                                                                
<td >INODE INDEX</td>
<td >INPUT BUFFER</td>
<td >MODE FLAG</td>
<td >USER AREA SWAP STATUS</td>
<td >USER AREA PAGE NUMBER</td>
<td >KERNEL STACK POINTER (KPTR)</td>
<td >USER STACK POINTER (UPTR)</td>                      
<td >PTBR</td>
<td >PTLR</td>
</tr>
</tbody></table>


* **TICK** (1 word)- keeps track of how long the process was in memory/ swapped state. It has an initial value of 0 and is updated whenever the scheduler is called. TICK is reset to 0 when a process is swapped out or in.
* **PID** (1 word) - process descriptor, a number that is unique to each process. This field is set by Fork System Call. In the present version of eXpOS, the pid is set to the index of the entry in the process table.
* **PPID** (1 word) - process descriptor of the parent process. This field is set by Fork System Call. PPID of a process is set to -1 when it's parent process exits. A process whose parent has exited is called an Orphan Process.
* **USERID** (1 word) - Userid of the currently logged in user. This field is set by Fork System Call.
* [**STATE**](#state) (2 words) - a two tuple that describes the current state of the process. The details of the states are explained below.
* **SWAP FLAG** (1 word) - Indicates if the process is swapped (1) or not (0). The process is said to be swapped if any of its user stack pages or its kernel stack page is swapped out.
* **INODE INDEX** (1 word)- Pointer to the Inode entry of the executable file, which was loaded into the process's address space.
* **INPUT BUFFER** (1 word) - Buffer used to store the input read from the terminal. Whenever a word is read from the terminal, Terminal Interrupt Handler will store the word into this buffer.
* **MODE FLAG** (1 word) - Used to store the system call number if the process is executing inside a system call. It is set to -1 when the process is executing the exception handler. The value is set to 0 otherwise.
* **USER AREA SWAP STATUS** (1 word) - Indicates whether the user area of the process has been swapped (1) or not (0).
* **USER AREA PAGE NUMBER** (1 word) - Page number allocated for the user area of the process.
* **KERNEL STACK POINTER** (1 word) - Pointer to the top of the kernel stack of the process. The **offset of this address within the user area** is stored in this field.
* **USER STACK POINTER** (1 word) - Logical address of the top of the user stack of the process. This is used when the process is running in kernel mode and the machine's stack pointer is pointing to the top of the kernel stack.
* **PTBR** (1 word) - pointer to [PER-PROCESS PAGE TABLE](#per_page_table).
* **PTLR** (1 word) - PAGE TABLE LENGTH REGISTER of the process.


Invalid entries are represented by -1.


**Note1:** In this version of eXpOS, the [Per-Process Resource Table](#per_process_table) is stored in the user area of each process. Generally, the Per-Process Resource Table is stored somewhere in memory and a pointer to the table is kept in the Process Table entry.


**Note2:** The Process Table is present in page 56 of the memory (see [Memory Organisation](../os_implementation.html)), and the SPL constant [PROCESS\_TABLE](../support_tools-files/constants.html) points to the starting address of the table. PROCESS\_TABLE + PID*16 gives the begining address of process table entry corresponding to the process with identifier PID.




  

  

#### STATE



The tuple can take the following values


* (ALLOCATED,\_\_\_) - The PCB Entry for the process has been allocated, but the process has not been created yet, because the Fork system call has not completed the creation of the new process.
* (CREATED,\_\_\_) – The process has been created in memory and data structures set up, but has never been scheduled. The fork system call creates the child process in CREATED state.

 * (RUNNING,\_\_\_) – The process is in execution. This field is set by the scheduler when a process is scheduled.
* (READY,\_\_\_) – The process is ready to be scheduled.
* (WAIT\_PROCESS, WAIT\_PID) – The process is waiting for a signal from another process whose PID is WAIT\_PID. This field is set by WAIT system call.
* (WAIT\_FILE, INODEINDEX) - The process is blocked for a file whose index in the inode table is INODEINDEX.
* (WAIT\_DISK,\_\_\_) - The process is blocked because of one of the following reasons: a) It is waiting for disk to complete a disk-memory transfer operation it had initiated OR b) It wants to execute a disk transfer, but the disk is busy, handling a disk-memory transfer request issued by some other process. The disk interrupt handler changes the state from (WAIT\_DISK,\_\_\_) to (READY,\_\_\_), after it has completed the disk transfer.
* (WAIT\_SEMAPHORE,SEMTABLEINDEX) - The process is waiting for a semaphore that was locked by some other process.
* (WAIT\_MEM, \_\_\_) – The process is blocked due to unavailability of memory pages.
* (WAIT\_BUFFER, BUFFERID) – The process is waiting for disk buffer of index BUFFERID to be unlocked.
* (WAIT\_TERMINAL,\_\_\_) – The process is waiting for one of the following: a) a Read from Terminal, which it has issued OR b)to be completed or if the terminal is blocked by some other process. The terminal interrupt handler changes the state from (WAIT\_TERMINAL,\_\_\_) to (READY,\_\_\_), after it has completed the terminal read/write.



Process states and transitions can be viewed [here](state_diag.html).


!!! note
    When a process terminates, the STATE field in it's process table entry is marked TERMINATED to indicate that the process table entry is free for allocation to new processes. 






  

  

  

#### PER-PROCESS PAGE TABLE



The Per-Process Page Table contains information regarding the physical location of the pages of a process. Each valid entry of a page table stores the physical page number corresponding to each logical (virtual) page associated with the process. The logical page number can vary from 0 to MAX\_PROC\_PAGES- 1 for each process. Therefore, each process has MAX\_NUM\_PAGES entries in the page table. The address of Page Table of the currently executing process is stored in PTBR of the machine and length of the page table is stored in PTLR. In this version of eXpOS, MAX\_NUM\_PAGES is set to 10, hence PTLR is always set to 10.


Associated with each page table entry, typically **auxiliary information** is also stored. This is to store information like whether the process has write permission to the page, whether the page is dirty, referenced, valid etc. The exact details are architecture dependent. The eXpOS specification expects that the hardware provides support for reference, valid and write bits. (See page table structure of XSM [here](../arch_spec-files/paging_hardware.html)). 


<table class="table table-bordered">
<tbody><tr>
<td style="border: 1px solid black">PHYSICAL PAGE NUMBER</td>
<td style="border: 1px solid black">REFERENCE BIT</td>
<td style="border: 1px solid black">VALID BIT</td>
<td style="border: 1px solid black">WRITE BIT</td>
</tr>
</tbody></table>


* **Reference bit** - The reference bit for a page table entry is set to 0 by the OS when the page is loaded to memory and the page table initialized. When a page is accessed by a running process, the corresponding reference bit is set to 1 by the machine hardware. This bit is used by the page replacement algorithm of the OS.
* **Valid bit**  - This bit is set to 1 by the OS when the physical page number field of a page table entry is valid (i.e, the page is loaded in memory). It is set to 0 if the entry is invalid. The OS expects the architecture to generate a page fault if any process attempts to access an invalid page.
* **Write bit**  - This bit is set to 1 by the OS if the page can be written and is set to 0 otherwise. The OS expects the architecture to generate an exception if any process, while running in the user mode, attempts to modify a page whose write bit is not set.
  
 
 If the Page Table entry is invalid, the Physical Page number is set to -1. 
 
 

  

!!! note
    In the XSM machine, the first three bits of the second word stores the reference bit, valid bit and the write permission bit. The fourth bit is the dirty bit which is not used by eXpOS.

For more information, see [XSM.](../arch_spec.html)


!!! note
    In the eXpOS implementation on the XSM architecture, if a page is not loaded to the memory, but is stored in a disk block, the disk block number corresponding to the physical page number is stored in the [disk map table](#disk_map_table) of the process. If memory access is made to a page whose page table entry is invalid, a *page fault* occurs and the machine transfers control to the Exception Handler routine, which is responsible for loading the correct physical page.


!!! note
    The Page Table is present in page 58 of the memory (see [Memory Organisation](../os_implementation.html)), and the SPL constant [PAGE\_TABLE\_BASE](../support_tools-files/constants.html) points to the starting address of the table. PAGE\_TABLE\_BASE + PID*20 gives the begining address of page table entry corresponding to the process with identifier PID.



 

#### PER-PROCESS DISK MAP TABLE



The per-process Disk Map Table stores the disk block number corresponding to the pages of each process. The Disk Map Table has 10 entries for a single process. When the memory pages of a process are swapped out into the disk, the corresponding disk block numbers of those pages are stored in this table. It also stores block numbers of the code pages of the process.


The entry in the disk map table entry has the following format: 

<table class="table table-bordered">
<tbody><tr>
<td style="border: 1px solid black">Unused</td>
<td style="border: 1px solid black">Unused</td>
<td style="border: 1px solid black">Heap 1 in disk</td>
<td style="border: 1px solid black">Heap 2 in disk</td>
<td style="border: 1px solid black">Code 1 in disk</td>
<td style="border: 1px solid black">Code 2 in disk</td>
<td style="border: 1px solid black">Code 3 in disk</td>
<td style="border: 1px solid black">Code 4 in disk</td>
<td style="border: 1px solid black">Stack Page 1 in disk</td>
<td style="border: 1px solid black">Stack Page 2 in disk</td>
</tr>
</tbody></table>


 If a memory page is not stored in a disk block, the corresponding entry must be set to -1. 


!!! note
    The Disk Map Table is present in page 58 of the memory (see [Memory Organisation](../os_implementation.html)), and the SPL constant [DISK\_MAP\_TABLE](../support_tools-files/constants.html) points to the starting address of the table. DISK\_MAP\_TABLE + PID*10 gives the begining address of disk map table entry corresponding to the process with identifier PID.





#### USER AREA



Corresponding to each user process, the kernel maintains a seperate memory region (called the user area) for its own purposes. The present version of eXpOS allocates one memory page per process as the user area. A part of this space is 
used to store the per process resource table of the process. The rest of the memory is alloted for the kernel stack of the process. 

Hence in eXpOS, each process has a kernel stack in addition to user stack. We maintain a seperate stack for the kernel operations to prevent user-level "hacks" into kernel. 



  

![User Area](http://exposnitc.github.io/img/user_area_new.png)

  

#### PER-PROCESS RESOURCE TABLE



The Per-Process Resource Table has 8 entries and each entry is of 2 words. **The last 16 words of the User Area Page are reserved for this**. For every instance of a file opened (or a semaphore acquired) by the process, it stores the index of the Open File Table (or Semaphore Table) entry for the file (or semaphore) is stored in this table. One word is used to store the resource identifier which indicates whether the resource opened by the process is a [FILE](../support_tools-files/constants.html) or a [SEMAPHORE](../support_tools-files/constants.html). Open system call sets the values of entries in this table for a file.


The per-process resource table entry has the following format. 

<table class="table table-bordered">
<tbody><tr>
<td style="border: 1px solid black">Resource Identifier (1 word)</td>                  
<td style="border: 1px solid black">Index of Open File Table/ Semaphore Table entry (1 word)</td>                      
</tr>
</tbody></table>


File descriptor, returned by Open system call, is the index of the per-process resource table entry for that open instance of the file.


A free entry is denoted by -1 in the Resource Identifier field.




  

#### PER-PROCESS KERNEL STACK



Control is tranferred from a user program to a kernel module on the occurence of one of the following events : 

1.  The user program executes a system call
2.  When an interrupt/exception occurs.


In either case, the kernel allocates a separate stack **for each process** (called the kernel stack of the process) which is different from the stack used by the process while executing in the user mode (called the user stack). Kernel modules use the space in the kernel stack for storing local data and do not use the user stack. This is to avoid user "hacks" into the kernel using the application's stack.


In the case of a system call, the application will store the parameters for the system call in its user stack. Upon entering the kernel module (system call), the kernel will extract these parameters from the application's stack and then change the stack pointer to its own stack before further execution. Since the application invokes the kernel module 
voluntarily, it is the responsibility of the application to save the contents of its registers (except the stack pointer and base pointer registers in the case of the XSM machine) before invoking the system call.


In the case of an interrupt/exception, the user process does not have control over the transfer to the kernel module (interrupt/exception handler). Hence the execution context of the user process (that is, values of the registers) must be saved by the kernel module, before the kernel module uses the machine registers for other purposes, so that the machine state can be restored after completion of the interrupt/exception handler. The kernel stack is used to store the execution context of the user process. This context is restored before the return from the kernel module. (For the implementation of eXpOS on the XSM architecture, the [backup](../arch_spec-files/instruction_set.html#backup) and [restore](../arch_spec-files/instruction_set.html#restore) instructions facilitate this).


In addition to the above, if a kernel module invokes another kernel module while executing a system call/interrupt, the parameters to the called module and the return values from the module are passed through the same kernel stack.




Here is a detailed tutorial on  [kernel stack management in system calls, interrupts and exceptions](../os_implementation.html). A separate tutorial is provided for [kernel stack managament during context switch](../os_design-files/timer_stack_management.html).


  