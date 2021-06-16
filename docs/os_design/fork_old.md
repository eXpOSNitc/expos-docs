---
title: 'Fork'
original_url: 'http://eXpOSNitc.github.io/os_design-files/fork_old.html'
---







Fork


































 



























  
  
  




Fork System Call
----------------


  

  

Arguments: None


Return Values:




|  |  |
| --- | --- |
| PID (Integer)  | Success, the return value to the **parent** is the process descriptor(PID) of the child process. |
| 0 | Success, the return value to the **child**. |
| -1 | Failure, Number of processes has reached the maximum limit. Returns to the parent |


*Description*: Replicates the process invoking the system call. The heap, code and library [regions](../os_spec-files/processmodel.html) of the parent are shared by the child. A new stack is allocated to the child and the parent's stack is copied into the child's stack.


When a process executes the Fork system call, the child process shares with the parent all the file and semaphore descriptors previously acquired by the parent. Semaphore/file descriptors acquired subsequent to the fork operation by either the child or the parent will be exclusive to the respective process and will not be shared.


Data Structures modified are [Process Table](process_table.html), [System Status Table](mem_ds.html#ss_table), [Open File Table](mem_ds.html#file_table), [Semaphore Table](mem_ds.html#sem_table), [Memory Free List](mem_ds.html#mem_free_list) and [Disk Free List](disk_ds.html#disk_free_list) (in case of swapped pages) .


The mode flag in the [Process Table](process_table.html) has to be set to Kernel mode when the process enters the system call and reset before exiting from the system call.


  

#### Algorithm:


**If** no free entry in the [Process Table](process_table.html), return -1.  /*If an entry is free, PID field will be set to -1.*/ 


Find the index of a free entry in the Process Table and set the PID field.    /* This entry is assigned to the child process */


Set the PPID field of child process to the current PID.


Count the number of **valid** [stack](../os_spec-files/processmodel.html) pages from the Page Table of the parent process.   /* Count stack pages which are not swapped out */


**If** sufficient number of free pages are not present in memory, then increment the WAIT\_MEM\_COUNT in the [System Status Table](mem_ds.html#ss_table). 


**while** sufficient number of free pages are not present in memory **do**    /* Check the MEM\_FREE\_COUNT in [System Status Table](mem_ds.html#ss_table). */


Change the state of the current process to ([WAIT\_MEM](constants.html), \_ ).


Call scheduler.    /* Scheduler will wake up the process when memory pages are available */


**endwhile**


Scan the page table of the parent process for the stack page entries. For **each** stack page do: 


**If** the stack page is valid


Find a free memory page and increment its [Memory Free List](mem_ds.html#mem_free_list) entry.


Decrement MEM\_FREE\_COUNT in the [System Status Table](mem_ds.html#ss_table). 


 In the page table entry of the child's stack, set the page number field to the number of the selected page.


 Auxiliary information for that entry is copied from the page table of the parent process. 


 Copy the stack page of the parent into the child stack page.    /* Word by word copy */



[/* This section of code is included only when swapper module and demand paging are included. */](#collapse14)



**else**    /* The page is swapped out, share the swap block with the child */


Copy the page table entry of the page to the child


Increment the [Disk Free List](disk_ds.html#disk_free_list) entry of the corresponding swap block


/* The code for swapper module and demand paging ends here. */




[Construct the context of the child process](#collapse1)



Copy the other page table entries (code, heap and library) from the parent's page table to the child    /* Shared between parent and child */


For each page shared, increment its value in the [Memory Free List](mem_ds.html#mem_free_list)


 Copy the parent's [Machine State](process_table.html#machine_state) (except PTBR) and [Per-Process Resource Table](process_table.html#per_process_table) to the child 

  Set the PTBR field of the Machine State to the address of the page table of the child. 


/* The parent and child are identical except for PID, PPID and PTBR */ 


Copy the Inode Index in [Process Table](process_table.html) entry of the parent to child's Inode Index field.    /* Both processes execute the same file */ 


 For every open file of the parent, increment the File Open Count in the [Open File Table](mem_ds.html#file_table).


 For every semaphore acquired by the parent, increment Process Count in the [Semaphore Table](mem_ds.html#sem_table).


 Set state of child process to (READY, \_ ).



Set the return value to 0 for the child process


The PID of the child process is set as the return value for the parent process


Return to the parent process.












































