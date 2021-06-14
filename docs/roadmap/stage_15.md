---
title: '
Stage 15 : Resource Manager Module (4 Hours)'
---
<div class="panel-collapse collapse" id="collapse15">
 <div class="panel-body">
  <!-- Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo15">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo15">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Familiarise with passing of parameters to modules.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Implement Resource Manager and Device Manager modules for terminal output handling.
        </li>
       </ul>
      </div>
     </li>
    </ul>
   </div>
  </div>
  <!-- End Learning Objectives-->
  <p>
   Processes in eXpOS require various resources like terminal, disk, inode etc. To manage these
                        resources among different processes eXpOS implements a
   <a href="os_modules/Module_0.html" target="_blank">
    resource manager module
   </a>
   (Module 0).
   <b>
    Before the use of a resource, a
                          process has to first acquire the required resource by invoking the resource manager. A
                          process can acquire a resource if the resource is not already acquired by some other process.
                          If the resource requested by a process is not available, then that process has to be blocked
                          until the resource becomes free.
   </b>
   In the meanwhile, other processes may be scheduled.
   <p>
    A blocked process must wake up when the requested resource is released by the process which
                          had acquired the resource. For this,
    <b>
     when a process releases a resource, the state of
                            other processes waiting for the resource must be set to READY
    </b>
    .
   </p>
   <p>
    The resource manager module handles acquisition and release of system resources. A process
                          must invoke the resource manager to acquire or release any system resource. The resource
                          manager implements two functions for each resource - one to acquire the resource and the
                          other to release the resource by a process. Details about different functions implemented in
                          resource manager module are given
    <a href="os_modules/Module_0.html" target="_blank">
     here
    </a>
    .
   </p>
   <p>
    In this stage, you will learn how the terminal is shared by the processes for writing. The
                          OS maintains a data structure called the
    <a href="os_design-files/mem_ds.html#ts_table" target="_blank">
     Terminal Status Table
    </a>
    . The Terminal Status table contains details of
                          the process that has acquired the terminal. (Since there is only one terminal in the system,
                          only one process is allowed to acquire the terminal at a time.) A flag named STATUS in the
                          terminal status table indicates whether the terminal is available or not. When a process
                          acquires the terminal, the PID of the process is updated in the terminal status table.
   </p>
   <p>
    There are two functions related to terminal management in module 0. These are the Acquire
                          Terminal and the Release Terminal functions. Each function has a function number to identify
                          the function within the module. In the Resource Manager module,
    <b>
     Acquire Terminal and
                            Release Terminal have function numbers 8 and 9 respectively
    </b>
    . When a module function is
                          invoked, the function number (identifying the particular function within the module) is
                          stored in register R1 and passed as argument to the module. The other arguments are passed
                          through registers R2, R3 etc. See
    <a href="support_tools-files/spl.html#con" target="_blank">
     SPL
                            module calling convention
    </a>
    . For both Acquire Terminal and Release Terminal, PID of the
                          currently running process needs to be passed as an argument through the register R2.
   </p>
   <p>
    Acquire Terminal and Release Terminal are not directly invoked from the write system call.
                          Write system call invokes a function called Terminal Write present in
    <a href="os_modules/Module_4.html" target="_blank">
     device manager module
    </a>
    (Module 4). Terminal Write function acts as an
                          abstract layer between the write system call and terminal handling functions in resource
                          manager module. The function number for Terminal Write is 3 which is stored in register R1.
                          The other arguments are PID of the current process and the word to be printed which are
                          passed through registers R2 and R3 respectively. Terminal Write first acquires the terminal
                          by calling Acquire Terminal. It prints the word (present in R3) passed as an argument. It
                          then frees the terminal by invoking Release Terminal.
   </p>
   <p>
    Since the invoked module will be modifying the contents of the machine registers during its
                          execution, The invoker must save the registers in use into the (kernel) stack of the process
                          before invoking the module. The module sets its return value in register R0 before returning
                          to the caller. The invoker must extract the return value, pop back the saved registers and
                          resume execution. SPL provides the facility to push and pop multiple registers in one
                          statement using multipush and mutlipop respectively. Refer to the usage of multipush and
                          multipop statements in
    <a href="support_tools-files/spl.html" target="_blank">
     SPL
    </a>
    before
                          proceeding further.
   </p>
   <p>
    There is one important conceptual point to be explained here relating to resource
                          acquisition. The Acquire Terminal function described above waits in a loop, in which it
                          repeatedly invokes the scheduler if the terminal is not free.
    <b>
     This kind of a waiting loop
                            is called a busy loop or
     <a href="https://en.wikipedia.org/wiki/Busy_waiting" target="_blank">
      busy
                              wait
     </a>
     .
    </b>
    <i>
     Why can't the process wait just once for a resource and simply proceed
                            to acquire the resource when it is scheduled?
    </i>
    In other words, what is the need for a
                          wait in a loop? Pause to think before you read the explanation below. You will encounter such
                          busy loops several times in this project, inside various module functions described in later
                          stages.
   </p>
   <br/>
   <div style="background-color: #dff0d8; padding: 24px; border-radius: 24px">
    <p>
     When a process invokes the scheduler waiting for a resource, the scheduler runs the
                            process again only after the resource becomes free. However, the process may find that the
                            resource is locked again when it tries to acquire the resource when it resumes execution.
                            This happens because when a resource is released, all processes waiting for the resource
                            are woken up by the OS. Only the one that get scheduled first will be able to lock the
                            resource successfully. Other processes will have to wait for the resource repeatedly before
                            finally acquiring the resource.
    </p>
    <p>
     A better solution to the problem that avoids a busy loop is to have the resource manager
                            maintain a request queue associated with each resource. When a process requests a resource,
                            it registers itself into a resource queue and goes into wait state. When the resource is
                            released, the release resource function can wake up only the process which is at head of
                            the queue. This avoids unnecessary scheduling of all the waiting processes. Real systems
                            implement resource queues for system resources that also maintains the priorities of
                            various requesting processes. In eXpOS, we avoid using resource queues to make the
                            implementation easier.
    </p>
   </div>
   <br/>
   <p style="text-indent: 0px">
    <code>
     Note:
    </code>
    We haven't saved any registers into the stack
                          while invoking the boot module from the OS startup code or the scheduler module from the
                          timer interrupt routine as there was no register context to be saved. However, to invoke
                          scheduler module from other modules or interrupt routines, it is necessary to save the
                          register context into the stack for proper resumption of execution.
   </p>
   <br/>
   <figure style="text-align: center;">
    <img src="img/roadmap/write.png" style="display:block;margin-left:auto;margin-right:auto"/>
    <br/>
    <figcaption>
     Control flow for
     <i>
      Write
     </i>
     system call
    </figcaption>
   </figure>
   <br/>
   <b>
    Modifying INT 7 routine
   </b>
   <br/>
   <br/>
   <p>
    Interrupt routine 7 implemented in stage 10 is modified as given below to invoke Terminal
                          Write function present in Device Manager module. Instead of print statement, write code to
                          invoke Terminal Write function. Rest of the code remains intact.
    <ol style="list-style-type: decimal; margin-left: 2px">
     <li>
      Push all registers used till now in this interrupt routine using multipush statement in
                              SPL.
      <div>
       <pre>multipush(R0, R1, R2, R3,...); // number of registers will depend on your code</pre>
      </div>
     </li>
     <li>
      Store the function number of Terminal Write in register R1, PID of the current process
                              in register R2 and word to be printed to the terminal in register R3.
     </li>
     <li>
      Call module 4 using
      <a href="./support_tools-files/spl.html" target="_blank">
       call
                                statement
      </a>
      .
     </li>
     <li>
      Ignore the value present in R0 as Terminal Write does not have any return value.
     </li>
     <li>
      Use multipop statement to restore the registers pushed. Specify the same order of
                              registers used in multipush as registers are popped in the
      <b>
       reverse order
      </b>
      in which
                              they are specified in the multipop statement.
      <div>
       <pre>multipop(R0, R1, R2, R3,...);</pre>
      </div>
     </li>
    </ol>
    <br/>
    <b>
     Implementation of Module 4 (Device Manager Module)
    </b>
    <br/>
    <br/>
    <p>
     In this stage, we will implement only Terminal Write function in this module.
    </p>
    <ol style="list-style-type: decimal;margin-left: 2px">
     <li>
      Function number and current PID are stored in registers R1 and R2. Give meaningful
                              names to these arguments.
      <div>
       <pre>alias functionNum R1;
alias currentPID R2;</pre>
      </div>
     </li>
     <li>
      Terminal write function has a function number 3. If the functionNum is 3, implement the
                              following steps else return using return statement.
     </li>
     <p style="text-indent: 0px">
      Calling Acquire Terminal :-
     </p>
     <li>
      Push all the registers used till now in this module using the multipush statement in
                              SPL as done earlier.
     </li>
     <li>
      Store the function number 8 in register R1 and PID of the current process from the
      <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
       System Status table
      </a>
      in
                              register R2 (Can use currentPID, as it already contain current PID value).
     </li>
     <li>
      Call module 0.
     </li>
     <li>
      Ignore the value present in R0 as Acquire Terminal does not have any return value.
     </li>
     <li>
      Use the multipop statement to restore the registers as done earlier.
     </li>
     <li>
      Print the word in register R3, using the print statement.
     </li>
     <p style="text-indent: 0px">
      Calling Release Terminal :-
     </p>
     <li>
      Push all the registers used till now using the multipush statement as done earlier.
     </li>
     <li>
      Store the function number 9 in register R1 and PID of the current process from the
                              System Status table in register R2 (Can use currentPID, as it already contain current PID
                              value).
     </li>
     <li>
      Call module 0.
     </li>
     <li>
      Return value will be stored in R0 by module 0. Save this return value in any other
                              register if needed.
     </li>
     <li>
      Restore the registers using the multipop statement.
     </li>
     <li>
      Return using the return statement.
     </li>
    </ol>
    <br/>
    <b>
     Implementation of Module 0 code for terminal handling
    </b>
    <br/>
    <br/>
    <ol style="list-style-type: decimal;margin-left: 2px">
     <li>
      Function number is present in R1 and PID passed as an argument is stored in R2. Give
                              meaningful names to these registers to use them further.
      <div>
       <pre>alias functionNum R1;
alias currentPID R2;</pre>
      </div>
     </li>
     <br/>
     <li>
      In Module 0, for the Acquire Terminal function (functionNum = 8) implement the
                              following steps.
     </li>
     <ol style="list-style-type: lower-roman; margin-left: 20px">
      <li>
       <b>
        The current process should wait in a loop until the terminal is free
       </b>
       . Repeat
                                the following steps if STATUS field in the Terminal Status table is 1(terminal is
                                allocated to other process).
       <ul style="list-style-type: disc;margin-left: 24px">
        <li>
         Change the state of the current process in its process table entry to
                                    WAIT_TERMINAL.
        </li>
        <li>
         Push the registers used till now using the multipush statement.
        </li>
        <li>
         Call the scheduler to schedule other process as this process is waiting for
                                    terminal.
        </li>
        <li>
         Pop the registers pushed before. (Note that this code will be executed only after
                                    the scheduler schedules the process again, which in turn occurs only after the
                                    terminal was released by the holding process by invoking the release terminal
                                    function.)
        </li>
       </ul>
      </li>
      <li>
       Change the STATUS field to 1 and PID field to currentPID in the Terminal Status
                                Table.
      </li>
      <li>
       Return using the return statement.
      </li>
     </ol>
     <br/>
     <li>
      for the Release Terminal function (functionNum = 9) implement the following steps.
     </li>
     <ol style="list-style-type: lower-roman; margin-left: 20px">
      <li>
       currentPID and PID stored in the Terminal Status table should be same. If these are
                                not same, then process is trying to release the terminal without acquiring it. If this
                                case occurs, store -1 as the return value in register R0 and return from the module.
      </li>
      <li>
       Change the STATUS field in the Terminal Status table to 0, indicating terminal is
                                released.
      </li>
      <li>
       Update the STATE to READY for all processes (with valid PID) which have STATE as
                                WAIT_TERMINAL.
      </li>
      <li>
       Save 0 in register R0 indicating success.
      </li>
      <li>
       Return to the caller.
      </li>
     </ol>
    </ol>
    <br/>
    <b>
     Modifying Boot Module code
    </b>
    <br/>
    <br/>
    <ol style="list-style-type: decimal;margin-left: 2px">
     <li>
      Load Module 0 from disk pages 53 and 54 to memory pages 40 and 41.
     </li>
     <li>
      Load Module 4 from disk pages 61 and 62 to memory pages 48 and 49.
     </li>
     <li>
      Initialize the STATUS field in the
      <a href="os_design-files/mem_ds.html#ts_table">
       Terminal
                                Status table
      </a>
      as 0. This will indicate that the terminal is free before scheduling
                              the first process.
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
      Compile and load boot module code, module 0, module 4, modified INT 7 routine using
                              XFS-interface.
     </li>
     <li>
      Run the machine with two programs one printing even numbers and another printing odd
                              numbers from 1 to 100 along with the idle process.
     </li>
    </ol>
    <div class="container col-md-12">
     <div class="section_area">
      <ul class="list-group">
       <li class="list-group-item">
        <a data-toggle="collapse" href="#collapseq7">
         <b>
          Q1.
         </b>
         According to eXpOS resource
                                    management system introduced here, will Deadlock occur? If yes, explain it with a
                                    situation. If no, which of the four conditions of Deadlock are not satisfied?
        </a>
        <div class="panel-collapse collapse" id="collapseq7">
         Deadlock will not occur according to the resource management system implemented
                                    here. As hold and wait, circular wait conditions are not satisfied (there is only
                                    one resource - the terminal - now).
        </div>
       </li>
      </ul>
     </div>
    </div>
    <br/>
    <p>
     See
     <a href="https://en.wikipedia.org/wiki/Deadlock#Necessary_conditions" target="_blank">
      link
     </a>
     for a set of neccessary conditions for deadlock.
    </p>
    <p>
     <b style="color:#26A65B">
      Assignment 1:
     </b>
     Set a
     <b>
      breakpoint
     </b>
     (see
     <a href="support_tools-files/spl.html" target="_blank">
      SPL breakpoint instruction
     </a>
     ) just before return from the Acquire Terminal and the Release Terminal functions in the Resource Manager module to dump the Terminal Status Table (see
     <a href="support_tools-files/xsm-simulator.html" target="_blank">
      XSM debugger
     </a>
     for various printing options).
    </p>
    <br/>
    <a data-toggle="collapse" href="#collapse15">
     <span class="fa fa-times">
     </span>
     Close
    </a>
   </p>
  </p>
 </div>
</div>
