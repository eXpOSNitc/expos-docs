---
title: 'Stage 25 :
                        File Write (12 Hours)'
---
<div class="panel-collapse collapse" id="collapse25">
 <div class="panel-body">
  <!--Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo25">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo25">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Understanding the allocation of disk blocks to a file.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Implementation of
         <i>
          Write
         </i>
         and
         <i>
          Seek
         </i>
         system calls.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Modify
         <i>
          Shutdown
         </i>
         system call so that file writes are committed to the disk
                                    properly.
        </li>
       </ul>
      </div>
     </li>
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo25a">
       Pre-requisite Reading
      </a>
      <div class="panel-collapse expand" id="lo25a">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Description of disk data structures -
         <a href="os_design-files/disk_ds.html#inode_table" target="_blank">
          Inode table
         </a>
         and
         <a href="os_design-files/disk_ds.html#disk_free_list">
          disk
                          free list
         </a>
         .
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Description of memory data structures -
         <a href="os_design-files/mem_ds.html#buffer_table" target="_blank">
          Buffer table
         </a>
         ,
         <a href="os_design-files/mem_ds.html#file_table" target="_blank">
          Open
                          file table
         </a>
         and
         <a href="os_design-files/process_table.html#per_process_table" target="_blank">
          per-process
                          resource table
         </a>
         .
        </li>
       </ul>
      </div>
     </li>
    </ul>
   </div>
  </div>
  <!--End Learning Objectives-->
  <br/>
  <p>
   In this stage, We will learn how contents of a file are modified using
   <i>
    Write
   </i>
   system
                        call.
   <i>
    Seek
   </i>
   system call which is used to change the LSEEK position for a open instance is
                        also implemented in this stage.
   <i>
    Shutdown
   </i>
   system call is modified to terminate all
                        processes and store back the memory buffers which are modified during
   <i>
    Write
   </i>
   system call
                        to the disk.
  </p>
  <br/>
  <b style="font-size: 20px">
   Interrupt routine 7 (
   <i>
    Write
   </i>
   system call)
  </b>
  <br/>
  <br/>
  <p>
   Interrupt routine 7 written in stage 15, writes data (words) only to the terminal. In this
                        stage, we will modify
   <i>
    Write
   </i>
   system call to write data into a file.
   <i>
    Write
   </i>
   system
                        call has system call number 5. From ExpL programs,
   <i>
    Write
   </i>
   system call is called using
   <a href="os_spec-files/dynamicmemoryroutines.html" target="_blank">
    exposcall function
   </a>
   .
  </p>
  <br/>
  <figure style="text-align: center;">
   <img src="img/roadmap/FileWrite.png" style="display:block;margin-left:auto;margin-right:auto"/>
   <br/>
   <figcaption>
    Control flow for writing a word to a file
   </figcaption>
  </figure>
  <br/>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    <b>
     Write system call
    </b>
   </li>
   <p>
    <i>
     Write
    </i>
    system call takes as arguments 1) a file descriptor and 2) a word to be written
                          into the file.
    <i>
     Write
    </i>
    system call locks the inode at the beginning of the system call
                          and releases the lock at the end of the system call. The functions
    <b>
     Acquire Inode
    </b>
    and
    <b>
     Release Inode
    </b>
    of
    <a href="os_modules/Module_0.html" target="_blank">
     Resource Manager
                            Module
    </a>
    are used to lock and release inodes.
   </p>
   <p>
    After acquiring the Inode,
    <i>
     Write
    </i>
    system call writes the given word to the file, at
                          the offset determined by LSEEK (field in the
    <a href="os_design-files/mem_ds.html#file_table">
     open
                            file table
    </a>
    entry). Previously present data, if any, at the position determined by LSEEK
                          is overwritten by the write operation. The maximum file size permitted by eXpOS is four disk
                          blocks. Hence,
    <i>
     Write
    </i>
    fails if the LSEEK value exceeds 2047.
   </p>
   <p>
    The
    <i>
     Write
    </i>
    system call finds the
    <b>
     logical block number
    </b>
    corresponding to the
                          LSEEK position using the formula LSEEK / 512. LSEEK % 512 gives the
    <b>
     offset position
    </b>
    in
                          the block to which data must be written into. For example, if the LSEEK value is 1024, then
                          the block number will be 2 (third data block) and the offset is 0. The block numbers of the
                          disk blocks that had been allocated for the file so far are stored in the
    <a href="os_design-files/disk_ds.html#inode_table" target="_blank">
     inode table
    </a>
    entry corresponding to the file.
   </p>
   <p>
    In the above example, suppose that the file had been allocated three or more
                          blocks earlier. Then, the physical block number corresponding to logical block number = 2
                          will have a valid entry in the inode table for the file. Hence,
    <i>
     Write
    </i>
    system call must
                          bring that block into the buffer and write the data into the required offset position within
                          the block. However, if there is no disk block allocated for logical block number = 2 (that is
                          the file had been allocated only 2 blocks so far), then
    <i>
     Write
    </i>
    system call must
                          allocate a new block for the file.
   </p>
   <p>
    eXpOS design ensures that the value of LSEEK can never exceed the file size. This ensures
                          that a write operation allocates exactly one new block for a file when
                          the LSEEK value is a multiple of 512 and is equal to the file size (why?). In particular, the
                          first data block for a newly created file is allocated upon the first write into the file. To
                          allocate a new block for the file,
    <i>
     Write
    </i>
    invokes
    <b>
     Get Free Block
    </b>
    function of
    <a href="os_modules/Module_2.html" target="_blank">
     memory manager module
    </a>
    .
   </p>
   <p>
    For writing to position LSEEK in the file, the disk block corresponding to position LSEEK
                          has to be present in the memory. To bring the required disk block into the memory buffer and
                          write the given word to position LSEEK,
    <i>
     Write
    </i>
    invokes
    <b>
     Buffered Write
    </b>
    function
                          of the
    <a href="os_modules/Module_3.html" target="_blank">
     file manager module
    </a>
    . Buffered
                          Write function expects the physical block number as argument.
    <i>
     Write
    </i>
    system call finds
                          the physical block number corresponding to the logical block number from the inode table
                          entry of the file.
   </p>
   <p>
    Write (and Delete) fails if the user id of the process calling Write has no access
                          permission to modify the file (see
    <a href="os_spec-files/multiuser.html#file_access_permissions" target="_blank">
     file access permissions
    </a>
    ). Since in the present stage the user id of all
                          processes is set to root, Write fails
                          only on the root file and executable files.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Write
    </i>
    system call using detailed algorithm
                          provided
    <a href="os_design-files/write.html" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <li>
    <b>
     Buffered Write (function number = 1,
     <a href="os_modules/Module_3.html" target="_blank">
      file
                              manager module
     </a>
     )
    </b>
   </li>
   <p>
    <b>
     Buffered Write
    </b>
    takes a disk block number, offset and a word as arguments. The task of
                          Buffered Write is to write the given word to the given disk block at the position specified
                          by the offset. To write a word to a disk block, the disk block has to be brought into memory.
    <a href="Tutorials/filesystem_implementation.html#memory_buffer_cache" target="_blank">
     Memory
                            buffer cache
    </a>
    is used for this purpose. The disk block is loaded (if not loaded already)
                          into the buffer page with buffer number specified by the formula -
    <i>
     (disk block number%4)
    </i>
    .
                          To use a buffer page, it has to be locked by invoking
    <b>
     Acquire Buffer
    </b>
    function of
    <a href="os_modules/Module_0.html" target="_blank">
     resource manager module
    </a>
    . To load a disk
                          block into a memory buffer page, Buffered Write invokes the function
    <b>
     Disk Load
    </b>
    of
    <a href="os_modules/Module_4.html" target="_blank">
     device manager module
    </a>
    . After loading
                          the given disk block into the corresponding buffer, the given word is written to the memory
                          buffer at the position specified by the offset.
    <b>
     As the buffer is modified, the DIRTY BIT
                            in the corresponding buffer table entry is set to 1.
    </b>
   </p>
   <p>
    Buffered Write may find that, the buffer page to which a disk block has to be loaded
                          contains some other disk block. In such case, if the buffer is modified (dirty bit is set),
                          the disk block present in the buffer is stored back into the disk before loading the new disk
                          block. To store a disk block back into the disk, Buffered Write invokes
    <b>
     Disk Store
    </b>
    function of the
    <a href="os_modules/Module_4.html" target="_blank">
     device manager module
    </a>
    .
                          Finally, the buffer page is released by invoking
    <b>
     Release Buffer
    </b>
    function of resource
                          manager module.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Buffered Write
    </i>
    function using the detailed
                          algorithm given in the file manager module link above.
   </p>
   <br/>
   <p style="text-indent: 0px">
    <code>
     Note :
    </code>
    <b>
     [Implementation Hazard]
    </b>
    Algorithms of
                          Buffered Write and Buffered Read functions are almost identical, except that in Buffered
                          Write - given word is written to the buffer whereas in Buffered Read - a word is read from
                          the buffer. If your code for file manager module exceeds maximum number of assembly
                          instructions permitted for a eXpOS module (512 instructions), then implement the code for
    <b>
     Buffered
                            Read
    </b>
    and
    <b>
     Buffered Write
    </b>
    in a single 'if block' to reduce number of instructions.
   </p>
   <br/>
   <li>
    <b>
     Get Free Block (function number = 3,
     <a href="os_modules/Module_2.html" target="_blank">
      memory
                              manager module
     </a>
     )
    </b>
   </li>
   <p>
    <b>
     Get Free Block
    </b>
    function does not take any argument and returns the block number of a
                          free block in the disk. If no free block is found, Get Free Block returns -1. A free block
                          can be found by searching for a free entry in the
    <a href="os_design-files/disk_ds.html#disk_free_list">
     disk
                            free list
    </a>
    from position DISK_FREE_AREA to DISK_SWAP_AREA-1. A free entry in the disk
                          free list is denoted by 0. In the disk, the blocks from 69 to 255 called User blocks, are
                          reserved for allocation to executable and data files. SPL constant
    <a href="support_tools-files/constants.html" target="_blank">
     DISK_FREE_AREA
    </a>
    gives the starting block number for User blocks.
    <a href="support_tools-files/constants.html" target="_blank">
     DISK_SWAP_AREA
    </a>
    gives the starting block number of swap area. See
    <a href="os_implementation.html" target="_blank">
     disk organization
    </a>
    .
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Get Free Block
    </i>
    function using the detailed
                          algorithm given in the memory manager module link above.
   </p>
   <br/>
  </ol>
  <p style="text-indent: 0px">
   <code>
    Note :
   </code>
   The implementation of
   <b>
    <i>
     Write
    </i>
   </b>
   system
                        call and
   <b>
    Buffered Write
   </b>
   ,
   <b>
    Get Free Block
   </b>
   functions are final.
  </p>
  <br/>
  <b style="font-size: 20px">
   Interrupt routine 5 (
   <i>
    Seek
   </i>
   system call)
  </b>
  <br/>
  <br/>
  <p>
   Interrupt routine 5 implements
   <i>
    Seek
   </i>
   system call along with
   <i>
    Open
   </i>
   and
   <i>
    Close
   </i>
   system calls.
   <i>
    Seek
   </i>
   has system call number 6. From ExpL programs,
   <i>
    Seek
   </i>
   system call
                        is called using
   <a href="os_spec-files/dynamicmemoryroutines.html" target="_blank">
    exposcall
                          function
   </a>
   .
  </p>
  <br/>
  <br/>
  <figure style="text-align: center;">
   <img src="img/roadmap/Seek.png" style="display:block;margin-left:auto;margin-right:auto"/>
   <br/>
   <figcaption>
    Control flow for
    <i>
     Seek
    </i>
    system call
   </figcaption>
  </figure>
  <br/>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    <b>
     Seek system call
    </b>
   </li>
   <p>
    <i>
     Seek
    </i>
    system call is used to move LSEEK pointer value for an open instance according
                          to users requirement.
    <i>
     Seek
    </i>
    system call takes as argument a file descriptor and an
                          offset from the user program.
    <i>
     Seek
    </i>
    updates the LSEEK field in the
    <a href="os_design-files/mem_ds.html#file_table" target="_blank">
     open file table
    </a>
    corresponding to the open instance according to the
                          provided offset value. Offset value can be any integer (positive, zero or negative). If the
                          given offset value is 0, then LSEEK field is set to the starting of the file. For a non-zero
                          value of offset, the given offset is added to the current LSEEK value. If the new LSEEK
                          exceeds size of the file, then LSEEK is set to file size. If the new LSEEK position becomes
                          negative, then
    <i>
     Seek
    </i>
    system call fails and return to user program with appropriate
                          error code without changing the LSEEK position.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Seek
    </i>
    system call using detailed algorithm provided
    <a href="os_design-files/seek.html">
     here
    </a>
    .
   </p>
   <br/>
  </ol>
  <p style="text-indent: 0px">
   <code>
    Note :
   </code>
   The implementation of
   <i>
    Seek
   </i>
   system call is
                        final.
  </p>
  <br/>
  <b style="font-size: 20px">
   Interrupt routine 15 (
   <i>
    Shutdown
   </i>
   system call)
  </b>
  <br/>
  <br/>
  <p>
   Now that eXpOS supports writing to the files, the disk has to be consistent with the modified
                        files before the system shuts down.
   <i>
    Shutdown
   </i>
   system call is modified in this stage to
                        store back the buffers changed by the
   <i>
    Write
   </i>
   system call.
   <i>
    Shutdown
   </i>
   system call
                        also terminates all the processes except current process, IDLE and INIT by invoking
   <b>
    Kill All
   </b>
   function of
   <a href="os_modules/Module_1.html" target="_blank">
    process manager module
   </a>
   .
                        Finally
   <i>
    Shutdown
   </i>
   halts the system after disk is made consistent.
  </p>
  <br/>
  <figure style="text-align: center;">
   <img src="img/roadmap/shutdown.png" style="display:block;margin-left:auto;margin-right:auto"/>
   <br/>
   <figcaption>
    Control flow for
    <i>
     Shutdown
    </i>
    system call
   </figcaption>
  </figure>
  <br/>
  <br/>
  <p style="text-indent: 0px">
   Modify
   <i>
    Shutdown
   </i>
   system call (interrupt routine 15) to perform
                        the following addition steps.
  </p>
  <ul style="list-style-type: disc; margin-left: 10px; ">
   <li style="padding-left: 20px">
    Invoke
    <b>
     Kill All
    </b>
    function of
    <a href="os_modules/Module_1.html" target="_blank">
     process manager module
    </a>
    . Kill All terminates all the processes except
                          IDLE, INIT and the process calling
    <i>
     Shutdown
    </i>
    .
   </li>
   <li style="padding-left: 20px">
    For every valid entry in the
    <a href="os_design-files/mem_ds.html#buffer_table" target="_blank">
     buffer table
    </a>
    (BLOCK NUMBER is not equal to -1), if the DIRTY BIT field
                          is set, then store back the buffer page of that buffer entry into the corresponding disk
                          block by invoking
    <b>
     Disk Store
    </b>
    function of the
    <a href="os_modules/Module_4.html" target="_blank">
     device
                            manager module
    </a>
    .
   </li>
  </ul>
  <p style="text-indent: 0px">
   Implement
   <i>
    Shutdown
   </i>
   system call using detailed algorithm
                        provided
   <a href="os_design-files/shutdown.html">
    here
   </a>
   .
  </p>
  <br/>
  <b>
   Kill All (function number = 5,
   <a href="os_modules/Module_1.html" target="_blank">
    process
                          manager module
   </a>
   )
  </b>
  <br/>
  <br/>
  <p>
   <b>
    Kill All
   </b>
   function takes PID of a process as an argument. Kill All terminates all the
                        processes except IDLE, INIT and the process with given PID. Kill All first locks all the files
                        present in the inode table by invoking
   <b>
    Acquire Inode
   </b>
   function of
   <a href="os_modules/Module_0.html" target="_blank">
    resource manager module
   </a>
   for every file. Locking all the inodes makes sure
                        that, no process is in the middle of any file operation. If suppose a process (say A) is using
                        a file and has locked the inode, then the process which has invoked Kill All will wait until
                        process A completes the file operation and releases the inode. After acquiring all the inodes,
                        Kill All terminates all the processes (except IDLE, INIT and process with given PID) by
                        invoking
   <b>
    Exit Process
   </b>
   function of
   <a href="os_modules/Module_1.html" target="_blank">
    process
                          manager module
   </a>
   for every process. Finally, all the acquired inodes are released by
                        invoking
   <b>
    Release Inode
   </b>
   function of resource manager module for each valid file.
  </p>
  <p style="text-indent: 0px">
   Implement Kill All function using the detailed algorithm given in the
                        process manager module link above.
  </p>
  <br/>
  <p style="text-indent: 0px">
   <code>
    Note :
   </code>
   The implementation of the
   <b>
    <i>
     Shutdown
    </i>
   </b>
   system call
   <b>
    Kill All
   </b>
   function is final.
  </p>
  <br/>
  <b>
   Implementation of Shell executable file commands
  </b>
  <br/>
  <br/>
  <p>
   Linux shell support file commands which makes working with files present in the system easier.
                        An example of such file commands that Linux support is "ls". (Command "ls" lists all the files
                        present in the current directory.) Now that all file related system calls are supported by
                        eXpOS, we can implement few of these commands in eXpOS. This will enrich user experience for
                        handling the files. Support for file commands ls, rm, cp, cat will be added to shell by
                        implementing executable files for the commands. To implement the command ls, write a program
                        ls.expl according to specification given in
   <a href="os_spec-files/shell_spec.html#executable_commands" target="_blank">
    executable commands/files
   </a>
   . Compile this program to generate executable
                        file ls.xsm and load into the disk using XFS-interface. To run command "ls", run the executable
                        file ls.xsm from the shell.
  </p>
  <p style="text-indent: 0px">
   Implement commands
   <b>
    ls, rm, cp, cat
   </b>
   as executable files
                        according to the specification of
   <a href="os_spec-files/shell_spec.html#executable_commands" target="_blank">
    executable commands/files
   </a>
   and load into the disk as executable files.
  </p>
  <br/>
  <b>
   Making things work
  </b>
  <br/>
  <br/>
  <p>
   Compile and load the modified files to the disk using XFS-interface.
  </p>
  <br/>
  <b style="color:#26A65B">
   Assignment 1:
  </b>
  Write an ExpL program to take file name(string) and
                      permission(integer) as input from the console and create a file with the provided name and
                      permission. Write numbers from 1 to 1100 into the file and print the contents of the file in the
                      reverse order (You will need Seek system call to do this). Run this program using shell.
  <br/>
  <br/>
  <b style="color:#26A65B">
   Assignment 2:
  </b>
  Write an ExpL program to append numbers from 2000 to
                      2513 to the file created in first assignment and print the contents of the file in reverse order.
                      Run this program using shell.
  <br/>
  <br/>
  <b style="color:#26A65B">
   Assignment 3:
  </b>
  Run the program provided
  <a href="test_prog.html#test_program_6" target="_blank">
   here
  </a>
  using shell. The program takes a file name and permission as input and
                      creates a new file with given input. It then forks to create two child processes. The two child
                      processes act as writers and parent as reader. A file open instance is shared between two writers
                      and there is separate open instance of the same file for reader. Two writers will write numbers
                      from 1 to 100 into the file, with one writer adding even numbers and other writing odd numbers.
                      The reader reads from the file and prints the data into the console concurrently. To synchronize the use of
                      the shared open file between two writers a semaphore is used. The program prints integers
                      from 1 to 100, not necessarily in sequential order.
  <br/>
  <br/>
  <b style="color:#26A65B">
   Assignment 4:
  </b>
  Run the program provided
  <a href="test_prog.html#test_program_15" target="_blank">
   here
  </a>
  using shell. The program first creates 4 files with values from s to 4*c+s, where s=1..4 and c=0..511. The program then, merges the 4 files taking 2 at a time, and finally, creates a
  <i>
   merge.dat
  </i>
  file containing numbers from 1 to 2048. Using
  <i>
   cat.xsm
  </i>
  , print the contents of
  <i>
   merge.dat
  </i>
  and check whether it contains the numbers from 1 to 2048 in ascending order.
  <br/>
  <br/>
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq25x">
       <b>
        POSTSCRIPT:
       </b>
       How does an Operating System handle multiple devices in a uniform way?
      </a>
      <div class="panel-collapse collapse" id="collapseq25x">
       <br/>
       <p>
        eXpOS supported just one file system and just two devices - the disk and the terminal. The application interface to the file system and the terminal is the same - through the Read/Write system calls. The OS presents a
        <b>
         single abstraction
        </b>
        (or interface) to the application program for file read/write and console read/write, hiding the fact that these are two completely different hardware devices.
       </p>
       <p>
        Let us review one of the system calls - say the Read system call. The system call code  checks whether the read is issued for the terminal or the file system. If the read is from the terminal, then the system call redirects control to the terminal read function of the device manager. If the read is for a disk file, Read system call directly access the file system data structures to perform the system call (with appropriate calls to resource manager, and file manager for performing subtasks - See
        <a href="os_design-files/read.html" target="_blank">
         here
        </a>
        ).
       </p>
       <p>
        Such a simple implementation works because eXpOS is dealing with just two devices. A modern OS might be connected to several hard disks and each hard disk may contain separate file systems on different disk partitions. Similarly, a plethora of devices - mouse, printer, USB devices and so on will be connected to the system. New devices may be needed to be connected to  the system and the OS shouldn’t require re-design to accommodate each new device! How should then OS design be changed to handle such complexity?
       </p>
       <br/>
       <p>
        The general
        <b>
         principle of abstraction
        </b>
        holds the key in designing the OS for  handling a large number of devices and file systems. We first look at devices.
       </p>
       <p>
        1. The OS will provide the same set of system calls to access every device -  say, Open, Close, Read, Write, Seek, etc. (Some system calls may be vaccus for some devices - for instance, a Read operation on a printer or a Write to a mouse may perform nothing).
       </p>
       <p>
        2. Open system call invoked with the appropriate device/file name returns a descriptor which shall be used for further Read/Write/Seek operations to the device.
       </p>
       <p>
        3. The OS expects that the manufacturer of each device supplies a device specific interface software called the
        <b>
         device driver
        </b>
        . The device driver code for each device must be loaded as part of the OS. The OS expects that each device driver contains functions Open, Close, Read, Write and Seek. For instance, Write function in the print device driver may take as input a word and may contain low level code to issue appropriate command to the printer device to print the word.
       </p>
       <p>
        4. When an application invokes a system call like Read, the system call handler checks the file descriptor and identifies the correct device. It then invokes the Read function of the appropriate device driver.
       </p>
       <br/>
       <p>
        The principle involved in handling multiple file systems is similar. Each file system will be associated with a corresponding file system driver implementing Open, Close, Read, Write and Seek operations for the corresponding file system. Thus files and devices are handled in a single uniform manner.
       </p>
       <p>
        The advantage of such abstract strategy is that any number of devices can be added to the system, provided device manufacturers and file system designers comply to provide appropriate device/file system drivers with the standard interface stipulated by the OS.
       </p>
       <p>
        The following figure demonstrates the flow of control in device/file operations.
       </p>
       <img src="img/os-design/device_driver.png" style="display:block;margin-left:auto;margin-right:auto"/>
       <br/>
       <p>
        <b>
         Note:
        </b>
        Each device will have a programmable device controller hardware that is connected to the machine through a port/serial bus or some such interface. The device driver issues the Write/Read command to the device controller and the device controller in turn commands the device to perform appropriate action to get the task done. Thus, in the case of a printer, the device driver will issue commands to the printer controller, which in turn controls the printer actions.
       </p>
       <br/>
       <p>
        Some additional implementation details and pointers to advanced reading concerning the above abstract principles are described below.
       </p>
       <p>
        1. All modern file systems support a directory structure for file systems. (This is one major feature missing in eXpOS). In a directory file system, the filename field in the inode entry of a file will be a complete pathname describing the logical directory location of the file in the directory structure of the file system. The last part of the pathname will be the name of the file. For instance, a pathname “/usr/myfiles/hello” specifies a file with name “hello” in the directory “/usr/myfiles”.
       </p>
       <p>
        2. Traditionally Operating systems have a default root file system that supports a directory structure. Other file systems are attached (mounted) as subdirectories of the root file system. When a Read/Write operation is performed on a file, the Read/Write system call checks the pathname of the file to determine which file system driver must be used for Read/Write operations. Devices are also mounted just like file systems.
       </p>
       <a data-toggle="collapse" href="#collapseq25x">
        <span class="fa fa-times">
        </span>
        Close
       </a>
      </div>
     </li>
    </ul>
   </div>
  </div>
  <a data-toggle="collapse" href="#collapse25">
   <span class="fa fa-times">
   </span>
   Close
  </a>
 </div>
</div>
