---
title: 'Stage 21 : Process Synchronization (4 Hours)'
original_url: https://exposnitc.github.io/Roadmap.html
---
!!! note "Learning Objectives"
    - Familiarize with process synchronization in eXpOS
    - Implementation of Wait and Signal system calls

!!! abstract "Pre-requisite Reading"
    Read and understand [Access control and synchronization](../os-spec/expos-abstractions.md) and [Process synchronization](../os-spec/synchronization.md#process-synchronization) documentations before proceeding further.

In this stage, we will add support for process synchronization using
<i> Wait</i> and <i>Signal</i>system calls to eXpOS. With the help of these system calls, we will design a more advanced
shell program. We will also implement <i>Getpid </i> and <i>Getppid</i>system calls.

When a process executes the <i>Wait</i> system call, its execution is suspended till the process whose PID is given as argument to
<i>Wait</i>terminates or executes the<i>Signal</i>system call. The process that enters<i>Wait</i>sets its state to WAIT_PROCESS and invokes the
scheduler.

A process executes the <i>Signal</i> system call to wake up all the processes waiting for it.
If a process terminates without invoking <i>Signal</i>, then<i>Exit</i>system call voluntarily 
wakes up all the processes waiting for it.

When several processes running concurrently share a resource (shared memory or file) it is
necessary to synchronize access to the shared resource to avoid data inconsistency.<i>Wait</i>
and <i>Signal</i> form one pair of primitives that help to achieve synchronization. In general,
synchronization primitives help two co-operating processes to ensure that one process stops
execution at certain program point, and waits for the other to issue a signal, before
continuing execution.

To understand how <i>Wait</i> and <i>Signal</i> help for process synchronization, assume that
two processes (say A and B) executing concurrently share a resource. When process A issues the
<i>Wait</i> system call with the PID of process B, it intends to wait until process B signals
or terminates. When process B is done with the resource, it can invoke the
<i>Signal</i> system call to wake up process A (and all other processes waiting for process B). Thus,
<i>Signal</i> and <i>Wait</i> can ensure that process A is allowed to access the resource only after process
B permits process A to do so.

In the above example suppose process B had finished using the shared resource and had executed
<i>Signal</i>system call before process A executed <i>Wait</i> system call, then process A
will wait for process B to issue another signal. Hence if process B does not issue another
signal, then process A will resume execution only after process B terminates. The issue here is
that, although the OS acts on the occurance of a signal immediately, it never records the
occurance of the signal for the future.**In other words, Signals are memoryless.**

A more advanced synchronization primitive that has a state variable associated with it - namely the
[semaphore](https://en.wikipedia.org/wiki/Semaphore_(programming)) - will be 
added to the OS in the next stage.

When a process issues the<i>Exit</i>system call, all processes waiting for it must be awakened. We will modify the
**Exit Process** function in the [process manager module](../modules/module-01.md) 
to wake up all processes waiting for the terminating process. However, there is one special case to handle here. The Exit Process
function is invoked by the<i> Exec</i> system call as well. In this case, the process waiting
for the current process must not be woken up (why?). The implementation details will be explained below.

Finally, when a process Exits, all its child processes become [orphan processes](https://en.wikipedia.org/wiki/Orphan_process) and their PPID field is set to -1 in the module function **Exit Process**. Here too, if Exit
Process in invoked from the <i>Exec</i> system call, the children must not become orphans.

#### Shell Program

The Shell is a user program that implements an interactive user interface for the OS. In the present stage, we will run the shell as the INIT program, so that the shell will interact with the user.

The shell asks you to enter a string (called a command). If the string entered is "Shutdown", the program executes the Shutdown system call to halt the OS. Otherwise, the shell program forks and create a child process. The parent process then waits for the child to exit using the Wait system call. The child process will try to execute the command (that is, execute the file with name command.) If no such file exists, Exec fails and the child prints "BAD COMMAND" and exits. Otherwise, the command file will be executed. In either case, upon completion of the child process, the parent process wakes up. The parent then goes on to ask the user for the next command.

#### Implementation of Interrupt routine 11

The system calls <i>Wait</i> ,<i>Signal</i>,<i>Getpid</i> and <i> Getppid</i> are all
implemented in the interrupt routine 11. Each system call has a different system call number.

- At the beginning of interrupt routine 11, extract the system call number from the user stack and switch to the kernel stack.
- Implement system calls according to the system call number extracted from above step. Steps to implement each system call are explained below.
- Change back to the user stack and return to the user mode.

The system call numbers for Getpid, Getppid, Wait and Signal are 11, 12, 13 and 14 respectively. From ExpL program, these system calls are invoked using [exposcall function](../os-spec/dynamicmemoryroutines.md).

##### Wait System Call

<i>Wait</i> system call takes PID of a process (for which the given process will wait) as an argument.

- Change the MODE FLAG in the [process table](../os-design/process-table.md)to the system call number.
- Extract the PID from the user stack. Check the valid conditions for argument. A process should not wait for itself or a TERMINATED process. The argument PID should be in valid range (what is the [valid range](../os-design/process-table.md)?). If any of the above conditons are not satisfying, return to the user mode with `-1` stored as return value indicating failure. At any point of return to user, remember to reset the MODE FLAG and change the stack to user stack.
- If all valid conditions are satisfied then proceed as follows. Change the state of the current process from RUNNING to the tuple [(WAIT_PROCESS, argument PID)](../os-design/process-table.md) in the process table. Note that the STATE field in the process table is a tuple (allocated 2 words).
- Invoke the scheduler to schedule other processes.
> The following step is executed only when the scheduler runs this process again, which in turn happens only when the state of the process becomes READY again.
- Reset the MODE FLAG in the process table of the current process.
Store 0 in the user stack as return value and return to the calling program.


##### Signal System Call

_Signal_ system call does not have any arguments.

- Set the MODE FLAG in the process table to the signal system call number.
- Loop through all process table entries, if there is a process with STATE as tuple (WAIT_PROCESS, current process PID) then change the STATE field to READY.
- Reset the MODE FLAG to 0 in the process table and store 0 as
return value in the user stack.

##### Getpid and Getppid System Calls

_Getpid_ and _Getppid_ system calls returns the PID of the current process and the PID of the parent process of the current process respectively to the user program. Implement both these system calls in interrupt routine 11.

!!! note 
    The system calls implemented above are final and will not change later.
    See algorithms for 
    Wait/Signal  and
    Getpid/Getppid 

#### Modifications to Exit Process Function (function number = 3, Process Manager Module)

Exit Process function is modified so that it wakes up all the processes waiting for the current process. Similarly, the children of the process are set as orphan processes by changing PPID field of child processes to -1. But when the Exit Process function is invoked from _Exec_ system call, the process is actually not terminating as the new program is being overlayed in the same address space and is executed with the same PID. when Exit Process is invoked from _Exec_ system call, it should not wake up the processes waiting for the current process and also should not set the children as orphan processes. Check the MODE FLAG in the process table of the current process to find out from which system call Exit Process function is invoked.

If MODE FLAG field in the 
[process table](../os-design/process-table.md) has system call number not equal to 9 (Exec)
implement below steps.

- Loop through the process table of all processes and change the state to READY for the
processes whose state is tuple (WAIT_PROCESS, current PID). Also if the PPID of a process
is PID of current process, then invalidate PPID field to -1.

!!! note 
    The function implemented above is final and will not change later.

#### Shutdown system call

To ensure graceful termination of the system we will write _Shutdown_ system call with just a HALT instruction. _Shutdown_ system call is implemented in interrupt routine 15. Create an xsm file with just the HALT instruction and load this file as interrupt routine 15. From this stage onwards, we will use a new version of Shell as our init program. This Shell version will invoke _Shutdown_ system call to halt the system.

In later stages, when a file system is added to the OS, the file system data will be loaded to the memory and modified, while the OS is running. The _Shutdown_ system call will be re-written so that it commits the changes to the file system data to the disk before the machine halts.

#### Modifications to boot module
Load interrupt routine 11 and interrupt routine 15 from disk to memory. See disk and memory
organization [here](../os-implementation.md).

#### Making things work
Compile and load the newly written/modified files to the disk using XFS-interface.

??? question "Q1. Does the eXpOS guarantees that two processes will not wait for each other i.e. circular wait will not happen"
    No. The present eXpOS does not provide any functionality to avoid circular wait. It is the responsiblity of the user program to make sure that such conditions will not occur.

!!! assignment "Assignment 1: [Shell Version-II]"
    It is recommended to implement the shell program according to the description given earlier on your own. One implementation of shell program is given [here](../test-programs/index.md#test-program-1-shell-version-ii-without-multiuser) . Load this program as the INIT program. Test the shell version by giving different ExpL programs written in previous stages. Remember to load the xsm files of ExpL programs as executables into the disk before trying to execute them using shell.

!!! assignment "Assignment 2"
    Write an ExpL program 'pid.expl' which invokes Getpid system call and prints the pid. Write another ExpL program which invokes Fork system call three times back to back. Then, the program shall use Exec system call to execute pid.xsm file. Run this program using the shell.