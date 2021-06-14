---
title: 'Stage 22 :
                        Semaphores (4 Hours)'
---
<div class="panel-collapse collapse" id="collapse22">
 <div class="panel-body">
  <!--Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo22">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo22">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Understanding how semaphores help to solve the critical section problem.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Add support for semaphores to eXpOS.
        </li>
       </ul>
      </div>
     </li>
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo22a">
       Pre-requisite Reading
      </a>
      <div class="panel-collapse expand" id="lo22a">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Read and understand
         <a href="os_spec-files/expos_abstractions.html#resource_sharing" target="_blank">
          Resource Sharing
         </a>
         and
         <a href="os_spec-files/synchronization.html#access_control" target="_blank">
          Access Control
         </a>
         documentations of eXpOS before proceeding further.
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
  <p>
   In this stage, we will add support for
   <a href="https://en.wikipedia.org/wiki/Semaphore_%28programming%29" target="_blank">
    semaphores
   </a>
   to the OS.
                        Semaphores are primitives that allow concurrent processes
                        to handle the
   <a href="https://en.wikipedia.org/wiki/Critical_section" target="_blank">
    critical
                          section
   </a>
   problem. A typical instance of
                        the critical section problem occurs when a set of processes share memory or files. Here it is
                        likely to be necessary to ensure that the processes
                        do not access the shared data (or file) simultaneously to
                        ensure data consistency. eXpOS provides
   <b>
    binary semaphores
   </b>
   which can be used by user
                        programs (ExpL programs) to synchronize the access to the shared resources so that data
                        inconsistency will not occur.
  </p>
  <p>
   There are four actions related to semaphores that a process can perform. Below are the actions
                        along with the corresponding eXpOS system calls -
   <br/>
   1) Acquiring a semaphore -
   <i>
    Semget
   </i>
   system call
   <br/>
   2) Releasing a semaphore -
   <i>
    Semrelease
   </i>
   system call
   <br/>
   3) Locking a semaphore -
   <i>
    SemLock
   </i>
   system call
   <br/>
   4) Unlocking a
                        semaphore -
   <i>
    SemUnLock
   </i>
   system call
   <br/>
  </p>
  <p>
   To use a semaphore, first a process has to acquire a semaphore.
   <b>
    When a process forks, the
                          semaphores currently acquired by a process is shared between the child and the parent.
   </b>
   A
                        process can lock and unlock a semaphore only after acquiring the semaphore. The process can
                        lock the semaphore when it needs to enter into the critical section. After exiting from the
                        critical section, the process unlocks the semaphore allowing other processes (with which the
                        semaphore is shared) to enter the critical section. After the use of a semaphore is finished, a
                        process can detach the semaphore by releasing the semaphore.
  </p>
  <p>
   A process maintains record of the semaphores acquired by it in its
   <a href="os_design-files/process_table.html#per_process_table" target="_blank">
    per-process resource table
   </a>
   . eXpOS uses the data structure,
   <a href="os_design-files/mem_ds.html#sem_table" target="_blank">
    semaphore table
   </a>
   to manage semaphores. Semaphore table is a global data
                        structure which is used to store details of semaphores currently used by all the processes. The
                        Semaphore table has 32 (
   <a href="support_tools-files/constants.html" target="_blank">
    MAX_SEM_COUNT
   </a>
   )
                        entries. This means that only 32 semaphores can be used by all the processes in the system at a
                        time. Each entry in the semaphore table occupies four words of which the last two are currently
                        unused. For each semaphore, the PROCESS COUNT field in it's semaphore table entry keeps track
                        of the number of processes currently sharing the semaphore. If a process locks the semaphore,
                        the LOCKING PID field is set to the PID of that process. LOCKING PID is set to -1 when the
                        semaphore is not locked by any process. An invalid semaphore table entry is indicated by
                        PROCESS COUNT equal to 0. The SPL constant
   <a href="support_tools-files/constants.html" target="_blank">
    SEMAPHORE_TABLE
   </a>
   gives the starting address of the semaphore table in the
   <a href="os_implementation.html" target="_blank">
    memory
   </a>
   . See
   <a href="os_design-files/mem_ds.html#sem_table" target="_blank">
    semaphore
                          table
   </a>
   for more details.
  </p>
  <p>
   The
   <a href="os_design-files/process_table.html#per_process_table" target="_blank">
    per-process
                          resource table
   </a>
   of each process keeps track of the resources (semaphores and files)
                        currently used by the process. The per-process resource table is stored in the last 16 words of
                        the
   <a href="os_design-files/process_table.html#user_area" target="_blank">
    user area page
   </a>
   of a process. Per-process resource table can store details of at most eight resources at a
                        time. Hence the total number of semaphores and files acquired by a process at a time is at most
                        eight. Each per process resource table entry contains two words. The first field, called the
   <b>
    Resource
                          Identifier
   </b>
   field, indicates whether the entry corresponds to a file or a semaphore. For
                        representing the resource as a file, the SPL constant
   <a href="support_tools-files/constants.html" target="_blank">
    FILE
   </a>
   (0) is used and for semaphore, the SPL constant
   <a href="support_tools-files/constants.html" target="_blank">
    SEMAPHORE
   </a>
   (1) is used. The second field stores the index of the semaphore
                        table entry if the resource is a semaphore. (If the resource is a file, an index to the open
                        file table entry will be stored - we will see this in later stages.) See the description of
   <a href="os_design-files/process_table.html#per_process_table" target="_blank">
    per-process
                          resource table
   </a>
   for details.
  </p>
  <figure style="text-align: center;">
   <img src="img/roadmap/sem.png" style="display:block;margin-left:auto;margin-right:auto"/>
   <br/>
   <figcaption>
    Control flow for
    <i>
     Semaphore
    </i>
    system calls
   </figcaption>
  </figure>
  <br/>
  <br/>
  <b style="font-size: 20px">
   Implementation of Interrupt routine 13
  </b>
  <br/>
  <br/>
  <p>
   The system calls
   <i>
    Semget
   </i>
   and
   <i>
    Semrelease
   </i>
   are implemented in the interrupt routine
                        13.
   <i>
    Semget
   </i>
   and
   <i>
    Semrelease
   </i>
   has system call numbers 17 and 18 respectively.
  </p>
  <ul style="list-style-type: disc; margin-left: 10px; ">
   <li style="padding-left: 20px">
    Extract the system call number from the user stack and switch to
                          the kernel stack.
   </li>
   <li style="padding-left: 20px">
    Implement system calls
    <i>
     Semget
    </i>
    and
    <i>
     Semrelease
    </i>
    according to the system call number extracted from above step. Steps to implement these
                          system calls are explained below.
   </li>
   <li style="padding-left: 20px">
    Change back to the user stack and return to the user mode.
   </li>
  </ul>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    <b>
     Semget System Call
    </b>
   </li>
   <p>
    <b>
     <i>
      Semget
     </i>
    </b>
    system call is used to acquire a new semaphore.
    <i>
     Semget
    </i>
    finds a free entry in the
    <a href="os_design-files/process_table.html#per_process_table" target="_blank">
     per-process resource table
    </a>
    .
    <i>
     Semget
    </i>
    then creates a new entry in the semaphore table by invoking the
    <b>
     Acquire
                            Semaphore
    </b>
    function of
    <a href="os_modules/Module_0.html" target="_blank">
     resource
                            manager module
    </a>
    . The index of the semaphore table entry returned by Acquire Semaphore
                          function is stored in the free entry of per-process resource table of the process. Finally,
    <i>
     Semget
    </i>
    system call returns the index of newly created entry in the per-process
                          resource table as
    <b>
     semaphore descriptor
    </b>
    (SEMID).
   </p>
   <p style="text-indent: 0px;">
    Implement
    <i>
     Semget
    </i>
    system call using the detailed algorithm
                          provided
    <a href="os_design-files/semaphore_algos.html#semget" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <li>
    <b>
     Semrelease System Call
    </b>
   </li>
   <p>
    <b>
     <i>
      Semrelease
     </i>
    </b>
    system call takes semaphore desciptor (SEMID) as argument from user
                          program.
    <i>
     Semrelease
    </i>
    system call is used to detach a semaphore from the process.
    <i>
     Semrelease
    </i>
    releases the acquired semaphore and wakes up all the processes waiting for the semaphore by
                          invoking the
    <b>
     Release Semaphore
    </b>
    function of
    <a href="os_modules/Module_0.html" target="_blank">
     resource
                            manager module
    </a>
    .
    <i>
     Semrelease
    </i>
    also invalidates the
    <a>
     per-process resource table
    </a>
    entry corresponding to the SEMID given as an argument.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Semrelease
    </i>
    system call using the detailed
                          algorithm provided
    <a href="os_design-files/semaphore_algos.html#semrelease" target="_blank">
     here
    </a>
    .
   </p>
   <p style="text-indent: 0px">
    <code>
     Note :
    </code>
    If any semaphore is not released by a process
                          during execution using
    <i>
     Semrelease
    </i>
    system call, then the semaphore is released at the
                          time of termination of the process in
    <i>
     Exit
    </i>
    system call.
   </p>
   <br/>
   <li>
    <b>
     Acquire Semaphore (function number = 6,
     <a href="os_modules/Module_0.html" target="_blank">
      resource
                              manager module
     </a>
     )
    </b>
   </li>
   <p>
    <b>
     Acquire Semaphore
    </b>
    function takes PID of the current process as argument.
    <i>
     Acquire
                            Semaphore
    </i>
    finds a free entry in the semaphore table and sets the PROCESS COUNT to 1 in
                          that entry. Finally,
    <i>
     Acquire Semaphore
    </i>
    returns the index of that free entry of
                          semaphore table.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Acquire Semaphore
    </i>
    function using the detailed
                          algorithm provided in resource manager module link above.
   </p>
   <br/>
   <li>
    <b>
     Release Semaphore (function number = 7,
     <a href="os_modules/Module_0.html" target="_blank">
      resource
                              manager module
     </a>
     )
    </b>
   </li>
   <p>
    <b>
     Release Semaphore
    </b>
    function takes a semaphore index (SEMID) and PID of a process as
                          arguments. If the semaphore to be released is locked by current process, then
    <i>
     Release
                            Semaphore
    </i>
    function unlocks the semaphore and wakes up all the processes waiting for
                          this semaphore.
    <i>
     Release Semaphore
    </i>
    function finally decrements the PROCESS COUNT of the
                          semaphore in its corresponding semaphore table entry.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Release Semaphore
    </i>
    function using the detailed
                          algorithm provided in resource manager module link above.
   </p>
   <br/>
  </ol>
  <b style="font-size: 20px">
   Implementation of Interrupt routine 14
  </b>
  <br/>
  <br/>
  <p>
   The system calls
   <i>
    SemLock
   </i>
   and
   <i>
    SemUnLock
   </i>
   are implemented in the interrupt routine
                        14.
   <i>
    SemLock
   </i>
   and
   <i>
    SemUnLock
   </i>
   has system call numbers 19 and 20 respectively.
  </p>
  <ul style="list-style-type: disc; margin-left: 10px;">
   <li style="padding-left: 20px">
    Extract the system call number from the user stack and switch to
                          the kernel stack.
   </li>
   <li style="padding-left: 20px">
    Implement system calls
    <i>
     SemLock
    </i>
    and
    <i>
     SemUnLock
    </i>
    according to the system call number extracted from above step. Steps to implement these
                          system calls are explained below.
   </li>
   <li style="padding-left: 20px">
    Change back to the user stack and return to the user mode.
   </li>
  </ul>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    <b>
     SemLock System Call
    </b>
   </li>
   <p>
    <b>
     <i>
      SemLock
     </i>
    </b>
    system call takes a semaphore desciptor (SEMID) as an argument from
                          user program. A process locks the semaphore it is sharing using the
    <i>
     SemLock
    </i>
    system
                          call. If the requested semaphore is currently locked by some other process, the current
                          process blocks its execution by changing its
    <a href="os_design-files/process_table.html#state" target="_blank">
     STATE
    </a>
    to the tuple (WAIT_SEMAPHORE, semaphore table index of requested
                          semaphore) until the requested semaphore is unlocked. When the semaphore is unlocked, then
                          STATE of the current process is made READY (by the process which has unlocked the semaphore).
                          When the current process is scheduled and the semaphore is still unlocked the current process
                          locks the semaphore by changing the LOCKING PID in the semaphore table entry to the PID of
                          the current process. When the process is scheduled but finds that the semaphore is locked by
                          some other process, current process again waits in the busy loop until the requested
                          semaphore is unlocked.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     SemLock
    </i>
    system call using the detailed algorithm
                          provided
    <a href="os_design-files/semaphore_algos.html#semlock" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <li>
    <b>
     SemUnLock System Call
    </b>
   </li>
   <p>
    <b>
     <i>
      SemUnLock
     </i>
    </b>
    system call takes a semaphore desciptor (SEMID) as argument. A
                          process invokes
    <i>
     SemUnLock
    </i>
    system call to unlock the semaphore.
    <i>
     SemUnLock
    </i>
    invalidates the LOCKING PID field (store -1) in the semaphore table entry for the semaphore.
                          All the processes waiting for the semaphore are made READY for execution.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     SemUnLock
    </i>
    system call using the detailed algorithm
                          provided
    <a href="os_design-files/semaphore_algos.html#semunlock" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <p style="text-indent: 0px">
    <code>
     Note :
    </code>
    The implementation of
    <b>
     <i>
      Semget
     </i>
    </b>
    ,
    <b>
     <i>
      Semrelease
     </i>
    </b>
    ,
    <b>
     <i>
      SemLock
     </i>
    </b>
    ,
    <b>
     <i>
      SemUnLock
     </i>
    </b>
    system calls and
    <b>
     Acquire Semaphore
    </b>
    ,
    <b>
     Release
                            Semaphore
    </b>
    module functions are final.
   </p>
  </ol>
  <br/>
  <b>
   Modifications to
   <i>
    Fork
   </i>
   system call
  </b>
  <br/>
  <br/>
  <p>
   In this stage,
   <i>
    Fork
   </i>
   is modified to update the semaphore table for the semaphores
                        acquired by the parent process. When a process forks, the semaphores acquired by the parent
                        process are now shared between parent and child. To reflect this change, PROCESS COUNT field is
                        incremented by one in the semaphore table entry for every semphore shared between parent and
                        child. Refer algorithm for
   <a href="os_design-files/fork.html" target="_blank">
    fork system call
   </a>
   .
  </p>
  <ul style="list-style-type: disc; margin-left: 10px">
   <li style="padding-left: 20px">
    While copying the per-process resource table of parent to the
                          child process do following -
   </li>
   <li style="padding-left: 20px">
    If the resource is semaphore (check the Resource Identifier
                          field in the
    <a href="os_design-files/process_table.html#per_process_table" target="_blank">
     per-process
                            resource table
    </a>
    ), then using the sempahore table index, increment the PROCESS COUNT
                          field in the
    <a href="os_design-files/mem_ds.html#sem_table" target="_blank">
     semaphore table
    </a>
    entry.
   </li>
  </ul>
  <br/>
  <b>
   Modifications to Free User Area Page (function number = 2,
   <a href="os_modules/Module_1.html" target="_blank">
    process manager module
   </a>
   )
  </b>
  <br/>
  <br/>
  <p>
   The user area page of every process contains the
   <a href="os_design-files/process_table.html#per_process_table" target="_blank">
    per-process resource table
   </a>
   in the last 16 words. When a process
                        terminates, all the semaphores the process has acquired (and haven't released explicitly) have
                        to be released. This is done in the
   <i>
    Free User Area Page
   </i>
   function. The
   <b>
    Release
                          Semaphore
   </b>
   function of resource manager module is invoked for every valid semaphore in the
                        per-process resource table of the process.
  </p>
  <ul style="list-style-type: disc; margin-left: 10px">
   <li style="padding-left: 20px">
    For each entry in the per-process resource table of the process
                          do following -
   </li>
   <li style="padding-left: 20px">
    If the resource is valid and is semaphore (check the Resource
                          Identifier field in the
    <a href="os_design-files/process_table.html#per_process_table" target="_blank">
     per-process
                            resource table
    </a>
    ), then invoke
    <b>
     Release Semaphore
    </b>
    function of
    <a href="os_modules/Module_0.html" target="_blank">
     resource manager module
    </a>
    .
   </li>
  </ul>
  <br/>
  <p style="text-indent: 0px">
   <code>
    Note :
   </code>
   <b>
    <i>
     Fork
    </i>
   </b>
   system call and
   <b>
    Free User
                          Area page
   </b>
   function will be further modified in later stages for the file resources.
  </p>
  <br/>
  <b>
   Modifications to boot module
  </b>
  <br/>
  <br/>
  <ul style="list-style-type: disc; margin-left: 10px">
   <li style="padding-left: 20px">
    Initialize the
    <a href="os_design-files/mem_ds.html#sem_table" target="_blank">
     semaphore table
    </a>
    by setting PROCESS COUNT to 0 and LOCKING PID to -1 for
                          all entries.
   </li>
   <li style="padding-left: 20px">
    Load interrupt routine 13 and 14 from the disk to the memory.
                          See
    <a href="os_implementation.html" target="_blank">
     memory organisation
    </a>
    .
   </li>
  </ul>
  <br/>
  <b>
   Making things work
  </b>
  <br/>
  <br/>
  <p>
   Compile and load the newly written/modified files to the disk using XFS-interface.
  </p>
  <br/>
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq20">
       <b>
        Q1.
       </b>
       When a process waiting for a
                                sempahore is scheduled again after the sempahore is unlocked, is it possible that the
                                process finds the sempahore still locked?
      </a>
      <div class="panel-collapse collapse" id="collapseq20">
       Yes, it is possible. As some other process waiting for the semaphore could be scheduled
                                before the current process and could have locked the semaphore. In this case the
                                present process finds the semaphore locked again and has to wait in a busy loop until
                                the required sempahore is unlocked.
      </div>
     </li>
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq21">
       <b>
        Q2.
       </b>
       A process first locks a semaphore
                                using SemLock system call and then forks to create a child. As the semaphore is now
                                shared between child and parent, what will be locking status for the semaphore?
      </a>
      <div class="panel-collapse collapse" id="collapseq21">
       The sempahore will still be locked by the parent process. In
       <i>
        Fork
       </i>
       system call,
                                the PROCESS COUNT in the semaphore table is incremented by one but LOCKING PID field is
                                left untouched.
      </div>
     </li>
    </ul>
   </div>
  </div>
  <b style="color:#26A65B">
   Assignment 1:
  </b>
  The reader-writer program given
  <a href="test_prog.html#test_program_4" target="_blank">
   here
  </a>
  has two writers and one reader. The parent process will create two
                      child processes by invoking
  <i>
   fork
  </i>
  . The parent and two child processes share a buffer of one
                      word. At a time only one process can read/write to this buffer. To acheive this, these three
                      processes use a shared semaphore. A writer process can write to the buffer if it is empty and the
                      reader process can only read from the buffer if it is full. Before the word in the buffer is
                      overwritten the reader process must read it and print the word to the console. The parent process
                      is the reader process and its two children are writers. One child process writes even numbers
                      from 1 to 100 and other one writes odd numbers from 1 to 100 to the buffer. The parent process
                      reads the numbers and prints them on to the console. Compile the program given in link above and
                      execute the program using the shell. The program must print all numbers from 1 to 100, but not
                      necessarily in sequential order.
  <br/>
  <br/>
  <b style="color:#26A65B">
   Assignment 2:
  </b>
  The ExpL programs given
  <a href="test_prog.html#test_program_13" target="_blank">
   here
  </a>
  describes a
  <i>
   parent.expl
  </i>
  program and a
  <i>
   child.expl
  </i>
  program. The
  <i>
   parent.xsm
  </i>
  program will create 8 child processes by invoking
  <i>
   Fork
  </i>
  3 times. Each of the child processes will print the process ID (PID) and then, invokes the
  <i>
   Exec
  </i>
  system call to execute the program
  <i>
   "child.xsm"
  </i>
  . The
  <i>
   child.xsm
  </i>
  program stores numbers from
  <i>
   PID*100
  </i>
  to
  <i>
   PID*100 + 9
  </i>
  onto a linked list and prints them to the console (each child process will have a seperate heap as the Exec system call alocates a seperate heap for each process). Compile the programs given in the link above and execute the parent program (
  <i>
   parent.xsm
  </i>
  ) using the shell. The program must print all numbers from
  <i>
   PID*100
  </i>
  to
  <i>
   PID*100+9
  </i>
  , where PID = 2 to 9, but not necessarily in sequential order. Also, calculate the
  <b>
   maximum memory usage, number of disk access and number of context switches
  </b>
  (by modifying the OS Kernel code).
  <br/>
  <br/>
  <b style="color:#26A65B">
   Assignment 3:
  </b>
  The two ExpL programs given
  <a href="test_prog.html#test_program_14" target="_blank">
   here
  </a>
  perform merge sort in two different ways. The first one is done in a sequential manner and the second one, in a concurrent approach. Values from 1 to 64 are stored in decreasing order in a linked list and are sorted using a recursive merge sort function. In the concurrent approach, the process is forked and the merge sort function is called recursively for the two sub-lists from the two child processes. Compile the programs given in the link above and execute each of them using the shell. The program must print values from 1 to 64 in a sorted manner. Also, calculate the
  <b>
   maximum memory usage, number of contexts switches and the number of switches to KERNEL mode
  </b>
  .
  <br/>
  <br/>
 
 </div>
</div>
