---
title: 'Exception Handler'
original_url: 'http://eXpOSNitc.github.io/os_design-files/exe_handler.html'
---







Exception Handler


































 



























  
  
  






Exception Handler
-----------------


  

  

Arguments : None


Return value : None


*Description* : If a process 1) generates an illegal instruction or an invalid address (outside its virtual address space) 2) do a division by zero 3) tries to write to a page which is read-only, 4) causes other faulty conditions which are machine dependent, the machine will generate an exception. See [Exception Handling (Tutorial)](../Tutorials/xsm_interrupts_tutorial.html). The exception handler must terminate the process and invoke the context switch module to to schedule other processes. 


The exception handler is also invoked when a page required by a process is not present in the memory. This condition is known as a [page fault](http://en.wikipedia.org/wiki/Page_fault). The eXpOS scheduler will never schedule a process if its stack page is not present in the memory. Hence, a page fault can occur only when either a) one of the code pages of the process (logical pages 4 to 7) has to be loaded from the disk or b) one of the heap pages has not been allocated (logical page 2 or 3). When a page fault exception occurs, the exception handler routine checks if the page resides in the disk. If it does, it is loaded to the memory and the page table is updated. Otherwise, a new page is allocated to the process by the exception handler.


The data structures updated are [Disk Status Table](mem_ds.html#ds_table), [System Status Table](mem_ds.html#ss_table), [Memory Free List](mem_ds.html#mem_free_list) and [Page Table](process_table.html#per_page_table).


The MODE FLAG must be set upon entering the system call and reset before returning.


  


![](../img/roadmap/exception.png)
  

Control flow diagram for *Exception handler*

  
  

#### Algorithm:



```
 
Set the MODE\_FLAG in the [process table](process_table.html) entry to -1 indicate that the process is in the execption handler.

Switch to the Kernel Stack. 	/* See [kernel stack management during system calls](stack_smcall.html) */
Save the value of SP to the USER SP field in the [Process Table](process_table.html) entry of the process.
Set the value of SP to the beginning of User Area Page.

Backup the register context of the current process using the [BACKUP](../arch_spec-files/instruction_set.html) instruction and push EIP onto the kernel stack.

**If** (the exception is not caused by a page fault or user stack is full)  /* Check the [Exception Cause registers](../Tutorials/xsm_interrupts_tutorial.html) */
             Display the cause of the exception.
	     Terminate the process using **exit\_process()** module function in the [Process Manager](../os_modules/Module_1.html) module.
	     Invoke the scheduler by calling the **switch\_context()** function in the [Scheduler Module](../os_modules/Module_5.html).

/* Exception is due to page fault */
Using the Exception registers, find the page number of the page causing the exception.

If (page corresponds to a code page)
	Get the disk block number to load from the [Disk Map Table](process_table.html#disk_map_table) entry of the process.
	Load the page to memory by calling the **get\_code\_page()** function in the [Memory Manager](../os_modules/Module_2.html) Module.
	In the [page table](process_table.html#per_page_table) entry, set the Page Number field to the page number returned by get\_code\_page()
	Set the [referenced and valid bits](process_table.html#per_page_table) to 1. Also set the [write bit](process_table.html#per_page_table) to 0.
	/* Code pages are not writable */
  
else if (page corresponds to a heap page)
	Allocate 2 new memory pages by calling the **get\_free\_page()** function in the [Memory Manager](../os_modules/Module_2.html) module.
	In the page table entry, set the Page Number field to the pages allocated above
	and auxiliary information to referenced and valid. Also set the write bit to 1.
	/* Heap is writable */

Pop EIP from the kernel stack and restore the register context of the process using [RESTORE](../arch_spec-files/instruction_set.html) instruction.

Reset the MODE\_FLAG back to 0.
Restore SP to the USER SP stored in the process table.
Increment SP and store EIP onto the location pointed to by SP.

ireturn.

```



  
  











































