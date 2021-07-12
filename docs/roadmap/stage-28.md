---
title: 'Stage 28 : Multi-Core Extension (12 Hours)'
original_url: https://exposnitc.github.io/Roadmap.html
---
!!! note "Learning Objectives"
    -   Modifying eXpOS kernel to exploit parallelism in a two core machine.
    -   Understanding processor synchronization in multi-core systems.
    
!!! abstract "Pre-requisite Reading"
    -   Read and understand [NEXSM](../arch-spec/nexsm.md) (two core extension of XSM) specification.
    -   Read and understand design documentation for [eXpOS on NEXSM](../os-design/nexpos.md)
    

**Installation**  
  

Since you will be working on a new machine architecture on this stage, upgraded versions of the XSM machine simulator, SPL compiler, ExpL compiler and xfs-interface has to be downloaded. Create a new folder and download the upgraded eXpOS package so that there are no conflicts with the old version. The OS kernel code and other programs will have to be copied into the new folder before you start working.

Follow the installation instructions [here](../support-tools/setting-up.md#nexsm) to download the upgraded eXpOS package.

  
  
**Outline**  
  

In this stage, you will port eXpOS to a two core extension of XSM called NEXSM. The specification of the OS does not undergo any change from the point of view of the end user or the application programmer (that is, the API - high level library interface or ABI - low level system call interface are unchanged except for some insignificant updates). Thus, the upward (application) interface of the OS does not change.

What changes is the downward (architecture) interface. NEXSM supports a few more memory pages, a few more disk blocks and more significantly, a second core processor. The question is - how to make the best use of the available parallelism with minimal changes to the eXpOS code?

The bootstrap process happens on one of the cores (called the **primary core** in NEXSM specification). The bootstrap code completes the initial set up operations and then start the other core (called **secondary core** ) into parallel action. A read only register called CORE will have value 0 in the primary and 1 in the secondary. This allows the kernel code to determine the core on which it is executing.

**It is absolutely necessary to have a careful reading of the [NEXSM architecture specification](../arch-spec/nexsm.md) before proceeding further.**

Once the OS is up and running on the two-core machine after bootstrap, **each core runs the same OS code and schedules processes parallelly** . The fundamental issue to be addressed is to ensure that *parallel actions of OS on the two cores do not lead the OS into an inconsistent state* .

Handling concurrency is a tricky issue. Here, we impose a few conservative design level restrictions to the level of parallelism permitted so that a simple and comprehensible design is possible. The resultant design is not an efficient one; but it is sufficient to demonstrate the underlying principles. The constraints imposed are the following:

1.  **A single process will never be scheduled simultaneously on both the cores.** The scheduler will be designed so as to ensure this policy. **Only one core will run scheduling code at a given time.** This makes implementation of the first policy straight-forward.
2.  **Only one core will be executing critical kernel code at a time.** By critical kernel code, we mean *'kernel code that updates the [Disk data structures and System-Wide data structures](../os-design/index.md) '* . We will ensure that critical kernel code gets executed quickly and thus **a core will never have to wait for a long time for the other core to leave critical section** . (Non-interfering routines of the OS kernel are allowed to run parallelly - for instance both cores can enter the timer interrupt routine parallely; one core may be running the scheduler while the other is executing a system call and so on.)
3.  A few other simplifying design decisions are:
    1.  **The Login process and Shell Process will be run only from the primary.** (As a consequence, logout and shutdown will be initiated only from the primary). **The pager module will also be run only from the primary.**
    2.  **An additional IDLE process** is created at boot time (called IDLE2 with PID=14). IDLE2 will be scheduled in the second core when no other process can be scheduled. (The primary will schedule IDLE when no other process can be scheduled as in the current design). IDLE2 will never be swapped out. The primary core will never schedule IDLE2 and the secondary core will never schedule IDLE.
    3.  When either **logout** or **paging** is initiated from the primary, the scheduler running on the **secondary core will schedule the IDLE2 process** .

How can the kernel implement the policies (a) and (b)? The implementation mechanism is to maintain two **access lock variables** \- called SCHED\_LOCK and KERN\_LOCK. The kernel maintains an **access lock table** (starting at location 29576 - see [here](../os-implementation.md) ) where these lock variables are stored. The use of these variables will be described in detail below.

Upon entry into a system call (respectively, scheduler code), the kernel first checks whether the other core is executing a system call code (respectively, scheduler code). If that is the case, the kernel waits for the other core to finish the critical system call code (respectively, scheduler code) before proceeding.

  
  
**Data Structure Updates**  
  

The [system status table](../os-design/mem-ds.md#ss_table) will now contain two new entries.

1.  **CURRENT\_PID2:** Stores the PID of the process running on the secondary core.
2.  **LOGOUT\_STATUS:** This field is set to 1 if logout is initiated on the primary core; set to 0 otherwise. If LOGOUT\_STATUS is on, only IDLE2 will be scheduled in the secondary core.

A new data structure called [**access lock table**](../os-design/mem-ds.md#al_table) is introduced. The fields that are of interest in this data structure are the following:  
a) KERN\_LOCK      b) SCHED\_LOCK

1.  When the kernel enters a system call/exception handler (in either core), it first checks whether KERN\_LOCK=1 (If so, the value should have been set to 1 by the kernel code running on the other core). In that case, the kernel executes a [**spin lock**](https://en.wikipedia.org/wiki/Spinlock) (details will follow) till the kernel code running on the other core sets the lock back to zero. When the lock becomes available, the system call/exception handler sets KERN\_LOCK to 1 and proceed with the normal execution of the system call. This ensures, mutual exclusion (between the two cores) for the critical code of system calls/exception handler. Since paging code is critical, KERN\_LOCK is set before invoking the [pager module](../modules/module-08.md) (from the [timer interrupt handler](../os-design/timer.md) ) and set back to zero upon return from the pager module.
2.  At any point of time, if the system call/exception handler has to block for some event, it sets KERN\_LOCK=0 before invoking the scheduler so that if the other core is waiting for KERN\_LOCK, it can acquire the lock and enter critical section. Upon getting scheduled again, the system call/exception handler must do a spin lock again and set KERN\_LOCK to 1 before proceeding. This protocol ensures that *a core holds onto the kernel lock only for short durations of time* . This also ensures that the kernel running on one core never holds on to SCHEDULE\_LOCK and KERN\_LOCK simultaneously. Finally, KERN\_LOCK is set to zero before return to user mode after completion of the system call handler/exception handler code.
3.  Before starting scheduling actions, the scheduler code first checks whether SCHED\_LOCK is set to 1 by the scheduler code running on the other core. If the lock is set, a **spin lock** is executed (details will follow) till the scheduler code running on the other core resets the lock back to zero. This ensures that when scheduling actions are ongoing in one core, the other core waits. Note that scheduler code is small and will execute quickly, and hence the wait will not be for long. SCHED\_LOCK is set to 0 at the end of scheduling.

-   The fundamental point that must be understood is that the **test and set operations on KERN\_LOCK and SCHED\_LOCK need to be atomic** , for otherwise while one core is testing the value of a lock, the other core can change it from 0 to 1 and both the cores will simultaneously enter critical section. Atomicity of test and set operations can be achieved in two ways:
    
    1.  **Hardware solution:** If the hardware provides instructions to perform atomic test and set operations on a variable then the facility can be used.
    2.  **Software Solution:** Even if no hardware support is available, there are clever software solutions that achieve synchronization. [Peterson’s algorithm](https://en.wikipedia.org/wiki/Peterson%27s_algorithm) is one famous solution.
    
    In our case, the NEXSM machine provides a hardware solution in the [**TSL instruction**](../arch-spec/nexsm.md#instr) to support atomic test and set operations and we will use this mechanism to implement atomic operations on KERN\_LOCK and SCHED\_LOCK variables.

  
  
**Access Control Module**  
  

You will add a new module that implements atomic test and set operations on KERN\_LOCK and SCHED\_LOCK. The module will be added as Module 8 ( [memory pages 132-133](../os-implementation.md) ). Access control module supports the following functions:

1.  AcquireKernLock()
2.  AcquireSchedLock()
3.  ReleaseLock(LockVarAddress)

!!! note
    The [eXpOS design documentation](../os-design/nexpos.md) supports a general purpose lock called GLOCK, reserved for future enhancements. The present implementation does not need it and we will not discuss it in the roadmap.

The AccessLock functions can be implemented using the NEXSM [TSL instruction](../arch-spec/nexsm.md#instr) to ensure that locking is atomic. SPL provides the [tsl instruction](../support-tools/spl.md#nespl) which is translated to the XSM TSL machine instruction. The general locking logic in SPL would be the following.

Acquire\*\*\*\*Lock() {
    ....
    .... 
    while (tsl (LockVariableAddress) == 1) 
       continue;
    endwhile; 
}

This would translate to the following XSM code (or equivalent):

L1: TSL Ri, \[LockVariableAddress\]
MOV Rj, 1
EQ Ri, Rj
JNZ Ri, L1

The code atomically reads the lock variable repeatedly until its value is zero. Once the value is founf to be zero, the value is set to one. This procedure is sometimes called a [spin lock](https://en.wikipedia.org/wiki/Spinlock) . A spin-lock is advisable only when the CPU only make a few iterations before the resource could be accessed, as in the present case.

**Important:** LOGOUT\_STATUS will be used by the [Acquire Kernel Lock function](../modules/module-08.md#acquire-kernel-lock) of the Access Control Module in the following way. **When the *Acquire Kernel Lock* function is called from the secondary core, if PAGING\_STATUS or LOGOUT\_STATUS is on, then the lock must not be acquired.** Instead, the state of the current process must be set to READY and the scheduler must be invoked. This is because when paging module is running or if the system has initiated logout (from the primary), normal processing is stopped and only IDLE2 must be scheduled in the secondary. (The scheduler will be designed so that under these circumstances, only IDLE2 will be scheduled for execution).

The access control module algorithms are given [here](../modules/module-08.md) .

  
  
**Bootstrap Procedure**  
  

When NEXSM boots up, only the primary core will execute. Upon execution of the START instruction from the primary (see [NEXSM specification](../arch-spec/nexsm.md) ), the secondary starts execution from physical address 65536 (page 128 - [see Memory Organisation](../os-implementation.md) ). Hence, the primary bootstrap routine (OS startup code) must load the secondary bootstrap loader into memory before issuing START instruction. The IDLE2 process needs to be set up in memory. The access lock table entries are also initialized during bootstrap. A couple of new entries will be added to the [system status table](../os-design/mem-ds.md#ss_table) as well.

  

The required changes to the primary [OS Startup code](../os-design/misc.md#os-startup-code) /boot module are summarized below:

1.  Transfer the secondary bootstrap loader code from disk to memory (from disk block 512 to memory page 128). The access control module also must be loaded from disk to memory (blocks 516-517 to pages 132-133) - see [disk and memory organization](../os-implementation.md) . (Note: The design allows 2 blocks of secondary bootstrap code, but you will only need one block for the present eXpOS version).
2.  Set up the page tables for IDLE2 (PID=14) in memory. Since one user stack and one kernel stack pages will have to be allocated for IDLE2 (the first two free pages, 83 and 84 may be allocated). The [**memory free list**](../os-design/mem-ds.md#mem_free_list) has to be updated accordingly. Also, the **free memory count** in the [system status table](../os-design/mem-ds.md#ss_table) will need corresponding update. The [process table entries](../os-design/process-table.md) for IDLE2 will be set (similar to IDLE). In particular, the state has to be set to RUNNING (as it is going to be running very soon on the secondary core!).
3.  New entries in the [system status table](../os-design/process-table.md) must be initialized. a) CURRENT\_PID2 must be set to the the PID of IDLE2 process (PID=14). b) LOGOUT\_STATUS must be set to 0.
4.  The access control variables KERN\_LOCK and SCHED\_LOCK of the [Access Lock Table](../os-design/mem-ds.md#al_table) must be initialized to 0.
5.  Issue the START instruction to start the secondary core into execution.

  

The **secondary bootstrap code** that begins parallel execution upon START must do the following:

1.  Set up the return address in user stack of the IDLE2 process; SP, PTBR and PTLR registers must be updated.
2.  Execute *ireturn* to run IDLE2.

Thus, the primary and secondary bootstrap code will schedule IDLE (PID=0) and IDLE2 (PID=14) on the respective cores at the end of system startup.

  
  
**Modifications to Scheduler Module**  
  

The scheduler module requires the following modifications:

1.  At the beginning of execution, determine whether scheduler is running on the primary or the secondary (read the CORE register value).
2.  SCHED\_LOCK must be acquired by calling AcquireSchedLock() function of the [access control module](../modules/module-08.md) .
3.  If the core is **primary** , there is no change to existing algorithm **except** that:
    1.  IDLE2 (PID=14) must not be scheduled. (IDLE2 is scheduled only in the secondary).
    2.  The Process which is currently running on the secondary core must not be scheduled (This can be determined by reading CURRENT\_PID2 field of the [system status table](../os-design/mem-ds.md#ss_table) ).
    3.  If LOGOUT\_STATUS=1 and the secondary core is not running IDLE2, then schedule IDLE (wait for the current running process to be scheduled out of the secondary core).
4.  If the core is **secondary** , there is no change to existing algorithm **except** that:
    1.  If PAGING\_STATUS or LOGOUT\_STATUS is set (in the [system status table](../os-design/mem-ds.md#ss_table) ), then IDLE2 must be scheduled).
    2.  IDLE (PID=0), LOGIN (PID=1), SHELL (PID=2) and SWAPPER\_DAEMON (PID=15) should never be scheduled, as the [eXpOS design](../os-design/nexpos.md) stipulates that these processes will run only on the primary.
    3.  Process which is currently running on the primary core must not be scheduled (read CURRENT\_PID field of the [system status table](../os-design/mem-ds.md#ss_table) ).
    4.  The PID of the process that is selected for scheduling in the secondary core must be set to CURRENT\_PID2 field of the system status table.
5.  SCHED\_LOCK must be released by calling *ReleaseLock()* function of the [access control module](../modules/module-08.md) before return from the scheduler. (Note: If the new process to be scheduled is in CREATED state, the scheduler directly returns to user mode using the ireturn statement. Do not forget to release SCHED\_LOCK in this case as well!).

  
  
**Modifications to Exception Handler and System Calls**  
  

1.  Before starting any system call, KERN\_LOCK must be acquired by invoking *AcquireKernLock()* function of the [access control module](../modules/module-08.md) .
2.  The value of **Current PID** will be different on the primary and the secondary cores - \[SYSTEM\_STATUS\_TABLE + 1\] in the primary core and \[SYSTEM\_STATUS\_TABLE + 6\] in the secondary core. ( **Implementation trick:** the formula \[SYSTEM\_STATUS\_TABLE + 5\*CORE + 1\] works on both the cores!!).
3.  *ReleaseLock()* function of the [access control module](../modules/module-08.md) must be used to release KERN\_LOCK before, a) any call to the scheduler, b) return from the system call/exception handler to the user program. Note that, the scheduler can be invoked not only from system calls, but also from kernel modules. In all such cases, KERN\_LOCK must be released before invoking the scheduler.
4.  *AcquireKernLock()* of the [access control module](../modules/module-08.md) must be invoked at any point after return from the scheduler (inside system calls as well as kernel modules).

`Important Note:` When a process has acquired KERN\_LOCK, any other process trying to acquire KERN\_LOCK on the other core will be in a spin lock, doing no userful processing. Hence, your implementation should ensure that *ReleaseLock()* is invoked at the earliest point when it is safe to allow parallel execution of critical code from the other core. Further note that under normal conditions (except in Logout, Shutdown, etc.), updates to [process table](../os-design/process-table.md) and [page table](../os-design/process-table.md#per-process-page-table) entries of a process are private to the process and there is no harm in letting other processes to run parallelly when a system call needs to make updates only to these data structures.

  
  
**Modifications to Timer Interrupt Handler**  
  

1.  Do not invoke [pager module](../modules/module-06.md) from the secondary core.
2.  When running on the primary core, call *AcquireKernLock()* and *ReleaseLock(KERN\_LOCK)* of the [access control module](../modules/module-08.md) before and after calling pager module.

  
  
**Modifications to Process Manager and Pager Modules**  
  

1.  *Kill All* function in [process manager module](../modules/module-01.md) must not call *Exit Process* function for IDLE2 (PID=14) as this process is never killed.
2.  [Pager module](../modules/module-06.md) must not swap out IDLE2 (PID=14).

  
  
**Modifications to Logout System Call**  
  

1.  In [Logout System call](../os-design/multiusersyscalls.md#logout) , first set LOGOUT\_STATUS=1 in the [system status table](../os-design/mem-ds.md#ss_table) , but then call the scheduler (wait until secondary core schedules IDLE2 before proceeding).
2.  After execution of *Kill All* function, set LOGOUT\_STATUS=0. In the [system status table](../os-design/mem-ds.md#ss_table) .

!!! note
    Since, Logout is also a system call, all the updates done to system calls in general will apply to Logout as well.

  
  
**Modifications to Shutdown System Call**  
  

In [Shutdown system call](../os-design/shutdown.md) , before calling *Kill All* function of the [process manager module](../modules/module-01.md) , reset the secondary core (using RESET instruction of NEXSM) and set SCHED\_LOCK to 0.

!!! note
    Since, Shutdown is also a system call, all the updates done to system calls in general will apply to Shutdown as well.


We have tried to include all the necessary details. We leave it to you to figure out anything that is missing here and get the OS working!!

??? question "Q1.Suppose the scheduler is about to resume execution of a process which was blocked while executing some system call, what would go wrong if we modify the present design so that **scheduler simply sets** KERN\_LOCK=1 before scheduling it (instead of the process doing a *AcquireKernLock()* inside the system call after being scheduled)? Note that the scheduler will not run simultaneously on both the cores."
    If the scheduler simply sets KERN\_LOCK=1, then there is a possibility that the other core may have already acquired the KERN\_LOCK. This causes both the cores to execute the critical section code parallelly, which will corrupt the OS data structures. Also, *AcquireKernLock()* function must be called from the system call, instead of the scheduler, as the return from scheduler may be to the timer interrupt handler which doesn't require a Kernel Lock.
    
??? question  "Q2. Why should the logout system call wait for the secondary to execute IDLE2 before proceeding?"
    The Logout system call terminates all the processes from 4 through 13 by calling the *Kill All* function in the process manager module. So, if this system call terminates the currently running process in the secondary core, the memory pages assigned to the process will be released by freeing the page table and user area page, which causes the secondary core to raise an exception. Waiting for the secondary core to schedule IDLE2 prevents this from happening.

!!! assignment "Assignment 1"
    Run all the test cases of the previous stage.  

!!! assignment "Assignment 2"
    Modify the access locking algorithm to use [Peterson’s algorithm](https://en.wikipedia.org/wiki/Peterson%27s_algorithm) instead of using the TSL instruction and run all test cases.  
  

`Thought Experiment:` Right now, all kernel code (except scheduler) operates with a single KERN\_LOCK. Instead, suppose you put different lock variables for each kernel data structure, clearly, better use of parallelism can be achieved. What are the issues you have to consider when such a re-design is one? (You don’t have to do the experiment, but try to work out the design details on pen and paper). Do you think this will make the kernel run considerably faster? Can such a design lead to deadlocks?