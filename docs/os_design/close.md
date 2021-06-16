---
title: 'Close'
original_url: 'http://eXpOSNitc.github.io/os_design-files/close.html'
---







Close


































 



























  
  
  




Close System Call
-----------------


  

  

Arguments: File Descriptor (Integer) 


Return Value:




|  |  |
| --- | --- |
| 0 | Success |
| -1 | File Descriptor given is invalid |


***Description*** : The Close system call closes an open file. The file descriptor ceases to be valid once the close system call is invoked. 



  


![](../img/roadmap/close.png)
  

Control flow diagram for *Close* system call

  
  

#### **Algorithm**:



```

	Set the MODE\_FLAG in the [process table](process_table.html) entry to 3, 
	indicating that the process is in the close system call.

	//Switch to Kernel Stack - See [Kernel Stack Management during System Calls](stack_smcall.html). 
	Save the value of SP to the USER SP field in the [Process Table](process_table.html) entry of the process.
	Set the value of SP to the beginning of User Area Page.

	If file descriptor is invalid, return -1.    /* File descriptor value should be within the range 0 to 7 (both included). */

	[Locate the Per-Process Resource Table of the current process.](#collapse5a)             
 Find the PID of the current process from the [System Status Table](./mem_ds.html#ss_table).
 Find the User Area page number from the [Process Table](process_table.html#per_process_table) entry.
 The [Per-Process Resource Table](../os_design-files/process_table.html#per_process_table) is located at the [RESOURCE\_TABLE\_OFFSET](constants.html) from the base of the  [User Area Page](./process_table.html#user_area) . 
	If the Resource identifier field of the [Per Process Resource Table](process_table.html#per_process_table) entry is invalid or does not indicate a [FILE](constants.html), return -1.     
                     /* No file is open with this file descriptor. */

	Get the index of the [Open File Table](mem_ds.html#file_table) entry from Per-Process Resource Table entry.

	Call the **close()** function in the [File Manager module](../os_modules/Module_3.html) with the Open File Table index as arguement.
	
	Invalidate the [Per-Process Resource Table](process_table.html#per_process_table) entry.

	Set the MODE\_FLAG in the [process table](process_table.html) entry to 0.
	Switch back to the user stack.

	Return from system call with 0.    /* success */
	
	**Note:**  At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.
	
```

  

#### Questions


1. Why did we not check if the file is locked?












































