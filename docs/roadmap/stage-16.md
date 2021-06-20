---
title: 'Stage 16 : Console Input (6 Hours)'
---

!!! note "Learning Objectives"
    - Familiarise with the Console Interrupt handling in XSM.
    - Implementation of console input using the read system call.
    - Introduction to input buffer.

!!! note "Pre-requisite Reading"
    Read and understand the <a href="Tutorials/xsm_interrupts_tutorial.html#disk_and_console_interrupts" target="_blank">
    XSM tutorial on Interrupts and Exception handling</a> before proceeding further. (Read only the console and disk interrupt part.)

In this stage, we will introduce you to XSM console interrupt handling. A process must use the
<a href="arch_spec-files/instruction_set.html">XSM instruction IN</a> to <b>read data from the console into the input </b>
<a href="arch_spec-files/machine_organisation.html" target="_blank">port P0</a>.
IN is a privileged instruction and can be executed only inside a system call/module.
Hence, to read data from the console, a user process invokes the <a href="os_spec-files/systemcallinterface.html" target="_blank">
read system call </a>. The read system call invokes the Terminal Read function present in <a href="os_modules/Module_4.html" target="_blank">
Device Manager module</a> (Module 4). The IN instruction will be executed within this Terminal Read function.

The most important fact about the <b> IN instruction is that it will not wait for the data to arrive in P0</b>.
Instead, the XSM machine continues advancing the instruction pointer and executing the next instruction.
Hence there must be some hardware mechanism provided by XSM to detect arrival of data in P0.

When does data arrive in P0? This happens when some string/number is entered from the key-board and ENTER is pressed. At this time,
<b>the XSM machine will raise the console interrupt</b>. Thus the console interrupt is the hardware mechanism that helps the OS to
infer that the execution of the IN instruction is complete.

As noted above, the IN instruction is typically executed from the Terminal Read function.
Since it is not useful for the process that invoked the Terminal Read function to continue
execution till data arrives in P0, **a process executing the IN instruction will sets its state to WAIT_TERMINAL and invoke the scheduler**. The process must resume execution only after the XSM machine sends an interrupt upon data arrival.


When the console interrupt occurs, the machine interrupts the current process (note that some
other process would be running) and executes the console interrupt handler. (The interrupt
mechanism is similar to the timer interrupt. The current value of IP+2 is pushed into the stack
and control transfers to the interrupt handler - see <a href="Tutorials/xsm_interrupts_tutorial.html#disk_and_console_interrupts" target="_blank"> XSM machine execution tutorial </a> for details).It is the responsiblity of the
<b>console interrupt handler to transfer the data arrived in port P0 to the process which is waiting for the data</b>.
This is done by copying the value present in port P0 into the <b>input buffer</b> field of the <a href="os_design-files/process_table.html" target="_blank">process table</a> entry of the process which has requested for the input.
<b>Console interrupt handler also wakes up the process in WAIT_TERMINAL by setting its state to READY</b>.
(Other processes in WAIT_TERMINAL state are also set to READY by the console interrupt handler.)


Each process maintains an input buffer which stores the last data read by the process from the
console. On the occurance of a terminal interrupt, the interrupt handler uses the PID field of
the terminal status table to identify the correct process that had acquired the terminal for a
read operation. The handler transfer the data from the input port to the input buffer of the
process.

User programs can invoke the read system call using the library interface. For a terminal
read, the file descriptor (-1 for terminal input) is passed as the first argument. The second
argument is a variable to store number/string from console. Refer to the read system call
calling convention <a href="os_spec-files/dynamicmemoryroutines.html" target="_blank">
here</a>.ExpL library converts exposcall to 
<a href="os_design-files/Sw_interface.html" target="_blank"> low level system call interface</a>
for read system call, to invoke interrupt 6.

The read system call (Interrupt 6) invokes the <b>Terminal Read</b> function present in the
<a href="os_modules/Module_4.html" target="_blank">Device manager Module</a>.
Reading from the terminal and storing the number/string (read from console) in the address provided is done by
the Terminal Read function. Function number for the Terminal Read function, current PID and
address where the word has to be stored are sent as arguments through registers R1, R2 and R3
respectively. After coming back from Terminal Read function, it is expected that the word
address (passed as argument to read system call) contains the number/string entered in the
terminal.   

The OS maintains a global data structure called the <a href="os_design-files/mem_ds.html#ts_table">
terminal status table </a> that stores information about the current state of the terminal. A process
can acquire the terminal by invoking the Acquire Terminal function of the
<a href="os_modules/Module_0.html"> resource manager module</a>.
<b>When the Acquire Terminal function assigns the terminal to a process,
it enters the PID of the process into the PID field of the terminal status table</b>.
The Terminal Read function must perform the following 1) Acquire the terminal 2) Issue an IN
instruction (SPL read statement translates to XSM instruction IN) 3) Set its state as
WAIT_TERMINAL 4) Invoke the scheduler and 5) After console interrupt wakes up this process,
transfer data present in the input buffer field of the process table into the word address
(passed as an argument).

<!--
When the data finally arrives, <b>the console interrupt handler must transfer the data (in port P0) into the input buffer of the process</b> in the <a href="os_design-files/process_table.html" target="_blank">process table</a>. Then the handler wakes up process waiting for the terminal.
Finally, the read system call, after waking up from the WAIT_TERMINAL state, returns the input data in the buffer and passes this data to the user program that invoked the system call. 
-->
Read about <a href="Tutorials/xsm_interrupts_tutorial.html" target="_blank"> XSM interrupts </a>
before proceeding further.

<figure style="text-align: center;">
    <img src="https://exposnitc.github.io/img/roadmap/read.png"/>
    <figcaption>Control flow for <i>Read</i> system call</figcaption>
</figure>

#### Implementation of read system call (interrupt 6 routine)

1) Set the MODE FLAG in the process table of the current process to the system call number
                        which is 7 for read system call.

2) Save the value of register SP as userSP.
```
alias userSP R0;
userSP=SP;
```

3) Store the value of register SP in the UPTR field of the <a href="os_design-files/process_table.html" target="_blank">process table</a>
entry of the current process.

4) Initialize SP (kernel stack pointer) to (user area page number)*512 -1.

5) Retrieve the file descriptor from the user stack, stored at userSP-4.

6) If the file descriptor is not -1

   1. Store -1 as the return value in the user stack (at position userSP-1).

7) If the file descriptor is -1, implement below steps.

   1. Retrieve the word address sent as an argument from the user stack (userSP-3).
   2. Push all the registers used till now in this interrupt.
   3. Save the function number of the Terminal Read function in the register R1. Save PID of the current process and the word address obtained above in registers R2 and R3 respectively.
   4. Call device manager module. (There is no return value for terminal Read.)
   5. Restore the registers.
   6. Store 0 as return value in the user stack indicating success.

8) Reset the MODE FLAG in the process table to 0.

9)  Change SP back to user stack and return to the user mode.


#### Modification to Device manager Module

In previous stage we implemented Terminal Write function in module 4, now we will add Terminal Read function.

1) If function number in R1 corresponds to Terminal Read, then implement below steps.

Calling Acquire Terminal function :-

2) Push all the registers used till now using multipush.

3) Initialize registers R1, R2 with function number of Acquire Terminal and PID of current process respectively.

4) Call resource manager module.

5) Restore the registers using the multipop statement.

6) Use read statement, for requesting to read from the terminal.
```
read;
```

7) Change the state of the current process to WAIT_TERMINAL.

Invoking the Context Switch Module :-

8) Push all the registers used till now.

9) Invoke the scheduler.

Following steps are executed after return from the scheduler

10) Restore the registers using the multipop statement.

11) The logical address of the word where the data has to be stored is in R3. Convert this logical address to physical address.

12) Store the value present in input buffer field of process table to the obtained physical address of the word. 

13) Return to the caller.


#### Implementation of <a href="os_design-files/term_handler.html" target="_blank">Console Interrupt Handler</a>

>  The console interrupt handler is entered while some other process is executing in the user mode. The handler must switch to the kernel stack of that process, do the interrupt handling, restore the user stack of the process that was running and return control back to the process 

1) Store the SP value in the UPTR field in the process table entry of the currently running process.

2) Initialize SP (kernel stack pointer) to (user area page number)*512 -1. //Switch to the kernel stack.

3) Backup the user context of the currently running process in the kernel stack as done in timer interrupt routine.

4) Get the PID of the process that has aqcuired the terminal from the <a href="os_design-files/mem_ds.html#ts_table" target="_blank">terminal status table</a>, Save this as reqPID.

5) Using the reqPID obtained in the above step, get the corresponding process table entry.

6) The input entered in the console is saved in port P0 by the XSM machine. Copy the value present in P0 into the input buffer field of the process table entry obtained in the above step.

/*next release the terminal */

7) Push the registers used in this interrupt.

8) Initialize register R1 with function number for release terminal, R2 with reqPID (The current process did not acquire the terminal. The process with reqPID as PID is holding the terminal.)

9) Call resource manager module.

10) Ignore the return value and restore the registers pushed before.

11) Restore the user context from the kernel stack as done in the timer interrupt routine.

12) Change SP to UPTR field from the process table entry of the currently running process and return to the user mode. //Switch back to us    er stack

#### Modification to Boot Module

1. Load console interrupt handler and interrupt 6 from disk to memory.
2. Remove the initialization of the third process, as we will run only idle and init processes in this stage.

#### Making things work
1. Compile and load boot module code, console interrupt and interrupt 6 using XFS interface.
2. Write an ExpL program which reads two numbers from console and finds the GCD using Euclidean's algorithm and print the GCD. Load this program as init program.

??? question "Q1. Is it possible that, the running process interrupted by the console interrupt be the same process that had acquired the terminal for reading?"
    No, The process which has acquired the terminal will be in WAIT_TERMINAL state after
    issuing a terminal read until the console interrupt occurs. Hence, this process will
    not be scheduled until console interrupt changes it's state to READY.

!!! assignment "Assignment 1"
    Write an ExpL program to read N numbers in an array,
    sort using bubble sort and print the sorted array to the terminal. Load this program as init
    program and run the machine.

!!! assignment "Assignment 2"
    Use the <a href="support_tools-files/xsm-simulator.html" target="_blank">XSM debugger</a> to print out the contents of the Terminal Status Table and the input buffer (by dumping process table entry of the process to which read was performed) before and after reading data from the input port to the input buffer of the process, inside the terminal interrupt handler.

