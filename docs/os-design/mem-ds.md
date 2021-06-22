---
title: 'Memory DS'
original_url: 'http://eXpOSNitc.github.io/os_design-files/mem_ds.html'
hide:
    - navigation
---


### Open File Table

The Open File Table stores the information about all the files that are open while the OS is running. It consists of MAX\_OPENFILE\_NUM (= 32 in the present eXpOS version) entries. Thus, there can be at most MAX\_OPENFILE\_NUM = 32 open files in the system at any time. 

The Open system call creates an entry in the Open file table when a process opens a file. If the file is opened again by some other process (or the same process), the Open system call a new entry is created in the open file table. The first field (Inode Index) of the Open file table entry for a file is set to the index of the Inode Table entry for the file. 
 
Each entry is of size 4 words of which last word is left unused.

Every entry of the Open File Table has the following format :

<table class="table table-bordered  table-responsive">
<tbody><tr>
<td>INODE INDEX</td>
<td>OPEN INSTANCE COUNT</td>                      
<td>LSEEK</td>                      
<td>Unused</td>
</tr>
</tbody></table>

* **INODE INDEX**  (1 word) - specifies the index of the entry for the file in the Inode table. The special constant [INODE\_ROOT](../support-tools/constants.md) is stored in the case of the "root" file.
* **OPEN INSTANCE COUNT**  (1 word) - specifies the number of processes sharing the open instance of the file represented by this open file table entry.
* **LSEEK** (1 word) - specifies the position from which the next word is read from or written into in the file.
* **Unused** (1 word)


All invalid entries are set to -1.

An Unused entry is indicated by value of -1 in the INODE INDEX field.


!!! note
    The Open File Table is present in page 56 of the memory (see [Memory Organisation](../os-implementation.md)), and the SPL constant [OPEN\_FILE\_TABLE](../support-tools/constants.md) points to the starting address of the table.


### File (Inode) Status Table

The File Status Table contains details about lock status and file open count of each file in the inode table. 
It consists of MAX\_FILE\_NUM (= 60 in the present eXpOS version) entries. 

For each file, the index of its entry in the  **inode table must match with** the index of its entry in the **file status table** . 
Each file lock status table entry is of size 4 words of which two are unused.

<table class="table table-bordered">
<tbody><tr>
<td>LOCKING PID</td>
<td>FILE OPEN COUNT</td>
<td>Unused</td>
</tr>
</tbody></table>



* **LOCK** (1 word)- If the file is locked by a process inside a system call, this field specifies the PID of the process, otherwise, it is set to -1.
* **FILE OPEN COUNT** (1 word) - specifies the number of open instances of the file. This field is set to -1 if there are no open instances of the file in the system.
* **Unused** (2 words)


All invalid entries are set to -1


!!! note
    The File Status Table is present in page 57 of the memory (see [Memory Organisation](../os-implementation.md)), and the SPL constant [FILE\_STATUS\_TABLE](../support-tools/constants.md) points to the starting address of the table.


### Semaphore Table

The Semaphore Table contains details about the semaphores used by all the processes. It consists of MAX\_SEM\_COUNT (= 32 in the present eXpOS version) entries. Thus, there can be at most MAX\_SEM\_COUNT = 32 semaphores used in the system at any time. For every semaphore entry in the per-process resource table, there is a corresponding entry in the semaphore table. 


A process can acquire a semaphore using the Semget system call, which returns a unique semid for the semaphore. Semid is basically the index of the semaphore table entry for the semaphore. 


The Process count field specifies the number of processes which are sharing the semaphore. Semget sets the Process Count to 1. When a process forks, all semaphores acquired by the parent is shared with the child and hence, Process Count is incremented. Semrelease system call decrements the Process Count. Process Count is also decremented when a process exits.


SemLock system call sets the Locking PID field to the PID of the process invoking it. When the semaphore is not locked, Locking PID is -1.


Each semaphore table entry is of size 4 words of which the last two are unused.


<table class="table table-bordered">
<tbody><tr>
<td>LOCKING PID</td>
<td>PROCESS COUNT</td>
<td>Unused</td>
</tr>
</tbody></table>


* **LOCKING PID**  (1 word)- specifies the PID of the process which has locked the semaphore. The entry is set to -1 if the semaphore is not locked by any processes.
* **PROCESS COUNT** (1 word) - specifies the number of processes which are sharing the semaphore. A value of 0 indicates that the semaphore has not been acquired by any process.
* **Unused** (2 words)


An unused entry is indicated by 0 in the PROCESS COUNT field.


!!! note
    The Semaphore Table is present in page 56 of the memory (see [Memory Organisation](../os-implementation.md)), and the SPL constant [SEMAPHORE\_TABLE](../support-tools/constants.md) points to the starting address of the table.


### Disk Status Table

It is assumed that the machine provides a *load* instruction to transfer a disk block to a memory page and a *store* instruction to transfer a memory page to a disk block. The Disk Status Table keeps track of these disk-memory transfers. Every time a disk operation is invoked, the information regarding the operation like the disk block and the memory page involved, the process that invoked the operation and type of disk operation are stored in Disk Status Table by the OS. In the present version of eXpOS, it is assumed that, the disk does not support multiple disk-memory transfers at the same time and is considered busy while a transfer is going on. The state of the disk (busy or free) is also stored in the Disk Status Table. 


The size of the table is 8 words of which the last 2 are unused.
<table class="table table-bordered">
<tbody><tr>
<td>STATUS</td>                         
<td>LOAD/STORE BIT</td>
<td>PAGE NUMBER</td>
<td>BLOCK NUMBER</td>
<td>PID</td>   
<td>Unused</td>  
</tr>
</tbody></table>

* **STATUS** (1 word) - specifies whether the disk is free (indicated by 0) or busy (indicated by 1) handling a memory-disk transfer.
* **LOAD/STORE BIT** (1 word) - specifies whether the operation being done on the device is a load (indicated by 0) or store (indicated by 1).
* **PAGE NUMBER** (1 word) - specifies the memory page number involved in the disk transfer.
* **BLOCK NUMBER** (1 word) - specifies the disk block number involved in the disk transfer.
* **PID** (1 word) - specifies the PID of the process which invoked the disk transfer. If the disk transfer was initiated by the OS during paging/swapping, the field is set to PID of [idle process](misc.md#idle), which is 0.
* **Unused** (2 words)


!!! note
    The Disk Staus Table is present in page 56 of the memory (see [Memory Organisation](../os-implementation.md)), and the SPL constant [DISK\_STATUS\_TABLE](../support-tools/constants.md) points to the starting address of the table.


### Buffer Table

When a process reads/writes into a file, the relevant disk block is first brought into a memory buffer by the OS and the read/write operation is performed on the buffer. The OS reserves MAX\_BUFFER number of memory pages as buffers. The buffer table is a data structure that stores the information regarding the disk block stored in each buffer. The present version of eXpOS sets MAX\_BUFFER = 4. Each buffer is identified by its index in the buffer table. 


Since all the 4 buffer pages are shared by all the files in the file system, a buffer page may be required to be replaced by another disk block. In this case, write-back is performed only if the page is modified. The  **dirty bit** indicates whether the page has been modified.


When a disk block is required to be brought into the buffer, the buffer to which it must be loaded is identifed by the formula :
 

 Buffer\_number = Disk\_block\_number % MAX\_BUFFER 


 Each entry of the Buffer Table has the following format:


<table class="table table-bordered">
<tbody><tr>
<td>BLOCK NUMBER</td>
<td>DIRTY BIT</td>
<td>LOCKING PID</td>
<td>Unused</td>
</tr>
</tbody></table>

* **BLOCK NUMBER** (1 word) - specifies block number of the disk block which is currently stored in the buffer. It is set to -1 if the buffer does not contain any valid disk block.
* **DIRTY BIT** (1 word) - specifies whether the block stored in the buffer has been modified. It is set to 0 when a disk block is loaded into the buffer and is set to 1 when modified by the Write System Call.
* **LOCKING PID** (1 word) - specifies the PID of the process which has currently locked the buffer table while executing a file system call.
* **Unused** (1 word)


Free entries are represented by -1 in all the fields.


!!! note
    The Buffer Table is present in page 58 of the memory (see [Memory Organisation](../os-implementation.md)), and the SPL constant [BUFFER\_TABLE](../support-tools/constants.md) points to the starting address of the table.




### System Status Table

It keeps the information about the number of free pages in memory, the number of processes blocked because memory is unavailable, the number of processes in swapped state and, the pid of the process to be scheduled next. The size of the table is 8 words out of which 2 words are unused.


The System Status Table has the following format:
<table class="table table-bordered" style="font-size: 0.7em">
<tbody><tr>
<td>CURRENT_USER_ID</td>
<td>CURRENT_PID</td>                      		      
<td>MEM_FREE_COUNT</td>
<td>WAIT_MEM_COUNT</td>
<td>SWAPPED_COUNT</td>
<td>PAGING_STATUS</td>
<td style="color:red">CURRENT_PID2</td>
<td style="color:red">LOGOUT_STATUS</td>
</tr>
</tbody></table>

* **CURRENT\_USER\_ID** (1 word) - specifies the userid of the currently logged in user.
* **CURRENT\_PID** (1 word) - specifies the pid of the currently running process.
* **MEM\_FREE\_COUNT** (1 word) - specifies the number of free pages available in memory.
* **WAIT\_MEM\_COUNT** (1 word) - specifies the number of processes waiting (blocked) for memory.
* **SWAPPED\_COUNT** (1 word) - specifies the number of processes which are swapped. A process is said to be swapped if any of its user stack pages or its kernel stack page is swapped out.
* **PAGING\_STATUS** (1 word) - specifies whether swapping is initiated. Swap Out/Swap In are indicated by 0 and 1, respectively. Set to 0 if paging is not in progress.
* <span style="color:red">**CURRENT\_PID2** (1 word) - specifies the pid of the currently running process on the secondary core. This field is used only when eXpOS is running on [NEXSM](../arch-spec/nexsm.md) (a two-core extension of XSM) machine.</span>
* <span style="color:red">***LOGOUT\_STATUS** (1 word) - specifies whether logout is initiated on the primary core. Set to 0 if logout is not initiated. This field is used only when eXpOS is running on [NEXSM](../arch-spec/nexsm.md) (a two-core extension of XSM) machine.</span>


Initially, when the table is set up by the OS startup code, the MEM\_FREE\_COUNT is initialized to the number of free pages available in the system, WAIT\_MEM\_COUNT to 0, SWAPPED\_COUNT to 0 and PAGING\_STATUS to 0. 


!!! note
    The System Status Table is present in page 57 of the memory (see [Memory Organisation](../os-implementation.md)), and the SPL constant [SYSTEM\_STATUS\_TABLE](../support-tools/constants.md) points to the starting address of the table.

### Terminal Status Table

The Terminal Status Table keeps track of the Read/Write operations done on the terminal. Every time a Read or Write system call is invoked on the terminal, the PID of the process that invoked the system call is stored in Terminal Status Table. The table also contains information on the status of the terminal (whether free or busy). The size of the table is 4 words of which the last 2 are unused.


Every entry of the Terminal Status Table has the following format:

<table class="table table-bordered table-responsive">
<tbody><tr>
<td>STATUS</td>  
<td>PID</td>  
<td>Unused</td>
</tr>
</tbody></table>

* **STATUS** (1 word) - specifies whether the terminal is free or is being used by a process to read or write. This field is initially set to 0. It is changed to 1 whenever terminal is busy. The Terminal Interrupt Handler sets back the status to 0 upon completion of Terminal Read. The Write system call sets back the status to 0 upon completion of Terminal Write.
* **PID** (1 word) - specifies the PID of the process which is currently using the terminal. This field is invalid when STATUS is 0.
* **Unused** (2 words)


!!! note
    The Terminal Table is present in page 57 of the memory (see [Memory Organisation](../os-implementation.md)), and the SPL constant [TERMINAL\_STATUS\_TABLE](../support-tools/constants.md) points to the starting address of the table.

### Memory Free List

The Memory free list is a data structure used for keeping track of used and unused pages in the memory. It consists of MAX\_MEM\_PAGE entries and each entry is of size one word. Thus, the total size of the free list is MAX\_MEM\_PAGE words. The number of memory pages available to the OS is architecture dependent. For the version of XSM discussed here, MAX\_MEM\_PAGE = 128.

Each entry of the free list contains either the value 0 indicating that the corresponding page in the memory is free (not allocated to any process) or contains the number of processes that are sharing the page. Memory free list entries for the pages allocated to the kernel are also set to 1.


!!! note
    Memory copy of the Mem Free List is present in page 57 of the memory (see [Memory Organisation](../os-implementation.md)), and the SPL constant [MEMORY\_FREE\_LIST](../support-tools/constants.md) points to the starting address of the data structure.


### <span style="color:red">Access Lock Table</span>

When eXpOS runs on a two-core machine like [NEXSM](../arch-spec/nexsm.md), the OS kernel code executes parallelly on the cores. Hence, to ensure atomicity of the resource acquire functions (of the resource manager module), as well as access/updates of OS data structures, an additional layer of access locking is introduced. The OS maintains an Access Lock Table in memory with the following fields to hold the additional locks.


The Access Lock Table has the following format:


<table class="table table-bordered">
<tbody><tr>
<td>KERN_LOCK</td>
<td>SCHED_LOCK</td>                      		      
<td>GLOCK</td>
<td>Unused</td>                 
</tr>
</tbody></table>



* **KERN\_LOCK** (1 word) - Common access lock to be set before running any critical kernel code other than scheduling. Before performing any kernel function, this lock must be set by the kernel module/interrupt handler so that the other core waits till the critical action is completed.
* **SCHED\_LOCK** (1 word) - Access lock to run the Scheduler Module. if one core has set the SCHEDULE\_LOCK, then upon entering the Scheduler Module, the other core executes a busy loop until execution of the Scheduler Module on the first core is completed.
* **GLOCK** (1 word) - A general purpose lock variable that is left unused for future use.
* **Unused** (5 words)


!!! note
    This data structure is used only when eXpOS is running on [NEXSM](../arch-spec/nexsm.md) (a two-core extension of XSM) machine.
