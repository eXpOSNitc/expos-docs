---
title: 'Stage 25 : File Write (12 Hours)'
original_url: https://exposnitc.github.io/Roadmap.html
---

!!! note "Learning Objectives"
    - Understanding the allocation of disk blocks to a file.
    - Implementation of *Write* and *Seek* system calls.
    - Modify *Shutdown* system call so that file writes are committed to the disk properly.
    
!!! abstract "Pre-requisite Reading"
    - Description of disk data structures - [Inode table](../os-design/disk-ds.md#inode-table) and [disk free list](../os-design/disk-ds.md#disk-free-list).
    - Description of memory data structures - [Buffer table](../os-design/mem-ds.md#buffer_table) , [Open file table](../os-design/mem-ds.md#file_table) and [per-process resource table](../os-design/process-table.md#per-process-resource-table) .
    
In this stage, We will learn how contents of a file are modified using *Write* system call. *Seek* system call which is used to change the LSEEK position for a open instance is also implemented in this stage. *Shutdown* system call is modified to terminate all processes and store back the memory buffers which are modified during *Write* system call to the disk.

  
**Interrupt routine 7 ( *Write* system call)**  
  

Interrupt routine 7 written in stage 15, writes data (words) only to the terminal. In this stage, we will modify *Write* system call to write data into a file. *Write* system call has system call number 5. From ExpL programs, *Write* system call is called using [exposcall function](../os-spec/dynamicmemoryroutines.md) .

  

![](../assets/img/roadmap/FileWrite.png)  

Control flow for writing a word to a file

  
  

1.  **Write system call**

*Write* system call takes as arguments 1) a file descriptor and 2) a word to be written into the file. *Write* system call locks the inode at the beginning of the system call and releases the lock at the end of the system call. The functions **Acquire Inode** and **Release Inode** of [Resource Manager Module](../modules/module-00.md) are used to lock and release inodes.

After acquiring the Inode, *Write* system call writes the given word to the file, at the offset determined by LSEEK (field in the [open file table](../os-design/mem-ds.md#file_table) entry). Previously present data, if any, at the position determined by LSEEK is overwritten by the write operation. The maximum file size permitted by eXpOS is four disk blocks. Hence, *Write* fails if the LSEEK value exceeds 2047.

The *Write* system call finds the **logical block number** corresponding to the LSEEK position using the formula LSEEK / 512. LSEEK % 512 gives the **offset position** in the block to which data must be written into. For example, if the LSEEK value is 1024, then the block number will be 2 (third data block) and the offset is 0. The block numbers of the disk blocks that had been allocated for the file so far are stored in the [inode table](../os-design/disk-ds.md#inode-table) entry corresponding to the file.

In the above example, suppose that the file had been allocated three or more blocks earlier. Then, the physical block number corresponding to logical block number = 2 will have a valid entry in the inode table for the file. Hence, *Write* system call must bring that block into the buffer and write the data into the required offset position within the block. However, if there is no disk block allocated for logical block number = 2 (that is the file had been allocated only 2 blocks so far), then *Write* system call must allocate a new block for the file.

eXpOS design ensures that the value of LSEEK can never exceed the file size. This ensures that a write operation allocates exactly one new block for a file when the LSEEK value is a multiple of 512 and is equal to the file size (why?). In particular, the first data block for a newly created file is allocated upon the first write into the file. To allocate a new block for the file, *Write* invokes **Get Free Block** function of [memory manager module](../modules/module-02.md) .

For writing to position LSEEK in the file, the disk block corresponding to position LSEEK has to be present in the memory. To bring the required disk block into the memory buffer and write the given word to position LSEEK, *Write* invokes **Buffered Write** function of the [file manager module](../modules/module-03.md) . Buffered Write function expects the physical block number as argument. *Write* system call finds the physical block number corresponding to the logical block number from the inode table entry of the file.

Write (and Delete) fails if the user id of the process calling Write has no access permission to modify the file (see [file access permissions](../os-spec/multiuser.md#file_access_permissions) ). Since in the present stage the user id of all processes is set to root, Write fails only on the root file and executable files.

Implement *Write* system call using detailed algorithm provided [here](../os-design/write.md) .

  
11.  **Buffered Write (function number = 1, [file manager module](../modules/module-03.md) )**

**Buffered Write** takes a disk block number, offset and a word as arguments. The task of Buffered Write is to write the given word to the given disk block at the position specified by the offset. To write a word to a disk block, the disk block has to be brought into memory. [Memory buffer cache](../tutorials/filesystem-implementation.md#memory_buffer_cache) is used for this purpose. The disk block is loaded (if not loaded already) into the buffer page with buffer number specified by the formula - *(disk block number%4)* . To use a buffer page, it has to be locked by invoking **Acquire Buffer** function of [resource manager module](../modules/module-00.md) . To load a disk block into a memory buffer page, Buffered Write invokes the function **Disk Load** of [device manager module](../modules/module-04.md) . After loading the given disk block into the corresponding buffer, the given word is written to the memory buffer at the position specified by the offset. **As the buffer is modified, the DIRTY BIT in the corresponding buffer table entry is set to 1.**

Buffered Write may find that, the buffer page to which a disk block has to be loaded contains some other disk block. In such case, if the buffer is modified (dirty bit is set), the disk block present in the buffer is stored back into the disk before loading the new disk block. To store a disk block back into the disk, Buffered Write invokes **Disk Store** function of the [device manager module](../modules/module-04.md) . Finally, the buffer page is released by invoking **Release Buffer** function of resource manager module.

Implement *Buffered Write* function using the detailed algorithm given in the file manager module link above.

  

!!! note 
    **\[Implementation Hazard\]** Algorithms of Buffered Write and Buffered Read functions are almost identical, except that in Buffered Write - given word is written to the buffer whereas in Buffered Read - a word is read from the buffer. If your code for file manager module exceeds maximum number of assembly instructions permitted for a eXpOS module (512 instructions), then implement the code for **Buffered Read** and **Buffered Write** in a single 'if block' to reduce number of instructions.

  
1.   **Get Free Block (function number = 3, [memory manager module](../modules/module-02.md) )**

**Get Free Block** function does not take any argument and returns the block number of a free block in the disk. If no free block is found, Get Free Block returns -1. A free block can be found by searching for a free entry in the [disk free list](../os-design/disk-ds.md#disk-free-list) from position DISK\_FREE\_AREA to DISK\_SWAP\_AREA-1. A free entry in the disk free list is denoted by 0. In the disk, the blocks from 69 to 255 called User blocks, are reserved for allocation to executable and data files. SPL constant [DISK\_FREE\_AREA](../support-tools/constants.md) gives the starting block number for User blocks. [DISK\_SWAP\_AREA](../support-tools/constants.md) gives the starting block number of swap area. See [disk organization](../os-implementation.md) .

Implement *Get Free Block* function using the detailed algorithm given in the memory manager module link above.

  

!!! note 
    The implementation of ***Write*** system call and **Buffered Write** , **Get Free Block** functions are final.

  
**Interrupt routine 5 ( *Seek* system call)**  
  

Interrupt routine 5 implements *Seek* system call along with *Open* and *Close* system calls. *Seek* has system call number 6. From ExpL programs, *Seek* system call is called using [exposcall function](../os-spec/dynamicmemoryroutines.md) .

  
  

![](../assets/img/roadmap/Seek.png)  

Control flow for *Seek* system call

  
  

1.  **Seek system call**

*Seek* system call is used to move LSEEK pointer value for an open instance according to users requirement. *Seek* system call takes as argument a file descriptor and an offset from the user program. *Seek* updates the LSEEK field in the [open file table](../os-design/mem-ds.md#file_table) corresponding to the open instance according to the provided offset value. Offset value can be any integer (positive, zero or negative). If the given offset value is 0, then LSEEK field is set to the starting of the file. For a non-zero value of offset, the given offset is added to the current LSEEK value. If the new LSEEK exceeds size of the file, then LSEEK is set to file size. If the new LSEEK position becomes negative, then *Seek* system call fails and return to user program with appropriate error code without changing the LSEEK position.

Implement *Seek* system call using detailed algorithm provided [here](../os-design/seek.md) .

  
!!! note
    The implementation of *Seek* system call is final.

  
**Interrupt routine 15 ( *Shutdown* system call)**  
  

Now that eXpOS supports writing to the files, the disk has to be consistent with the modified files before the system shuts down. *Shutdown* system call is modified in this stage to store back the buffers changed by the *Write* system call. *Shutdown* system call also terminates all the processes except current process, IDLE and INIT by invoking **Kill All** function of [process manager module](../modules/module-01.md) . Finally *Shutdown* halts the system after disk is made consistent.

  

![](../assets/img/roadmap/shutdown.png)  

Control flow for *Shutdown* system call

  
  

Modify *Shutdown* system call (interrupt routine 15) to perform the following addition steps.

-   Invoke **Kill All** function of [process manager module](../modules/module-01.md) . Kill All terminates all the processes except IDLE, INIT and the process calling *Shutdown* .
-   For every valid entry in the [buffer table](../os-design/mem-ds.md#buffer_table) (BLOCK NUMBER is not equal to -1), if the DIRTY BIT field is set, then store back the buffer page of that buffer entry into the corresponding disk block by invoking **Disk Store** function of the [device manager module](../modules/module-04.md) .

Implement *Shutdown* system call using detailed algorithm provided [here](../os-design/shutdown.md) .

  
**Kill All (function number = 5, [process manager module](../modules/module-01.md) )**  
  

**Kill All** function takes PID of a process as an argument. Kill All terminates all the processes except IDLE, INIT and the process with given PID. Kill All first locks all the files present in the inode table by invoking **Acquire Inode** function of [resource manager module](../modules/module-00.md) for every file. Locking all the inodes makes sure that, no process is in the middle of any file operation. If suppose a process (say A) is using a file and has locked the inode, then the process which has invoked Kill All will wait until process A completes the file operation and releases the inode. After acquiring all the inodes, Kill All terminates all the processes (except IDLE, INIT and process with given PID) by invoking **Exit Process** function of [process manager module](../modules/module-01.md) for every process. Finally, all the acquired inodes are released by invoking **Release Inode** function of resource manager module for each valid file.

Implement Kill All function using the detailed algorithm given in the process manager module link above.

  
!!! note 
    The implementation of the ***Shutdown*** system call **Kill All** function is final.

  
#### Implementation of Shell executable file commands
  

Linux shell support file commands which makes working with files present in the system easier. An example of such file commands that Linux support is "ls". (Command "ls" lists all the files present in the current directory.) Now that all file related system calls are supported by eXpOS, we can implement few of these commands in eXpOS. This will enrich user experience for handling the files. Support for file commands ls, rm, cp, cat will be added to shell by implementing executable files for the commands. To implement the command ls, write a program ls.expl according to specification given in [executable commands/files](../os-spec/shell-spec.md#executable_commands) . Compile this program to generate executable file ls.xsm and load into the disk using XFS-interface. To run command "ls", run the executable file ls.xsm from the shell.

Implement commands **ls, rm, cp, cat** as executable files according to the specification of [executable commands/files](../os-spec/shell-spec.md#executable_commands) and load into the disk as executable files.

  
#### Making things work  
Compile and load the modified files to the disk using XFS-interface.

  
!!! assignment "Assignment 1"
    Write an ExpL program to take file name(string) and permission(integer) as input from the console and create a file with the provided name and permission. Write numbers from 1 to 1100 into the file and print the contents of the file in the reverse order (You will need Seek system call to do this). Run this program using shell.  
  
!!! assignment "Assignment 2"
    Write an ExpL program to append numbers from 2000 to 2513 to the file created in first assignment and print the contents of the file in reverse order. Run this program using shell.  
  
!!! assignment "Assignment 3"
    Run the program provided [here](../test-programs/index.md#test-program-6) using shell. The program takes a file name and permission as input and creates a new file with given input. It then forks to create two child processes. The two child processes act as writers and parent as reader. A file open instance is shared between two writers and there is separate open instance of the same file for reader. Two writers will write numbers from 1 to 100 into the file, with one writer adding even numbers and other writing odd numbers. The reader reads from the file and prints the data into the console concurrently. To synchronize the use of the shared open file between two writers a semaphore is used. The program prints integers from 1 to 100, not necessarily in sequential order.  
  
!!! assignment "Assignment 4"
    Run the program provided [here](../test-programs/index.md#test-program-15) using shell. The program first creates 4 files with values from s to 4\*c+s, where s=1..4 and c=0..511. The program then, merges the 4 files taking 2 at a time, and finally, creates a *merge.dat* file containing numbers from 1 to 2048. Using *cat.xsm* , print the contents of *merge.dat* and check whether it contains the numbers from 1 to 2048 in ascending order.  
  

-   [**POSTSCRIPT:** How does an Operating System handle multiple devices in a uniform way?](index.md#collapseq25x)
    
      
    
    eXpOS supported just one file system and just two devices - the disk and the terminal. The application interface to the file system and the terminal is the same - through the Read/Write system calls. The OS presents a **single abstraction** (or interface) to the application program for file read/write and console read/write, hiding the fact that these are two completely different hardware devices.
    
    Let us review one of the system calls - say the Read system call. The system call code checks whether the read is issued for the terminal or the file system. If the read is from the terminal, then the system call redirects control to the terminal read function of the device manager. If the read is for a disk file, Read system call directly access the file system data structures to perform the system call (with appropriate calls to resource manager, and file manager for performing subtasks - See [here](../os-design/read.md) ).
    
    Such a simple implementation works because eXpOS is dealing with just two devices. A modern OS might be connected to several hard disks and each hard disk may contain separate file systems on different disk partitions. Similarly, a plethora of devices - mouse, printer, USB devices and so on will be connected to the system. New devices may be needed to be connected to the system and the OS shouldn’t require re-design to accommodate each new device! How should then OS design be changed to handle such complexity?
    
      
    
    The general **principle of abstraction** holds the key in designing the OS for handling a large number of devices and file systems. We first look at devices.
    
    1\. The OS will provide the same set of system calls to access every device - say, Open, Close, Read, Write, Seek, etc. (Some system calls may be vaccus for some devices - for instance, a Read operation on a printer or a Write to a mouse may perform nothing).
    
    2\. Open system call invoked with the appropriate device/file name returns a descriptor which shall be used for further Read/Write/Seek operations to the device.
    
    3\. The OS expects that the manufacturer of each device supplies a device specific interface software called the **device driver** . The device driver code for each device must be loaded as part of the OS. The OS expects that each device driver contains functions Open, Close, Read, Write and Seek. For instance, Write function in the print device driver may take as input a word and may contain low level code to issue appropriate command to the printer device to print the word.
    
    4\. When an application invokes a system call like Read, the system call handler checks the file descriptor and identifies the correct device. It then invokes the Read function of the appropriate device driver.
    
      
    
    The principle involved in handling multiple file systems is similar. Each file system will be associated with a corresponding file system driver implementing Open, Close, Read, Write and Seek operations for the corresponding file system. Thus files and devices are handled in a single uniform manner.
    
    The advantage of such abstract strategy is that any number of devices can be added to the system, provided device manufacturers and file system designers comply to provide appropriate device/file system drivers with the standard interface stipulated by the OS.
    
    The following figure demonstrates the flow of control in device/file operations.
    
    ![](../assets/img/os-design/device_driver.png)  
    
    **Note:** Each device will have a programmable device controller hardware that is connected to the machine through a port/serial bus or some such interface. The device driver issues the Write/Read command to the device controller and the device controller in turn commands the device to perform appropriate action to get the task done. Thus, in the case of a printer, the device driver will issue commands to the printer controller, which in turn controls the printer actions.
    
      
    
    Some additional implementation details and pointers to advanced reading concerning the above abstract principles are described below.
    
    1\. All modern file systems support a directory structure for file systems. (This is one major feature missing in eXpOS). In a directory file system, the filename field in the inode entry of a file will be a complete pathname describing the logical directory location of the file in the directory structure of the file system. The last part of the pathname will be the name of the file. For instance, a pathname “/usr/myfiles/hello” specifies a file with name “hello” in the directory “/usr/myfiles”.
    
    2\. Traditionally Operating systems have a default root file system that supports a directory structure. Other file systems are attached (mounted) as subdirectories of the root file system. When a Read/Write operation is performed on a file, the Read/Write system call checks the pathname of the file to determine which file system driver must be used for Read/Write operations. Devices are also mounted just like file systems.
  