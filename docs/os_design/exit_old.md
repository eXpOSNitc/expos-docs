---
title: 'Exit'
original_url: 'http://eXpOSNitc.github.io/os_design-files/exit_old.html'
---







Exit


































 



























  
  
  




Exit system call
----------------


  

  

Arguments: None


Return Value: None


*Description*: Exit system call terminates the execution of the process which invoked it and destroys its memory address space. The calling application ceases to exist after the system call and hence the system call never returns.


Data structures modified are [Memory Free List](mem_ds.html#mem_free_list), [Disk Free List](disk_ds.html#disk_free_list), [Open File Table](mem_ds.html#file_table), [Semaphore Table](mem_ds.html#sem_table) and [System Status Table](mem_ds.html#ss_table).


  

#### Algorithm:


**If** no more processes to schedule, shutdown the machine     /* If no process in [([READY](constants.html), \_ )](process_table.html) state, invoke [Shutdown system call](shutdown.html) */


Unlock all files opened by the current process.    /* Follow the procedures in [FunLock system call](synchronization_algos.html) */ 


Close all files opened by the current process.     /* Follow the procedures in [Close system call](close.html) */


Release all the semaphores used by the current process.     /* Follow the procedures in [Semrelease system call](semaphore_algos.html#semrelease) */


Wake up all processes waiting for the current process.     /* Follow the procedures in [Signal system call](synchronization_algos.html#signal) */


[Invalidate the page table entries of the current process](#collapse3)



Scan the page table. For **each** page do : 


**If** the page is valid 



 In the [Memory Free List](mem_ds.html#mem_free_list), decrement the value corresponding to the page.


 If the value becomes 0, then increment MEM\_FREE\_COUNT in the [System Status Table](mem_ds.html#ss_table).



[/* This section of code is included only when swapper module and demand paging are included. */](#collapse14)



**else**  /* action required if the page is swapped out*/


If the block number in Page Table lies in the swap area, decrement its entry in the [Disk Free List](disk_ds.html#disk_free_list). 


/* The code for swapper module and demand paging ends here. */





Invalidate the Process Table entry.  /*Set the PID field to -1.*/


Invoke the scheduler to schedule the next process.   /*Scheduler never returns.*/












































