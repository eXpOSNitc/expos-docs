---
title: 'Stage 21 :
                        Process Synchronization (4 Hours)'
---
<div class="panel-collapse collapse" id="collapse21">
 <div class="panel-body">
  <!-- Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo21">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo21">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Familiarize with process synchronization in eXpOS
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Implementation of
         <i>
          Wait
         </i>
         and
         <i>
          Signal
         </i>
         system calls
        </li>
       </ul>
      </div>
     </li>
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo21a">
       Pre-requisite Reading
      </a>
      <div class="panel-collapse expand" id="lo21a">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Read and understand
         <a href="os_spec-files/expos_abstractions.html" target="_blank">
          Access
                                      control and synchronization
         </a>
         and
         <a href="os_spec-files/synchronization.html#process_synchronization" target="_blank">
          Process synchronization
         </a>
         documentations before proceeding further.
        </li>
       </ul>
      </div>
     </li>
    </ul>
   </div>
  </div>
  <!-- End Learning Objectives-->
  <br/>
  <br/>
  <p>
   In this stage, we will add support for process synchronization using
   <i>
    Wait
   </i>
   and
   <i>
    Signal
   </i>
   system calls to eXpOS. With the help of these system calls, we will design a more advanced
                        shell program. We will also implement
   <i>
    Getpid
   </i>
   and
   <i>
    Getppid
   </i>
   system calls.
  </p>
  <p>
   When a process executes the
   <i>
    Wait
   </i>
   system call, its execution is suspended till the
                        process whose PID is given as argument to
   <i>
    Wait
   </i>
   terminates or executes the
   <i>
    Signal
   </i>
   system call. The process that enters
   <i>
    Wait
   </i>
   sets its state to WAIT_PROCESS and invokes the
                        scheduler.
  </p>
  <p>
   A process executes the
   <i>
    Signal
   </i>
   system call to wake up all the processes waiting for it.
                        If a process terminates without invoking
   <i>
    Signal
   </i>
   , then
   <i>
    Exit
   </i>
   system call
                        voluntarily wakes up all the processes waiting for it.
  </p>
  <p>
   When several processes running concurrently share a resource (shared memory or file) it is
                        necessary to synchronize access to the shared resource to avoid data inconsistency.
   <i>
    Wait
   </i>
   and
   <i>
    Signal
   </i>
   form one pair of primitives that help to achieve synchronization. In general,
                        synchronization primitives help two co-operating processes to ensure that one process stops
                        execution at certain program point, and waits for the other to issue a signal, before
                        continuing execution.
  </p>
  <p>
   To understand how
   <i>
    Wait
   </i>
   and
   <i>
    Signal
   </i>
   help for process synchronization, assume that
                        two processes (say A and B) executing concurrently share a resource. When process A issues the
   <i>
    Wait
   </i>
   system call with the PID of process B, it intends to wait until process B signals
                        or terminates. When process B is done with the resource, it can invoke the
   <i>
    Signal
   </i>
   system
                        call to wake up process A (and all other processes waiting for process B). Thus,
   <i>
    Signal
   </i>
   and
   <i>
    Wait
   </i>
   can ensure that process A is allowed to access the resource only after process
                        B permits process A to do so.
  </p>
  <p>
   In the above example suppose process B had finished using the shared resource and had executed
   <i>
    Signal
   </i>
   system call before process A executed
   <i>
    Wait
   </i>
   system call, then process A
                        will wait for process B to issue another signal. Hence if process B does not issue another
                        signal, then process A will resume execution only after process B terminates. The issue here is
                        that, although the OS acts on the occurance of a signal immediately, it never records the
                        occurance of the signal for the future.
   <b>
    In other words, Signals are memoryless.
   </b>
   A more
                        advanced synchronization primitive that has a state variable associated with it - namely the
   <a href="https://en.wikipedia.org/wiki/Semaphore_(programming)" target="_blank">
    semaphore
   </a>
   -
                        will be added to the OS in the next stage.
  </p>
  <p>
   When a process issues the
   <i>
    Exit
   </i>
   system call, all processes waiting for it must be
                        awakened. We will modify the
   <b>
    Exit Process
   </b>
   function in the
   <a href="os_modules/Module_1.html" target="_blank">
    process manager module
   </a>
   to wake up all processes waiting for the
                        terminating process. However, there is one special case to handle here. The Exit Process
                        function is invoked by the
   <i>
    Exec
   </i>
   system call as well. In this case, the process waiting
                        for the current process must not be woken up (why?). The implementation details will be
                        explained below.
  </p>
  <p>
   Finally, when a process Exits, all its child processes
                        become
   <a href="https://en.wikipedia.org/wiki/Orphan_process" target="_blank">
    orphan processes
   </a>
   and their PPID field is set to -1 in the module function
   <b>
    Exit Process
   </b>
   . Here too, if Exit
                        Process in invoked from the
   <i>
    Exec
   </i>
   system call, the children must not become orphans.
  </p>
  <br/>
  <b>
   Shell Program
  </b>
  <br/>
  <br/>
  <p>
   The Shell is a user program that implements an interactive user interface for the OS. In the
                        present stage, we will run the shell as the INIT program, so that the shell will interact with
                        the user.
  </p>
  <p>
   The shell asks you to enter a string (called a
   <i>
    command
   </i>
   ). If the string entered is
                        "Shutdown", the program executes the
   <i>
    Shutdown
   </i>
   system call to halt the OS. Otherwise, the
                        shell program forks and create a child process. The parent process then waits for the child to
                        exit using the
   <i>
    Wait
   </i>
   system call. The child process will try to execute the
   <i>
    command
   </i>
   (that is, execute the file with name
   <i>
    command
   </i>
   .) If no such file exists,
   <i>
    Exec
   </i>
   fails
                        and the child prints "BAD COMMAND" and exits. Otherwise, the
   <i>
    command
   </i>
   file will be
                        executed. In either case, upon completion of the child process, the parent process wakes up.
                        The parent then goes on to ask the user for the next
   <i>
    command
   </i>
   .
  </p>
  <br/>
  <b style="font-size: 20px">
   Implementation of Interrupt routine 11
  </b>
  <br/>
  <br/>
  <p>
   The system calls
   <i>
    Wait
   </i>
   ,
   <i>
    Signal
   </i>
   ,
   <i>
    Getpid
   </i>
   and
   <i>
    Getppid
   </i>
   are all
                        implemented in the interrupt routine 11. Each system call has a different system call number.
  </p>
  <ul style="list-style-type: disc; margin-left: 10px;">
   <li style="padding-left: 20px">
    At the beginning of interrupt routine 11, extract the system
                          call number from the user stack and switch to the kernel stack.
   </li>
   <li style="padding-left: 20px">
    Implement system calls according to the system call number
                          extracted from above step. Steps to implement each system call are explained below.
   </li>
   <li style="padding-left: 20px">
    Change back to the user stack and return to the user mode.
   </li>
  </ul>
  <p>
   The system call numbers for
   <i>
    Getpid
   </i>
   ,
   <i>
    Getppid
   </i>
   ,
   <i>
    Wait
   </i>
   and
   <i>
    Signal
   </i>
   are
                        11, 12, 13 and 14 respectively. From ExpL program, these system calls are invoked using
   <a href="os_spec-files/dynamicmemoryroutines.html" target="_blank">
    exposcall function
   </a>
   .
  </p>
  <br/>
  <b>
   Wait System Call
  </b>
  <br/>
  <br/>
  <p>
   <i>
    Wait
   </i>
   system call takes PID of a process (for which the given process will wait) as an
                        argument.
  </p>
  <ul style="list-style-type: disc; margin-left: 10px; ">
   <li style="padding-left: 20px">
    Change the MODE FLAG in the
    <a href="os_design-files/process_table.html" target="_blank">
     process table
    </a>
    to the system call number.
   </li>
   <li style="padding-left: 20px">
    Extract the PID from the user stack. Check the valid conditions
                          for argument. A process should not wait for itself or a TERMINATED process. The argument PID
                          should be in valid range (what is the
    <a href="os_design-files/process_table.html" target="_blank">
     valid
                            range
    </a>
    ?). If any of the above conditons are not satisfying, return to the user mode with
                          -1 stored as return value indicating failure. At any point of return to user, remember to
                          reset the MODE FLAG and change the stack to user stack.
   </li>
   <li style="padding-left: 20px">
    If all valid conditions are satisfied then proceed as follows.
                          Change the state of the current process from RUNNING to the tuple
    <a href="os_design-files/process_table.html#state" target="_blank">
     (WAIT_PROCESS, argument PID)
    </a>
    in the process table. Note that the STATE
                          field in the process table is a tuple (allocated 2 words).
   </li>
   <li style="padding-left: 20px">
    Invoke the scheduler to schedule other processes.
   </li>
   <p style="padding-left: 20px;text-indent: 0px;">
    /*The following step is executed only when the
                          scheduler runs this process again, which in turn happens only when the state of the process
                          becomes READY again.*/
   </p>
   <li style="padding-left: 20px">
    Reset the MODE FLAG in the process table of the current process.
                          Store 0 in the user stack as return value and return to the calling program.
    <br/>
   </li>
  </ul>
  <br/>
  <b>
   Signal System Call
  </b>
  <br/>
  <br/>
  <p>
   <i>
    Signal
   </i>
   system call does not have any arguments.
  </p>
  <ul style="list-style-type: disc; margin-left: 10px; ">
   <li style="padding-left: 20px">
    Set the MODE FLAG in the process table to the signal system
                          call number.
   </li>
   <li style="padding-left: 20px">
    Loop through all process table entries, if there is a process
                          with STATE as tuple (WAIT_PROCESS, current process PID) then change the STATE field to READY.
   </li>
   <li style="padding-left: 20px">
    Reset the MODE FLAG to 0 in the process table and store 0 as
                          return value in the user stack.
   </li>
   <br/>
   <b>
    Getpid and Getppid System Calls
   </b>
   <br/>
   <br/>
   <p>
    <i>
     Getpid
    </i>
    and
    <i>
     Getppid
    </i>
    system calls returns the PID of the current process and the
                          PID of the parent process of the current process respectively to the user program. Implement
                          both these system calls in interrupt routine 11.
   </p>
   <p>
    <code>
     Note :
    </code>
    The system calls implemented above are final and will not change later.
                          See algorithms for
    <a href="os_design-files/synchronization_algos.html" target="_blank">
     Wait/Signal
    </a>
    and
    <a href="os_design-files/proc_misc.html" target="_blank">
     Getpid/Getppid
    </a>
    .
   </p>
   <br/>
   <b>
    Modifications to Exit Process Function (function number = 3,
    <a href="os_modules/Module_1.html" target="_blank">
     Process Manager Module
    </a>
    )
   </b>
   <br/>
   <br/>
   <p>
    Exit Process function is modified so that it wakes up all the processes waiting for the
                          current process. Similarly, the children of the process are set as orphan processes by
                          changing PPID field of child processes to -1. But when the Exit Process function is invoked
                          from
    <i>
     Exec
    </i>
    system call, the process is actually not terminating as the new program is
                          being overlayed in the same address space and is executed with the same PID.
                          when Exit Process is invoked from
    <i>
     Exec
    </i>
    system call, it should not wake up the
                          processes waiting for the current process and also should not set the children as orphan
                          processes. Check the MODE FLAG in the process table of the current process to find out from
                          which system call Exit Process function is invoked.
   </p>
   <ul style="list-style-type: disc; margin-left: 10px; ">
    <p style="text-indent: 0px">
     If MODE FLAG field in the
     <a href="os_design-files/process_table.html" target="_blank">
      process table
     </a>
     has system call number not equal to 9 (
     <i>
      Exec
     </i>
     )
                            implement below steps.
    </p>
    <li style="padding-left:20px">
     Loop through the process table of all processes and change the state to READY for the
                            processes whose state is tuple (WAIT_PROCESS, current PID). Also if the PPID of a process
                            is PID of current process, then invalidate PPID field to -1.
    </li>
    <p>
     <code>
      Note :
     </code>
     The function implemented above is final and will not change later.
    </p>
    <br/>
   </ul>
   <b>
    Shutdown system call
   </b>
   <br/>
   <br/>
   <p>
    To ensure graceful termination of the system we will write
    <i>
     Shutdown
    </i>
    system call with
                          just a HALT instruction.
    <i>
     Shutdown
    </i>
    system call is implemented in interrupt routine 15.
                          Create an xsm file with just the HALT instruction and load this file as interrupt routine 15.
                          From this stage onwards, we will use a new version of Shell as our init program. This Shell
                          version will invoke
    <i>
     Shutdown
    </i>
    system call to halt the system.
   </p>
   <p>
    In later stages, when a file system is added to the OS, the file system data will be loaded
                          to the memory and modified, while the OS is running. The
    <i>
     Shutdown
    </i>
    system call will be
                          re-written so that it commits the changes to the file system data to the disk before the
                          machine halts.
   </p>
   <br/>
   <b>
    Modifications to boot module
   </b>
   <br/>
   <br/>
   <p>
    Load interrupt routine 11 and interrupt routine 15 from disk to memory. See disk and memory
                          organization
    <a href="os_implementation.html" target="_blank">
     here
    </a>
    .
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
   <div class="container col-md-12">
    <div class="section_area">
     <ul class="list-group">
      <li class="list-group-item">
       <a data-toggle="collapse" href="#collapseq19">
        <b>
         Q1.
        </b>
        Does the eXpOS guarantees that
                                  two processes will not wait for each other i.e. circular wait will not happen?
       </a>
       <div class="panel-collapse collapse" id="collapseq19">
        No. The present eXpOS does not provide any functionality to avoid circular wait. It
                                  is the responsiblity of the user program to make sure that such conditions will not
                                  occur.
       </div>
      </li>
     </ul>
    </div>
   </div>
   <b style="color:#26A65B">
    Assignment 1:
   </b>
   <b>
    [Shell Version-II]
   </b>
   It is recommended to
                        implement the shell program according to the description given earlier on your own. One
                        implementation of shell program is given
   <a href="test_prog.html#shell_version_2_p" target="_blank">
    here
   </a>
   .
                        Load this program as the INIT program. Test the shell version by giving different ExpL programs
                        written in previous stages. Remember to load the xsm files of ExpL programs as executables into
                        the disk before trying to execute them using shell.
   <br/>
   <br/>
   <!--<b style="color:#26A65B">Assignment 2: </b>Modify <a href="test_prog.html#ll_fork" target="_blank">the program</a> given in assignment-2 of previous stage to use <i>Wait</i> and <i>Signal</i> system calls to synchronize the order of printing the numbers. The program given creates linked list of the first 100 numbers. The program then forks to create a child so that the parent and the child has separate pointers to the head of the shared linked list.  Now, the child prints the  1st, 3rd, 5th, 7th... etc. entries of the list whereas the parent prints the 2nd, 4th, 6th, 8th....etc. entries of the list. Modify the program to invoke <i>Wait</i> system call from parent with PID of child process before printing a number and child to invoke <i>Signal</i> system call after child prints an entry. Usage of <i>Wait</i> and <i>Signal</i> system calls make sure that numbers are printed in sequential order. Run this program using the shell.
   <br><br>
-->
   <b style="color:#26A65B">
    Assignment 2:
   </b>
   Write an ExpL program 'pid.expl' which invokes
   <i>
    Getpid
   </i>
   system call and prints the pid. Write another ExpL program which invokes
   <i>
    Fork
   </i>
   system
                        call three times back to back. Then, the program shall use
   <i>
    Exec
   </i>
   system call to execute
                        pid.xsm file. Run this program using the shell.
   <br/>
   <br/>
   <a data-toggle="collapse" href="#collapse21">
    <span class="fa fa-times">
    </span>
    Close
   </a>
  </ul>
 </div>
</div>
