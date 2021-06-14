---
title: 'Stage 28 : Multi-Core Extension (12 Hours)'
---
<div class="panel-collapse collapse" id="collapse28">
 <div class="panel-body">
  <!--Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo28">
       Learning Objectives
      </a>
      <div class="panel-collapse expand" id="lo28">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Modifying eXpOS kernel to exploit parallelism in a two core machine.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Understanding processor synchronization in multi-core systems.
        </li>
       </ul>
      </div>
     </li>
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo28a">
       Pre-requisite Reading
      </a>
      <div class="panel-collapse expand" id="lo28a">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Read and understand
         <a href="arch_spec-files/nexsm.html" target="_blank">
          NEXSM
         </a>
         (two core extension of XSM) specification.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Read and understand design documentation for
         <a href="os_design-files/nexpos.html" target="_blank">
          eXpOS on NEXSM
         </a>
        </li>
       </ul>
      </div>
     </li>
    </ul>
   </div>
  </div>
  <!--End Learning Objectives-->
  <br/>
  <br/>
  <b style="font-size: 20px">
   Installation
  </b>
  <br/>
  <br/>
  <p>
   Since you will be working on a new machine architecture on this stage, upgraded versions of the XSM machine simulator, SPL compiler, ExpL compiler and xfs-interface has to be downloaded. Create a new folder and download the upgraded eXpOS package so that there are no conflicts with the old version. The OS kernel code and other programs will have to be copied into the new folder before you start working.
  </p>
  <p>
   Follow the installation instructions
   <a href="support_tools-files/setting-up.html#nexsm" target="_blank">
    here
   </a>
   to download the upgraded eXpOS package.
  </p>
  <br/>
  <br/>
  <b style="font-size: 20px">
   Outline
  </b>
  <br/>
  <br/>
  <p>
   In this stage, you will port eXpOS to a two core extension of XSM called NEXSM. The specification of the OS does not undergo any change from the point of view of the end user or the application programmer (that is, the API - high level library interface or ABI - low level system call interface are unchanged except for some insignificant updates). Thus, the upward (application) interface of the OS does not change.
  </p>
  <p>
   What changes is the downward (architecture) interface. NEXSM supports a few more memory pages, a few more disk blocks and more significantly, a second core processor. The question is - how to make the best use of the available parallelism with minimal changes to the eXpOS code?
  </p>
  <p>
   The bootstrap process happens on one of the cores (called the
   <b>
    primary core
   </b>
   in NEXSM specification).  The bootstrap code completes the initial set up operations and then start the other core (called
   <b>
    secondary core
   </b>
   ) into parallel action.  A read only register called CORE will have value 0 in the primary and 1 in the secondary.  This allows the kernel code to determine the core on which it is executing.
  </p>
  <p>
   <b>
    It is absolutely necessary to have a careful reading of the
    <a href="arch_spec-files/nexsm.html" target="_blank">
     NEXSM architecture specification
    </a>
    before proceeding further.
   </b>
  </p>
  <p>
   Once the OS is up and running on the two-core machine after bootstrap,
   <b>
    each core runs the same OS code and schedules processes parallelly
   </b>
   . The fundamental issue to be addressed is to ensure that
   <i>
    parallel actions of OS on the two cores do not lead the OS into an inconsistent state
   </i>
   .
  </p>
  <p>
   Handling concurrency is a tricky issue. Here, we impose a few conservative design level restrictions to the level of parallelism permitted so that a simple and comprehensible design is possible. The resultant design is not an efficient one; but it is sufficient to demonstrate the underlying principles. The constraints imposed are the following:
  </p>
  <ol style="margin-left:1.8em" type="a">
   <li>
    <b>
     A single process will never be scheduled simultaneously on both the cores.
    </b>
    The scheduler will be designed so as to ensure this policy.
    <b>
     Only one core will run scheduling code at a given time.
    </b>
    This makes implementation of the first policy straight-forward.
   </li>
   <li>
    <b>
     Only one core will be executing critical kernel code at a time.
    </b>
    By critical kernel code, we mean
    <i>
     'kernel code that updates the
     <a href="os_design.html" target="_blank">
      Disk data structures and System-Wide data structures
     </a>
     '
    </i>
    . We will ensure that critical kernel code gets executed quickly and thus
    <b>
     a core will never have to wait for a long time for the other core to leave critical section
    </b>
    . (Non-interfering routines of the OS kernel are allowed to run parallelly - for instance both cores can enter the timer interrupt routine parallely; one core may be running the scheduler while the other is executing a system call and so on.)
   </li>
   <li>
    A few other simplifying design decisions are:
    <ol style="margin-left:2.5em">
     <li>
      <b>
       The Login process and Shell Process will be run only from the primary.
      </b>
      (As a consequence, logout  and shutdown will be initiated only from the primary).
      <b>
       The pager module will also be run only from the primary.
      </b>
     </li>
     <li>
      <b>
       An additional IDLE process
      </b>
      is created at boot time (called IDLE2 with PID=14).  IDLE2 will be scheduled in the second core when no other process can be scheduled.  (The primary will schedule IDLE when no other process can be scheduled as in the current design). IDLE2 will never be swapped out. The primary core will never schedule IDLE2 and the secondary core will never schedule IDLE.
     </li>
     <li>
      When either
      <b>
       logout
      </b>
      or
      <b>
       paging
      </b>
      is initiated from the primary, the scheduler running on the
      <b>
       secondary core will schedule the IDLE2 process
      </b>
      .
     </li>
    </ol>
   </li>
  </ol>
  <p>
   How can the kernel implement the policies (a) and (b)? The implementation mechanism is to maintain two
   <b>
    access lock variables
   </b>
   - called SCHED_LOCK and KERN_LOCK. The kernel maintains an
   <b>
    access lock table
   </b>
   (starting at location 29576 - see
   <a href="os_implementation.html" target="_blank">
    here
   </a>
   ) where these lock variables are stored. The use of these variables will be described in detail below.
  </p>
  <p>
   Upon entry into a system call (respectively, scheduler code), the kernel first checks whether the other core is executing a system call code (respectively, scheduler code).  If that is the case, the kernel waits for the other core to finish the critical system call code (respectively, scheduler code) before proceeding.
  </p>
  <br/>
  <br/>
  <b style="font-size: 20px">
   Data Structure Updates
  </b>
  <br/>
  <br/>
  <p>
   The
   <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
    system status table
   </a>
   will now contain two new entries.
  </p>
  <ol style="margin-left:1.8em" type="a">
   <li>
    <b>
     CURRENT_PID2:
    </b>
    Stores the PID of the process running on the secondary core.
   </li>
   <li>
    <b>
     LOGOUT_STATUS:
    </b>
    This field is set to 1 if logout is initiated on the primary core;  set to 0 otherwise. If LOGOUT_STATUS is on, only IDLE2 will be scheduled in the secondary core.
   </li>
  </ol>
  <p>
   A new data structure called
   <a href="os_design-files/mem_ds.html#al_table" target="_blank">
    <b>
     access lock table
    </b>
   </a>
   is introduced. The fields that are of interest in this data structure are the following:
   <br/>
   a) KERN_LOCK      b) SCHED_LOCK
  </p>
  <ol style="margin-left:1.8em">
   <li>
    When the kernel enters a system call/exception handler (in either core),  it first checks whether KERN_LOCK=1 (If so, the value should have been set to 1 by the kernel code running on the other core). In that case, the kernel executes a
    <a href="https://en.wikipedia.org/wiki/Spinlock" target="_blank">
     <b>
      spin lock
     </b>
    </a>
    (details will follow) till the kernel code running on the other core sets the lock back to zero. When the lock becomes available, the system call/exception handler sets KERN_LOCK to 1 and proceed with the normal execution of the system call. This ensures, mutual exclusion (between the two cores) for the critical code of system calls/exception handler. Since paging code is critical, KERN_LOCK is set before invoking the
    <a href="os_modules/Module_8.html" target="_blank">
     pager module
    </a>
    (from the
    <a href="os_design-files/timer.html" target="_blank">
     timer interrupt handler
    </a>
    ) and set back to zero upon return from the pager module.
   </li>
   <li>
    At any point of time, if the system call/exception handler has to block for some event, it sets KERN_LOCK=0 before invoking the scheduler so that if the other core is waiting for KERN_LOCK, it can acquire the lock and enter critical section. Upon getting scheduled again, the system call/exception handler must do a spin lock again and set KERN_LOCK to 1 before proceeding. This protocol ensures that
    <i>
     a core holds onto the kernel lock only for short durations of time
    </i>
    . This also ensures that the kernel running on one core never holds on to SCHEDULE_LOCK and KERN_LOCK simultaneously. Finally, KERN_LOCK is set to zero before return to user mode after completion of the system call handler/exception handler code.
   </li>
   <li>
    Before starting scheduling actions, the scheduler code first checks whether SCHED_LOCK is set to 1 by the scheduler code running on the other core. If the lock is set, a
    <b>
     spin lock
    </b>
    is executed (details will follow) till the scheduler code running on the other core resets the lock back to zero. This ensures that when scheduling actions are ongoing in one core, the other core waits. Note that scheduler code is small and will execute quickly, and hence the wait will not be for long. SCHED_LOCK is set to 0 at the end of scheduling.
   </li>
  </ol>
  <ul class="list-group">
   <li class="list-group-item" style="background:#dff0d8">
    The fundamental point that must be understood is that the
    <b>
     test and set operations on KERN_LOCK and SCHED_LOCK need to be atomic
    </b>
    , for otherwise while one core is testing the value of a lock, the other core can change it from 0 to 1 and both the cores will simultaneously enter critical section. Atomicity of test and set operations can be achieved in two ways:
    <ol style="margin-left:1.8em" type="a">
     <li>
      <b>
       Hardware solution:
      </b>
      If the hardware provides instructions to perform atomic test and set operations on a variable then the facility can be used.
     </li>
     <li>
      <b>
       Software Solution:
      </b>
      Even if no hardware support is available, there are clever software solutions that achieve synchronization.
      <a href="https://en.wikipedia.org/wiki/Peterson%27s_algorithm" target="_blank">
       Peterson’s algorithm
      </a>
      is one famous solution.
     </li>
    </ol>
    In our case, the NEXSM machine provides a hardware solution in the
    <a href="arch_spec-files/nexsm.html#instr" target="_blank">
     <b>
      TSL instruction
     </b>
    </a>
    to support atomic test and set operations and we will use this mechanism to implement atomic operations on KERN_LOCK and SCHED_LOCK variables.
   </li>
  </ul>
  <br/>
  <br/>
  <b style="font-size: 20px">
   Access Control Module
  </b>
  <br/>
  <br/>
  <p>
   You will add a new module that implements atomic test and set operations on KERN_LOCK and SCHED_LOCK. The module will be added as Module 8 (
   <a href="os_implementation.html" target="_blank">
    memory pages 132-133
   </a>
   ). Access control module supports the following functions:
  </p>
  <ol style="margin-left:1.8em" type="a">
   <li>
    AcquireKernLock()
   </li>
   <li>
    AcquireSchedLock()
   </li>
   <li>
    ReleaseLock(LockVarAddress)
   </li>
  </ol>
  <p>
   <code>
    Note:
   </code>
   The
   <a href="os_design-files/nexpos.html" target="_blank">
    eXpOS design documentation
   </a>
   supports a general purpose lock called GLOCK, reserved for future enhancements. The present implementation does not need it and we will not discuss it in the roadmap.
  </p>
  <p>
   The AccessLock functions can be implemented using the NEXSM
   <a href="arch_spec-files/nexsm.html#instr" target="_blank">
    TSL instruction
   </a>
   to ensure that locking is atomic. SPL provides the
   <a href="support_tools-files/spl.html#nespl" target="_blank">
    tsl instruction
   </a>
   which is translated to the XSM TSL machine instruction. The general locking logic in SPL would be the following.
  </p>
  <pre>
Acquire****Lock() {
    ....
    .... 
    while (tsl (LockVariableAddress) == 1) 
       continue;
    endwhile; 
}</pre>
  <p>
   This would translate to the following XSM code (or equivalent):
  </p>
  <pre>
L1: TSL Ri, [LockVariableAddress]
MOV Rj, 1
EQ Ri, Rj
JNZ Ri, L1</pre>
  <p>
   The code atomically reads the lock variable repeatedly until its value is zero. Once the value is founf to be zero, the value is set to one. This procedure is sometimes called a
   <a href="https://en.wikipedia.org/wiki/Spinlock" target="_blank">
    spin lock
   </a>
   . A spin-lock is advisable only when the CPU only make a few iterations before the resource could be accessed, as in the present case.
  </p>
  <p>
   <b>
    Important:
   </b>
   LOGOUT_STATUS will be used by the
   <a href="os_modules/Module_8.html#f1" target="_blank">
    Acquire Kernel Lock function
   </a>
   of the Access Control Module in the following way.
   <b>
    When the
    <i>
     Acquire Kernel Lock
    </i>
    function is called from the secondary core, if PAGING_STATUS or LOGOUT_STATUS is on, then the lock must not be acquired.
   </b>
   Instead, the state of the current process must be set to READY and the scheduler must be invoked. This is because when paging module is running or if the system has initiated logout (from the primary), normal processing is stopped and only IDLE2 must be scheduled in the secondary. (The scheduler will be designed so that under these circumstances, only IDLE2 will be scheduled for execution).
  </p>
  <p>
   The access control module algorithms are given
   <a href="os_modules/Module_8.html" target="_blank">
    here
   </a>
   .
  </p>
  <br/>
  <br/>
  <b style="font-size: 20px">
   Bootstrap Procedure
  </b>
  <br/>
  <br/>
  <p>
   When NEXSM boots up, only the primary core will execute. Upon execution of the START instruction from the primary (see
   <a href="arch_spec-files/nexsm.html" target="_blank">
    NEXSM specification
   </a>
   ), the secondary starts execution from physical address 65536 (page 128 -
   <a href="os_implementation.html" target="_blank">
    see Memory Organisation
   </a>
   ). Hence, the primary bootstrap routine (OS startup code) must load the secondary bootstrap loader into memory before issuing START instruction. The IDLE2 process needs to be set up in memory. The access lock table entries are also initialized during bootstrap. A couple of new entries will be added to the
   <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
    system status table
   </a>
   as well.
  </p>
  <br/>
  <p>
   The required changes to the primary
   <a href="os_design-files/misc.html#os_startup" target="_blank">
    OS Startup code
   </a>
   /boot module are summarized below:
  </p>
  <ol style="margin-left:1.8em">
   <li>
    Transfer the secondary bootstrap loader code from disk to memory (from disk block 512 to memory page 128). The access control module also must be loaded from disk to memory  (blocks 516-517 to pages 132-133) - see
    <a href="os_implementation.html" target="_blank">
     disk and memory organization
    </a>
    . (Note: The design allows 2 blocks of secondary bootstrap code, but you will only need one block for the present eXpOS version).
   </li>
   <li>
    Set up the page tables for IDLE2 (PID=14) in memory. Since one user stack and one kernel stack pages will have to be allocated for IDLE2 (the first two free pages, 83 and 84 may be allocated). The
    <a href="os_design-files/mem_ds.html#mem_free_list" target="_blank">
     <b>
      memory free list
     </b>
    </a>
    has to be updated accordingly. Also, the
    <b>
     free memory count
    </b>
    in the
    <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
     system status table
    </a>
    will need corresponding update. The
    <a href="os_design-files/process_table.html" target="_blank">
     process table entries
    </a>
    for IDLE2 will be set (similar to IDLE). In particular, the state has to be set to RUNNING (as it is going to be running very soon on the secondary core!).
   </li>
   <li>
    New entries in the
    <a href="os_design-files/process_table.html" target="_blank">
     system status table
    </a>
    must be initialized. a) CURRENT_PID2 must be set to the the PID of IDLE2 process (PID=14). b) LOGOUT_STATUS must be set to 0.
   </li>
   <li>
    The access control variables KERN_LOCK and SCHED_LOCK of the
    <a href="os_design-files/mem_ds.html#al_table" target="_blank">
     Access Lock Table
    </a>
    must be initialized to 0.
   </li>
   <li>
    Issue the START instruction to start the secondary core into execution.
   </li>
  </ol>
  <br/>
  <p>
   The
   <b>
    secondary bootstrap code
   </b>
   that begins parallel execution upon START must do the following:
  </p>
  <ol style="margin-left:1.8em">
   <li>
    Set up the return address in user stack of the IDLE2 process; SP, PTBR and PTLR registers must be updated.
   </li>
   <li>
    Execute
    <i>
     ireturn
    </i>
    to run IDLE2.
   </li>
  </ol>
  <p>
   Thus, the primary and secondary bootstrap code will schedule IDLE (PID=0) and IDLE2 (PID=14) on the respective cores at the end of system startup.
  </p>
  <br/>
  <br/>
  <b style="font-size: 20px">
   Modifications to Scheduler Module
  </b>
  <br/>
  <br/>
  <p>
   The scheduler module requires the following modifications:
  </p>
  <ol style="margin-left:1.8em">
   <li>
    At the beginning of execution, determine whether scheduler is running on the primary or the secondary (read the CORE register value).
   </li>
   <li>
    SCHED_LOCK must be acquired by calling AcquireSchedLock() function of the
    <a href="os_modules/Module_8.html" target="_blank">
     access control module
    </a>
    .
   </li>
   <li>
    If the core is
    <b>
     primary
    </b>
    , there is no change to existing algorithm
    <b>
     except
    </b>
    that:
    <ol style="margin-left:2.5em" type="a">
     <li>
      IDLE2 (PID=14) must not be scheduled. (IDLE2 is scheduled only in the secondary).
     </li>
     <li>
      The Process which is currently running on the secondary core must not be scheduled (This can be determined by reading CURRENT_PID2 field of the
      <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
       system status table
      </a>
      ).
     </li>
     <li>
      If LOGOUT_STATUS=1 and the secondary core is not running IDLE2, then schedule IDLE (wait for the current running process to be scheduled out of the secondary core).
     </li>
    </ol>
   </li>
   <li>
    If the core is
    <b>
     secondary
    </b>
    , there is no change to existing algorithm
    <b>
     except
    </b>
    that:
    <ol style="margin-left:2.5em" type="a">
     <li>
      If PAGING_STATUS or LOGOUT_STATUS is set (in the
      <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
       system status table
      </a>
      ), then IDLE2 must be scheduled).
     </li>
     <li>
      IDLE (PID=0), LOGIN (PID=1), SHELL (PID=2) and SWAPPER_DAEMON (PID=15) should never be scheduled, as the
      <a href="os_design-files/nexpos.html" target="_blank">
       eXpOS design
      </a>
      stipulates that these processes will run only on the primary.
     </li>
     <li>
      Process which is currently running on the primary core must not be scheduled (read CURRENT_PID field of the
      <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
       system status table
      </a>
      ).
     </li>
     <li>
      The PID of the process that is selected for scheduling in the secondary core must be set to CURRENT_PID2 field of the system status table.
     </li>
    </ol>
   </li>
   <li>
    SCHED_LOCK must be released by calling
    <i>
     ReleaseLock()
    </i>
    function of the
    <a href="os_modules/Module_8.html" target="_blank">
     access control module
    </a>
    before return from the scheduler. (Note: If the new process to be scheduled is in CREATED state, the scheduler directly returns to user mode using the ireturn statement. Do not forget to release SCHED_LOCK in this case as well!).
   </li>
  </ol>
  <br/>
  <br/>
  <b style="font-size: 20px">
   Modifications to Exception Handler and System Calls
  </b>
  <br/>
  <br/>
  <ol style="margin-left:1.8em">
   <li>
    Before starting any system call, KERN_LOCK must be acquired by invoking
    <i>
     AcquireKernLock()
    </i>
    function of the
    <a href="os_modules/Module_8.html" target="_blank">
     access control module
    </a>
    .
   </li>
   <li>
    The value of
    <b>
     Current PID
    </b>
    will be different on the primary and the secondary cores - [SYSTEM_STATUS_TABLE + 1] in the primary core and [SYSTEM_STATUS_TABLE + 6] in the secondary core. (
    <b>
     Implementation trick:
    </b>
    the formula [SYSTEM_STATUS_TABLE + 5*CORE + 1] works on both the cores!!).
   </li>
   <li>
    <i>
     ReleaseLock()
    </i>
    function of the
    <a href="os_modules/Module_8.html" target="_blank">
     access control module
    </a>
    must be used to release KERN_LOCK before, a)  any call to the scheduler, b) return from the system call/exception handler to the user program. Note that, the scheduler can be invoked not only from system calls, but also from kernel modules. In all such cases, KERN_LOCK must be released before invoking the scheduler.
   </li>
   <li>
    <i>
     AcquireKernLock()
    </i>
    of the
    <a href="os_modules/Module_8.html" target="_blank">
     access control module
    </a>
    must be invoked at any point after return from the scheduler (inside system calls as well as kernel modules).
   </li>
  </ol>
  <p>
   <code>
    Important Note:
   </code>
   When a process has acquired KERN_LOCK, any other process trying to acquire KERN_LOCK on the other core will be in a spin lock, doing no userful processing. Hence, your implementation should ensure that
   <i>
    ReleaseLock()
   </i>
   is invoked at the earliest point when it is safe to allow parallel execution of critical code from the other core. Further note that under normal conditions (except in Logout, Shutdown, etc.), updates to
   <a href="os_design-files/process_table.html" target="_blank">
    process table
   </a>
   and
   <a href="os_design-files/process_table.html#per_page_table" target="_blank">
    page table
   </a>
   entries of a process are private to the process and there is no harm in letting other processes to run parallelly when a system call needs to make updates only to these data structures.
  </p>
  <br/>
  <br/>
  <b style="font-size: 20px">
   Modifications to Timer Interrupt Handler
  </b>
  <br/>
  <br/>
  <ol style="margin-left:1.8em">
   <li>
    Do not invoke
    <a href="os_modules/Module_6.html" target="_blank">
     pager module
    </a>
    from the secondary core.
   </li>
   <li>
    When running on the primary core, call
    <i>
     AcquireKernLock()
    </i>
    and
    <i>
     ReleaseLock(KERN_LOCK)
    </i>
    of the
    <a href="os_modules/Module_8.html" target="_blank">
     access control module
    </a>
    before and after calling pager module.
   </li>
  </ol>
  <br/>
  <br/>
  <b style="font-size: 20px">
   Modifications to Process Manager and Pager Modules
  </b>
  <br/>
  <br/>
  <ol style="margin-left:1.8em">
   <li>
    <i>
     Kill All
    </i>
    function in
    <a href="os_modules/Module_1.html">
     process manager module
    </a>
    must not call
    <i>
     Exit Process
    </i>
    function for IDLE2 (PID=14) as this process is never killed.
   </li>
   <li>
    <a href="os_modules/Module_6.html" target="_blank">
     Pager module
    </a>
    must not swap out IDLE2 (PID=14).
   </li>
  </ol>
  <br/>
  <br/>
  <b style="font-size: 20px">
   Modifications to Logout System Call
  </b>
  <br/>
  <br/>
  <ol style="margin-left:1.8em">
   <li>
    In
    <a href="os_design-files/multiusersyscalls.html#logout" target="_blank">
     Logout System call
    </a>
    , first set LOGOUT_STATUS=1 in the
    <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
     system status table
    </a>
    , but then call the scheduler (wait until secondary core schedules IDLE2 before proceeding).
   </li>
   <li>
    After execution of
    <i>
     Kill All
    </i>
    function, set LOGOUT_STATUS=0. In the
    <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
     system status table
    </a>
    .
   </li>
  </ol>
  <p>
   <code>
    Note:
   </code>
   Since, Logout is also a system call, all the updates done to system calls in general will apply to Logout as well.
  </p>
  <br/>
  <br/>
  <b style="font-size: 20px">
   Modifications to Shutdown System Call
  </b>
  <br/>
  <br/>
  <p>
   In
   <a href="os_design-files/shutdown.html" target="_blank">
    Shutdown system call
   </a>
   , before calling
   <i>
    Kill All
   </i>
   function of the
   <a href="os_modules/Module_1.html" target="_blank">
    process manager module
   </a>
   , reset the secondary core (using RESET instruction of NEXSM) and set SCHED_LOCK to 0.
  </p>
  <p>
   <code>
    Note:
   </code>
   Since, Shutdown is also a system call, all the updates done to system calls in general will apply to Shutdown as well.
  </p>
  <br/>
  <p>
   We have tried to include all the necessary details. We leave it to you to figure out anything that is missing here and get the OS working!!
  </p>
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq28_a">
       <b>
        Q1.
       </b>
       Suppose the scheduler is about to resume execution of a process which was blocked while executing some system call, what would go wrong if we modify the present design so that
       <b>
        scheduler simply sets
       </b>
       KERN_LOCK=1 before scheduling it (instead of the process doing a
       <i>
        AcquireKernLock()
       </i>
       inside the system call after being scheduled)? Note that the scheduler will not run simultaneously on both the cores.
      </a>
      <div class="panel-collapse collapse" id="collapseq28_a">
       If the scheduler simply sets KERN_LOCK=1, then there is a possibility that the other core may have already acquired the KERN_LOCK. This causes both the cores to execute the critical section code parallelly, which will corrupt the OS data structures. Also,
       <i>
        AcquireKernLock()
       </i>
       function must be called from the system call, instead of the scheduler, as the return from scheduler may be to the timer interrupt handler which doesn't require a Kernel Lock.
      </div>
     </li>
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq28_b">
       <b>
        Q2.
       </b>
       Why should the logout system call wait for the secondary to execute IDLE2 before proceeding?
      </a>
      <div class="panel-collapse collapse" id="collapseq28_b">
       The Logout system call terminates all the processes from 4 through 13 by calling the
       <i>
        Kill All
       </i>
       function in the process manager module. So, if this system call terminates the currently running process in the secondary core, the memory pages assigned to the process will be released by freeing the page table and user area page, which causes the secondary core to raise an exception. Waiting for the secondary core to schedule IDLE2 prevents this from happening.
      </div>
     </li>
    </ul>
   </div>
  </div>
  <br/>
  <b style="color:#26A65B">
   Assignment 1:
  </b>
  Run all the test cases of the previous stage.
  <br/>
  <br/>
  <b style="color:#26A65B">
   Assignment 2:
  </b>
  Modify the access locking algorithm to use
  <a href="https://en.wikipedia.org/wiki/Peterson%27s_algorithm" target="_blank">
   Peterson’s algorithm
  </a>
  instead of using the TSL instruction and run all test cases.
  <br/>
  <br/>
  <code>
   Thought Experiment:
  </code>
  Right now, all kernel code (except scheduler) operates with a single KERN_LOCK. Instead, suppose you put different lock variables for each kernel data structure, clearly, better use of parallelism can be achieved. What are the issues you have to consider when such a re-design is one? (You don’t have to do the experiment, but try to work out the design details on pen and paper). Do you think this will make the kernel run considerably faster? Can such a design lead to deadlocks?
  <br/>
  <br/>
 
 </div>
</div>
