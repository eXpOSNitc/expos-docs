---
title: 'Semaphore System Calls'
original_url: 'http://eXpOSNitc.github.io/os_design-files/semaphore_algos.html'
---







Semaphore System Calls


































 



























  
  
  




Semget system call
------------------


  

  

Argument: None


Return Value : 




|  |  |
| --- | --- |
| SEMID (Integer)  | Success, returns a semaphore descriptor(SEMID) |
| -1 | Process has reached its limit of resources  |
| -2 | Number of semaphores has reached its maximum |


Description: This system call is used to obtain a binary [semaphore](https://en.wikipedia.org/wiki/Semaphore_(programming)). eXpOS has a fixed number of semaphores.
 The semaphores of a process are shared with it's child processes. Data Structures updated are [Per Process Resource Table](process_table.html#per_process_table) and [Semaphore table](mem_ds.html#sem_table).


The mode flag in the [Process Table](process_table.html) has to be set to Kernel mode when the process enters the system call and must be reset before exiting from the system call.


  


![](../img/roadmap/semget.png)
  

Control flow diagram for *Semget* system call

  
  

#### Algorithm:



```

Set the MODE\_FLAG in the [Process Table](process_table.html) to 17 and [switch](stack_smcall.html) to kernel stack.

Find the index of a free entry in the [Per Process Resource Table](process_table.html#per_process_table). /* This will be our semaphore descriptor */
If no free entry, then return -1.

Resource Identifier field of the per-process resource table entry is set to 1 to indicate that the resource is a semaphore.

Acquire a semaphore by calling the **acquire\_semaphore()** function in the [Resource Manager](../os_modules/Module_0.html) Module.

/* acquire\_semaphore() module function acquires a semaphore by making an entry in the [Semaphore Table](mem_ds.html#sem_table) and 
returns the index of the entry. If there are no free semaphores, it returns -1 */

If there are no free semaphores, return -2.
             
Store the index of the Semaphore table entry in the Per Process Resource Table entry.   /*Attach the semaphore to the process.*/
             
Switch back to the user stack by resoring the USER SP from the process table.

Set the MODE\_FLAG in the [process table](process_table.html) entry of the parent process to 0.

Return the Per-process Resource Table entry index.   /* Semaphore Descriptor */
	
**Note:**  At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.
		
```






  
  
  




Semrelease system call
----------------------


  

  

Arguments: Semaphore Descriptor (Integer)


Return Value:




|  |  |
| --- | --- |
| 0 | Success |
| -1 | Semaphore Descriptor is invalid |


*Description* : This system call is used to release a semaphore descriptor held by the process. Data Structures updated are [Per Process Resource Table](process_table.html#per_process_table) and [Semaphore table](mem_ds.html#sem_table). The mode flag in the [Process Table](process_table.html) has to be set to Kernel mode when the process enters the system call and reset before exiting from the system call.


  


![](../img/roadmap/semrelease.png)
  

Control flow diagram for *Semrelease* system call

  
  

#### Algorithm:



```
 
Set the MODE\_FLAG in the [Process Table](process_table.html) to 18 and [switch](stack_smcall.html) to kernel stack.

**If** Semaphore descriptor is not valid or the entry in the [Per Process Resource Table](process_table.html#per_process_table) is not valid, return -1. 
/* The descriptor is invalid if not in the range 0 - 7, or if the resource identifier field of the table entry is not 1 */

Invoke the release\_semaphore() function in the [Resource Manager](../os_modules/Module_0.html) Module.
             
Invalidate the Per-Process resource table entry.   /* Set to -1 */ 
               
Switch back to the user stack by restoring the USER SP from the process table.

Set the MODE\_FLAG in the [process table](process_table.html) entry of the parent process to 0.

Return 0.
	
**Note:**  At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.
		
```






  
  
  




SemLock system call
-------------------


  

  

Arguments: Semaphore Descriptor (Integer)


Return Value:




|  |  |
| --- | --- |
| 0 | Success or the semaphore is already locked by the current process |
| -1 | Semaphore Descriptor is invalid |


*Description* : This system call is used to lock the semaphore. If the semaphore is already locked by some other process, then the calling process goes to sleep and wakes up only when the semaphore is unlocked. Otherwise, it locks the semaphore and continues execution. Data Structures updated are [Process Table](process_table.html) and [Semaphore table](mem_ds.html#sem_table).



The mode flag in the [Process Table](process_table.html) has to be set to Kernel mode when the process enters the system call and reset before exiting from the system call.


  

#### Algorithm:



```

Set the MODE\_FLAG in the [Process Table](process_table.html) to 19 and [switch](stack_smcall.html) to kernel stack.

**If** Semaphore descriptor is not valid or the entry in the [Per Process Resource Table](process_table.html#per_process_table) is not valid, return -1. 
/* The descriptor is invalid if not in the range 0 - 7, or if the resource identifier field of the table entry is not 1 */
             
**while** the semaphore is locked by a process other than the current process **do**    /* Check the Locking PID field in the [Semaphore table](mem_ds.html#sem_table) */
              Change the [state](process_table.html#state) of the current process to ([WAIT\_SEMAPHORE](constants.html), Semaphore table index of the locked semaphore).
              Invoke the **switch\_context()** function in the [Scheduler Module](../os_modules/Module_5.html).
**endwhile**

/* Reaches here when the semaphore becomes free for locking */

Change the Locking PID to PID of the current process in the [Semaphore Table](mem_ds.html#sem_table) .

Reset the mode flag in the [Process Table](process_table.html) to 0 and switch back to the user stack.

Return 0.   /* success */
	
**Note:**  At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.

```






  
  
  




SemUnLock system call
---------------------


  

  

Arguments: Semaphore Descriptor (Integer)


Return Value:




|  |  |
| --- | --- |
| 0 | Success |
| -1 | Semaphore Descriptor is invalid |
| -2 | Semaphore was not locked by the calling process |


*Description* : This system call is used to unlock a semaphore that was previously locked by the calling process. It wakes up all the processes which went to sleep trying to lock the semaphore while the semaphore was locked by the calling process. Data Structures updated are [Process Table](process_table.html) and [Semaphore table](mem_ds.html#sem_table). 


  

The mode flag in the [Process Table](process_table.html) has to be set to Kernel mode when the process enters the system call and reset before exiting from the system call.


#### Algorithm:



```

Set the MODE\_FLAG in the [Process Table](process_table.html) to 20 and [switch](stack_smcall.html) to kernel stack.

**If** Semaphore descriptor is not valid or the entry in the [Per Process Resource Table](process_table.html#per_process_table) is not valid, return -1. 
/* The descriptor is invalid if not in the range 0 - 7, or if the resource identifier field of the table entry is not 1 */
         
**If** semaphore is locked. /* Check the Locking PID in the [Semaphore table](mem_ds.html#sem_table) */

              **If** current process has not locked the semaphore, return -2.   /* The semaphore is locked by some other process.*/

              Set the Locking PID to -1.   /* Unlock the semaphore. */

              Loop through the process table and change the [state](process_table.html#state) to (READY, \_ ) for all the processes 
	      in the state ([WAIT\_SEMAPHORE](constants.html), Semaphore table index of the locked semaphore). 

Reset the MODE\_FLAG in the [Process Table](process_table.html) to 0 and switch back to the user stack. 

Return 0.   /* success */
	
**Note:**  At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.

```





 <
 





































