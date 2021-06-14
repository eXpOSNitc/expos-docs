---
title: 'Stage 12 :
                        Introduction to Multiprogramming (4 Hours)'
---
<div class="panel-collapse collapse" id="collapse12">
 <div class="panel-body">
  <!-- Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo12">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo12">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Familiarise with the idle process.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Program the timer interrupt handler to concurrently schedule two processes.
        </li>
       </ul>
      </div>
     </li>
    </ul>
   </div>
  </div>
  <!-- End Learning Objectives-->
  <p>
   This stage introduces you to multi-programming. You will load two processes
                        into memory during OS bootstrap and put them on concurrent execution.
                        For this, you need to modify the timer interrupt
                        handler to switch between the two processes.
  </p>
  <p>
   We will use the the same init process as in stage 11. A second process called
                        an
   <a href="os_spec-files/processmodel.html" target="_blank">
    <b>
     idle process
    </b>
   </a>
   will also
                        be set up in memory
                        for execution during OS startup.
                        The idle process simply contains an infinite loop.
  </p>
  <p>
   You will modify the timer to implement a very primitive scheduler which shares
                        the machine between the two processes. More detailed implementation of the OS
                        scheduler will be taken up in later stages.
  </p>
  <b>
   Idle Program
  </b>
  <br/>
  <br/>
  <p>
   Idle is a user program which is loaded for execution during OS bootstrap.
                        Before OS bootstrap, it must be stored in the disk blocks 11 and 12.
                        The OS bootstrap loader must load this program to memory pages 69 and 70 (See
   <a href="os_implementation.html" target="_blank">
    eXpOS Disk and Memory layout
   </a>
   for details).
                        The Page Table and Process Table for the idle process must be set up by the bootstrap loader.
                        The PID of the idle process is fixed to be 0.
  </p>
  Idle program runs an infinite loop. The algorithm for the idle is as follows.
  <div>
   <pre>while(1) do
endwhile</pre>
  </div>
  <br/>
  An ExpL program for idle process is given below.
  <div>
   <pre>int main()
{
	decl
		int a;
	enddecl
	begin
		while(1==1) do
			a=1;
		endwhile;
		return 0;
	end
}
</pre>
  </div>
  Compile the above code and load it into disk blocks 11 and 12 before system startup, using the
                      command.
  <div>
   <pre>load --idle &lt;...path to idle...&gt;</pre>
  </div>
  <br/>
  <br/>
  <b>
   Modifications to OS Startup Code
  </b>
  <br/>
  <br/>
  <p>
   The eXpOS assigns each process a unique process ID (PID). The
   <a href="os_spec-files/processmodel.html" target="_blank">
    eXpOS design
   </a>
   stipulates that the
                        PID of idle process is 0.
                        INIT program is assigned PID 1. Our implementation plan in this road map is to store the
                        process
                        table entry for the process with
                        ID=0 in the 16 words starting at memory address PROCESS_TABLE, the process table entry for
                        process with PID=1 in 16 words starting at memory address PROCESS_TABLE+16 and so on.
                        Similarly,
                        the page table for the process with PID=0 will be
                        stored in 20 words starting at address PAGE_TABLE_BASE, page table for PID=1 will start at
                        PAGE_TABLE_BASE+20 and so on. The
   <a href="os_implementation.html" target="_blank">
    memory
                          layout design
   </a>
   permits space for process/page table
                        entries for a maximum of 16 processes. Thus, the OS can run at most 16 processes
                        concurrently.
  </p>
  <p>
   At present, we will run just two processes - the idle process with PID=0 and the init process
                        with PID=1.
                        Since there are two processes, we need to set up several data structures so that the operating
                        system is able to
                        keep track of the state of each process while in execution. The steps are described below.
  </p>
  <ol style="list-style-type:decimal;margin-left:2px;">
   <li>
    Load the idle code from disk to memory.
    <div>
     <pre>loadi(69,11);
loadi(70,12);</pre>
    </div>
   </li>
   <li>
    Set the page table entries for idle process. As idle process does not use library functions
                          or
                          dynamic memory allocation, it doesn't need library and heap pages. Therefore, you need to set
                          up
                          entries for only the code and stack pages. As memory requirements of idle are very low,
                          we need to allocate only one physical page for stack.


                          We will allocate page 81 for stack as pages
                          76-80 will be used by the init process.
    <br/>
    <br/>
    <div>
     <pre>PTBR=PAGE_TABLE_BASE;  //as PID of idle process is 0

//Library
[PTBR+0] = -1;
[PTBR+1] = "0000";
[PTBR+2] = -1;
[PTBR+3] = "0000";

//Heap
[PTBR+4] = -1;
[PTBR+5] = "0000";
[PTBR+6] = -1;
[PTBR+7] = "0000";

//Code
[PTBR+8] = 69;
[PTBR+9] = "0100";
[PTBR+10] = 70;
[PTBR+11] = "0100";
[PTBR+12] = -1;
[PTBR+13] = "0000";
[PTBR+14] = -1;
[PTBR+15] = "0000";

//Stack
[PTBR+16] = 81;
[PTBR+17] = "0110";
[PTBR+18] = -1;
[PTBR+19] = "0000";</pre>
    </div>
   </li>
   <li>
    We will run the INIT process of stage 11 (to print all numbers
                          below 50) concurrently.

                          Set the Page Table entries for init as done in previous stages with PTBR as
                          PAGE_TABLE_BASE+20.
   </li>
   <li>
    As noted earlier,
    <a href="os_design-files/process_table.html" target="_blank">
     Process
                            Table
    </a>
    entries for idle starts from address PROCESS_TABLE and
                          init from PROCESS_TABLE + 16. Set the PID field in the Process Table entry to 0 for idle
                          and 1 for init.
   </li>
   <li>
    The process being currently scheduled is said to be in
    <a href="support_tools-files/constants.html" target="_blank">
     RUNNING
    </a>
    state.
                          The bootstrap loader will schedule the init process first.
                          Thus, in the OS startup code, set the STATE field in process table entry of the idle process
                          to
    <a href="support_tools-files/constants.html" target="_blank">
     CREATED
    </a>
    and INIT process
                          to
    <a href="support_tools-files/constants.html" target="_blank">
     RUNNING
    </a>
    .
                          The CREATED state indicates that the process had never been scheduled for execution
                          previously. The need for a separate CREATED state will be explained later.
                          Subsequent "re-scheduling" will be done by the timer interrupt handler. According to process
                          table, STATE field occupies 2 words. In case of RUNNING and CREATED states, second word is
                          not required. See
    <a href="os_design-files/process_table.html#state" target="_blank">
     process
                            states
    </a>
    .
   </li>
   <li>
    We will allocate the next free page, 82 as the User Area Page for the idle process.
                          Set the User Area Page number field in the Process Table entry of idle to 82.
   </li>
   <li>
    Set the UPTR field in the Process Table entry for idle
                          to 8*512 which is the logical address of user SP.
                          (The reasoning behind this step was explained in detail in Stage 7).
   </li>
   <li>
    Set the KPTR field of the process table for idle to 0.
   </li>
   <p>
    The User Area Page Number field of a process table entry stores the page number of the user
                          area page allocated
                          to the process. The KPTR field must store the offset of the kernel stack pointer within this
                          page. The UPTR
                          points to the top of the current value of user stack pointer.
   </p>
   <p>
    Some explanation is of the order here. When a process is executing in user mode, the active
                          stack will be
                          the user stack (logical pages 8-9 of the process). When the process switches to kernel mode,
                          the first action by
                          the kernel code will be to save the SP value to UPTR and set the SP register to the physical
                          address of the
                          top of the kernel stack. When a process enters the kernel mode from user mode, the kernel
                          stack will always
                          be empty. Hence, SP must be set to value (User Area Page Number * 512 - 1) whenever kernel
                          mode is entered
                          from the user mode.
   </p>
   <p>
    Similarly, before a process executes IRET instruction and switch from kernel mode to user
                          mode, the SP
                          register must be set to previously stored value in UPTR field of the process table. The
                          kernel stack
                          will be empty when a process returns to user mode as there is no kernel context to be
                          remembered.
   </p>
   <li>
    Set the PTBR field to PAGE_TABLE_BASE and PTLR field to 10 in the Process Table entry of
                          idle process.
   </li>
   <li>
    Set the entry point IP value from the header of idle process to top of the user stack of
                          the idle process as done in the previous stage.
    <div>
     <pre>[81 * 512] = [69*512 + 1];</pre>
    </div>
   </li>
   <p>
    The values of PTBR, PTLR, User Area Page Number, UPTR, KPTR etc. stored in the process table
                          entry for a process
                          will be used to set up the values of the hardware registers just before the process is
                          scheduled for execution.
                          We will not be scheduling the idle process immediately. Hence, the hardware registers will
                          not
                          be set based on the above values now. Instead, we will schedule the INIT process from the OS
                          startup code.
                          Hence your OS startup code must contain code to set up registers to schedule the INIT
                          process, as outlined below:
   </p>
   <li>
    Set User Area Page number, UPTR, KPTR, PTBR and PTLR fields in the Process Table entry for
                          init.
   </li>
   <li>
    Initialise the machine's PTBR and PTLR registers for scheduling the INIT process.
                          (You have alreay gone through the steps in Stage 7).
   </li>
   <li>
    Set the Entry point address for INIT process in the beginning of Stack page of INIT. Also
                          set the SP register accordingly.
   </li>
   <li>
    Set the current PID field in
    <a href="os_design-files/mem_ds.html#ss_table">
     system status
                            table
    </a>
    to 1, as PID for INIT is 1.
   </li>
   <li>
    Transfer control to INIT using ireturn instruction.
   </li>
  </ol>
  <p style="text-indent: 0px">
   <code>
    Note:
   </code>
   You must be clear with
   <a href="Tutorials/xsm_unprivileged_tutorial.html" target="_blank">
    XSM unprivileged mode execution
   </a>
   to understand the description that
                        follows.
  </p>
  <br/>
  <b>
   Modifications to timer interrupt handler
  </b>
  <br/>
  <br/>
  <p>
   In the previous stage you made the timer interrupt display "TIMER" at fixed intervals. However,
                        the actual
                        function of timer interrupt routine is to preempt the current running process and to transfer
                        execution to another
                        ready processes.
  </p>
  <p>
   In this stage, you will write a sample scheduler which will schedule just two processes.
                        The scheduler will be implemented in the timer interrupt handler. After saving the context of
                        the currently executing process in its kernel stack, the scheduler must switch to the kernel
                        stack to that of the next process to be scheduled. The context of the next process has to be
                        loaded to the registers and then control of execution can be transferred to the process.
                        Detailed intructions for scheduling are given below.
  </p>
  <br/>
  <ol style="list-style-type:decimal;margin-left:2px">
   <li>
    Switch from the user stack to kernel stack of the currently executing process and save the
                          register context
                          using the
    <a href="arch_spec-files/instruction_set.html#backup">
     <b>
      backup
     </b>
    </a>
    instruction
                          as done in stage 9.
   </li>
   <li>
    Obtain the PID of currently executing process from
    <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
     System Status Table
    </a>
    .
    <div>
     <pre>alias currentPID R0;
currentPID = [SYSTEM_STATUS_TABLE+1];</pre>
    </div>
   </li>
   <li>
    The Process table entry of the current process can be computed as PROCESS_TABLE +
                          currentPID*16.
                          Save the KPTR, PTBR and PTLR values to the Process Table entry of the current process.
                          Set the state of the process as READY.
    <div>
     <pre>alias process_table_entry R1;
process_table_entry = PROCESS_TABLE + currentPID * 16;

[process_table_entry + 12] = SP % 512;
[process_table_entry + 14] = PTBR;
[process_table_entry + 15] = PTLR;

[process_table_entry + 4] = READY;
</pre>
    </div>
    Note that instead of saving the actual value of KPTR, we are saving KPTR%512. This is because
                          the OS design
                          stipulates that KPTR must contain the offset of the kernel stack pointer within the User Area
                          Page. This is
                          done so as to allow the OS to relocate the User Area Page if necessary.
   </li>
   <li>
    As we have only two processes to schedule, the scheduling algorithm we are going to use
                          will just toggle
                          between the two processes.
    <div>
     <pre>alias newPID R2;
if(currentPID == 0) then
	newPID = 1;
else
	newPID = 0;
endif;</pre>
    </div>
   </li>
   <li>
    Restore the SP, PTBR and PTLR values from the Process Table entry for the new process.
    <div>
     <pre>alias new_process_table R3;
new_process_table = PROCESS_TABLE + newPID * 16;

//Set back Kernel SP, PTBR , PTLR
SP =  [new_process_table + 11] * 512 + [new_process_table + 12] ;
PTBR = [new_process_table + 14];
PTLR = [new_process_table + 15];</pre>
    </div>
   </li>
   <li>
    Set the PID field of the System Status Table as newPID.
    <div>
     <pre>[SYSTEM_STATUS_TABLE + 1] = newPID;
</pre>
    </div>
   </li>
   <li>
    Our scheduler must distinguish between two cases when a process is scheduled for execution.
                          If a process is in CREATED state, the process had never been scheduled for execution earlier.
                          Such a process will have no "history" to remember, and thus no "user context" to be restored
                          before being scheduled. On the other hand, a process in READY state is one which had been in
                          RUNNING state in the past. Such a process will have an associated (saved user context) which
                          the scheduler
                          would have saved in the kernel stack when it was scheduled out earlier. This context
                          has to be restored before the process is scheduled again for correct resumption of execution.
    <br/>
    Check if the newly found process is in CREATED state.
                          If so, set SP to top of its user stack and return to user mode.
    <br/>
    <br/>
    <div>
     <pre>if([new_process_table + 4] == CREATED) then
	[new_process_table + 4] = RUNNING;
	SP = [new_process_table + 13];
	ireturn;
endif;
</pre>
    </div>
    <code>
     Note:
    </code>
    In this stage, the only situation where the timer finds the next process
                          in CREATED state is when
                          the IDLE process is to be scheduled for the first time. Since INIT is scheduled directly from
                          the OS startup code,
                          the INIT process never goes through the CREATED state.
   </li>
   <li>
    Set the state of the newly found process as RUNNING.
    <div>
     <pre>[new_process_table + 4] = RUNNING;</pre>
    </div>
   </li>
   <li>
    Restore the register context of the new process from its kernel stack and change the stack
                          to user stack
                          as done in previous stages. Note that if this is the case, then the process would have been
                          in RUNNING state before.
   </li>
  </ol>
  <br/>
  <b>
   Making Things Work
  </b>
  <br/>
  <br/>
  <ol style="list-style-type:decimal;margin-left:2px">
   <li>
    Compile and load the modified OS statup code and Timer Interrupt handler to XSM disk.
   </li>
   <li>
    Compile and load the idle program into the XSM disk.
   </li>
   <li>
    Run the machine with timer enabled.
   </li>
  </ol>
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq5">
       <b>
        Q1.
       </b>
       What is the significance of the
                                idle process?
      </a>
      <div class="panel-collapse collapse" id="collapseq5">
       The main purpose of the idle process is to run as a background process in an infinite
                                loop.
                                The idle process does nothing except running an infinite loop.
                                This is demanded by the OS so that the scheduler will always have atleast one "READY"
                                process to schedule.
                                It is to be scheduled only when
                                no other process is available for scheduling. However, in this stage we have scheduled
                                idle just like
                                any other process.
      </div>
     </li>
    </ul>
   </div>
  </div>
  <p>
   <b style="color:#26A65B">
    Assignment 1:
   </b>
   Load a program to print numbers from 1-100 as the
                        INIT program, and modify IDLE to print numbers from 101-200. (You will have to link the library
                        to address space of IDLE for the Write function call to work.)
  </p>
  <p>
   <b style="color:#26A65B">
    Assignment 2:
   </b>
   Set two
   <b>
    breakpoints
   </b>
   (see
   <a href="support_tools-files/spl.html" target="_blank">
    SPL breakpoint instruction
   </a>
   ) in the timer interrupt routine, the first one immediately upon entering the timer routine and the second one just before return from the timer routine.  Dump the process table entry and page table entries of current process (see
   <a href="support_tools-files/xsm-simulator.html" target="_blank">
    XSM debugger
   </a>
   for various printing options).
  </p>
  <br/>
  <br/>
  <a data-toggle="collapse" href="#collapse12">
   <span class="fa fa-times">
   </span>
   Close
  </a>
 </div>
</div>
