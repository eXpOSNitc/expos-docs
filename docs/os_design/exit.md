---
title: 'Exit'
original_url: 'http://eXpOSNitc.github.io/os_design-files/exit.html'
---







Exit


































 



























  
  
  




Exit system call
----------------


  

  

Arguments: None


Return Value: None


*Description*: Exit system call terminates the execution of the process which invoked it and destroys its memory address space. The calling application ceases to exist after the system call and hence the system call never returns.


Data structures modified are [Memory Free List](mem_ds.html#mem_free_list), [Disk Free List](disk_ds.html#disk_free_list), [Open File Table](mem_ds.html#file_table), [Semaphore Table](mem_ds.html#sem_table), [System Status Table](mem_ds.html#ss_table), [Resource Table](process_table.html#per_process_table) and the [Disk Map Table](process_table.html#disk_map_table).


  


![](../img/roadmap/exit.png)
  

Control flow diagram for *Exit* system call

  
  

#### Algorithm:



```
  
Set the MODE\_FLAG in the [process table](process_table.html) entry to 10.

//Switch to the Kernel Stack. see [kernel stack management during system calls](stack_smcall.html)
Save the value of SP to the USER SP field in the [Process Table](process_table.html) entry of the process.
Set the value of SP to the beginning of User Area Page.

Invoke the **exit\_process()** function from the [Process Manager](../os_modules/Module_1.html) module.

/* exit\_process() releases all the memory pages of the process including the page holding kernel stack.
Still, as exit\_process is non-blocking, the kernel stack page will not be allocated to another process.
This makes it possible to make a final call from the process to the scheduler. There is no return to
the process after the following scheduler invocation. */ 

Invoke the **context\_switch()** function in the [Scheduler Module](../os_modules/Module_5.html).
	
               
```











































