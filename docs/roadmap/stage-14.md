---
title: 'Stage 14 : Round robin scheduler (4 Hours)'
original_url: https://exposnitc.github.io/Roadmap.html
---
!!! info "Learning Objectives"
    Implement a preliminary version of the Round Robin scheduling algorithm as an eXpOS module.

Multiprogramming refers to running more than one process simultaneously.
In this stage, you will implement an initial version of the 
<a href="https://en.wikipedia.org/wiki/Round-robin_scheduling" target="_blank">Round Robin scheduler</a>
used in eXpOS. You will hand create another user process (apart from idle and init) and schedule its execution using the timer interrupt.

1) Write an ExpL program to print the odd numbers from 1-100. Load this odd program as init.
```
load --init <path to odd.xsm>;
```
Using the `--exec` option of XFS interface, you can load an executable program into the XFS
disk. XFS interface will load the executable into the disk and create
<a href="os_design-files/disk_ds.html#inode_table" target="_blank">Inode table</a>
entry for the file. XFS interface will also create a <a href="os_design-files/disk_ds.html#root_file" target="_blank">
root entry</a> for the loaded file. From the Inode Table Entry, 
you will be able to find out the disk blocks where the contents of the file are loaded by XFS
interface. Recall that these were discussed in detail in Stage 2 : <a href="#collapse2" target="_blank">Understanding the File System</a>)

2) Write an ExpL program to print the even numbers from 1-100. Load this even program as an
executable.
```
load --exec <path to even.xsm>;
```
Dump the
<a href="os_design-files/disk_ds.html#inode_table" target="_blank">inode table</a>using
<i>dump --inodeusertable</i> command in xfs-interface. Check the disk address of code blocks of even.xsm.

#### Modifications to the boot module code

1) Load the code pages of the even program from disk to memory.

2) Set the <a href="os_design-files/process_table.html">Process Table</a> entry and
<a href="os_design-files/process_table.html#per_page_table">PageTable</a>
entries for setting up a process for the even program. You should set up the PTBR, PTLR, UPTR, KPTR, 
User Area Page Number etc. and also initialize the process state as CREATED in the process
table entry for the even process. Set the PID field in the process table entry to 2.

*Make sure that you do not allot memory pages that are already allotted to some other
process or reserved for the operating system.*

3) Set the starting IP of the new process on top of its user stack.

4) We will implement the scheduler as a seperate module that can be invoked from the timer ISR
(Interrupt Service Routine).
<!--Such stand alone subroutines are implemented as <a href="os_modules/Module_Design.html" target="_blank"> kernel modules </a> in eXpOS.-->
The eXpOS design stipulates that the scheduler is implemented as MODULE_5, and loaded in
<a href="os_implementation.html" target="_blank"> disk blocks </a> 63 and 64 of the
XFS disk. The boot module must load this module from disk to <a href="os_implementation.html" target="_blank">
memory pages</a> 50 and 51. (We will take up the implementation of the module soon below).
```
loadi(50,63);
loadi(51,64);
```

5) First 3 process table entries are occupied. Initialize STATE field of all other process
table entries to TERMINATED. This will be useful while finding the next process to schedule
using round robin scheduling algorithm. Note that when the STATE field in the process table
entry is marked as TERMINATED, this indicates that the process table entry is free for
allocation to new processes.

#### Modifications to Timer Interrupt Routine

As we are going to write the scheduler code as a separate module (MOD_5), we will modify the
timer interrupt routine so that it calls that module.

When the timer ISR calls the scheduler, the active kernel stack will be that of the currently
RUNNING process. The scheduler assumes that the timer handler would have saved the user context of the
current process (values of R0-R19 and BP registers) into the kernel stack before the call. 
It also assumes that the state of the process has been changed to READY.However, the machine's 
SP register will still point to the top of the kernel stack of the currently running process at
the time of the call.

The scheduler first saves the values of the registers SP, PTBR and PTLR to the process table
entry of the current process. Next, it must decide which process to run next. This is done using the
<a href="https://en.wikipedia.org/wiki/Round-robin_scheduling" target="_blank">Round Robin Scheduling
algorithm</a>. Having decided on the new process, the scheduler loads new values into SP,
PTBR and PTLR registers from the process table entry of the new process. It also updates the system status table to
store PID of new process. If the state of the new process is READY, then the scheduler
changes the state to RUNNING. Now, the scheduler returns using the return instruction.

!!! note ""
    The control flow at this point is tricky and must be carefully understood. The key point
    to note here is that although the scheduler module was called by one process
    (from the timer ISR), since the stack was changed inside the scheduler, 
    **the return is to a program instruction in some other process! (determined by the value on top of the kernel stack of the newly
    scheduled process)**.
    
    The return is to that instruction which immediately follows the *call scheduler*
    instruction in the newly selected process. (why? - ensure that you understand this point clearly.) 
    An exception to this rule happens only when the newly selected process to be scheduled is in the CREATED
    state.

    Here, the process was never run and hence there is no return address in the kernel stack.
    Hence, the scheduler directly kick-starts execution of the process by initiating user mode
    execution of the process (using the ireturn instruction). The design of eXpOS
    guarantees that a process can invoke the scheduler module only from the kernel mode.
    Consequently, the return address will be always stored on top of the kernel stack of the
    process.
    
    The round robin scheduling algorithm generally schedules the "next process" in the process
    table that is in CREATED/READY state. (There are exceptions to this rule, which we will
    encounter in later stages.) Moreover, in the present stage, a process will invoke the
    scheduler only from the timer interrupt. We will see other situations in later stages.


As noted above, the timer resumes execution from the return address stored on the top of the
kernel stack of the new process. The timer will restore the user context of the new process
from the stack and return to the user mode, resulting in the new process being executed.

If the scheduler finds that the new process is in state CREATED and not
READY, then as noted above, the timer ISR would not have set
any return address in its kernel stack previously. In this case,
the scheduler will set the state of the process to RUNNING
and initialize machine registers PTLR and PTBR. Now, the scheduler proceeds to run the process
in user mode.Hence, SP is set to the top of the user stack. The scheduler then
starts the execution of the new process by transferring control to user mode using the IRET
instruction.

The scheduler expects that when a process is in the CREATED state, the following
values have been already set in the process table. (In the present stage, the OS
startup code/Boot module is responsible for setting up these values.)


1. The state of the process has been set to CREATED.
2. The UPTR field of the process table entry has been set to the top of the user stack (and
the stack-top contains the address of the instruction to be fetched next when the process is
run in the user mode).
3. PTBR, PTLR, User Area Page Number and KPTR fields in the process table entry has been set
up.

**It is absolutely necessary to be clear about <a href="os_design-files/stack_module.html" target="_blank">
Kernel Stack Management during Module calls </a> and <a href="os_design-files/timer_stack_management.html" target="_blank">
Kernel Stack Management during Context Switch</a> before proceeding further.**

Modify the timer interrupt routine as explained above using the algorithm given
<a href="os_design-files/timer.html" target="_blank">here</a>.
(Ignore the part relating to the swapping operation as it will be dealt in a later stage.)

#### Context Switch Module (Scheduler Module)

The scheduler module (module 5) saves the values of SP, PTBR and PTLR registers of the current
process in its process table entry. It finds a new process to schedule which is in READY or
CREATED state and has a valid PID (PID not equal to -1). Initialize the registers SP, PTBR,
PTLR according to the values present in the process table entry of the new process selected for
scheduling. Also update the System status table.

Write an SPL program for the scheduler module (module 5) as given below:

1. Obtain the PID of the current process from the <a href="os_design-files/mem_ds.html#ss_table" target="_blank"> System Status Table</a>.
2. Push the BP of the current process on top of the kernel stack. (See the box below)
3. Obtain the <a href="os_design-files/process_table.html">Process Table</a> entry corresponding to the current PID.
4. Save SP % 512 in the kernel stack pointer field, also PTBR and PTLR into the corresponding fields in the Process Table entry.
5. Iterate through the Process Table entries, starting from the succeeding entry of the current process to find a process in READY or CREATED state.
6. If no such process can be found, select the idle process as the new process to be scheduled. Save PID of new process to be scheduled as newPID.
7. Obtain User Area Page number and kernel stack pointer value from Process Table entry of the new process and set SP as (User Area Page number) * 512 + (Kernel Stack pointer value).
8. Restore PTBR and PTLR from the corresponding fields in the Process Table entry of the new
process.
9. Set the PID of the new process in the current PID field of the System Status Table.
10. If the new process is in CREATED state, then do the following steps.
    1. Set SP to the value in the UPTR field of the process table entry.
    2. Set state of the newly scheduled process as RUNNING.
    3. Store 0 in the MODE FLAG field in the process table of the process.
    4. Switch to the user mode using the ireturn statement.
11. Set the state of the new process as RUNNING.
12. Restore the BP of the new process from the top of it's kernel stack.
13. Return using return statement.

!!! note 
    In later stages you will modify the scheduler module to the final form given <a href="os_modules/Module_5.html" target="_blank"> here</a>.

!!! note ""
    In the present stage, the scheduler module is called only from the time interrupt handler.
    The timer interrupt handler already contains the instruction to backup the register context
    of the current process. Hence, the scheduler does not have to worry about having to save the
    user register context (including the value of the BP register) of the current process. What
    then is the need for the scheduler to push the BP register?

    The reason is that, in later stages, the scheduler may be called from <a href="os_design.html"><b>kernel modules</b></a>
    other than the timer interrupt routine. Such calls typically happen when an application invokes a
    <a href="os_design.html"><b>system call</b></a>and the system call routine invokes a kernel module which in turn 
    invokes the scheduler. Whenever this is the case, the OS kernel expects that the application saves all the 
    user mode registers <b>except the BP register</b> before making the system call.

    For instance, if the application is written in ExpL and compiled using the ExpL compiler
    given to you, the compiler saves all the user registers<b>except BP</b>
    before making the system call. The ExpL compiler expects that the OS will save the value of the BP register
    before scheduling another application process. This explains why the scheduler needs to save
    the BP register before a context switch.

#### Modifications to INT 10 handler

The ExpL compiler sets every user program to execute the INT 10 instruction (exit system
call) at the end of execution to terminate the process gracefully. In previous stages, we wrote
an INT 10 routine containing just a halt instruction. Hence, if any process invoked INT 10 upon
exit, the machine would halt and no other process would execute further. However, to allow
multiple processes to run till completion, INT 10 must terminate only the process which invoked
it, and schedule other surviving processes. (INT 10 shall set the state of the dying process to
TERMINATED). If all processes except idle are in TERMINATED state, then INT 10 routine can halt
the system.

Write INT 10 program in SPL following below steps :

1. Change the state of the invoking process to <a href="support_tools-files/constants.html">TERMINATED</a>.
2. Find out whether all processes except idle are terminated. In that case, halt the system.Otherwise invoke the scheduler

There will be no return to this process as the scheduler will never schedule this process again.

#### Making things work
1. Compile and load the Boot module code, timer interrupt routine, scheduler module (module 5)
and interrupt 10 routine into disk using XFS interface.
2. Run XSM machine with timer enabled.

??? question "When does the OS kernel invoke the scheduler from some routine other than the timer interrupt handler?"
    In later stages, if a process gets blocked inside a kernel module (waiting for some
    resource), then the process will set its state to "WAITING" and will invoke the
    scheduler. Later when the process is back in READY state (as the resource becomes free)
    and the scheduler selects the process for running, execution returns to the instruction
    following the call to the scheduler in the kernel module.

!!! assignment "Assignment 1"
    Write ExpL programs to print odd numbers, even numbers
    and prime numbers between 1 and 100. Modify the boot module code accordingly and run the machine
    with these 3 processes along with idle process.
