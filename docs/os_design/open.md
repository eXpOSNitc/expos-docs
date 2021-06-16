---
title: 'Open'
original_url: 'http://eXpOSNitc.github.io/os_design-files/open.html'
---







Open


































 




























  
  
  




Open System Call
----------------


  

  

Arguments: Filename (String) 


Return Value:




|  |  |
| --- | --- |
| File Descriptor (Integer) | Success, the return value is the file descriptor for the opened file.  |
| -1 | File not found or file is not a data or root file |
| -2 | System has reached its limit of open files |
| -3 | Process has reached its limit of resources |


***Description*** : For a process to read/write a file, it must first open the file. Only data and root files can be opened. The Open operation returns a file descriptor which identifies the open instance of the file. An application can open the same file several times and each time, a different descriptor will be returned by the Open operation. 

 The OS associates a seek position with every open instance of a file. The seek position indicates the current location of file access (read/write). The Open system call initilizes the seek position to 0 (beginning of the file). The seek position can be modified using the [Seek system call](seek.html).


 The [root file](disk_ds.html#root_file) can be opened for Reading by specifying the filename as  ***"root"***. Note that the Root file is different from the other files - It has a reserved memory page copy. So this will be treated as a special case in all related system calls. 


   


![](../img/roadmap/open.png)
  

Control flow diagram for *Open* system call

  
  

#### **Algorithm**:



```

	Set the MODE\_FLAG in the [process table](process_table.html) entry to 2, 
	indicating that the process is in the open system call.

	//Switch to Kernel Stack - See [Kernel Stack Management during System Calls](stack_smcall.html). 
	Save the value of SP to the USER SP field in the [Process Table](process_table.html) entry of the process.
	Set the value of SP to the beginning of User Area Page.

 	[Find a free Per-Process Resource Table entry.](#collapse5b) 
 Find the PID of the current process from the [System Status Table](./mem_ds.html#ss_table).
 Find the User Area page number from the [Process Table](process_table.html) entry.
 The [Per-Process Resource Table](../os_design-files/process_table.html#per_process_table) is located at the [RESOURCE\_TABLE\_OFFSET](../support_tools-files/constants.html) from the base of the  [User Area Page](./process_table.html#user_area) . 
 Find a free [Resource Table](process_table.html#per_process_table) entry.  
 If there is no free entry, return -3. 
 
	Call the **open()** function from the [File Manager module](../os_modules/Module_3.html) to get the [Open File table](../os_design-files/mem_ds.html#file_table) entry.
		
	If Open fails, return the error code.

 	[Set the Per-Process Resource Table entry](#collapse6)             
 Set the Resource Identifier field to [FILE](../support_tools-files/constants.html) . 
 Set the Open File Table index field to the free Open File Table entry found. 

	Set the MODE\_FLAG in the [process table](process_table.html) entry to 0.

	Restore SP to User SP.

	Return the index of the [Per-Process Resource Table](process_table.html#per_process_table) entry.   /* success */
	/* The index of this entry is the File Descriptor of the file. */

	**Note:**  At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.
     
```

  

#### Questions


1. Why must a free Per Process Resource Table entry be found before calling the open() module function?


2. Why should the "root" file be treated seperately? Where is this change implimented for the open system call?


3. Why do we maintain OPEN INSTANCE COUNT in Open File table and FILE OPEN COUNT in File Status table? Why do we need two tables?












































