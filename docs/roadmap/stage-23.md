---
title: 'Stage 23 : File Creation and Deletion (6 Hours)'
original_url: https://exposnitc.github.io/Roadmap.html
---

!!! note 
    - Familiarize with eXpOS file system and implemtation.
    - Add support for file creation and deletion to the OS by implementing Create and Delete system calls

!!! abstract "Pre-requisite Reading"
    - It is **absolutely necessary** to read and understand **[eXpOS FILE SYSTEM and Implementation Tutorial](Tutorials/filesystem_implementation.html)** documentation.
    - Description of data structures- [Inode Table](os_design-files/disk_ds.html#inode_table) , [Root file](os_design-files/disk_ds.html#root_file) , [File(inode) status table](os_design-files/mem_ds.html#file_lock_status_table) and [buffer table](os_design-files/mem_ds.html#buffer_table) .


 
 
 
 
 
 
 In this stage, we will discuss how files are created and deleted by the application program with the help of file system calls _Create_ and _Delete_ . _Shutdown_ system call will be modified in this stage.

_Create_ system call creates an empty file with the name given as input. _Create_ system call initializes the disk data structures with meta data related to the file. [Inode table](os_design-files/disk_ds.html#inode_table) and [root file](os_design-files/disk_ds.html#root_file) are the disk data structures used to maintain permanent record of files. _Delete_ system call deletes the record of the file with the given name from inode table and root file. _Delete_ also releases the disk blocks occupied by the file to be deleted. The _Shutdown_ system call is modified to commit the changes made by _Create_ and _Delete_ system calls in the memory copy of the disk data structures back into the disk.

Inode table and root file stores details of every eXpOS file stored in the disk. eXpOS allows at most [MAX\_FILE\_NUM](support_tools-files/constants.html) (60) files to be stored in the disk. Hence, both inode table and root file has MAX\_FILE\_NUM entries. The entry for a file in the inode table is identified by an index of its record in the inode table. For each file, the inode table entry and root file entry should have the same index. The disk data structures have to be loaded from the disk to the memory in order to use them while OS is running. The OS maintains the memory copy of the inode table in memory pages 59 and 60. Also the memory copy of root file is present in memory page 62. See [memory organization](os_implementation.html) for more details.



#### Interrupt routine 4
<figure>
    <img src="http://exposnitc.github.io/img/roadmap/create_delete.png"/>
    <figcaption>Control flow for <i>Create </i>and<i>Delete </i>system calls</figcaption>
</figure>

The system calls _Create_ and _Delete_ are implemented in the interrupt routine 4. _Create_ and _Delete_ have system call numbers 1 and 4 respectively. From ExpL programs, these system calls are called using [exposcall function](os_spec-files/dynamicmemoryroutines.html) .

##### Create system call

_Create_ system call takes filename and permission (integer 0 or 1) as arguments from the user program. As _Create_ allows to create only data file, it is recommended to use _.dat_ as extension for file names. _Create_ finds a free entry (indicated by -1 in the FILE NAME field) in the inode table to store details related to the new file. The fields in the free inode table entry and corresponding root file entry are initialized with the meta-data of the new file.

The USERID field in the inode table is initialized to the USERID field from the process table of the current process. Hence, the user executing the _Create_ system call becomes the **owner** of the file. The USERNAME field in the root file entry is initialized to the username corresponding to the USERID. The username can be obtained from memory copy of the [user table](os_design-files/disk_ds.html#user_table) with index as USERID. User table in the disk is initialized by the XFS-interface (during disk formatting) to create two users - kernel and root.

Implement _Create_ system call using the detailed algorithm provided [here](os_design-files/create.html).

##### Delete system call
_Delete_ system call takes file name as an argument from the user program. A file can not be deleted if it is currently opened by one or more processes. _Delete_ first acquires the lock on the file by invoking **Acquire Inode** function from [resource manager module](os_modules/Module_0.html) . _Delete_ then invalidates the record of the file in entries of the inode table and root file. Also, the blocks allocated to the file are released. Finally, _Delete_ releases the lock on file by invoking **Release Inode** function of the resource manager module.

There is one subtility involved in deleting a file. If any of the disk blocks of the deleted file are in the buffer cache, and if the buffer page is marked dirty, the OS will write back the buffer page into the disk block when another disk block needs to be brought into the same buffer page. However, such write back is unnecessary if the file is deleted (and can even be catastrophic- why?). Hence, Delete system call must clear the dirty bit (in the buffer table) of all the buffered disk blocks of the file.

Implement _Delete_ system call using the detailed algorithm provided [here](os_design-files/delete.html) .

#### Acquire Inode (function number = 4, <a href="os_modules/Module_0.html" target="_blank">resource manager module </a>)

Acquire Inode takes an inode index and PID of a process as arguments. To lock the inode (file), **Acquire Inode** first waits in a busy loop by changing state to (WAIT\_FILE, inode index) until the file becomes free. After the inode becomes free and current process resumes execution, acquire inode checks whether the file is deleted from the system. (This check is necessary because, some other process may delete the file while the current process was waiting for the inode to be free.) **Acquire Inode** then locks the inode by setting LOCKING PID field in the [file status table](os_design-files/mem_ds.html#file_lock_status_table) to the given PID.

Implement Acquire Inode function using the detailed algorithm given in the resource manager module link above.

#### Release Inode (function number = 5, <a href="os_modules/Module_0.html" target="_blank"> resource manager module </a>)
Release Inode takes an inode index and PID of a process as arguments. Release Inode frees the inode (file) by invalidating the LOCKING PID field in the [file status table](os_design-files/mem_ds.html#file_lock_status_table) . The function then wakes up the processes waiting for the file with given inode index by changing state of those processes to READY.

Implement Release Inode function using the detailed algorithm given in the resource manager module link above.

<!--
**Release Block (function number = 4, [Memory manager module](os_modules/Module_2.html) )**

There is one subtility involved in deleting a file. If any of the disk blocks of the deleted file is in the buffer cache, and if the buffer page is marked dirty, the OS will write back the buffer page into the disk block when another disk block needs to be brought into the same buffer page. However, such write back is unnecessary if the file is deleted (and can even be catastrophic- why?). Hence, Delete system call must clear the dirty bit (in the buffer table) of all the buffered disk blocks of the file. 
-->

!!! note
    The implementation of **_Create_** , **_Delete_** , **Acquire Inode** and **Release Inode** are final.

#### Interrupt routine 15 ( <i>Shutdown</i> system call)

_Create_ and _Delete_ system calls update the memory copies of Inode table, disk free list and root file. The changed data structures are not committed into the disk by these system calls. The disk update for these data structures are done during system shutdown.

<figure>
    <img src="http://exposnitc.github.io/img/roadmap/Initial_shutdown.png"/>
    <figcaption>Control flow for <i>Shutdown</i>system call</figcaption>
</figure>

Interrupt routine 15 written in stage 21 contains just HALT instruction. In this stage, _Shutdown_ system call is implemented in the interrupt routine 15. _Shutdown_ system call has system call number 21 and it does not have any arguments.

##### Shutdown system call
- Switch to the kernel stack and set the MODE FLAG in the [process table](os_design-files/process_table.html) to the system call number.
- _Shutdown_ system call can be invoked only from the shell process of the root user. If the current process is not shell (PID in the [process table](os_design-files/process_table.html) is not equal to 1) or the current user is not root user (USERID in the process table is not equal to 1) then store -1 as return value, reset the MODE FLAG, change the stack to user stack and return to user mode.
- Commit the changes made in the memory copies of the **inode table** (along with user table), the **root file** and the **disk free list** by storing them back to the disk invoking the **Disk Store** function of [device manager module](os_modules/Module_4.html) . Refer to [disk/memory organization](os_implementation.html) for block and page numbers of these data structures. Finally, halt the system using the [SPL statement](./support_tools-files/spl.html) halt.

!!! note
    The implementation of the _Shutdown_ system call is not final. Implementation will change in later stages.


#### Disk Store (function number = 1, <a href="os_modules/Module_4.html" target="_blank"> Device manager module </a>)

Disk Store function takes PID of a process, a page number and a block number as arguments. To store data into the disk, Disk Store first needs to lock the disk by invoking the **Acquire Disk** function of the [resource manager module](os_modules/Module_0.html) . After locking the disk, Disk Store updates the [disk status table](os_design-files/mem_ds.html#ds_table) . Finally, Disk Store initiates the store operation for given page number and block number and waits in WAIT\_DISK state until the store operation is complete. When store operation is completed, system raises the disk interrupt which makes this process READY again.

Implement **Disk Store** function using the detailed algorithm given in the device manager module link above.

!!! note 
    The implementation of **Disk Store** function is final.

#### Modifications to boot module
 
- Load interrupt routine 4 and root file from the disk to the memory. See the memory organization [here](os_implementation.html) .
- Initialize the [file status table](os_design-files/mem_ds.html#file_lock_status_table) by setting LOCKING PID and FILE OPEN COUNT fields of all entries to -1.
- Initialize the [buffer table](os_design-files/mem_ds.html#buffer_table) by setting BLOCK NUMBER and LOCKING PID fields to -1 and DIRTY BIT to 0 in all entries.
- At present to simplify the implementation, we consider a single user system with only one user called root, USERID of root is 1. Hence, set the USERID field in the process table of INIT to 1. Later when INIT is forked, the USERID field is copied to the process table of the child process.

#### Making things work

Compile and load the newly written/modified files to the disk using XFS-interface.


??? question "Q1. What is the need for Delete system call to lock the file before deleting it?"
    Locking the file in Delete system call makes sure that some other process will not be able to open the file or perform any other operation on the file during the deletion of the file.

!!! assignment "Assignment 1"
    Write an ExpL program to take file name(string) and permission(integer) as input from the console and create a file with the provided input. (It is recommended to have .dat as extension for data files.) Run this program using shell. Using XFS-interface check if the entry for the file is created in inode table and root file.

!!! assignment "Assignment 2"
    Write an ExpL program to take file name(string) as input from the console and delete a file with provided input. Run the program using shell. Using XFS-interface check if the entry for the file is deleted from inode table and root file. Check the program for different files- like files created using Create system call, files not present in disk and files loaded using XFS-interface having some data (eg- sample.dat used in stage 2).