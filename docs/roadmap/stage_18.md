---
title: 'Stage 18 :
                        Disk Interrupt Handler (6 Hours)'
---
<div class="panel-collapse collapse" id="collapse18">
 <div class="panel-body">
  <!-- Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo18">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo18">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Familiarize with disk interrupt handling in XSM.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Modify the Exec system call to handle disk interrupt.
        </li>
       </ul>
      </div>
     </li>
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo18a">
       Pre-requisite Reading
      </a>
      <div class="panel-collapse expand" id="lo18a">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Read and understand the
         <a href="Tutorials/xsm_interrupts_tutorial.html#disk_and_console_interrupts" target="_blank">
          XSM tutorial on Interrupts and Exception handling
         </a>
         before proceeding
                        further.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Revise the console and disk interrupt part.
        </li>
       </ul>
      </div>
     </li>
    </ul>
   </div>
  </div>
  <!-- End Learning Objectives-->
  <br/>
  <p>
   In this stage, we will introduce disk interrupt handling in XSM. In the previous stage, we used
                        the
   <i>
    loadi
   </i>
   statement to load a disk block into a memory page. When the
   <a href="support_tools-files/spl.html" target="_blank">
    <i>
     loadi statement
    </i>
   </a>
   (immediate load) is used for loading, the machine
                        will execute the next instruction only after the block transfer is complete by the
   <a href="arch_spec-files/interrupts_exception_handling.html#disk_interrupt" target="_blank">
    disk controller
   </a>
   . A process can use the
   <b>
    load statement
   </b>
   instead of
   <i>
    loadi
   </i>
   to load a disk block to a memory page. The
   <a href="support_tools-files/spl.html" target="_blank">
    <i>
     load statement
    </i>
   </a>
   in SPL translates to
   <a href="arch_spec-files/instruction_set.html" target="_blank">
    LOAD instruction in XSM
   </a>
   .
  </p>
  <p>
   The LOAD instruction takes two arguments, a page number and a block number. The LOAD
                        instruction initiates the transfer of data from the specified disk block to the memory page.
                        The
   <b>
    XSM machine doesn't wait for the block transfer to complete
   </b>
   , it continues with the
                        execution of the next instruction. Instead, the XSM machine provides a hardware mechanism to
                        detect the completion of data transfer. XSM machine raises the
   <a href="Tutorials/xsm_interrupts_tutorial.html#disk_and_console_interrupts" target="_blank">
    disk interrupt
   </a>
   when the disk operation is complete.
  </p>
  <div style="background-color: #dff0d8; padding: 24px; border-radius: 24px">
   <p>
    In real operating systems, the OS maintains a software module called the disk
    <a href="https://en.wikipedia.org/wiki/Device_driver" target="_blank">
     device driver
    </a>
    module for handling disk access. This module is
                          responsible for programming the
    <a href="https://en.wikipedia.org/wiki/Disk_controller" target="_blank">
     disk controller
    </a>
    hardware for handling disk operations. When the OS
                          initiates a disk read/write operation from the context of a process, the device driver module
                          is invoked with appropriate arguments. In our present context, the
    <a href="os_modules/Module_4.html" target="_blank">
     device manager module
    </a>
    integrates
                          a common "driver software" for all devices of XSM. The load and store instructions
                          actually are high level "macro operations" given to you that abstract away
                          the low level details of the device specific code to program the disk controller hardware.

                          The
    <i>
     loadi
    </i>
    instruction abstracts disk I/O using the method of
    <a href="https://en.wikipedia.org/wiki/Polling_(computer_science)" target="_blank">
     polling
    </a>
    whereas
                          the
    <i>
     load
    </i>
    instruction abstracts
    <a href="https://en.wikipedia.org/wiki/Asynchronous_I/O" target="_blank">
     interrupt based
    </a>
    disk I/O.
   </p>
  </div>
  <br/>
  <p>
   To initiate the disk transfer using the load statement, first the process has to
   <b>
    acquire
   </b>
   the disk. This ensures that no other process uses the disk while the process which has acquired
                        the disk is loading the disk block to the memory page. eXpOS maintains a data structure called
   <a href="os_design-files/mem_ds.html#ds_table" target="_blank">
    Disk Status Table
   </a>
   to keep
                        track of these disk-memory transfers. The disk status table stores the status of the disk
                        indicating whether the disk is busy or free. The disk status table has a LOAD/STORE bit
                        indicating whether the disk operation is a load or store. The table also stores the page number
                        and the block number involved in the transfer. To keep track of the process that has currently
                        acquired the disk, the PID of the process is also stored in the disk status table. The SPL
                        constant
   <a href="support_tools-files/constants.html" target="_blank">
    DISK_STATUS_TABLE
   </a>
   gives the starting address of the Disk Status Table in the
   <a href="os_implementation.html" target="_blank">
    XSM memory
   </a>
   .
  </p>
  <p>
   After the current process has acquired the disk for loading, it initializes the Disk Status
                        Table according to the operation to be perfromed (read/write). The process then issues the
   <i>
    load
   </i>
   statement to initiate the loading of the disk block to the memory page. As mentioned earlier,
                        the XSM machine does not wait for the transfer to complete. It continues with the execution of
                        the next instruction. However, virtually in any situation in eXpOS, the process has to wait
                        till the data transfer is complete before proceeding (why?). Hence, the process suspends its
                        execution by changing its state to WAIT_DISK and invokes the scheduler, allowing other
                        concurrent processes to run. (At present, the only concurrent process for the OS to schedule is
                        the IDLE process. However, in subsequent stages we will see that the OS will have more
                        meaningful processes to run.)
  </p>
  <p>
   When the load/store transfer is complete, XSM machine raises the hardware interrupt called the
   <b>
    disk interrupt
   </b>
   . This interrupt mechanism is similar to the console interrupt. Note that
                        when disk interrupt occurs, XSM machine stops the execution of the currently running process.
                        The currently running process is not the one that has acquired the disk (why?). The disk
                        interrupt handler releases the disk by changing the STATUS field in the Disk Status table to 0.
                        It then wakes up all the processes waiting for the disk (by changing the STATE from WAIT_DISK
                        to READY) which also includes the process which is waiting for the disk-transfer to complete.
                        Then returns to the process which was interrupted by disk controller.
  </p>
  <p>
   <div style="background-color: #dff0d8; padding: 24px; border-radius: 24px">
    <p>
     XSM machine disables interrupts when executing in the kernel mode. Hence, the disk
                            controller can raise an interrupt only when the machine is executing in the user mode.
                            Hence the OS has to schedule "some process" even if all processess are waiting for
                            disk/terminal interrupt - for otherwise, the device concerned will never be able to
                            interrupt the processor. The IDLE process is precisely designed to take care of this and
                            other similar situations.
    </p>
   </div>
   <br/>
   <figure style="text-align: center;">
    <img src="img/roadmap/exec2.png" style="display:block;margin-left:auto;margin-right:auto"/>
    <br/>
    <figcaption>
     Control flow for
     <i>
      Exec
     </i>
     system call
    </figcaption>
   </figure>
   <br/>
   <p>
    In this stage,
    <b>
     you have to modify the exec system call by replacing the
     <a href="support_tools-files/spl.html" target="_blank">
      loadi statement
     </a>
     by a call to the
     <i>
      Disk Load
     </i>
     function. The
     <i>
      Disk
                              Load
     </i>
     function (in device manager module), the
     <i>
      Acquire Disk
     </i>
     function (in
                            resource manager module) and the
     <i>
      disk interrupt handler
     </i>
     must also be implemented in
                            this stage.
    </b>
    Minor modifications are also required for the boot module.
   </p>
   <br/>
   <ol style="list-style-type: decimal;margin-left: 2px">
    <li>
     <b>
      Disk Load (function number = 2,
      <a href="os_modules/Module_4.html" target="_blank">
       device
                                manager module
      </a>
      )
     </b>
    </li>
    <p>
     The Disk Load function takes the PID of a process, a page number and a block number as
                            input and performs the following tasks :
     <br/>
     1) Acquires the disk by invoking the Acquire
                            Disk function in the
     <a href="os_modules/Module_0.html" target="_blank">
      resource manager
                              module
     </a>
     (module 0)
     <br/>
     2) Set the
     <a href="os_design-files/mem_ds.html#ds_table" target="_blank">
      Disk Status table
     </a>
     entries as mentioned in the algorithm (specified in the above link).
     <br/>
     3) Issue the
     <a href="support_tools-files/spl.html" target="_blank">
      load statement
     </a>
     to initiate a disk
                            block to memory page DMA transfer.
     <br/>
     4) Set the state of the process (with given PID) to
                            WAIT_DISK and invoke the scheduler.
    </p>
    <br/>
    <li>
     <b>
      Acquire Disk (function number = 3,
      <a href="os_modules/Module_0.html" target="_blank">
       resource
                                manager module
      </a>
      )
     </b>
    </li>
    <p>
     The Acquire Disk function in the resource manager module takes the PID of a process as an
                            argument. The Acquire disk function performs the following tasks :
     <br/>
     1) While the disk is busy (STATUS field in the Disk Status Table is 1), set the state of
                            the process to WAIT_DISK and invoke the scheduler.
     <br/>
     /* When the disk is finally free,
                            the process is woken up by the disk interrupt handler.*/
     <br/>
     2) Lock the disk by setting
                            the STATUS and the PID fields in the Disk Status Table to 1 and PID of the process
                            respectively.
    </p>
    <br/>
    <p style="text-indent: 0px">
     <code>
      Note :
     </code>
     Both Disk Load and Acquire Disk module
                            functions implemented above are final versions according to the algorithm given in
                            respective modules.
    </p>
    <br/>
    <li>
     <b>
      Implementation of
      <a href="os_design-files/disk_interrupt.html" target="_blank">
       Disk
                                Interrupt handler
      </a>
     </b>
    </li>
    <p>
     When the disk-memory transfer is complete, XSM raises the disk interrupt. The disk
                            interrupt handler then performs the following tasks :
     <br/>
     1) Switch to the kernel stack and back up the register context.
     <br/>
     2) Set the STATUS field in the Disk Status table to 0 indicating that disk is no longer
                            busy.
     <br/>
     3) Go through all the process table entries, and change the state of the process to
                            READY, which is in WAIT_DISK state.
     <br/>
     4) Restore the register context and return to user mode using the ireturn statement.
    </p>
    <p style="text-indent: 0px">
     <code>
      Note:
     </code>
     There is no Release Disk function to release
                            the disk instead the disk interrupt handler completes the task of the Release Disk
                            function.
    </p>
    <br/>
    <li>
     <b>
      Modification to exec system call (interrupt 9 routine)
     </b>
    </li>
    <p>
     Instead of the loadi statement used to load the disk block to the memory page, invoke the
     <b>
      Disk Load
     </b>
     function present in the
     <a href="os_modules/Module_4.html" target="_blank">
      device
                              manager module
     </a>
     .
    </p>
    <p>
     We will initialize another data strucutre as well in this stage. This is the
     <a href="os_design-files/process_table.html#per_process_table" target="_blank">
      per-process resource table
     </a>
     . (This step can be deferred to later
                            stages, but since the work involved is simple, we will finish it here). The per-process
                            resource table stores the information about the files and semaphores which a process is
                            currently using. For each process, per-process resource table is stored in the user area
                            page of the process. This table has 8 entries with 2 words each, in total it occupies 16
                            words.
     <i>
      We will reserve the last 16 words of the User Area Page to store the per-process
                              Resource Table of the process.
     </i>
     In exec, after reacquiring the
     <a href="os_design-files/process_table.html#user_area" target="_blank">
      user area page
     </a>
     for the new process, per-process resource table should
                            be initialized in this user area page. Since the newly created process has not opened any
                            files or semaphores, each entry in the per-process table is initialized to -1.
    </p>
    <br/>
    <li>
     <b>
      Modifications to boot module
     </b>
    </li>
    <p>
     Following modifications are done in boot module :
     <br/>
     1) Load the disk interrupt routine from the disk to the memory.
     <br/>
     2) Initialize the STATUS field in the Disk Status Table to 0.
     <br/>
     3) Initialize the
     <a href="os_design-files/process_table.html#per_process_table" target="_blank">
      per-process
                              resource table
     </a>
     of init process.
    </p>
   </ol>
   <br/>
   <p>
    Compile and load the modified and newly written files into the disk using XFS-interface. Run
                          the Shell version-I with any program to check for errors.
   </p>
   <div class="container col-md-12">
    <div class="section_area">
     <ul class="list-group">
      <li class="list-group-item">
       <a data-toggle="collapse" href="#collapseq11">
        <b>
         Q1.
        </b>
        Can we use the load statement
                                  in the boot module code instead of the loadi statement? Why?
       </a>
       <div class="panel-collapse collapse" id="collapseq11">
        No. The modules needed for the execution of load, need to be present in the memory
                                  first. And even if they are present, at the time of execution of the boot module, no
                                  process or data structures are initialized (like Disk Status Table).
       </div>
      </li>
      <li class="list-group-item">
       <a data-toggle="collapse" href="#collapseq12">
        <b>
         Q2.
        </b>
        Why does the disk interrupt
                                  handler has to backup the register context?
       </a>
       <div class="panel-collapse collapse" id="collapseq12">
        Disk interrupt handler is a hardware interrupt. When disk interrupt occurs, the XSM
                                  machine just pushes IP+2 value on stack and transfers control to disk interrupt.
                                  Occurance of a hardware interrupt is unexpected. When the disk interrupt is raised,
                                  the process will not have control over it so the process (curently running) cannot
                                  backup the registers. That's why interrupt handler must back up the context of the
                                  process (currently running) before modifying the machine registers. The interrupt
                                  handler also needs to restore the context before returning to user mode.
       </div>
      </li>
      <li class="list-group-item">
       <a data-toggle="collapse" href="#collapseq13">
        <b>
         Q3.
        </b>
        Why doesn't system calls
                                  backup the register context?
       </a>
       <div class="panel-collapse collapse" id="collapseq13">
        The process currently running is in full control over calling the interrupt (software
                                  interrupt) corresponding to a system call. This allows a process to back up the
                                  registers used till that point (not all registers). Note that instead of process, the
                                  software interrupt can also back up the registers. But, the software interrupt will
                                  not know how many registers are used by the process so it has to back up all the
                                  registers. Backing up the registers by a process saves space and time.
       </div>
      </li>
      <li class="list-group-item">
       <a data-toggle="collapse" href="#collapseq14">
        <b>
         Q4.
        </b>
        Does the XSM terminal input
                                  provide polling based input?
       </a>
       <div class="panel-collapse collapse" id="collapseq14">
        Yes,
        <i>
         readi
        </i>
        statement provided in SPL gives polling based terminal I/O. But
                                  readi statement only works in debug mode. Write operation is always asynchronous.
       </div>
      </li>
     </ul>
    </div>
   </div>
   <p>
    <b style="color:#26A65B">
     Assignment 1:
    </b>
    Use the
    <a href="support_tools-files/xsm-simulator.html" target="_blank">
     XSM debugger
    </a>
    to print out the contents of the Disk Status Table after entry and before return from the disk interrupt handler.
   </p>
   <br/>
   <a data-toggle="collapse" href="#collapse18">
    <span class="fa fa-times">
    </span>
    Close
   </a>
  </p>
 </div>
</div>
