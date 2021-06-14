---
title: 'Stage 26 :
                        User Management (12 Hours)'
---
<div class="panel-collapse collapse" id="collapse26">
 <div class="panel-body">
  <!--Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo26">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo26">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Adding support in eXpOS to manage multiple users.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Implementation of multi-user system calls.
        </li>
       </ul>
      </div>
     </li>
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo26a">
       Pre-requisite Reading
      </a>
      <div class="panel-collapse expand" id="lo26a">
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
          <a href="Tutorials/multiuser_implementation.html" target="_blank">
           multi-user management and
                                      implementation
          </a>
         </b>
         documentation.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Description of data structures-
         <a href="os_design-files/disk_ds.html#user_table" target="_blank">
          User
                                      Table
         </a>
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Description of special processes -
         <a href="os_spec-files/misc.html" target="_blank">
          Init
                                      (Login) and Shell process
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
   In this stage, we will enable eXpOS to handle multiple users by implementing
   <a href="os_spec-files/systemcallinterface.html#multiusersystemcalls" target="_blank">
    multi-user system calls
   </a>
   .
   <i>
    Newusr
   </i>
   and
   <i>
    Remusr
   </i>
   system calls are
                        implemented to create new users and delete existing users in the system. The data structure
                        called
   <a href="os_design-files/disk_ds.html#user_table" target="_blank">
    user table
   </a>
   is
                        maintained to store user name and encrypted password of each user in the system. The index of
                        the user table entry for a user is the USERID for the user. Two special users called "kernel"
                        (USERID = 0) and "root" (USERID = 1) are already initialized in the user table at the time of
                        disk formatting (executing fdisk command in XFS-interface). Password of "kernel" is unspecified
                        and "root" user is given default password "root" (The user table will store the encrypted form
                        of the string "root"). System calls
   <i>
    Setpwd
   </i>
   ,
   <i>
    Getuname
   </i>
   and
   <i>
    Getuid
   </i>
   are also
                        implemented in this stage.
  </p>
  <p>
   <i>
    Login
   </i>
   and
   <i>
    Logout
   </i>
   system calls are implemented to enable users to login into the
                        system and logout from the system. From this stage onwards, we will modify the INIT process to
                        work as a special
   <b>
    login process
   </b>
   , running with PID=1 and owned by the kernel (user id is
                        set to 0). Login process enables users to login into the system with their user name and
                        password. After a user logs into the system, the OS (the login system call) will schedule the
                        shell process with PID=2.
   <b>
    The shell will run in the context of the logged in user
   </b>
   (that
                        is, user id of the shell will be set to the user id of the logged in user). Note that the
                        address space for the shell process would be already set up in the memory by the OS boot code.
                        Hence the login process simply sets the shell process to ready state and invoke the scheduler
                        to start its execution. The Shell program will be modified in this stage to support
   <a href="os_spec-files/shell_spec.html" target="_blank">
    built-in shell commands
   </a>
   .
  </p>
  <br/>
  <b style="font-size: 20px">
   Interrupt routine 17
  </b>
  <br/>
  <br/>
  <p>
   The
   <i>
    Login
   </i>
   system call is implemented in the interrupt routine 17.
   <i>
    Login
   </i>
   has
                        system call number 27. From ExpL programs, this system call is called using
   <a href="os_spec-files/dynamicmemoryroutines.html" target="_blank">
    exposcall function
   </a>
   .
  </p>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    <b>
     <i>
      Login
     </i>
     system call
    </b>
   </li>
   <p>
    <i>
     Login
    </i>
    system call takes two arguments 1) a user name (string) and 2) an unencrypted
                          password (string).
    <b>
     <i>
      Login
     </i>
     system call can only be invoked from the
     <a href="os_design-files/misc.html#login" target="_blank">
      login process
     </a>
     (PID = 1).
    </b>
    The init process of eXpOS is called
                          login process. Login process will ask the user to enter user name and password from the
                          console and invokes
    <i>
     Login
    </i>
    system call with provided login credentials.
   </p>
   <p>
    To login a user into the system,
    <i>
     Login
    </i>
    system call checks whether the user with given
                          user name and password is present in the
    <a href="os_design-files/disk_ds.html#user_table" target="_blank">
     user table
    </a>
    or not. Note that the password given as input is unencrypted
                          and should be encrypted (using
    <a href="arch_spec-files/instruction_set.html" target="_blank">
     encrypt statement
    </a>
    )
                          before comparing to ENCRYPTED PASSWORD field in the user table.
    <i>
     Login
    </i>
    system call
                          fails if the user with given user name and password is not found.
   </p>
   <p>
    When a user with given login credentials is found,
    <i>
     Login
    </i>
    system call makes the shell
                          process (PID = 2) ready for execution by changing the STATE field in the
    <a href="os_design-files/process_table.html" target="_blank">
     process table
    </a>
    entry of shell process to CREATED. Although, login
                          process does not explicitly invoke
    <i>
     Fork
    </i>
    and
    <i>
     Exec
    </i>
    system calls to create child,
                          conceptually login process is considered as parent of shell process. So the PPID field in the
                          process table entry of shell process is set to PID of login process (PID = 1). Also, login
                          process must wait for shell process to terminate, so STATE of login process is changed to the
                          tuple (WAIT_PROCESS, PID of shell). Then, Scheduler is invoked in order to schedule shell
                          process for execution.
   </p>
   <p>
    Note that the shell process is already loaded into the address space in boot module so Login
                          system call is not required to load shell process into the memory.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Login
    </i>
    system call using detailed algorithm
                          provided
    <a href="os_design-files/multiusersyscalls.html#login" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <p style="text-indent: 0px">
    <code>
     Note :
    </code>
    The implementation of
    <b>
     <i>
      Login
     </i>
    </b>
    system
                          call is final.
   </p>
  </ol>
  <br/>
  <b style="font-size: 20px">
   Interrupt routine 12
  </b>
  <br/>
  <br/>
  <p>
   The
   <i>
    Logout
   </i>
   system call is implemented in the interrupt routine 12.
   <i>
    Logout
   </i>
   has
                        system call number 28. From ExpL programs, this system call is called using
   <a href="os_spec-files/dynamicmemoryroutines.html" target="_blank">
    exposcall function
   </a>
   .
  </p>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    <b>
     <i>
      Logout
     </i>
     system call
    </b>
   </li>
   <br/>
   <figure style="text-align: center;">
    <img src="img/roadmap/logout.png" style="display:block;margin-left:auto;margin-right:auto"/>
    <br/>
    <figcaption>
     Control flow for
     <i>
      Logout
     </i>
     system call
    </figcaption>
   </figure>
   <br/>
   <br/>
   <p>
    <i>
     Logout
    </i>
    system call is used to logout the current user from the system and does not
                          take any arguments.
    <b>
     <i>
      Logout
     </i>
     system call can only be executed from the shell process
                            (PID = 2).
    </b>
    Before leaving the system, all the non-terminated processes of the user
                          should be terminated. As a consequence of terminating the processes, the resources acquired
                          by these processes will be released.
    <i>
     Logout
    </i>
    system call invokes
    <b>
     Kill All
    </b>
    function of
    <a href="os_modules/Module_1.html" target="_blank">
     process manager module
    </a>
    to
                          terminate the processes. Recall that Kill All function terminates all processes in the system
                          except idle, init (login) and the current process.
   </p>
   <p>
    <i>
     Logout
    </i>
    system call changes the STATE of current process (shell) to TERMINATED.
    <b>
     The
                            starting IP of the shell process is stored at first word of user stack of shell, so that
                            the next time when a new user is logged in and shell process is scheduled for the first
                            time in the context of the new user, shell will run as newly created process.
    </b>
    Login
                          process (PID = 1) is made ready for execution and scheduler is invoked to schedule login
                          process.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Logout
    </i>
    system call using detailed algorithm
                          provided
    <a href="os_design-files/multiusersyscalls.html#logout" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <p style="text-indent: 0px">
    <code>
     Note :
    </code>
    The implementation of
    <b>
     <i>
      Logout
     </i>
    </b>
    system call is final.
   </p>
  </ol>
  <br/>
  <b style="font-size: 20px">
   Interrupt routine 16
  </b>
  <br/>
  <br/>
  <p>
   The system calls
   <i>
    Newusr
   </i>
   ,
   <i>
    Remusr
   </i>
   ,
   <i>
    Setpwd
   </i>
   ,
   <i>
    Getuname
   </i>
   and
   <i>
    Getuid
   </i>
   are implemented in the interrupt routine 16.
   <i>
    Newusr
   </i>
   ,
   <i>
    Remusr
   </i>
   ,
   <i>
    Setpwd
   </i>
   ,
   <i>
    Getuname
   </i>
   and
   <i>
    Getuid
   </i>
   have system call numbers 22, 23, 24, 25, 26 respectively. From ExpL programs,
                        these system calls are called using
   <a href="os_spec-files/dynamicmemoryroutines.html" target="_blank">
    exposcall
                          function
   </a>
   .
  </p>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    <b>
     <i>
      Newusr
     </i>
     system call
    </b>
   </li>
   <p>
    A user name and an unencrypted text password are arguments to the
    <i>
     Newusr
    </i>
    system call.
    <b>
     <i>
      Newusr
     </i>
     system call can only be invoked from the
     <a>
      shell process
     </a>
     of the root
                            user.
    </b>
   </p>
   <p>
    <i>
     Newusr
    </i>
    finds a free entry for the new user in the
    <a href="os_design-files/disk_ds.html#user_table" target="_blank">
     user table
    </a>
    and initialize this entry with the provided user name and
                          password. The password is encrypted (using
    <a href="support_tools-files/spl.html" target="_blank">
     encrypt
                            statement
    </a>
    ) before storing it into the user table.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Newusr
    </i>
    system call using detailed algorithm
                          provided
    <a href="os_design-files/multiusersyscalls.html#newusr" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <li>
    <b>
     <i>
      Remusr
     </i>
     system call
    </b>
   </li>
   <p>
    <b>
     <i>
      Remusr
     </i>
    </b>
    system call takes the user name of the user to be removed as an
                          argument.
    <b>
     <i>
      Remusr
     </i>
     system call can only be invoked from the
     <a>
      shell process
     </a>
     of
                            the root user. A user can not be removed from the system if the user is the owner of one or
                            more files in the system.
    </b>
    To remove a user from the system,
    <i>
     Remusr
    </i>
    system call
                          invalidates the entry in the
    <a href="os_design-files/disk_ds.html#user_table" target="_blank">
     user
                            table
    </a>
    corresponding to given username by storing -1 in the USERNAME and ENCRYPTED
                          PASSWORD fields. Note that the special users "root" and "kernel" can not be removed using
    <i>
     Remusr
    </i>
    system call.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Remusr
    </i>
    system call using detailed algorithm
                          provided
    <a href="os_design-files/multiusersyscalls.html#remusr" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <li>
    <b>
     <i>
      Setpwd
     </i>
     system call
    </b>
   </li>
   <p>
    <b>
     <i>
      Setpwd
     </i>
    </b>
    changes the password of a user to newly provided password. It takes as
                          arguments a user name and a new password from application program.
    <i>
     Setpwd
    </i>
    can only be
                          executed by shell process. A user is permitted to change only its own password. The
                          privileged user "root" has permission to change the password of any user. The "root" user is
                          provided the default password "root". The password of root user can be changed later using
    <i>
     Setpwd
    </i>
    .
    <i>
     Setpwd
    </i>
    encrypts the provided password and replaces the ENCRYPTED PASSWORD field in the
    <a href="os_design-files/disk_ds.html#user_table" target="_blank">
     user table
    </a>
    entry
                          corresponding to provided user name.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Setpwd
    </i>
    system call using detailed algorithm
                          provided
    <a href="os_design-files/multiusersyscalls.html#setpwd" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <li>
    <b>
     <i>
      Getuname
     </i>
     and
     <i>
      Getuid
     </i>
     system calls
    </b>
   </li>
   <p>
    <b>
     <i>
      Getuname
     </i>
    </b>
    takes as argument a USERID from user program.
    <i>
     Getuname
    </i>
    returns
                          the user name of the given USERID from the
    <a href="os_design-files/disk_ds.html#user_table" target="_blank">
     user table
    </a>
    .
    <b>
     <i>
      Getuid
     </i>
    </b>
    takes a user name (string) as an
                          argument from the user program.
    <i>
     Getuid
    </i>
    returns the USERID of the given user name. The
                          system calls
    <i>
     Getuname
    </i>
    and
    <i>
     Getuid
    </i>
    can be executed from any process of any user.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Getuid
    </i>
    and
    <i>
     Getuname
    </i>
    system calls using
                          detailed algorithms provided
    <a href="os_design-files/multiusersyscalls.html#getuid" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <p style="text-indent: 0px">
    <code>
     Note :
    </code>
    The implementation of
    <b>
     <i>
      Newusr
     </i>
    </b>
    ,
    <b>
     <i>
      Remusr
     </i>
    </b>
    ,
    <b>
     <i>
      Setpwd
     </i>
    </b>
    ,
    <b>
     <i>
      Getuname
     </i>
    </b>
    and
    <b>
     <i>
      Getuid
     </i>
    </b>
    system calls are final.
   </p>
  </ol>
  <br/>
  <b>
   Modification to
   <i>
    Shutdown
   </i>
   system call
  </b>
  <br/>
  <br/>
  <p>
   There is a slight modification in
   <i>
    Shutdown
   </i>
   system call.
   <i>
    Shutdown
   </i>
   system call can
                        only be invoked from shell process. Until this stage, shell process was loaded as init program
                        with PID = 1, but now login process is loaded as init and shell is loaded with PID = 2. So in
   <i>
    Shutdown
   </i>
   system call, modify the condition to check whether current process is shell or
                        not, by comparing current PID to 2 (instead of the previous value 1).
  </p>
  <p style="text-indent: 0px">
   <code>
    Note :
   </code>
   The implementation of
   <b>
    <i>
     Shutdown
    </i>
   </b>
   system call is final.
  </p>
  <br/>
  <b>
   Modifications to boot module and OS startup code
  </b>
  <br/>
  <br/>
  <p>
   The boot module is modified to initialize the Shell process. Shell process has PID equal to 2.
                        The process table entry and page table with index as 2 is initialized in the boot module for
                        shell process. Heap, user stack and kernel stack pages are also allocated for the shell.
  </p>
  <p>
   The boot module will set the shell process to TERMINATED state so that it will not be
                        scheduled. The state of the shell process will be set to CREATED by the login system
                        call when a valid user is logged in. This ensures that the shell process is scheduled
                        only after a valid user is logged in.
  </p>
  <br/>
  <code>
   Implementation Note:
  </code>
  <br/>
  <br/>
  <p>
   Since Idle, Shell and Login processes are system processes that does pre-defined
                        functionality, it is easy to design ExpL programs for them so that 1) they require no heap
                        pages 2) Idle and login (init) processes require only one user stack page each 3) Idle and
                        login code will fit into just one code page each (shell will be
                        hard to implement without two pages of code). Hence, we will modify the boot code so as to
                        allocate only one stack page apart from the user area page and code pages for Idle and Login
                        processes. Shell process will be allocated two stack pages.
  </p>
  <p>
   Note that the
   <a href="os_implementation.html" target="_blank">
    memory organization
   </a>
   allocates two pages each for Idle and Login. Since the code for Idle and Login can fit into
                        just one page, the second page can be allocated for their user stack. Kernel stack pages will
                        have to be allocated in the free memory area. This leads to better memory utilization so that
                        more concurrent processes may be run with the available memory. The page table entries for
                        unallocated heap pages, stack page and code pages must be set to invalid.
  </p>
  <ul style="list-style-type: disc; margin-left: 10px;">
   <br/>
   <p style="text-indent: 0px">
    <b>
     Steps to be done in the OS startup code to reflect the above
                            changes are described below:
    </b>
   </p>
   <li style="padding-left: 20px">
    Changes for idle process allocation
   </li>
   <ol style="padding-left: 60px">
    <li style="padding-left: 20px">
     Load only the first code page from disk to memory (instead of
                            two code pages). See
     <a href="os_implementation.html" target="_blank">
      disk/memory
                              organization
     </a>
     .
    </li>
    <li style="padding-left: 20px">
     Allocate second code page (70) as user stack page for idle
                            (only one page for user stack is needed). Allocate memory page 76 for kernel stack of idle.
    </li>
    <li style="padding-left: 20px">
     Change the page table entries for stack and code pages
                            according to above allocation. Also change the user area page number in the
     <a href="os_design-files/process_table.html" target="_blank">
      process table
     </a>
     entry of idle.
    </li>
    <li style="padding-left: 20px">
     Store the starting IP address from the header of the first
                            code page on the top of new user stack as the user stack page number is changed now for
                            idle.
    </li>
   </ol>
  </ul>
  <ul style="list-style-type: disc; margin-left: 10px;">
   <br/>
   <p style="text-indent: 0px">
    <b>
     Steps to be done in the boot module to reflect the above changes
                            are described below:
    </b>
   </p>
   <li style="padding-left: 20px">
    Load shell process, int 16, int 12 (Logout), int 17 from
                          disk to memory. See disk and memory organization
    <a href="os_implementation.html" target="_blank">
     here
    </a>
    .
   </li>
   <li style="padding-left: 20px">
    Changes for init process allocation
   </li>
   <ol style="padding-left: 60px">
    <li style="padding-left: 20px">
     Load only the first code page from disk to memory (instead of
                            two code pages). See
     <a href="os_implementation.html" target="_blank">
      disk/memory
                              organization
     </a>
     .
    </li>
    <li style="padding-left: 20px">
     Allocate second code page (66) as user stack page for init
                            (only one page for user stack is needed). Allocate memory page 77 for kernel stack of init.
    </li>
    <li style="padding-left: 20px">
     Invalidate the heap page entries in the page table of the
                            INIT process. Change the page table entries for stack and code pages according to above
                            allocation. Also change the user area page number in the
     <a href="os_design-files/process_table.html" target="_blank">
      process table
     </a>
     entry of init.
    </li>
    <li style="padding-left: 20px">
     Store the starting IP address from the header of the first
                            code page on the top of new user stack as the user stack page number is changed now for
                            init.
    </li>
    <li style="padding-left: 20px">
     Remove
     <a>
      disk map table
     </a>
     initialization for the init
                            process as it is not needed any longer.
    </li>
   </ol>
   <li style="padding-left: 20px">
    Shell process allocation
   </li>
   <ol style="padding-left: 60px">
    <li style="padding-left: 20px">
     Load two code pages from disk to memory. See
     <a href="os_implementation.html" target="_blank">
      disk/memory organization
     </a>
     .
    </li>
    <li style="padding-left: 20px">
     Allocate memory pages 78 and 79 for user stack of shell. Also
                            allocate memory page 80 for kernel stack of shell.
    </li>
    <li style="padding-left: 20px">
     Set the library page entries to 63 and 64 in the page table of
                            shell. Invalidate the heap page entries in the page table. Initialize the page table
                            entries for stack and code pages according to above allocation. Also change the user area
                            page number in the
     <a href="os_design-files/process_table.html" target="_blank">
      process
                              table
     </a>
     entry of shell.
    </li>
    <li style="padding-left: 20px">
     Initialize the
     <a href="os_design-files/process_table.html" target="_blank">
      process table
     </a>
     entry of the shell process (PID = 2) as follows- Set
                            the STATE field to TERMINATED. Store PID and PPID fields to 2 and 1 respectively. Store the
                            kernel stack page number allocated above in the USER AREA PAGE NUMBER field. Set the KERNEL
                            STACK POINTER field to 0 and USER STACK POINTER to 8*512. Also initialize PTBR and PTLR
                            fields for the shell process.
    </li>
    <li style="padding-left: 20px">
     Initialize the
     <a href="os_design-files/process_table.html#disk_map_table" target="_blank">
      disk map table
     </a>
     entry of the shell process (PID = 2) as follows -
                            Store the block numbers of the two code pages in the disk map table entry of the shell.
                            Invalidate all other entries of the disk map table entry by storing -1.
    </li>
    <li style="padding-left: 20px">
     Store the starting IP address from the header of the first
                            code page on the top of user stack for the shell process.
    </li>
   </ol>
   <p style="padding-left: 60px; text-indent: 0px">
    Note that shell process is set up for execution
                          but STATE of the shell process is set to TERMINATED in the boot module. The shell process
                          will be made READY only upon successful login of the user.
   </p>
   <li style="padding-left: 20px;">
    Change the initialization of
    <a href="os_design-files/mem_ds.html#mem_free_list" target="_blank">
     memory free list
    </a>
    according to the memory pages allocated for idle, init
                          and shell processes.
   </li>
   <li style="padding-left: 20px">
    Update the MEM_FREE_COUNT in the
    <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
     system status table
    </a>
    to 47 as now 47 memory pages are available.
   </li>
  </ul>
  <br/>
  <b>
   Login program
  </b>
  <br/>
  <br/>
  <p>
   Login program is run as the Init process from this stage onwards. This program asks user for a
                        user name and a password to log into the system. Login process uses
   <i>
    Login
   </i>
   system call to
                        log in the user into the system. This is repeated in a loop. Write login program using the
                        pseudocode provided
   <a href="os_design-files/misc.html#login" target="_blank">
    here
   </a>
   and load
                        the XSM excutable as init program using
   <a href="support_tools-files/xfs-interface.html" target="_blank">
    XFS-interface
   </a>
   .
  </p>
  <br/>
  <b>
   Extended Shell program
  </b>
  <br/>
  <br/>
  <p>
   Shell program is improvised to support the built-in shell commands and XSM executable
                        commands/files according to the specification provided in
   <a href="os_spec-files/shell_spec.html" target="_blank">
    eXpOS shell specification
   </a>
   . An implementation of the ExpL shell program is
                        given
   <a href="test_prog.html#test_program_7" target="_blank">
    here
   </a>
   . Compile and load this
                        program as shell into the disk using
   <a href="support_tools-files/xfs-interface.html" target="_blank">
    XFS-interface
   </a>
   .
                        This program will be run as shell when a user logs into the system.
  </p>
  <p>
   Now that multiple user related system calls are supported in eXpOS, the shell commands - "lu"
                        and "ru" can be implemented. Implement commands lu, ru as executable files according to the
                        specification of
   <a href="os_spec-files/shell_spec.html#executable_commands" target="_blank">
    executable
                          commands/files
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
   Compile and load the newly written/modified files to the disk using XFS-interface.
  </p>
  <br/>
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq23">
       <b>
        Q1.
       </b>
       Why
       <i>
        Newusr
       </i>
       ,
       <i>
        Remusr
       </i>
       and
       <i>
        Setpwd
       </i>
       system calls are permitted to execute only from shell program whereas
       <i>
        Getuid
       </i>
       and
       <i>
        Getuname
       </i>
       can be executed from any application program?
      </a>
      <div class="panel-collapse collapse" id="collapseq23">
       The system calls
       <i>
        Newusr
       </i>
       ,
       <i>
        Remusr
       </i>
       and
       <i>
        Setpwd
       </i>
       modify the data related
                                to users in the user table.
       <i>
        Getuid
       </i>
       and
       <i>
        Getuname
       </i>
       system calls only access
                                data related to users. As application programs other than Shell are not allowed to
                                modify the user related data, system calls
       <i>
        Newusr
       </i>
       ,
       <i>
        Remusr
       </i>
       ,
       <i>
        Setpwd
       </i>
       are only executed from shell process.
      </div>
     </li>
    </ul>
   </div>
  </div>
  <br/>
  <b style="color:#26A65B">
   Assignment 1:
  </b>
  Test the system calls, login and shell process by
                      performing following sequence of actions -
  <br/>
  1) Login into the system as root user and change
                      the password of root user using Setpwd command
  <br/>
  2) Create new user using Newusr command
  <br/>
  3) Log out from system
  <br/>
  4) Login as newly created user
  <br/>
  5) Create new files and perform
                      file operations on them
  <br/>
  5) List all users using "lu.xsm" executable file
  <br/>
  6) Logout and
                      again login as root user
  <br/>
  7) Remove files owned by the new user using excutable file command
                      "ru.xsm" from the shell of root.
  <br/>
  You can further test the system by running all build-in shell commands and excutable files
                      commands to make sure that implementation is correct.
  <br/>
  <br/>
 
 </div>
</div>
