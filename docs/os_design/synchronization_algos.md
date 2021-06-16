---
title: 'System calls for Synchronization'
original_url: 'http://eXpOSNitc.github.io/os_design-files/synchronization_algos.html'
---







System calls for Synchronization


































 



























  
  
  




Wait system call
----------------


  

  

Arguments: Process Identifier of the process for which the current
process has to wait.



Return Values: 




|  |  |
| --- | --- |
| 0 | Success |
| -1 | Given process identifier is invalid or it is the pid of the same process invoking wait |


*Description* : The current process is blocked till the process with PID given as argument
executes a Signal system call or exits. The system call will fail
if a process attempts to wait for itself. The only data structure updated is [Process Table](process_table.html). The mode flag in the [Process Table](process_table.html) has to be set to Kernel mode when the process enters the system call and reset before exiting from the system call. 


  

#### Algorithm:



```

Set the MODE\_FLAG in the [process table](process_table.html) entry to 13.

Switch to the Kernel Stack. 	/* See [kernel stack management during system calls](stack_smcall.html) */
Save the value of SP to the USER SP field in the [Process Table](process_table.html) entry of the process.
Set the value of SP to the beginning of User Area Page.

**If** process is intending to wait for itself or for a non-existent process, return -1.    /* Check the status from Process table.  */ 
           
Change the status from (RUNNING,\_ ) to (WAIT\_PROCESS, Argument\_PID ) in the [Process Table](process_table.html).
             
Invoke the Scheduler by calling the **switch\_context()** function in the [Scheduler Module](../os_modules/Module_5.html).

/* The following code excutes only when scheduled again after the occurance of a signal/exit of the process waiting for. */

Restore SP to the USER SP stored in the process table.

Reset the MODE\_FLAG in the [process table](process_table.html) entry to 0.

Return 0.  /* Success */
	
**Note:**  At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.
        
```






  
  
  




Signal system call
------------------


  

  

Arguments: None


Return Value: 




|  |  |
| --- | --- |
| 0 | Success |


*Description*: All processes waiting for the signalling process are resumed. The system
call does not fail. The only data structure updated is [Process Table](process_table.html).The mode flag in the [Process Table](process_table.html) has to be set to Kernel mode when the process enters the system call and reset before exiting from the system call.



  

#### Algorithm:



```

Set the MODE\_FLAG in the [process table](process_table.html) entry to 14.

[Wake up all processes waiting for the current process.](#collapse1)
 Traverse through the [Process Table](process_table.html)
 **If** the process is in state ([WAIT\_PROCESS](constants.html), Pid) where Pid matches with the PID of the current process.
 Change the status to ([READY](constants.html), \_ ).

Reset the MODE\_FLAG in the [process table](process_table.html) entry to 0.

Return 0.   /* Success */

```






 
 <
 





































