---
title: 'Stage 27 :
                        Pager Module (18 Hours)'
---
<div class="panel-collapse collapse" id="collapse27">
 <div class="panel-body">
  <!--Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo27">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo27">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Understand the disk swap-out and swap-in mechanisms.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Implement the pager module that supports Swap in and Swap out functions.
        </li>
       </ul>
      </div>
     </li>
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo27a">
       Pre-requisite Reading
      </a>
      <div class="panel-collapse expand" id="lo27a">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Revisit the description of data structures-
         <a href="os_design-files/process_table.html" target="_blank">
          Process table
         </a>
         ,
         <a href="os_design-files/process_table.html#per_page_table" target="_blank">
          Page table
         </a>
         ,
         <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
          System
                          status table
         </a>
         ,
         <a href="os_design-files/process_table.html#disk_map_table" target="_blank">
          Disk
                          Map table
         </a>
         .
        </li>
       </ul>
      </div>
     </li>
    </ul>
   </div>
  </div>
  <!--End Learning Objectives-->
  <br/>
  <p>
   In this stage, we will learn how the limited physical memory pages of the XSM machine can be used effectively to run the maximum number of concurrent processes. To achieve this, we will implement the functions
   <b>
    Swap Out
   </b>
   and
   <b>
    Swap In
   </b>
   of
   <a href="os_modules/Module_6.html" target="_blank">
    Pager module
   </a>
   (Module 6). Corresponding modifications are done in
   <a href="os_design-files/timer.html" target="_blank">
    Timer Interrupt
   </a>
   and
   <a href="os_modules/Module_5.html" target="_blank">
    Context
                          Switch module
   </a>
   as well.
  </p>
  <p>
   eXpOS gives provision to execute 16 processes concurrently in the system and the number of memory pages available for user processes are 52 (from 76 to 127 - See
   <a href="os_implementation.html" target="_blank">
    memory organization
   </a>
   ). Consider a case, where every process uses four
                        code, two heap, two user stack and one kernel stack pages. Then each process will need 9 memory
                        pages. In this situation, the OS will run out of memory before all 16 processes can be brought
                        into the memory, as the memory required will be 144 pages in total. A solution to this problem
                        is following - when the OS falls short of free memory pages needed for a process, try to
                        identify some inactive process whose memory pages could be swapped out to the disk. The memory
                        pages freed this way can be allocated to the new process. At a later point of time, the OS can
                        swap back the swapped out pages when the inactive process needs to be re-activated. This gives
                        illusion of more memory than actual available memory.
                        (Also see
   <a href="https://en.wikipedia.org/wiki/Virtual_memory" target="_blank">
    Virtual Memory
   </a>
   .)
  </p>
  <p>
   eXpOS uses an approach for memory management where the system does not wait for all the memory
                        to become completely exhausted before initiating a process swap out. Instead, the OS regularly
                        checks for the status of available memory.
   <b>
    At any time if the OS finds that the available
                          (free) memory drops below a critical level, a swap out is initiated.
   </b>
   In such case, the OS
                        identifies a relatively inactive process and swaps out some of the pages of the process to make
                        more free memory available. The critical level in eXpOS is denoted by
   <a href="support_tools-files/constants.html" target="_blank">
    MEM_LOW
   </a>
   (MEM_LOW is equal to 4 in present design). When available memory
                        pages are less than MEM_LOW, eXpOS calls
   <b>
    Swap Out
   </b>
   function of
   <a href="os_modules/Module_6.html" target="_blank">
    pager module
   </a>
   .
   <i>
    Swap Out
   </i>
   function selects a suitable process to swap
                        out to the disk. The memory pages used by the selected process are moved into the disk blocks
                        and the memory pages (except the memory pages of the library) are released. The code pages are not
                        required to be copied to the disk as the disk already contains a copy of the code pages. The kernel stack page of a process is also not swapped out by eXpOS. However, the
                        heap and the user stack pages are swapped out into the disk. eXpOS has
                        256 reserved blocks in the disk (256 to 511 - see
   <a href="os_implementation.html" target="_blank">
    disk organization
   </a>
   ) for swapping purpose. This area is called
   <b>
    swap area
   </b>
   .
  </p>
  <p>
   A swapped out process is swapped back into memory, when one of the following events occur:
   <br/>
   <br/>
   1) A process has remained in swapped out state for more than a threshold amount of time.
   <br/>
   2) The available memory pages exceed
                        certain level denoted by
   <a href="support_tools-files/constants.html" target="_blank">
    MEM_HIGH
   </a>
   (MEM_HIGH is set to 12 in present design).
   <br/>
   <br/>
  </p>
  <p>
   Each process has an associated TICK value (see
   <a href="os_design-files/process_table.html" target="_blank">
    process table
   </a>
   ) which is reset
                            whenever the process is swapped out.  The TICK value is incremented every time
                            the system enters the timer interrupt routine.  If the TICK value of a swapped out
                            process exceeds the value
   <a href="support_tools-files/constants.html#swap" target="_blank">
    MAX_TICK
   </a>
   , the OS decides that the process must be swapped in.
                            A second condition when the OS decides that a process can be swapped in is when
                            the available number of free memory pages (see MEM_FREE_COUNT in
   <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
    system status table
   </a>
   ) exceeds the value MEM_HIGH.
  </p>
  <!-- <p>
                        When one of the above conditions occur, 
                        eXpOS calls <b>Swap In</b> function of the pager module. <i>Swap In</i> function selects
                        a suitable swapped out process to swap back into the memory. New memory pages are allocated to the process and
                        disk blocks corresponding to the process are loaded into the allocated memory pages.
                        </p>
                        
                        <p>The exact details of the strategy used by eXpOS to select a suitable process for Swap In/Out will be discussed later.</p>-->
  <p>
   When does the OS check for MEM_LOW/MEM_HIGH condition? This is done in the
   <a href="os_design-files/timer.html" target="_blank">
    timer interrupt handler
   </a>
   . Since the system enters the timer routine at regular intervals, this design ensures that
                        regular monitoring of TICK/MEM_FREE_COUNT is achieved.
  </p>
  <p>
   We will modify the timer interrupt handler in the following way.  Whenever it is entered from the context of any process
   <b>
    except
   </b>
   a special
   <b>
    swapper daemon process
   </b>
   (to be described later), the handler will inspect the TICK status of the swapped out processes and the memory availability status in the system status table to decide whether a swap-in/swap-out must be initiated.  If swap-in/swap-out is needed, the timer will set the PAGING_STATUS field in the system status table to SWAP_IN/SWAP_OUT appropriately to inform the 
                        scheduler about the need for a swap-in/swap-out.  The timer handler then passes control 
                        to the scheduler. Note that the timer does not initiate any swap-in/swap-out now.  We will describe the actions performed when the timer interrupt handler is entered from the context of the swapper daemon soon below.
  </p>
  <p>
   We will modify the eXpOS scheduler to schedule the swapper daemon whenever PAGING_STATUS field in the system status table is set to SWAP_IN/SWAP_OUT.   
                        The OS reserves PID=15 for the swapper daemon process.  (Thus the swapper daemon joins login, shell and idle processess as special processess initiated by the kernel.)
   <b>
    The swapper daemon shares the code of the idle process, and is essentially a duplicate 
                        idle process running with a different PID. Its sole purpose is to set up a user context for swapping operations.
   </b>
   A consequence of the introduction of the swapper daemon is that only 12 user applications can run concurrently now.
  </p>
  <p>
   If the timer interrupt handler is entered from the context of the swapper daemon, then it will call the Swap-in/Swap-out functions of the pager module after inspecting
                         the value of PAGING_STATUS in the system status table.
   <b>
    Thus, swap-in/swap out will be initiated by the timer interrupt handler only from the context of the swapper daemon.
   </b>
  </p>
  <p>
   While swapping is ongoing, the swapper daemon may get blocked when
                            swap-in/swap-out operation waits for a disk-memory transfer. The OS scheduler 
                            will run the Idle process in such case. Note that the Idle process   
                            will never get blocked, and can always be scheduled whenever no other process is 
                            ready to run.
  </p>
  <p>
   Once a swap-in/swap-out is initiated from the timer, the OS scheduler will not schedule any process other than
                          the swapper daemon or the idle process until the swap-in/swap-out is completed.
                          This policy is taken to avoid unpredicatable conditions that can arise if other processes
                          rapidly acquire/release memory and change the memory availability in the system while a swap
                          operation is ongoing. This design, though not very efficient, is simple to implement and
                        yet achieves the goal
                        of having the full quota of 16 process in concurrent execution. (Note that the size of
                        the process table in the eXpOS implementation outlined here limits the number of concurrent
                        processes to 16).
  </p>
  <p>
   The algorithms for Swap-in and Swap-out are implemented in the
   <a href="os_modules/Module_6.html" target="_blank">
    Pager Module
   </a>
   (Module 6).
  </p>
  <br/>
  <br/>
  <b style="font-size: 20px">
   Modifications to Timer Interrupt
  </b>
  <br/>
  <br/>
  <br/>
  <figure style="text-align: center;">
   <img src="img/roadmap/timer_interrupt.png" style="display:block;margin-left:auto;margin-right:auto"/>
   <br/>
   <figcaption>
    Control flow for timer interrupt
   </figcaption>
  </figure>
  <br/>
  <br/>
  <p>
   Timer interrupt handler is modified as follows:
  </p>
  <p>
   The handler must check whether the current process is the
   <a href="os_design-files/misc.html#swapper" target="_blank">
    swapper daemon
   </a>
   .  
                        This condition can happen only when a swap operation is to be initiated.  
                        In this case, PAGING_STATUS field of the system status table must be checked
                        and Swap_in/Swap_out function of the pager module must be invoked appropriately (SWAP_OUT = 1 and SWAP_IN = 2).
  </p>
  <p>
   If the current process is the idle process, there are two possibilities.
                        If swapping is ongoing (check PAGING_STATUS), one can infer that Idle
                        was scheduled because the swapper daemon was blocked.  In this case, the 
                        timer must invoke the scheduler.  (The scheduler will run Idle again if
                        the daemon is not unblocked.  Otherwise, the daemon will be scheduled.)
                        The second possibility is that swapping was not on-going.  This case is
                        not different from the condition to be checked when timer is entered from
                        any process other than the paging process, and will be descibed next.
  </p>
  <p>
   Generally, when the timer handler is entered from a process when scheduling
                        was not on, the handler must decide whether normal scheduling shall continue
                        or swap-in/swap-out must be inititiated.  Swap-in must be initiated if 
                        the value of MEM_FREE COUNT in the system status table is below MEM_LOW.
                        Swap-out must be inititated if either a) memory availability is high (MEM_FREE_COUNT
                        value exceeds MEM_HIGH) or b) some swapped process has TICK value exceeding 
                        the threshold MAX_TICK.
  </p>
  <br/>
  <p>
   Another modification in the Timer interrupt is to increment the TICK field in the
   <a href="os_design-files/process_table.html" target="_blank">
    process table
   </a>
   of every NON-TERMINATED process. When a process is created
                        by the Fork system call, the TICK value of the process is set to 0 in the process table. Each
                        time the system enters the timer interrupt handler, the TICK value of the process is
                        incremented. The TICK value of a process is reset to zero whenever the process is swapped out
                        or swapped in. Thus the tick value of a process that is not swapped out indicates for how long
                        that process had been in memory without being swapped out. Similarly, the tick value of a
                        swapped out process indicates how long the process had been in swapped state. The
                        swap-in/swap-out algorithms will use the value of TICK to determine the process which had been
                        in swapped state (or not swapped state) for the longest time for swapping in (or out).
  </p>
  <p style="text-indent: 0px">
   Modify Timer Interrupt implemented in earlier stages according to the
                        detailed algorithm given
   <a href="os_design-files/timer.html" target="_blank">
    here
   </a>
   .
  </p>
  <br/>
  <br/>
  <b style="font-size: 20px">
   Pager Module (Module 6)
  </b>
  <br/>
  <br/>
  <p>
   Pager module is responsible for selecting processes to swap-out/swap-in and also to conduct
                        the swap-out/swap-in operations for effective memory management.
  </p>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    <b>
     Swap Out (function number = 1,
     <a href="os_modules/Module_6.html" target="_blank">
      Pager
                              module
     </a>
     )
    </b>
   </li>
   <br/>
   <figure style="text-align: center;">
    <img src="img/roadmap/swap_out.png" style="display:block;margin-left:auto;margin-right:auto"/>
    <br/>
    <figcaption>
     Control flow for
     <b>
      Swap Out
     </b>
    </figcaption>
   </figure>
   <br/>
   <br/>
   <p>
    Swap Out function is invoked from the
    <a href="os_design-files/timer.html" target="_blank">
     timer
                            interrupt handler
    </a>
    and does not take any arguments. As mentioned earlier, the timer interrupt handler will invoke Swap Out only from the context of the
    <b>
     Swapper Daemon
    </b>
    .
   </p>
   <p>
    Swap Out function first chooses a suitable process for swapping out into the disk.  The processes which are not running and are in WAIT_PROCESS or
                          WAIT_SEMAPHORE state are considered first for swapping out (why?). When no such process is
                          found, the process which has stayed longest in the memory is selected for swapping out into
                          the disk. To detect the processes which has stayed longest in the memory, the TICK field in
                          the
    <a href="os_design-files/process_table.html" target="_blank">
     process table
    </a>
    is used.
                          Thus the process with the highest TICK is selected for swapping out.
   </p>
   <p>
    Now that, a process is selected to swap out, the TICK field for the selected process is
                          initialized to 0. (From now on, the TICK field must count for what amount of time the process has been in memory).  The code pages for the swapping-out process are released and the page table
                          entries of the code pages are invalidated. The process selected for swapping out, can have
                          shared heap pages. To simplify implementation, shared heap pages are not swapped out into the
                          disk. Again, to simplify implementation, the kernel stack page is also not swapped out. Non-shared heap pages and user stack pages are stored in the swap
                          area in the disk.
    <b>
     Get Swap Block
    </b>
    function of the
    <a href="os_modules/Module_2.html" target="_blank">
     memory manager module
    </a>
    is invoked to find free blocks in the swap area.
                          These memory pages are stored into the allocated disk blocks by invoking
    <b>
     Disk Store
    </b>
    function of the
    <a href="os_modules/Module_4.html" target="_blank">
     device manager module
    </a>
    and
    <a href="os_design-files/process_table.html#disk_map_table" target="_blank">
     disk map
                            table
    </a>
    is updated with the disk numbers of corresponding pages. Memory pages of the
                          process are released using
    <b>
     Release Page
    </b>
    function of memory manager module and page
                          table entries for these swapped out pages are invalidated. Also the SWAP FLAG in the process table of the
                          swapped out process is set to 1, indicating that the process is swapped out.
   </p>
   <p>
    <b>
     Finally, the PAGING_STATUS in the System Status Table is reset to 0. This step informs the scheduler that the swap operation is complete and normal scheduling can be resumed.
    </b>
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Swap Out
    </i>
    function using the detailed algorithm
                          given in the pager module link above.
   </p>
   <br/>
   <li>
    <b>
     Swap In (function number = 2,
     <a href="os_modules/Module_6.html" target="_blank">
      Pager
                              module
     </a>
     )
    </b>
   </li>
   <br/>
   <br/>
   <figure style="text-align: center;">
    <img src="img/roadmap/swap_in.png" style="display:block;margin-left:auto;margin-right:auto"/>
    <br/>
    <figcaption>
     Control flow for
     <b>
      Swap In
     </b>
    </figcaption>
   </figure>
   <br/>
   <br/>
   <p>
    <b>
     <i>
      Swap In
     </i>
    </b>
    function is invoked from the
    <a href="os_design-files/timer.html" target="_blank">
     timer interrupt handler
    </a>
    and does not take any arguments.
   </p>
   <p>
    The
    <i>
     Swap In
    </i>
    function selects a swapped out process to be brought back to memory. The process which has stayed for longest time in the disk and is ready to
                          run is selected.  That is, the process with the highest TICK among the swapped-out READY processes is selected).
   </p>
   <p>
    Now that, a process is selected to be swapped back into the memory, the TICK field for the
                          selected process is initialized to 0. Code pages of the process are not loaded
                          into the memory, as these pages can be loaded later when exception occurs during execution of
                          the process. Free memory pages for the heap and user stack are allocated using
                          the
    <b>
     Get Free Page
    </b>
    function of the
    <a href="os_modules/Module_2.html" target="_blank">
     memory
                            manager module
    </a>
    and disk blocks of the process are loaded into these memory pages using
                          the
    <b>
     Disk Load
    </b>
    function of the
    <a href="os_modules/Module_4.html" target="_blank">
     device
                            manager module
    </a>
    . The Page table is updated for the new heap and user stack
                          pages. The swap disk blocks used by these pages are released using
    <b>
     Release Block
    </b>
    function of the memory manager module and
    <a href="os_design-files/process_table.html#disk_map_table" target="_blank">
     Disk map table
    </a>
    is invalidated for these pages. Also the SWAP FLAG in
                          the process table of the swapped in process is set to 0, indicating that the process is no
                          longer swapped out.
   </p>
   <p>
    <b>
     Finally, the PAGING_STATUS in the System Status Table is reset to 0. This step informs the scheduler that the swap operation is complete and normal scheduling can be resumed.
    </b>
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Swap In
    </i>
    function using the detailed algorithm
                          given in the pager module link above.
   </p>
   <br/>
   <p style="text-indent: 0px">
    <code>
     Note :
    </code>
    <b>
     [Implementation Hazard]
    </b>
    There is a
                          possibility that the code of the Pager module will exceed more than 2 disk blocks (more than
                          512 instructions). Try to write optimized code to fit the pager module code in 2 blocks. You
                          can use the following strategy to reduce the number of instructions. According to given
                          algorithm for
    <b>
     Swap Out
    </b>
    function, the actions done for code pages, heap pages, user stack pages are written separately. This results in calling Release Page function 2
                          times, Get Swap Block and Disk Store functions 2 times each. Combine these actions into a
                          single while loop where each module function is called only once. The loop should traverse
                          through the page table entries one by one (except library page entries) and perform
                          appropriate actions if the page table entry for a page is valid. Apply similar strategy for
    <b>
     Swap In
    </b>
    function also.
   </p>
   <br/>
   <li>
    <b>
     Get Swap Block (function number = 6,
     <a href="os_modules/Module_2.html" target="_blank">
      Memory
                              Manager Module
     </a>
     )
    </b>
   </li>
   <p>
    <b>
     Get Swap Block
    </b>
    function does not take any arguments. The function returns a free
                          block from the swap area (disk blocks 256 to 511 - see
    <a href="os_implementation.html" target="_blank">
     disk organization
    </a>
    ) of the eXpOS. Get Swap Block searches for a free
                          block from
    <a href="support_tools-files/constants.html" target="_blank">
     DISK_SWAP_AREA
    </a>
    (starting of disk swap area) to
    <a href="support_tools-files/constants.html" target="_blank">
     DISK_SIZE
    </a>
    -1
                          (ending of the eXpOS disk). If a free block is found, the block number is returned. If no free block in swap area is found, -1 is returned to the caller.
   </p>
   <p style="text-indent: 0px">
    Implement
    <i>
     Get Swap Block
    </i>
    function using the detailed
                          algorithm given in the memory manager module link above.
   </p>
   <br/>
   <p style="text-indent: 0px">
    <code>
     Note :
    </code>
    The implementation of module functions
    <b>
     <i>
      Swap Out
     </i>
    </b>
    ,
    <b>
     <i>
      Swap In
     </i>
    </b>
    and
    <b>
     <i>
      Get Swap Block
     </i>
    </b>
    are final.
   </p>
   <br/>
   <b>
    Modification to Context Switch Module (Module 5)
   </b>
   <br/>
   <br/>
   <p>
    Previously, the
    <a href="os_modules/Module_5.html" target="_blank">
     Context Switch module
    </a>
    (scheduler module) would select a new process to schedule according to the Round Robin
                          scheduling algorithm. The procedure for selecting a process to execute is slightly modified
                          in this stage. If swap-in/swap-out is ongoing (that is, if the PAGING_STATUS field of the
    <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
     system status table
    </a>
    is
                          set), the context switch module schedules the Swapper Daemon (PID = 15)
    <b>
     whenever it is not blocked
    </b>
    .  If the swapper daemon is blocked (for some disk operation), then the idle process (PID = 0) must be scheduled.  (The OS design disallows scheduling any process except Idle and Swapper daemon when swapping is on-going.)   If the PAGING_STATUS is set to 0,  swapping is not on-going and hence the next READY/CREATED process which is not swapped out is scheduled in normal Round Robin order. Finally, if no process is in READY or CREATED state,
                          then the idle process is scheduled.
   </p>
   <p style="text-indent: 0px">
    Modify Context Switch module implemented in earlier stages
                          according to the detailed algorithm given
    <a href="os_modules/Module_5.html" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <br/>
   <b>
    Modifications to OS Startup Code
   </b>
   <br/>
   <br/>
   <p style="text-indent: 0px">
    Modify
    <a href="os_design-files/misc.html#os_startup" target="_blank">
     OS Startup Code
    </a>
    to initialize the process table and page table for the Swapper Daemon (similar to the Idle Process).
   </p>
   <p style="text-indent: 0px">
    The final algorithm is given
    <a href="os_design-files/misc.html#os_startup" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <br/>
   <br/>
   <b>
    Modifications to boot module
   </b>
   <br/>
   <br/>
   <ul style="list-style-type: disc; margin-left: 10px;">
    <p style="text-indent: 0px">
     Modify
     <a href="os_modules/Module_7.html" target="_blank">
      Boot
                              module
     </a>
     to add the following steps :
    </p>
    <li style="padding-left: 20px">
     Load module 6 (Pager Module) form disk to memory. See
     <a href="os_implementation.html" target="_blank">
      disk/memory organization
     </a>
     .
    </li>
    <li style="padding-left: 20px">
     Initialize the SWAPPED_COUNT field to 0 and PAGING_STATUS
                            field to 0 in the
     <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
      system
                              status table
     </a>
     to 0, as initially there are no swapped out processes.
    </li>
    <li style="padding-left: 20px">
     Initialize the TICK field to 0 for all the 16
     <a href="os_design-files/process_table.html" target="_blank">
      process table
     </a>
     entries.
    </li>
    <li style="padding-left: 20px">
     Update the MEM_FREE_COUNT to 45 in the
     <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
      system
                                status table
     </a>
     . (The 2 pages are allocated for the user/kernel stack for Swapper Daemon reducing the number from 47 to 45).
    </li>
   </ul>
   <div class="container col-md-12">
    <div class="section_area">
     <ul class="list-group">
      <!--  <li class="list-group-item">

<a data-toggle="collapse"  href="#collapseq24"><b>Q1.</b> Why the processes with state WAIT_PROCESS is given high preference and then WAIT_TERMINAL are preferred to while selecting swap out process?</a>
                            <div id="collapseq24" class="panel-collapse collapse">
                            The processes waiting in pr

                            </div>
    </li>-->
      <li class="list-group-item">
       <a data-toggle="collapse" href="#collapseq25">
        <b>
         Q1.
        </b>
        Why only READY state processes
                                  are selected for swap in, even though swapped out processes can be in blocked state
                                  also?
       </a>
       <div class="panel-collapse collapse" id="collapseq25">
        It is not very useful to swap in a process which is in blocked state into the memory.
                                  As the process is in blocked state, even after swapping in, the process will not
                                  execute until it is made READY. Until the process is made READY, it will just occupy
                                  memory pages which could be used for some other READY/RUNNING process.
       </div>
      </li>
     </ul>
    </div>
   </div>
   <br/>
   <b style="color:#26A65B">
    Assignment 1:
   </b>
   Write an ExpL program which invokes
   <i>
    Fork
   </i>
   system call four times back to back. Then, the program shall use
   <i>
    Exec
   </i>
   system call to
                        execute pid.xsm file (used in
   <a href="#collapse21" target="_blank">
    stage 21
   </a>
   ) to print the
                        PID of the processes. Invoking four Forks back to back is supposed to create 16 new processes,
                        but only 12 new processes will be created as eXpOS will run out of process table entries. Run
                        this program using the shell in the context of a user.
   <br/>
   <br/>
   <b style="color:#26A65B">
    Assignment 2:
   </b>
   Run the program provided
   <a href="test_prog.html#test_program_8" target="_blank">
    here
   </a>
   using shell in the context of a user. The program given in the given link will first read a delay parameter and then, call the Fork system call and create 12 processes. Each process prints numbers from PID*100 to PID*100 + 7. After printing each number, a delay function is called with the the delay parameter provided.
   <br/>
   <br/>
   <b style="color:#26A65B">
    Assignment 3:
   </b>
   Run the program provided
   <a href="test_prog.html#test_program_9" target="_blank">
    here
   </a>
   using shell in the context of a user. The program will create a file
                        with name as "num.dat" and permission as
   <i>
    open access
   </i>
   . Integers 1 to 1200 are written to
                        this file and file is closed. The program will then invoke
   <i>
    Fork
   </i>
   system call four times,
                        back to back to create 12 processes and
   <i>
    Exec
   </i>
   system call is invoked with file
                        "pgm1.xsm". The program for "pgm1.xsm" is provided
   <a href="test_prog.html#test_program_10" target="_blank">
    here
   </a>
   . "pgm1.xsm" will create a new file according to the PID of the
                        process and read 100 numbers from file "num.dat" from offset (PID-3)*100 to (PID-3)*100+99 and
                        write to newly created file. After successful execution, there should be 12 data files each
                        containing 100 consecutive numbers (PID-3)*100+1 to (PID-3)*100+100.
   <br/>
   <br/>
   <b style="color:#26A65B">
    Assignment 4:
   </b>
   Run the program provided
   <a href="test_prog.html#test_program_11" target="_blank">
    here
   </a>
   using shell in the context of a user. The program will create a file
                        with name as "numbers.dat" and permission as
   <i>
    open access
   </i>
   and open the file. The program
                        also invokes
   <i>
    Semget
   </i>
   for a shared semaphore. The program will then invoke
   <i>
    Fork
   </i>
   system call four times, back to back to create 12 processes. The 12 processes now share a file
                        open instance and a semaphore. Each process will write 100 numbers consecutively (PID*1000+1 to
                        PID*1000+100) to the file "numbers.dat".
   <!--After all processes complete writing to the file "numbers.dat" (Share count becomes 1300), -->
   Each process then invokes the
   <i>
    Exec
   </i>
   system call to run the program "pgm2.xsm". The program for "pgm2.xsm" is provided
   <a href="test_prog.html#test_program_12" target="_blank">
    here
   </a>
   . "pgm2.xsm" will create a new file according to the PID of the
                        process and read 100 numbers from file "numbers.dat" from offset (PID-3)*100 to (PID-3)*100+99
                        and write to newly created file. After successful execution, there should be 12 data files each
                        containing 100 numbers from X*1000 to X*1000+99, where X ∈ {3,4..15}. The numbers written
                        by a process in the newly created file need not be the same numbers the process has written in
                        "numbers.dat" file.
   <br/>
   <br/>
   <b style="color:#26A65B">
    Assignment 5:
   </b>
   Run the program (
   <i>
    merge.expl
   </i>
   ) provided
   <a href="test_prog.html#test_program_16" target="_blank">
    here
   </a>
   using shell in the context of a user. The
   <i>
    merge.expl
   </i>
   program, first stores numbers from 1 to 512 in a random order into a file
   <i>
    merge.dat
   </i>
   . It then forks and executes
   <i>
    m_store.expl
   </i>
   which creates 8 files
   <i>
    temp{i}.dat
   </i>
   , where i=1..8 and stores 64 numbers each from
   <i>
    merge.expl
   </i>
   . Then, all the temporary files are sorted by executing
   <i>
    m_sort.expl
   </i>
   . Next, the first ExpL program forks and executes
   <i>
    m_merge.expl
   </i>
   which merges all the temporary files back into
   <i>
    merge.dat
   </i>
   and finally, prints the contents of the file in ascending order. If all
                        the system calls in your OS implementation works correctly, then numbers
                        1 to 512 will be printed out in order.
   <br/>
   <br/>
   <code>
    Note :
   </code>
   To run the program provided by the user, Shell process first invokes
   <i>
    fork
   </i>
   to create a child process. Shell will wait until this first child process completes its
                        execution. When the first child exits, shell will resume execution even if some processes
                        created by the given program are running in the background. This can lead to the following
                        interesting situation. Suppose that all active processes execept idle, login and shell were
                        swapped out and the XSM simulator is waiting for terminal input from the user
                        into the shell. In this case, you will have to issue some command to the 
                        shell, so that the system keeps on running.
   <br/>
   <a data-toggle="collapse" href="#collapse27">
    <span class="fa fa-times">
    </span>
    Close
   </a>
  </ol>
 </div>
</div>
