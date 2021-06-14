---
title: 'Stage 23 :
                        File Creation and Deletion (6 Hours)'
---
<div class="panel-collapse collapse" id="collapse23">
 <div class="panel-body">
  <!--Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo23">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo23">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Familiarize with eXpOS file system and implemtation.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Add support for file creation and deletion to the OS by implementing
         <i>
          Create
         </i>
         and
         <i>
          Delete
         </i>
         system calls
        </li>
       </ul>
      </div>
     </li>
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo23a">
       Pre-requisite Reading
      </a>
      <div class="panel-collapse expand" id="lo23a">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         It is
         <b>
          absolutely necessary
         </b>
         to read and understand
         <b>
          <a href="Tutorials/filesystem_implementation.html" target="_blank">
           eXpOS FILE SYSTEM and
                                      Implementation Tutorial
          </a>
         </b>
         documentation.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Description of data structures-
         <a href="os_design-files/disk_ds.html#inode_table" target="_blank">
          Inode
                                      Table
         </a>
         ,
         <a href="os_design-files/disk_ds.html#root_file" target="_blank">
          Root file
         </a>
         ,
         <a href="os_design-files/mem_ds.html#file_lock_status_table" target="_blank">
          File(inode) status
                                      table
         </a>
         and
         <a href="os_design-files/mem_ds.html#buffer_table" target="_blank">
          buffer table
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
   In this stage, we will discuss how files are created and deleted by the application program
                        with the help of file system calls
   <i>
    Create
   </i>
   and
   <i>
    Delete
   </i>
   .
   <i>
    Shutdown
   </i>
   system call
                        will be modified in this stage.
  </p>
  <p>
   <i>
    Create
   </i>
   system call creates an empty file with the name given as input.
   <i>
    Create
   </i>
   system call initializes the disk data structures with meta data related to the file.
   <a href="os_design-files/disk_ds.html#inode_table" target="_blank">
    Inode table
   </a>
   and
   <a href="os_design-files/disk_ds.html#root_file" target="_blank">
    root
                          file
   </a>
   are the disk data structures used to maintain permanent record of files.
   <i>
    Delete
   </i>
   system call deletes the record of the file with the given name from inode table and root file.
   <i>
    Delete
   </i>
   also releases the disk blocks occupied by the file to be deleted. The
   <i>
    Shutdown
   </i>
   system call is modified to commit the changes made by
   <i>
    Create
   </i>
   and
   <i>
    Delete
   </i>
   system
                        calls in the memory copy of the disk data structures back into the disk.
  </p>
  <p>
   Inode table and root file stores details of every eXpOS file stored in the disk. eXpOS allows
                        at most
   <a href="support_tools-files/constants.html" target="_blank">
    MAX_FILE_NUM
   </a>
   (60)
                        files to be stored in the disk. Hence, both inode table and root file has MAX_FILE_NUM entries.
                        The entry for a file in the inode table is identified by an index of its record in the inode
                        table. For each file, the inode table entry and root file entry should have the same index. The
                        disk data structures have to be loaded from the disk to the memory in order to use them while
                        OS is running. The OS maintains the memory copy of the inode table in memory pages 59 and 60.
                        Also the memory copy of root file is present in memory page 62. See
   <a href="os_implementation.html" target="_blank">
    memory organization
   </a>
   for more details.
  </p>
  <br/>
  <b style="font-size: 20px">
   Interrupt routine 4
  </b>
  <br/>
  <br/>
  <figure style="text-align: center;">
   <img src="img/roadmap/create_delete.png" style="display:block;margin-left:auto;margin-right:auto"/>
   <br/>
   <figcaption>
    Control flow for
    <i>
     Create
    </i>
    and
    <i>
     Delete
    </i>
    system calls
   </figcaption>
  </figure>
  <br/>
  <p>
   The system calls
   <i>
    Create
   </i>
   and
   <i>
    Delete
   </i>
   are implemented in the interrupt routine 4.
   <i>
    Create
   </i>
   and
   <i>
    Delete
   </i>
   have system call numbers 1 and 4 respectively. From ExpL
                        programs, these system calls are called using
   <a href="os_spec-files/dynamicmemoryroutines.html" target="_blank">
    exposcall function
   </a>
   .
  </p>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    <b>
     Create system call
    </b>
   </li>
   <p>
    <i>
     Create
    </i>
    system call takes filename and permission (integer 0 or 1) as arguments from
                          the user program. As
    <i>
     Create
    </i>
    allows to create only data file, it is recommended to use
    <i>
     .dat
    </i>
    as extension for file names.
    <i>
     Create
    </i>
    finds a free entry (indicated by -1 in
                          the FILE NAME field) in the inode table to store details related to the new file. The fields
                          in the free inode table entry and corresponding root file entry are initialized with the
                          meta-data of the new file.
   </p>
   <p>
    The USERID field in the inode table is initialized to the USERID field from the process
                          table of the current process. Hence, the user executing the
    <i>
     Create
    </i>
    system call becomes
                          the
    <b>
     owner
    </b>
    of the file. The USERNAME field in the root file entry is initialized to the
                          username corresponding to the USERID. The username can be obtained from memory copy of the
    <a href="os_design-files/disk_ds.html#user_table" target="_blank">
     user table
    </a>
    with index as
                          USERID. User table in the disk is initialized by the XFS-interface (during disk formatting)
                          to create two users - kernel and root.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Create
    </i>
    system call using the detailed algorithm
                          provided
    <a href="os_design-files/create.html">
     here
    </a>
    .
   </p>
   <br/>
   <li>
    <b>
     Delete system call
    </b>
   </li>
   <p>
    <i>
     Delete
    </i>
    system call takes file name as an argument from the user program. A file can
                          not be deleted if it is currently opened by one or more processes.
    <i>
     Delete
    </i>
    first
                          acquires the lock on the file by invoking
    <b>
     Acquire Inode
    </b>
    function from
    <a href="os_modules/Module_0.html" target="_blank">
     resource manager module
    </a>
    .
    <i>
     Delete
    </i>
    then invalidates the record of
                          the file in entries of the inode table and root file. Also, the blocks allocated to the file
                          are released. Finally,
    <i>
     Delete
    </i>
    releases the lock on file by invoking
    <b>
     Release Inode
    </b>
    function of the resource manager module.
   </p>
   <p>
    There is one subtility involved in deleting a file. If any of the disk blocks of the deleted
                          file are in the buffer cache, and if the buffer page is marked dirty, the OS will write back
                          the buffer page into the disk block when another disk block needs to be brought into the same
                          buffer page.
                          However, such write back is unnecessary if the file is deleted (and can even be catastrophic-
                          why?). Hence, Delete system call must clear the dirty
                          bit (in the buffer table) of all the buffered disk blocks of the file.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Delete
    </i>
    system call using the detailed algorithm
                          provided
    <a href="os_design-files/delete.html">
     here
    </a>
    .
   </p>
   <br/>
   <li>
    <b>
     Acquire Inode (function number = 4,
     <a href="os_modules/Module_0.html" target="_blank">
      resource
                              manager module
     </a>
     )
    </b>
   </li>
   <p>
    Acquire Inode takes an inode index and PID of a process as arguments. To lock the inode
                          (file),
    <b>
     Acquire Inode
    </b>
    first waits in a busy loop by changing state to (WAIT_FILE,
                          inode index) until the file becomes free. After the inode becomes free and current process
                          resumes execution, acquire inode checks whether the file is deleted from the system. (This
                          check is necessary because, some other process may delete the file while the current process
                          was waiting for the inode to be free.)
    <b>
     Acquire Inode
    </b>
    then locks the inode by setting
                          LOCKING PID field in the
    <a href="os_design-files/mem_ds.html#file_lock_status_table" target="_blank">
     file
                            status table
    </a>
    to the given PID.
   </p>
   <p style="text-indent: 0px">
    Implement Acquire Inode function using the detailed algorithm given
                          in the resource manager module link above.
   </p>
   <br/>
   <li>
    <b>
     Release Inode (function number = 5,
     <a href="os_modules/Module_0.html" target="_blank">
      resource
                              manager module
     </a>
     )
    </b>
   </li>
   <p>
    Release Inode takes an inode index and PID of a process as arguments. Release Inode frees
                          the inode (file) by invalidating the LOCKING PID field in the
    <a href="os_design-files/mem_ds.html#file_lock_status_table" target="_blank">
     file status table
    </a>
    . The function then wakes up the processes waiting for
                          the file with given inode index by changing state of those processes to READY.
   </p>
   <p style="text-indent: 0px">
    Implement Release Inode function using the detailed algorithm
                          given in the resource manager module link above.
   </p>
   <!--
<li><b>Release Block (function number = 4, <a href="os_modules/Module_2.html" target="_blank">Memory manager module</a> )</b></li>
<p>There is one subtility involved in deleting a file. If any of the disk blocks of the deleted file is in the buffer cache, and if the buffer page is marked dirty, the OS will write back the buffer page into the disk block when another disk block needs to be brought into the same buffer page.
However, such write back is unnecessary if the file is deleted (and can even be catastrophic- why?). Hence, Delete system call must clear the dirty
bit (in the buffer table) of all the buffered disk blocks of the file.

 </p>-->
  </ol>
  <p style="text-indent: 0px">
   <code>
    Note :
   </code>
   The implementation of
   <b>
    <i>
     Create
    </i>
   </b>
   ,
   <b>
    <i>
     Delete
    </i>
   </b>
   ,
   <b>
    Acquire Inode
   </b>
   and
   <b>
    Release Inode
   </b>
   are final.
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
   <i>
    Create
   </i>
   and
   <i>
    Delete
   </i>
   system calls update the memory copies
                        of Inode table, disk free list and root file. The changed data
                        structures are not committed into the disk by these system calls.
                        The disk update for these data structures are done during system
                        shutdown.
  </p>
  <br/>
  <figure style="text-align: center;">
   <img src="img/roadmap/Initial_shutdown.png" style="display:block;margin-left:auto;margin-right:auto"/>
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
  <p>
   Interrupt routine 15 written in stage 21 contains just HALT instruction. In this stage,
   <i>
    Shutdown
   </i>
   system call is implemented in the interrupt routine 15.
   <i>
    Shutdown
   </i>
   system call has system
                        call number 21 and it does not have any arguments.
  </p>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    <b>
     Shutdown system call
    </b>
   </li>
   <ul style="list-style-type: disc; margin-left: 10px; ">
    <li style="padding-left: 20px">
     Switch to the kernel stack and set the MODE FLAG in the
     <a href="os_design-files/process_table.html" target="_blank">
      process table
     </a>
     to the system
                            call number.
    </li>
    <li style="padding-left: 20px">
     <i>
      Shutdown
     </i>
     system call can be invoked only from the shell
                            process of the root user. If the current process is not shell (PID in the
     <a href="os_design-files/process_table.html" target="_blank">
      process table
     </a>
     is not equal to 1) or the current user is not root user
                            (USERID in the process table is not equal to 1) then store -1 as return value, reset the
                            MODE FLAG, change the stack to user stack and return to user mode.
    </li>
    <li style="padding-left: 20px">
     Commit the changes made in the memory copies of the
     <b>
      inode
                              table
     </b>
     (along with user table), the
     <b>
      root file
     </b>
     and the
     <b>
      disk free list
     </b>
     by
                            storing them back to the disk invoking the
     <b>
      Disk Store
     </b>
     function of
     <a href="os_modules/Module_4.html" target="_blank">
      device manager module
     </a>
     . Refer to
     <a href="os_implementation.html" target="_blank">
      disk/memory organization
     </a>
     for block and page numbers of these data
                            structures. Finally, halt the system using the
     <a href="./support_tools-files/spl.html" target="_blank">
      SPL statement
     </a>
     halt.
    </li>
   </ul>
   <p style="text-indent: 0px">
    <code>
     Note :
    </code>
    The implementation of the
    <i>
     Shutdown
    </i>
    system
                          call is not final. Implementation will change in later stages.
   </p>
   <br/>
   <li>
    <b>
     Disk Store (function number = 1,
     <a href="os_modules/Module_4.html" target="_blank">
      Device
                              manager module
     </a>
     )
    </b>
   </li>
   <p>
    Disk Store function takes PID of a process, a page number and a block number as arguments.
                          To store data into the disk, Disk Store first needs to lock the disk by invoking the
    <b>
     Acquire
                            Disk
    </b>
    function of the
    <a href="os_modules/Module_0.html" target="_blank">
     resource
                            manager module
    </a>
    . After locking the disk, Disk Store updates the
    <a href="os_design-files/mem_ds.html#ds_table" target="_blank">
     disk status table
    </a>
    . Finally, Disk Store initiates the store operation
                          for given page number and block number and waits in WAIT_DISK state until the store operation
                          is complete. When store operation is completed, system raises the disk interrupt which makes
                          this process READY again.
   </p>
   <p style="text-indent:  0px">
    Implement
    <b>
     Disk Store
    </b>
    function using the detailed algorithm
                          given in the device manager module link above.
   </p>
   <p style="text-indent: 0px">
    <code>
     Note :
    </code>
    The implementation of
    <b>
     Disk Store
    </b>
    function
                          is final.
   </p>
   <br/>
  </ol>
  <b>
   Modifications to boot module
  </b>
  <br/>
  <br/>
  <ul style="list-style-type: disc; margin-left: 10px;">
   <li style="padding-left: 20px">
    Load interrupt routine 4 and root file from the disk to the
                          memory. See the memory organization
    <a href="os_implementation.html" target="_blank">
     here
    </a>
    .
   </li>
   <li style="padding-left: 20px">
    Initialize the
    <a href="os_design-files/mem_ds.html#file_lock_status_table" target="_blank">
     file status table
    </a>
    by setting LOCKING PID and FILE OPEN COUNT fields of
                          all entries to -1.
   </li>
   <li style="padding-left: 20px">
    Initialize the
    <a href="os_design-files/mem_ds.html#buffer_table" target="_blank">
     buffer table
    </a>
    by setting BLOCK NUMBER and LOCKING PID fields to -1 and
                          DIRTY BIT to 0 in all entries.
   </li>
   <li style="padding-left: 20px">
    At present to simplify the implementation, we consider a single
                          user system with only one user called root, USERID of root is 1. Hence, set the USERID field
                          in the process table of INIT to 1. Later when INIT is forked, the USERID field is copied to
                          the process table of the child process.
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
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq22">
       <b>
        Q1.
       </b>
       What is the need for
       <i>
        Delete
       </i>
       system call to lock the file before deleting it?
      </a>
      <div class="panel-collapse collapse" id="collapseq22">
       Locking the file in
       <i>
        Delete
       </i>
       system call makes sure that some other process will
                                not be able to open the file or perform any other operation on the file during the
                                deletion of the file.
      </div>
     </li>
    </ul>
   </div>
  </div>
  <br/>
  <b style="color:#26A65B">
   Assignment 1:
  </b>
  Write an ExpL program to take file name(string) and
                      permission(integer) as input from the console and create a file with the provided input. (It is
                      recommended to have .dat as extension for data files.) Run this program using shell. Using
                      XFS-interface check if the entry for the file is created in inode table and root file.
  <br/>
  <br/>
  <b style="color:#26A65B">
   Assignment 2:
  </b>
  Write an ExpL program to take file name(string) as
                      input from the console and delete a file with provided input. Run the program using shell. Using
                      XFS-interface check if the entry for the file is deleted from inode table and root file. Check
                      the program for different files- like files created using
  <i>
   Create
  </i>
  system call, files not
                      present in disk and files loaded using XFS-interface having some data (eg- sample.dat used in
                      stage 2).
  <br/>
  <br/>
  <a data-toggle="collapse" href="#collapse23">
   <span class="fa fa-times">
   </span>
   Close
  </a>
 </div>
</div>
