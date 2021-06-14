---
title: 'Stage 13 :
                        Boot Module (4 Hours)'
---
<div class="panel-collapse collapse" id="collapse13">
 <div class="panel-body">
  <!-- Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo13">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo13">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Introduction to XSM Module Programming.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Implementation of Boot Module.
        </li>
       </ul>
      </div>
     </li>
    </ul>
    <p>
     Modules in eXpOS are used to perform certain logical tasks, which are performed
                            frequently. eXpOS modules serve various purposes like scheduling new process, acquiring and
                            releasing resources etc. These modules run in kernel mode and are invoked only from the
                            kernel mode. A user program can never invoke a module directly. Modules can be invoked from
                            interrupt routines, other modules or the OS startup code.
    </p>
    <p>
     As modules execute in kernel mode, the kernel stack of the currently scheduled process is
                            used as the caller-stack for module invocation. XSM supports eight modules - MOD_0 to MOD_7
                            - which can be invoked using the CALL MOD_n / CALL &lt;MODULE_NAME&gt; instruction (see
     <a href="support_tools-files/constants.html#interrupts" target="_blank">
      SPL constants
     </a>
     ). While switching to module, the
                            CALL instruction pushes the IP address of the instruction following the CALL instruction on
                            the top of the kernel stack and starts execution of the corresponding module. A module
                            returns to the caller using the RET instruction (return statement in SPL) which restores
                            the IP value present on the top of the kernel stack, pushed earlier by the CALL
                            instruction. Note that we use the return statement, instead of the ireturn statement, to
                            return to the caller. The IRET instruction (ireturn statement) changes mode from kernel to
                            user as it assumes that SP contains a logical address. The RET instruction (return
                            statement) on the other hand just returns to the caller in kernel mode, using the IP value
                            pointed by SP. Read about kernel stack management during kernel module calls
     <a href="os_design-files/stack_module.html" target="_blank">
      here
     </a>
     .
    </p>
    <p>
     A module in eXpOS may implement several functions, each for a particular task ( eg-
     <a href="os_modules/Module_0.html" target="_blank">
      resource manager module
     </a>
     -module 0).
                            Some modules may perform a single task (eg- scheduler, boot module). For a module with
                            several functions, each function is given a function number to distinguish them within the
                            module. This function number should be passed as argument in the register R1 along with
                            other arguments in R2, R3 etc. Register R0 is reserved for return value. See
     <a href="support_tools-files/spl.html" target="_blank">
      SPL module calling conventions
     </a>
     for details.
                            For details about the OS functions implemented in various eXpOS modules, see
     <a href="os_modules/Module_Design.html" target="_blank">
      here
     </a>
     .
    </p>
    <p>
     According to the
     <a href="os_implementation" target="_blank">
      memory organization
     </a>
     of
                            eXpOS, the OS startup code is provided with only one memory page (page numer 1). However,
                            the code for OS startup may exceed one page due to initialization of several OS data
                            structures. So we design a module for the purpose of OS initialization. This module will be
                            called the
     <b>
      Boot module
     </b>
     (module 7). The Boot module is invoked from the OS startup
                            code. The OS startup code hand-creates the idle process, initializes the SP register to the
                            kernel stack of the idle process, loads module 7 in memory and then invokes the boot module
                            (using the stack of the IDLE process). Upon return from the boot module, the OS startup
                            code initiates user mode execution of the idle process. Note that in the previous stage, we
                            had scheduled the INIT process first, before executing the IDLE pocess. Starting from the
                            present stage, the idle process will be scheduled first. All further scheduling of
                            processes will be controlled by the timer interrupt routine and a scheduler module, which
                            will be discussed in the next stage. The Boot module is responsible for initialization of
                            all eXpOS data structures, user processes and also loading of all interrupt routines and
                            modules. You will not modify the OS startup code written in this stage in subsequent
                            stages. However, you will add more code to the boot module as you go through various stages
                            of the roadmap.
    </p>
    <!-- <p>OS startup code loads module 7 and idle process. It intializes page table and process table entry for idle process. It sets SP to kernel stack pointer of idle process and invokes boot module (module 7).</p>-->
    <p>
     The idle process is run first to ensure that this process is scheduled at least once, so
                            that its context gets initialized. This useful because in later stages, certain kernel
                            operations (like disk swap) are performed from the context of the IDLE process. For now, we
                            skip over this matter.
    </p>
    <b>
     Modifications to OS startup code
    </b>
    <br/>
    <br/>
    <ol style="list-style-type: decimal;margin-left: 2px">
     <li>
      Load module 7 from disk blocks 67 and 68 to memory pages 54 and 55 respectively, also
                              load idle process from the
      <a href="os_implementation.html#accordion" target="_blank">
       disk
      </a>
      to the corresponding
      <a href="os_implementation.html#accordion">
       memory pages
      </a>
      .
     </li>
     <li>
      Set SP to (user area page number) * 512 -1. The user area page number for the idle
                              process is 82 (as decided in the previous stage). This sets up a stack for calling the
                              boot module.
     </li>
     <li>
      Call module 7 (boot module) using call statement in SPL.
      <div>
       <pre>call BOOT_MODULE;</pre>
      </div>
     </li>
     <p>
      /*The following code is executed after return from the boot module*/
     </p>
     <li>
      Setup the page table entries for the idle process as was done in the previous stage.
                              Also set up PTBR to the page table base of the idle process. (The SPL constant
                              PAGE_TABLE_BASE will point to the start of the page table of the idle process - figure
                              out why.) Initialize PTLR (all user process in eXpOS must have PTLR=10).
     </li>
     <li>
      Initialize PID, UPTR, KPTR, PTBR, PTLR and user area page number fields in the
      <a href="os_design-files/process_table.html" target="_blank">
       Process Table
      </a>
      entry for the idle process as was done in the
                              previous stage.
     </li>
     <li>
      As the idle process is scheduled first, initialize the STATE field in the process table
                              entry of the idle process as RUNNING and current PID field in the
      <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
       System Status Table
      </a>
      to 0 (PID of the idle process).
     </li>
     <li>
      Transfer the entry point value from the header of the idle process to the top of the
                              user stack of the idle process, as was done in the previous stage.
     </li>
     <li>
      Set the SP to the logical address of the user stack (8*512).
     </li>
     <li>
      Switch to the user mode using the ireturn statement.
     </li>
    </ol>
    <br/>
    <b>
     Boot module
    </b>
    <br/>
    <br/>
    <ol style="list-style-type: decimal; margin-left: 2px">
     <li>
      Load all the required interrupts routines, eXpOS library, exception handler and the
                              INIT process from the disk to the memory as was done in the OS startup code of the
                              previous stage.
     </li>
     <li>
      Set the page table entries for INIT process as was done in the previous stage.
     </li>
     <li>
      Initialize the process table entry for the INIT process (setting PID, UPTR, KPTR, PTLR,
                              PTBR, user area page number etc.) as was done in the previous stage.
     </li>
     <li>
      Set the STATE field in the process table entry of INIT to CREATED. (INIT will not be
                              scheduled immedietely, as the idle process is going to be scheduled first.)
     </li>
     <li>
      Transfer the entry point value from the header of the INIT process to the top of the
                              user stack of the INIT process, as was done in the previous stage.
     </li>
     <li>
      Return from module to OS startup code using return statement in SPL.
     </li>
    </ol>
    <br/>
    <b>
     Making things work
    </b>
    <p>
     Compile and load module 7 and the modified OS startup code to the disk using XFS
                            interface. Run the XSM machine with timer enabled.
    </p>
    <br/>
    <b style="color:#26A65B">
     Assignment 1:
    </b>
    Write ExpL programs to print even and odd numbers
                          below 100. Modify the boot module code and the timer interrupt handler to schedule the two
                          processes along with the idle process concurrently using the Round Robin scheduling
                          algorithm.
    <br/>
    <br/>
    <b style="color:#26A65B">
     Assignment 2:
    </b>
    In the program of the previous assignment, add a
    <i>
     breakpoint
    </i>
    immediately upon entering the timer interrupt handler and print out in debug mode the contents of the page table entry and the process table entry of the current process (that is, the process from which timer was entered).  You need to use use
    <i>
     p
    </i>
    and
    <i>
     pt
    </i>
    options of xsm debugger.  Add another
    <i>
     breakpoint
    </i>
    just before return from the timer interrupt handler to print out the same contents.
    <br/>
   </div>
  </div>
  <!-- End Learning Objectives-->
  <a data-toggle="collapse" href="#collapse13">
   <span class="fa fa-times">
   </span>
   Close
  </a>
 </div>
</div>
