---
title: 'Stage 16 : Console Input (6 Hours)'
---
<div class="panel-collapse collapse" id="collapse16">
 <div class="panel-body">
  <!-- Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo16">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo16">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Familiarise with the Console Interrupt handling in XSM.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Implementation of console input using the read system call.
        </li>
        <li>
         <span class="fa fa-hand-o-right">
         </span>
         Introduction to input
                                    buffer.
        </li>
       </ul>
      </div>
     </li>
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo16">
       Pre-requisite
                                Reading
      </a>
      <div class="panel-collapse expand" id="lo16">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Read and understand the
         <a href="Tutorials/xsm_interrupts_tutorial.html#disk_and_console_interrupts" target="_blank">
          XSM tutorial on Interrupts and Exception handling
         </a>
         before
                                    proceeding further. (Read only the console and disk interrupt part.)
        </li>
       </ul>
      </div>
     </li>
    </ul>
   </div>
  </div>
  <!-- End Learning Objectives-->
  <p>
   In this stage, we will introduce you to XSM console interrupt handling. A process must use
                        the
   <a href="arch_spec-files/instruction_set.html">
    XSM instruction IN
   </a>
   to
   <b>
    read data from
                          the console into the input
   </b>
   <a href="arch_spec-files/machine_organisation.html" target="_blank">
    port
                          P0
   </a>
   . IN is a privileged instruction and can be executed only inside a system call/module.
                        Hence, to read data from the console, a user process invokes the
   <a href="os_spec-files/systemcallinterface.html" target="_blank">
    read system call
   </a>
   . The read system call invokes the Terminal Read
                        function present in
   <a href="os_modules/Module_4.html" target="_blank">
    Device Manager module
   </a>
   (Module 4). The IN instruction will be executed within this Terminal Read function.
  </p>
  <p>
   The most important fact about the
   <b>
    IN instruction is that it will not wait for the data to
                          arrive in P0
   </b>
   . Instead, the XSM machine continues advancing the instruction pointer and
                        executing the next instruction. Hence there must be some hardware mechanism provided by XSM to
                        detect arrival of data in P0.
  </p>
  <p>
   When does data arrive in P0? This happens when some string/number is entered from the
                        key-board and ENTER is pressed. At this time,
   <b>
    the XSM machine will raise the console
                          interrupt
   </b>
   . Thus the console interrupt is the hardware mechanism that helps the OS to
                        infer that the execution of the IN instruction is complete.
  </p>
  <p>
   As noted above, the IN instruction is typically executed from the Terminal Read function.
                        Since it is not useful for the process that invoked the Terminal Read function to continue
                        execution till data arrives in P0,
   <b>
    a process executing the IN instruction will sets its
                          state to WAIT_TERMINAL and invoke the scheduler
   </b>
   . The process must resume execution only
                        after the XSM machine sends an interrupt upon data arrival.
  </p>
  <p>
   When the console interrupt occurs, the machine interrupts the current process (note that some
                        other process would be running) and executes the console interrupt handler. (The interrupt
                        mechanism is similar to the timer interrupt. The current value of IP+2 is pushed into the stack
                        and control transfers to the interrupt handler - see
   <a href="Tutorials/xsm_interrupts_tutorial.html#disk_and_console_interrupts" target="_blank">
    XSM machine execution tutorial
   </a>
   for details).
                        It is the responsiblity of the
   <b>
    console interrupt handler to transfer the data arrived in
                          port P0 to the process which is waiting for the data
   </b>
   . This is done by copying the value
                        present in port P0 into the
   <b>
    input buffer
   </b>
   field of the
   <a href="os_design-files/process_table.html" target="_blank">
    process table
   </a>
   entry of the process which has requested for the input.
   <b>
    Console
                          interrupt handler also wakes up the process in WAIT_TERMINAL by setting its state to READY
   </b>
   .
                        (Other processes in WAIT_TERMINAL state are also set to READY by the console interrupt
                        handler.)
  </p>
  <p>
   Each process maintains an input buffer which stores the last data read by the process from the
                        console. On the occurance of a terminal interrupt, the interrupt handler uses the PID field of
                        the terminal status table to identify the correct process that had acquired the terminal for a
                        read operation. The handler transfer the data from the input port to the input buffer of the
                        process.
  </p>
  <p>
   User programs can invoke the read system call using the library interface. For a terminal
                        read, the file descriptor (-1 for terminal input) is passed as the first argument. The second
                        argument is a variable to store number/string from console. Refer to the read system call
                        calling convention
   <a href="os_spec-files/dynamicmemoryroutines.html" target="_blank">
    here
   </a>
   .
                        ExpL library converts exposcall to
   <a href="os_design-files/Sw_interface.html" target="_blank">
    low
                          level system call interface
   </a>
   for read system call, to invoke interrupt 6.
  </p>
  <p>
   The read system call (Interrupt 6) invokes the
   <b>
    Terminal Read
   </b>
   function present in the
   <a href="os_modules/Module_4.html" target="_blank">
    Device manager Module
   </a>
   . Reading from the
                        terminal and storing the number/string (read from console) in the address provided is done by
                        the Terminal Read function. Function number for the Terminal Read function, current PID and
                        address where the word has to be stored are sent as arguments through registers R1, R2 and R3
                        respectively. After coming back from Terminal Read function, it is expected that the word
                        address (passed as argument to read system call) contains the number/string entered in the
                        terminal.
  </p>
  <p>
   The OS maintains a global data structure called the
   <a href="os_design-files/mem_ds.html#ts_table">
    terminal
                          status table
   </a>
   that stores information about the current state of the terminal. A process
                        can acquire the terminal by invoking the Acquire Terminal function of the
   <a href="os_modules/Module_0.html">
    resource
                          manager module
   </a>
   .
   <b>
    When the Acquire Terminal function assigns the terminal to a process,
                          it enters the PID of the process into the PID field of the terminal status table
   </b>
   . The
                        Terminal Read function must perform the following 1) Acquire the terminal 2) Issue an IN
                        instruction (SPL read statement translates to XSM instruction IN) 3) Set its state as
                        WAIT_TERMINAL 4) Invoke the scheduler and 5) After console interrupt wakes up this process,
                        transfer data present in the input buffer field of the process table into the word address
                        (passed as an argument).
  </p>
  <!--
                           <p> When the data finally arrives, <b>the console interrupt handler must transfer the data (in port P0) into the input buffer of the process</b> in the <a href="os_design-files/process_table.html" target="_blank">process table</a>. Then the handler wakes up process waiting for the terminal.</p>

                          <p>  Finally, the read system call, after waking up from the WAIT_TERMINAL state, returns the input data in the buffer and passes this data to the user program that invoked the system call.  </p> -->
  Read about
  <a href="Tutorials/xsm_interrupts_tutorial.html" target="_blank">
   XSM interrupts
  </a>
  before proceeding further.
  <br/>
  <br/>
  <figure style="text-align: center;">
   <img src="img/roadmap/read.png" style="display:block;margin-left:auto;margin-right:auto"/>
   <br/>
   <figcaption>
    Control flow for
    <i>
     Read
    </i>
    system call
   </figcaption>
  </figure>
  <br/>
  <b>
   Implementation of read system call (interrupt 6 routine)
  </b>
  <br/>
  <br/>
  <ol style="list-style-type: decimal;margin-left: 2px">
   <li>
    Set the MODE FLAG in the process table of the current process to the system call number
                          which is 7 for read system call.
   </li>
   <li>
    Save the value of register SP as userSP.
    <div>
     <pre>alias userSP R0;
userSP=SP;</pre>
    </div>
   </li>
   <li>
    Store the value of register SP in the UPTR field of the
    <a href="os_design-files/process_table.html" target="_blank">
     process table
    </a>
    entry of the current process.
   </li>
   <li>
    Initialize SP (kernel stack pointer) to (user area page number)*512 -1.
   </li>
   <li>
    Retrieve the file descriptor from the user stack, stored at userSP-4.
   </li>
   <li>
    If the file descriptor is not -1
    <ol style="list-style-type: lower-roman;margin-left: 20px">
     <li>
      Store -1 as the return value in the user stack (at position userSP-1).
     </li>
    </ol>
   </li>
   <li>
    If the file descriptor is -1, implement below steps.
    <ol style="list-style-type: lower-roman; margin-left: 20px">
     <li>
      Retrieve the word address sent as an argument from the user stack (userSP-3).
     </li>
     <li>
      Push all the registers used till now in this interrupt.
     </li>
     <li>
      Save the function number of the Terminal Read function in the register R1. Save PID of
                              the current process and the word address obtained above in registers R2 and R3
                              respectively.
     </li>
     <li>
      Call device manager module.
     </li>
     <p style="text-indent: 0px">
      There is no return value for terminal Read.
     </p>
     <li>
      Restore the registers.
     </li>
     <li>
      Store 0 as return value in the user stack indicating success.
     </li>
    </ol>
   </li>
   <li>
    Reset the MODE FLAG in the process table to 0.
   </li>
   <li>
    Change SP back to user stack and return to the user mode.
   </li>
  </ol>
  <br/>
  <b>
   Modification to Device manager Module
  </b>
  <br/>
  <br/>
  <p style="text-indent: 0px">
   In previous stage we implemented Terminal Write function in module 4,
                        now we will add Terminal Read function.
  </p>
  <ol>
   <li>
    If function number in R1 corresponds to Terminal Read, then implement below steps.
   </li>
   <p style="text-indent: 0px">
    Calling Acquire Terminal function :-
   </p>
   <li>
    Push all the registers used till now using multipush.
   </li>
   <li>
    Initialize registers R1, R2 with function number of Acquire Terminal and PID of current
                          process respectively.
   </li>
   <li>
    Call resource manager module.
   </li>
   <li>
    Restore the registers using the multipop statement.
   </li>
   <li>
    Use read statement, for requesting to read from the terminal.
    <div>
     <pre>read;</pre>
    </div>
   </li>
   <li>
    Change the state of the current process to WAIT_TERMINAL.
   </li>
   <p style="text-indent: 0px">
    Invoking the Context Switch Module :-
   </p>
   <li>
    Push all the registers used till now.
   </li>
   <li>
    Invoke the scheduler.
   </li>
   <p style="text-indent: 0px">
    Following steps are executed after return from the scheduler
   </p>
   <li>
    Restore the registers using the multipop statement.
   </li>
   <li>
    The logical address of the word where the data has to be stored is in R3. Convert this
                          logical address to physical address.
   </li>
   <li>
    Store the value present in input buffer field of process table to the obtained physical
                          address of the word.
   </li>
   <li>
    Return to the caller.
   </li>
  </ol>
  <br/>
  <b>
   Implementation of
   <a href="os_design-files/term_handler.html" target="_blank">
    Console
                          Interrupt Handler
   </a>
  </b>
  <br/>
  <br/>
  <p style="text-indent: 0px">
   /* The console interrupt handler is entered while some other process
                        is executing in the user mode. The handler must switch to the kernel stack of that process, do
                        the interrupt handling, restore the user stack of the process that was running and return
                        control back to the process */
  </p>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    Store the SP value in the UPTR field in the process table entry of the currently running
                          process.
   </li>
   <li>
    Initialize SP (kernel stack pointer) to (user area page number)*512 -1. //Switch to the
                          kernel stack.
   </li>
   <li>
    Backup the user context of the currently running process in the kernel stack as done in
                          timer interrupt routine.
   </li>
   <li>
    Get the PID of the process that has aqcuired the terminal from the
    <a href="os_design-files/mem_ds.html#ts_table" target="_blank">
     terminal status table
    </a>
    , Save this as reqPID.
   </li>
   <li>
    Using the reqPID obtained in the above step, get the corresponding process table entry.
   </li>
   <li>
    The input entered in the console is saved in port P0 by the XSM machine. Copy the value
                          present in P0 into the input buffer field of the process table entry obtained in the above
                          step.
   </li>
   <p style="text-indent: 0px">
    /*next release the terminal */
   </p>
   <li>
    Push the registers used in this interrupt.
   </li>
   <li>
    Initialize register R1 with function number for release terminal, R2 with reqPID (The
                          current process did not acquire the terminal. The process with reqPID as PID is holding the
                          terminal.)
   </li>
   <li>
    Call resource manager module.
   </li>
   <li>
    Ignore the return value and restore the registers pushed before.
   </li>
   <li>
    Restore the user context from the kernel stack as done in the timer interrupt routine.
   </li>
   <li>
    Change SP to UPTR field from the process table entry of the currently running process and
                          return to the user mode. //Switch back to user stack
   </li>
  </ol>
  <br/>
  <b>
   Modification to Boot Module
  </b>
  <br/>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    Load console interrupt handler and interrupt 6 from disk to memory.
   </li>
   <li>
    Remove the initialization of the third process, as we will run only idle and init processes
                          in this stage.
   </li>
  </ol>
  <br/>
  <b>
   Making things work
  </b>
  <br/>
  <br/>
  <ol style="list-style-type: decimal;margin-left: 2px">
   <li>
    Compile and load boot module code, console interrupt and interrupt 6 using XFS interface.
   </li>
   <li>
    Write an ExpL program which reads two numbers from console and finds the GCD using
                          Euclidean's algorithm and print the GCD. Load this program as init program.
   </li>
  </ol>
  <br/>
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq8">
       <b>
        Q1.
       </b>
       Is it possible that, the running
                                process interrupted by the console interrupt be the same process that had acquired the
                                terminal for reading?
      </a>
      <div class="panel-collapse collapse" id="collapseq8">
       No, The process which has acquired the terminal will be in WAIT_TERMINAL state after
                                issuing a terminal read until the console interrupt occurs. Hence, this process will
                                not be scheduled until console interrupt changes it's state to READY.
      </div>
     </li>
    </ul>
   </div>
  </div>
  <p>
   <b style="color:#26A65B">
    Assignment 1:
   </b>
   Write an ExpL program to read N numbers in an array,
                      sort using bubble sort and print the sorted array to the terminal. Load this program as init
                      program and run the machine.
  </p>
  <p>
   <b style="color:#26A65B">
    Assignment 2:
   </b>
   Use the
   <a href="support_tools-files/xsm-simulator.html" target="_blank">
    XSM debugger
   </a>
   to print out the contents of the Terminal Status Table and the input buffer (by dumping process table entry of the process to which read was performed) before and after reading data from the input port to the input buffer of the process, inside the terminal interrupt handler.
  </p>
  <br/>
  <br/>
 
 </div>
</div>
