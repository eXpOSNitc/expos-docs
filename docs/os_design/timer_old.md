---
title: 'Timer Interrupt Handler'
original_url: 'http://eXpOSNitc.github.io/os_design-files/timer_old.html'
---







Timer Interrupt Handler


































 



























  
  
  




Timer Interrupt Handler
-----------------------


  

  

The hardware requirement specification for eXpOS assumes that the machine is equipped with a timer device that sends periodic hardware interrupts. The Timer Interrupt routine handler implements a co-operative multitasking [round robin scheduler](http://en.wikipedia.org/wiki/Round-robin_scheduling) for eXpOS. The timer interrupt routine in eXpOS does the following tasks: 
 1. Schedules the next ready process for execution.
2. Swaps in (or out) processes from (or to) the disk.
3. If unused memory pages are present in the system, wake up those processes which were blocked due to lack of memory.


  

#### Algorithm:


[Save the context of current process and change its state from ([RUNNING](constants.html),\_) to ([READY](constants.html),\_)](#collapse1)




 1. Find the PID of the currently running process from the [Process Table](process_table.html). This will be the PID of unique process in the state (RUNNING, \_ ).


 2. Save the machine state to the location pointed to by [Machine State Pointer](process_table.html#machine_state). 


3. Change the state of the current process from RUNNING to READY by setting the STATE field of the Process Table entry to (READY, \_ ). 



Increment TICK   /* Increment the TICK of all the processes. TICK is given in [Process Table](process_table.html). */ 


**If** free memory pages present     /* Check the MEM\_FREE\_COUNT in [System Status Table](mem_ds.html#ss_table). */


**If** there are sleeping processes that requires memory pages     /* Check the WAIT\_MEM\_COUNT in [System Status Table](mem_ds.html#ss_table). */


[Wake up all processes that requires memory pages.](#collapse5)



1. Change the state from ([WAIT\_MEM](constants.html), \_ ) to (READY, \_ ).


2. Reset the WAIT\_MEM\_COUNT in the [System Status Table](mem_ds.html#ss_table) to 0.




[/* This section of code is included only when swapper module and demand paging are included. */](#collapse14)



**else**    /* Since memory is free and there are no processes waiting for memory, **swap in** the seniormost swapped process. */


**If** disk is free     /* Check the [Disk Status Table](mem_ds.html#ds_table). */


**If** there are swapped processes     /* Check the SWAPPED\_COUNT in [System Status Table](mem_ds.html#ss_table). */


[For the senior most swapped process not in SWAPPED\_WAIT state, find the block which has to be swapped in.](#collapse7)



1. Process with highest value for TICK among the swapped process is the seniormost process.


 /* Processes in SWAPPED\_WAIT state must not be considered for swap in */ 


2. Using the SP value in the [Machine State](process_table.html#Machine_state), find the stack page to be swapped in.


3. The page table entry for this page stores the block number of the disk block containing the page.



Find a free page in memory by checking the [Memory Free List](mem_ds.html).


Mark the free page as used by incrementing its Memory Free List entry 


Decrement MEM\_FREE\_COUNT in System Status Table.


[Load](load_store.html) the block (in which the stack page is stored) from disk to the selected page in memory.


/* Page Table updates will be done by the [Disk Interrupt Handler](disk_interrupt.html) on completion of Load */


**else**     /* When there is no free memory, **swap out** process, if necessary. */


**If** disk is free     /* Check the [Disk Status Table](mem_ds.html#ds_table). */


**If** there are sleeping processes that require memory pages    /* Check the WAIT\_MEM\_COUNT in [System Status Table](mem_ds.html#ss_table)*/


Use the [modified second chance algorithm](sec_chance_algo.html) to find an unreferenced page and the PID of the process that owns the page


Locate the page table of the process.  /* Check the Process Table */


**If** the unreferenced page is a [code page](../os_spec-files/processmodel.html)   /* since code pages are not modified, they need not be stored back */


Mark the unreferenced page as free by decrementing its [Memory Free List](mem_ds.html#mem_free_list) entry.


Increment the MEM\_FREE\_COUNT in the [System Status Table](mem_ds.html#ss_table).


Using pointer to [Inode Table](disk_ds.html#inode_table), find the corresponding code block number


In the page table entry of the unreferenced page, set Physical Page Number field to the code block number


Mark the page as invalid in the [Page Table](process_table.html#per_page_table) by updating the auxiliary information


**Else if** the unreferenced page is a [stack](../os_spec-files/processmodel.html) or [heap](../os_spec-files/processmodel.html) page


Find a free block in swap area.   /* If no swap block is free, abort the swap out and schedule next ready process */


 Mark the block as used by incrementing its [Disk Free List](disk_ds.html) entry


Mark the page as invalid in the [Page Table](process_table.html#per_page_table) by updating the auxiliary information


[Store](load_store.html) the selected page in the swap block


/* Page Table, Process Table and System Status Table updates must be done by the [Disk Interrupt Handler](disk_interrupt.html) */ 


**if** unreferenced page is pointed to by the stack pointer of the process    /* The process cannot run without this stack page */


**if** the process is in ([WAIT\_PROCESS](constants.html), pid) state.   /*If the process swapped out is waiting for a signal.


Change the state to ([SWAPPED\_WAIT](constants.html),pid).  /*This process will not be swapped in before Signal is invoked.*/


else


Set the state of the process to ([SWAPPED](constants.html), \_ ) 


Increment the SWAPPED\_COUNT in [System Status Table](mem_ds.html#ss_table).


Reset the TICK for the process to 0.


/* The code for swapper module and demand paging ends here. */




[Find the next process to be scheduled](#collapse10) 



1. Scan the Process Table in Round Robin fashion to find the next process in ready state (that is, state field has value (READY, \_ ).



[Schedule the next ready process](#collapse11)



Change the state of that process to (RUNNING, \_ ) and restore the execution context of the process using [Machine State Pointer](process_table.html#Machine_state). 


**If** the [mode flag](process_table.html) of the process is set to the Kernel mode, then the return address is obtained from the Kernel Re-entry Point. 


/* Process was running in Kernel mode when it got scheduled out. */


Otherwise obtain return address from IP field in the Machine State.


Return to the new process.



#### Questions


1. Why are processes in swapped\_wait not swapped in?


2. While loading or storing, why are some updates done by disk interrupt handler and some by timer interrupt handler? Is there anything wrong if the updates done by each handler is switched?














































