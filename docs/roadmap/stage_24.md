---
title: 'Stage 24 :
                        File Read (12 Hours)'
---
<div class="panel-collapse collapse" id="collapse24">
 <div class="panel-body">
  <!--Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo24">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo24">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Understanding buffer cache.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Implementation of
         <i>
          Open
         </i>
         ,
         <i>
          Close
         </i>
         and
         <i>
          Read
         </i>
         system calls.
        </li>
       </ul>
      </div>
     </li>
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo24a">
       Pre-requisite Reading
      </a>
      <div class="panel-collapse expand" id="lo24a">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Description of data structures -
         <a href="os_design-files/mem_ds.html#file_lock_status_table" target="_blank">
          File(inode) status table
         </a>
         ,
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
  <!--
<b>Gain the understanding of the following data structures and their fields if you haven't done already - <a href="os_design-files/mem_ds.html#file_lock_status_table" target="_blank">File(inode) status table</a>, <a href="os_design-files/mem_ds.html#buffer_table" target="_blank">Buffer table</a>, <a href="os_design-files/mem_ds.html#file_table" target="_blank">Open file table</a> and <a href="os_design-files/process_table.html#per_process_table" target="_blank">per-process resource table</a>.</b><br><br>-->
  <p>
   In this stage, we will understand the mechanism of opening and closing a file with the help of
   <i>
    Open
   </i>
   and
   <i>
    Close
   </i>
   system calls. We will also understand how contents of a file can
                        be read by using
   <i>
    Read
   </i>
   system call.
   <i>
    Fork
   </i>
   system call and
   <b>
    Free User Area Page
   </b>
   function of process manager module are also modified in this stage.
  </p>
  <br/>
  <b style="font-size: 20px">
   Interrupt routine 5
  </b>
  <br/>
  <br/>
  <p>
   The system calls
   <i>
    Open
   </i>
   and
   <i>
    Close
   </i>
   are implemented in the interrupt routine 5.
   <i>
    Open
   </i>
   and
   <i>
    Close
   </i>
   have system call numbers 2 and 3 respectively. From ExpL programs, these
                        system calls are called using
   <a href="os_spec-files/dynamicmemoryroutines.html" target="_blank">
    exposcall
                          function
   </a>
   .
  </p>
  <br/>
  <figure style="text-align: center;">
   <img src="img/roadmap/open_close.png" style="display:block;margin-left:auto;margin-right:auto"/>
   <br/>
   <figcaption>
    Control flow for
    <i>
     Open
    </i>
    and
    <i>
     Close
    </i>
    system calls
   </figcaption>
  </figure>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    <b>
     Open system call
    </b>
   </li>
   <p>
    <i>
     Open
    </i>
    system call takes a filename as an argument from the user program. To perform
                          read/write operations on a file, a process must open the file first.
    <i>
     Open
    </i>
    system call
                          creates a new
    <b>
     open instance
    </b>
    for the file and returns a
    <b>
     file descriptor
    </b>
    (index
                          of the new
    <a href="os_design-files/process_table.html#per_process_table" target="_blank">
     per-process
                            resource table
    </a>
    entry created for the open instance). Further operations on the open
                          instance are performed using this file descriptor. A process can open a file several times
                          and each time a different open instance (and new descriptor) is created. The global data
                          structure,
    <a href="os_design-files/mem_ds.html#file_table" target="_blank">
     Open file table
    </a>
    keeps track of all the open file instances in the system. (A new
                          entry is created in this table whenever the
    <i>
     Open
    </i>
    system call is invoked with any file
                          name.)
    <a href="os_design-files/mem_ds.html#file_lock_status_table">
     File status table
    </a>
    is
                          a global data structure that maintains an entry for every file in the system (not just opened
                          files).
   </p>
   <p>
    <i>
     Open
    </i>
    system call creates new entries for the file to be opened in the per-process
                          resource table and the open file table. A process keeps track of an open instance by storing
                          the index of the open file table entry of the instance in (the corresponding) resource table
                          entry. When a file is opened, the OPEN INSTANCE COUNT in the open file table is set to 1 and
    <b>
     seek
    </b>
    position is initialized to the starting of the file (0).
   </p>
   <p>
    Each time when a file is opened, the FILE OPEN COUNT in the file status table entry for the
                          file is incremented by one.
    <i>
     Open
    </i>
    system call invokes
    <b>
     Open
    </b>
    function of
    <a href="os_modules/Module_3.html" target="_blank">
     file manager module
    </a>
    to deal with global data structures -
    <a href="os_design-files/mem_ds.html#file_lock_status_table" target="_blank">
     file status table
    </a>
    and
    <a href="os_design-files/mem_ds.html#file_table" target="_blank">
     open file table
    </a>
    . When a process executes a
    <i>
     Fork
    </i>
    system call, the
                          open instances of files (and semaphores) created by the process are shared between the
                          current process and its child. As an effect of
    <i>
     Fork
    </i>
    , the OPEN INSTANCE COUNT in the
                          open file table entry corresponding to the open instance is incremented by one.
   </p>
   <p>
    It is necessary not to be confused between FILE OPEN COUNT (in the file status
                          table) and OPEN INSTANCE COUNT (in the open file table). The former keeps track of the global
                          count of how many times
    <i>
     Open
    </i>
    system call has been invoked with each file in the system
                          - that is the number of open instances of a file at a given point of time. This count is
                          decremented each time when a
    <i>
     Close
    </i>
    is invoked on the file by any process. Each open
                          instance could be further
    <b>
     shared
    </b>
    between multiple processes (via
    <i>
     Fork
    </i>
    ). OPEN
                          INSTANCE COUNT value of a particular open instance essentially keeps track of this "share
                          count".
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Open
    </i>
    system call using the detailed algorithm
                          provided
    <a href="os_design-files/open.html" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <li>
    <b>
     Close system call
    </b>
   </li>
   <p>
    When a process no longer needs to perform read/write operations on an open instance of a
                          file, the open instance may be closed using the
    <i>
     Close
    </i>
    system call. Even if a process
                          does not explicitly close an open instance by invoking
    <i>
     Close
    </i>
    system call, the open
                          instance is closed at the termination of the process by
    <i>
     Exit
    </i>
    system call.
   </p>
   <p>
    <i>
     Close
    </i>
    system call takes a file descriptor (index of the
    <a href="os_design-files/process_table.html#per_process_table" target="_blank">
     per-process resource table
    </a>
    entry) as argument from the user program.
    <i>
     Close
    </i>
    system call invalidates the per-process resource table entry (corresponding to given file
                          descriptor) by storing -1 in the Resource Identifier field. To decrement share count of the
                          open instance in the
    <a href="os_design-files/mem_ds.html#file_table" target="_blank">
     open
                            file table
    </a>
    and update the
    <a href="os_design-files/mem_ds.html#file_lock_status_table" target="_blank">
     file status table
    </a>
    accordingly,
    <b>
     Close
    </b>
    function of
    <a href="os_modules/Module_3.html" target="_blank">
     file manager module
    </a>
    is invoked by the
    <i>
     Close
    </i>
    system call.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Close
    </i>
    system call using the detailed algorithm
                          provided
    <a href="os_design-files/close.html">
     here
    </a>
    .
   </p>
   <br/>
   <li>
    <b>
     Open (function number = 3,
     <a href="os_modules/Module_3.html" target="_blank">
      file
                              manager module
     </a>
     )
    </b>
   </li>
   <p>
    <b>
     Open
    </b>
    function is invoked by
    <i>
     Open
    </i>
    system call to update the
    <a href="os_design-files/mem_ds.html#file_lock_status_table" target="_blank">
     file status table
    </a>
    and the
    <a href="os_design-files/mem_ds.html#file_table" target="_blank">
     open file table
    </a>
    when a file is opened. Open takes a file name as an
                          argument. This function locates the inode index for the file in the
    <a href="os_design-files/disk_ds.html#inode_table" target="_blank">
     inode table
    </a>
    and
    <b>
     locks the inode
    </b>
    before proceeding further.
    <b>
     Acquire
                            Inode
    </b>
    function of
    <a href="os_modules/Module_0.html" target="_blank">
     resource manager
                            module
    </a>
    is invoked to lock the file. Locking the file is necessary to make sure that no
                          other process tries to delete the file concurrently. Open function creates a new entry in the
                          open file table and returns the index of this entry to the caller. (Note that this index
                          recieved as return value is stored in the per-process resource table entry by the
    <i>
     Open
    </i>
    system call.) All the fields of the open file table entry are initialized. In case the file
                          is "root" file, INODE INDEX field is initialized to the
    <a href="support_tools-files/constants.html" target="_blank">
     INODE_ROOT
    </a>
    (0). Open function increments the FILE OPEN COUNT field by
                          one in the file status table entry for the file, except if the file is "root" file. (FILE
                          OPEN COUNT is irrelevent for the root file as the root file is pre-loaded into the memory at
                          boot time and can never be deleted.) The lock on the file is released by invoking
    <b>
     Release
                            Inode
    </b>
    function of
    <a href="os_modules/Module_0.html" target="_blank">
     resource manager
                            module
    </a>
    before returning to the caller.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Open
    </i>
    function using the detailed algorithm given
                          in the file manager module link above.
   </p>
   <br/>
   <li>
    <b>
     Close (function number = 4,
     <a href="os_modules/Module_3.html" target="_blank">
      file
                              manager module
     </a>
     )
    </b>
   </li>
   <p>
    <b>
     Close
    </b>
    function is invoked by the
    <i>
     Close
    </i>
    system call to update the
    <a href="os_design-files/mem_ds.html#file_lock_status_table" target="_blank">
     file status table
    </a>
    and the
    <a href="os_design-files/mem_ds.html#file_table" target="_blank">
     open file table
    </a>
    when a file is closed. Close takes an open file table
                          index as argument.
    <i>
     Close
    </i>
    function decrements the share count (i.e OPEN INSTANCE COUNT
                          field in the
    <a href="os_design-files/mem_ds.html" target="_blank">
     open file table
    </a>
    entry)
                          as the process no longer shares the open instance of the file. When the share count becomes
                          zero, this indicates that all processes sharing that open instance of the file have closed
                          the file. Hence, open file table entry corresponding to that open instance of the file is
                          invalidated by setting the INODE INDEX field to -1 and the open count of the file (FILE OPEN
                          COUNT field in
    <a href="os_design-files/mem_ds.html#file_lock_status_table" target="_blank">
     file
                            status table
    </a>
    entry) is decremented.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Close
    </i>
    function using the detailed algorithm given
                          in the file manager module link above.
   </p>
   <br/>
   <li>
    <b>
     Modifications to
     <i>
      Fork
     </i>
     system call
    </b>
   </li>
   <p style="padding-left: 20px">
    There is a simple modification required to the
    <i>
     Fork
    </i>
    System call. When a process forks to create a child process, the file instances currently
                          opened by the parent are now shared between child and parent. To reflect this change, the
                          OPEN INSTANCE COUNT field in the
    <a href="os_design-files/mem_ds.html#file_table" target="_blank">
     open
                            file table
    </a>
    is incremented for each open file instance in the per-process resource table
                          of parent process.
   </p>
   <ul style="list-style-type: disc; margin-left: 10px;">
    <li style="padding-left: 20px">
     While Copying the
     <a href="os_design-files/process_table.html#per_process_table" target="_blank">
      per-process resource table
     </a>
     of parent to the child process do
                            following -
    </li>
    <li style="padding-left: 20px">
     If the resource is a file (check the Resource Identifier field
                            in the per-process resource table), then using the open file table index, increment the
                            OPEN INSTANCE COUNT field in the
     <a href="os_design-files/mem_ds.html#file_table" target="_blank">
      open
                              file table
     </a>
     entry.
    </li>
    /*The change in
    <i>
     Fork
    </i>
    system call to update the
    <a href="os_design-files/mem_ds.html#sem_table" target="_blank">
     semaphore table
    </a>
    , is already done in stage 22*/
   </ul>
   <br/>
   <br/>
   <li>
    <b>
     Modifications to Free User Area Page (function number = 2,
     <a href="os_modules/Module_1.html" target="_blank">
      process manager module
     </a>
     )
    </b>
   </li>
   <p style="padding-left: 20px">
    When a process terminates, all the files the process has opened
                          (and haven't closed explicitly) have to be closed. This is done in the Free User Area page
                          function. The
    <b>
     Close
    </b>
    function of the
    <a href="os_modules/Module_3.html">
     file manager
                            module
    </a>
    is invoked for every open file in the per-process resource table of the process.
   </p>
   <ul style="list-style-type: disc; margin-left: 10px;">
    <li style="padding-left: 20px">
     For each entry in the
     <a href="os_design-files/process_table.html#per_process_table" target="_blank">
      per-process resource table
     </a>
     of the process, do following -
    </li>
    <li style="padding-left: 20px">
     If the resource is valid and is file (check the Resource
                            Identifier field in the per-process resource table), then invoke the Close function of the
     <a href="os_modules/Module_3.html" target="_blank">
      file manager module
     </a>
     .
    </li>
    /*The change in the Free User Area Page to release the unrelased semaphores is already done
                          in stage 22*/
   </ul>
   <br/>
  </ol>
  <p style="text-indent: 0px">
   <code>
    Note :
   </code>
   The implementation of
   <b>
    <i>
     Open
    </i>
   </b>
   ,
   <b>
    <i>
     Close
    </i>
   </b>
   ,
   <b>
    <i>
     Fork
    </i>
   </b>
   system calls and
   <b>
    Open
   </b>
   ,
   <b>
    Close
   </b>
   ,
   <b>
    Free User Area Page
   </b>
   functions are final.
  </p>
  <br/>
  <b style="font-size: 20px">
   Interrupt routine 6 (
   <i>
    Read
   </i>
   system call)
  </b>
  <br/>
  <br/>
  <p>
   Interrupt routine 6 written in stage 16 reads data (words) only from the terminal. In this
                        stage,
   <i>
    Read
   </i>
   system call is modified to read data from files.
   <i>
    Read
   </i>
   system call has
                        system call number 7. From ExpL programs,
   <i>
    Read
   </i>
   system call is called using
   <a href="os_spec-files/dynamicmemoryroutines.html" target="_blank">
    exposcall function
   </a>
   .
  </p>
  <br/>
  <figure style="text-align: center;">
   <img src="img/roadmap/FileRead.png" style="display:block;margin-left:auto;margin-right:auto"/>
   <br/>
   <figcaption>
    Control flow for reading a word from a file
   </figcaption>
  </figure>
  <br/>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    <b>
     <i>
      Read
     </i>
     system call
    </b>
   </li>
   <p>
    <i>
     Read
    </i>
    system call takes as input a file descriptor and the address of a word into
                          which data should be read.
    <i>
     Read
    </i>
    system call locks the inode (corresponding to the file
                          descriptor) at the beginning of the system call and releases the lock at the end of the
                          system call. The functions
    <b>
     Acquire Inode
    </b>
    and
    <b>
     Release Inode
    </b>
    of
    <a href="os_modules/Module_0.html" target="_blank">
     resource manager module
    </a>
    are used to lock and release the inode
                          respectively.
   </p>
   <p>
    <i>
     Read
    </i>
    system call reads the word at the position pointed to by the
                          value of LSEEK (in the
    <a href="os_design-files/mem_ds.html#file_table">
     open file table
    </a>
    entry) and stores it into the memory address provided as input. After reading the word from
                          the file, LSEEK is incremented by one.
   </p>
   <p>
    As file data is stored in the disk blocks allocated to the file, in order to read from
                          position pointed to by LSEEK, the disk block containing the word pointed to by LSEEK has to
                          be loaded first into the memory. eXpOS maintains a
    <b>
     buffer cache
    </b>
    (see
    <a href="os_implementation.html" target="_blank">
     memory organization
    </a>
    )that can store up to four disk blocks in memory
                          simultaneously. The cache pages are numbered 0,1,2 and 3 and are stored in memory pages 71,
                          72, 73 and 74. The simple caching scheme we user here is the following. If we want to bring
                          disk block
    <i>
     N
    </i>
    into memory, the cache page
    <i>
     N mod 4
    </i>
    will be used. Hence, if the
                          disk block number to be loaded is - say 195 - then the cache page number to which the block
                          will be noded is 3 and hence, the block will be loaded to page number 74. The functions
    <b>
     Buffered
                            Read
    </b>
    and
    <b>
     Buffered Write
    </b>
    of the
    <a href="os_modules/Module_3.html" target="_blank">
     file
                            manager module
    </a>
    are designed to handle buffer management.
    <i>
     Read
    </i>
    invokes
    <b>
     Buffered
                            Read
    </b>
    function to bring the required disk block into the memory buffer and read the word
                          present at position LSEEK.
   </p>
   <p>
    <b>
     Reading from the root file does not require a buffer, as root file is already loaded into
                            the memory at boot-time.
    </b>
    Memory copy of the root file is present in memory page 62 and
                          the start address of this page is denoted by the SPL constant
    <a href="support_tools-files/constants.html" target="_blank">
     ROOT_FILE
    </a>
    . The word in the root file at LSEEK position is copied into
                          the address provided. Note that the memory address provided as argument is a logical address,
                          and as system call runs in kernel mode logical address should be translated to physical
                          address before storing data.
   </p>
   <p>
    <i>
     Read
    </i>
    system call needs to lock the resources - Inode (file), buffer and disk before
                          using them. These are locked in the order 1) Inode 2) buffer and 3) disk and released in the
                          reverse order. This order is also followed while writing to a file. Ordering of resource
                          acquisition is imposed in order to avoid processes getting into
    <b>
     circular wait
    </b>
    for
                          resources. Avoiding circular wait prevents
    <a href="https://en.wikipedia.org/wiki/Deadlock" target="_blank">
     deadlocks
    </a>
    .
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Read
    </i>
    system call using detailed algorithm provided
    <a href="os_design-files/read.html" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <li>
    <b>
     Buffered Read (function number = 2,
     <a href="os_modules/Module_3.html" target="_blank">
      file
                              manager module
     </a>
     )
    </b>
   </li>
   <p>
    <b>
     Buffered Read
    </b>
    takes as input 1) a disk block number, 2) an offset value and 3) a
                          physical memory address. The task of Buffered read is to read a word at position specified by
                          the offset within the given disk block and store it into the given
    <b>
     physical
    </b>
    memory
                          address. To read a word from a disk block, it has to be present in the memory.
    <b>
     <a href="Tutorials/filesystem_implementation.html#memory_buffer_cache" target="_blank">
      Memory buffer cache
     </a>
    </b>
    is used for this purpose. The disk block is
                          loaded (if not loaded already) into the buffer page with buffer number given by formula -
    <i>
     (disk
                            block number%4)
    </i>
    .
   </p>
   <p>
    To use a buffer page, it has to be locked first by invoking
    <b>
     Acquire Buffer
    </b>
    function
                          of
    <a href="os_modules/Module_0.html" target="_blank">
     resource manager module
    </a>
    . To load a
                          disk block into a memory buffer page,
    <b>
     Buffered Read
    </b>
    invokes the function
    <b>
     Disk Load
    </b>
    of the
    <a href="os_modules/Module_4.html" target="_blank">
     device manager module
    </a>
    . After
                          loading the given disk block into the corresponding buffer, the word present at the given
                          offset in the memory buffer is copied into the address given as argument.
   </p>
   <p>
    The buffer page to which a disk block has to be loaded may contain some other disk block. In
                          such case, if the buffer page has been modified earlier (
    <b>
     dirty bit
    </b>
    in the buffer table
                          is set), the disk block present in the buffer has to be stored back into the disk before
                          loading a new disk block. To store a disk block back into the disk, Buffered Read invokes
    <b>
     Disk
                            Store
    </b>
    function of
    <a>
     device manager module.
    </a>
   </p>
   <p>
    After completion of the read operation, Buffered Read unlocks the buffer page by invoking
    <b>
     Release
                            Buffer
    </b>
    function of
    <a>
     resource manager module
    </a>
    . Now that the buffer is unlocked,
                          other processes are allowed to use the buffer.
   </p>
   <p style="text-indent: 0px">
    Implement Buffered Read function using the detailed algorithm given
                          in the file manager module link above.
   </p>
   <br/>
   <li>
    <b>
     Acquire Buffer (function number = 1,
     <a href="os_modules/Module_0.html" target="_blank">
      resource
                              manager module
     </a>
     )
    </b>
   </li>
   <p>
    <b>
     Acquire Buffer
    </b>
    takes a buffer number and PID of a process as arguments. This function
                          is invoked by the
    <b>
     Buffered Read
    </b>
    and
    <b>
     Buffered Write
    </b>
    functions of the
    <a href="os_modules/Module_3.html" target="_blank">
     file manager module
    </a>
    to lock a buffer before its use. A process needs to
                          acquire a buffer before accessing it to prevent data inconsistency that may arise if other
                          processes are allowed to access the buffer concurrently.
   </p>
   <p>
    Acquire Buffer locks a buffer by storing the given PID in the LOCKING PID field of the
    <a href="os_design-files/mem_ds.html#buffer_table" target="_blank">
     buffer table
    </a>
    entry
                          corresponding to the given buffer number. If the required buffer is locked by some other
                          process (some other process has set the LOCKING PID), then the process with the given PID is
                          blocked (
    <a href="os_design-files/process_table.html#state" target="_blank">
     STATE
    </a>
    is
                          changed to (WAIT_BUFFER, buffer number) in the
    <a href="os_design-files/process_table.html" target="_blank">
     process table
    </a>
    ). The process waits in the blocked state, until the
                          required buffer is free. When the process which has acquired the buffer releases the buffer
                          by invoking
    <b>
     Release Buffer
    </b>
    function (described next), the state of this blocked
                          process is made READY and
    <b>
     Acquire Buffer
    </b>
    attempts to lock the buffer again.
   </p>
   <p style="text-indent: 0px">
    Implement Acquire Buffer function using the detailed algorithm
                          given in the resource manager module link above.
   </p>
   <br/>
   <li>
    <b>
     Release Buffer (function number = 2,
     <a href="os_modules/Module_0.html" target="_blank">
      resource
                              manager module
     </a>
     )
    </b>
   </li>
   <p>
    A process uses the
    <b>
     Release Buffer
    </b>
    function to release a buffer page that it has
                          acquired earlier.
   </p>
   <p>
    <b>
     Release Buffer
    </b>
    takes as input the number of a buffer page to be released and the PID
                          of a process. Release Buffer function invalidates the LOCKING PID field (store -1) in the
                          buffer table entry corresponding to the given buffer number. Release Buffer also wakes up all
                          processes waiting for the buffer with given buffer number by changing the STATE in the
    <a href="os_design-files/process_table.html" target="_blank">
     process table
    </a>
    from tuple
                          (WAIT_BUFFER, buffer number) to READY.
   </p>
   <p style="text-indent: 0px">
    Implement Release Buffer function using the detailed algorithm
                          given in the resource manager module link above.
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
     Read
    </i>
   </b>
   system
                        call and
   <b>
    Buffered Read
   </b>
   ,
   <b>
    Acquire Buffer
   </b>
   ,
   <b>
    Release Buffer
   </b>
   functions are
                        final.
  </p>
  <br/>
  <b>
   Modifications to boot module
  </b>
  <br/>
  <br/>
  <ul style="list-style-type: disc; margin-left: 10px;">
   <li style="padding-left: 20px">
    Load interrupt routine 5 and module 3 from the disk to the
                          memory. See the memory organization
    <a href="os_implementation.html" target="_blank">
     here
    </a>
    .
   </li>
   <li style="padding-left: 20px">
    Initialize all entries of the
    <a href="os_design-files/mem_ds.html#file_table" target="_blank">
     open file table
    </a>
    by setting INODE INDEX field to -1 and OPEN INSTANCE
                          COUNT field to 0.
   </li>
  </ul>
  <br/>
  <b>
   Making things work
  </b>
  <br/>
  <br/>
  <p>
   Compile and load the newly written/modified files to the disk using XFS-interface.
  </p>
  <br/>
  <b style="color:#26A65B">
   Assignment 1:
  </b>
  Write an ExpL program to take file name as input from
                      the console, read the contents of the file and print to the console. Run this program using
                      shell. Load external data files needed for the program using XFS-interface, as at present eXpOS
                      does not support writing to a file. Check the program with following data files as input - 1)
                      sample.dat from stage 2, 2) "numbers.dat" containing numbers 1 to 2047 separated by new line.
                      (You may write a C program to generate the file "numbers.dat".)
  <br/>
  <br/>
  <b style="color:#26A65B">
   Assignment 2:
  </b>
  Run the program provided
  <a href="test_prog.html#test_program_5" target="_blank">
   here
  </a>
  using shell. Use data files from previous question as input. The
                      program takes name of a data file as input and opens the file first. It then forks to create
                      child process. The content of the file with shared open instance (shared LSEEK) will be printed
                      to the terminal concurrently by parent and child. A semaphore is used to synchronize the use of
                      the open instance between parent and child.
  <br/>
  <br/>
  <a data-toggle="collapse" href="#collapse24">
   <span class="fa fa-times">
   </span>
   Close
  </a>
 </div>
</div>
