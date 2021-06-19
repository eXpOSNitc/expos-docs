---
title: 'Seek'
original_url: 'http://eXpOSNitc.github.io/os_design-files/seek.html'
---







Seek


































 



























  
  
  




Seek System Call
----------------


  

  

Arguments: File Descriptor(Integer) , Offset (Integer)


Return Value:




|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|| 0 | Success |
| -1 | File Descriptor given is invalid |
| -2 | Offset value moves the file pointer to a position outside the file |



***Description*** : The Seek operation allows the application program to change the value of the file pointer so that subsequent Read/Write is performed from a new position in the file. The new value of the file pointer is determined by adding the offset to the current value. (A negative Offset will move the pointer backwards). An Offset of 0 will reset the pointer to the beginning of the file. 


If a positive offset goes beyond the size of the file, the seek position will be set to the file size (in the [inode table](../os_design-files/disk_ds.html#inode_table) entry). A negative offset leading to LSeek value below 0 will give an error.



  


![](../img/roadmap/Seek.png)
  

Control flow diagram for *Seek* system call

  
  

#### **Algorithm**:



```

Set the MODE\_FLAG in the [process table](process_table.html) entry to 6, 
indicating that the process is in the seek system call.

//Switch to Kernel Stack - See [Kernel Stack Management during System Calls](stack_smcall.html). 
Save the value of SP to the USER SP field in the [Process Table](process_table.html) entry of the process.
Set the value of SP to the beginning of User Area Page.

If file descriptor is invalid, return -1.    /* File descriptor value must lie within the range from 0 to 7 (both included). */

[Locate the Per-Process Resource Table of the current process.](#collapse5b)
 Find the PID of the current process from the [System Status Table](./mem_ds.html#ss_table).
 Find the User Area page number from the [Process Table](process_table.html#per_process_table) entry.
 The [Per-Process Resource Table](../os_design-files/process_table.html#per_process_table) is located at the [RESOURCE\_TABLE\_OFFSET](constants.html) from the base of the  [User Area Page](./process_table.html#user_area) . 

**If** entry in the Per Process Resource Table corresponding to the file descriptor is invalid, return -1.   
/* No file is open with this file descriptor. */

Get the index of the [Open File Table](mem_ds.html#file_table) entry from the Per Process Resource Table entry.

Get the index of the [Inode Table](./disk_ds.html#inode_table) entry from the Open File Table entry.

Call the **acquire\_inode()** function in the [Resource Manager](../os_modules/Module_0.html) module.   /* Lock the inode */
If the locking fails, return -1. 

Get the current Lseek position from the Open File Table entry. 

[Check the validity of the given offset](#collapse2) 
1. Get the file size of the file from the [Inode Table](disk_ds.html#inode_table) (Use 480 if inode index is "INODE\_ROOT").
2. **If** (lseek + the given offset) is less than 0, **release\_inode()** and return -2.  

**If** the given offset is 0,
	Set lseek value in the Open File Table entry to 0.
**else if** lseek+offset is greater than the file size,
	Set the lseek value to file size. /* Check inode table for file size */
**else**
	Change the lseek value in the Per-Process Resource Table entry to lseek+offset.

Call the **release\_inode()** function in the [Resource Manager](../os_modules/Module_0.html) module.   /* Free the inode */

Set the MODE\_FLAG in the [process table](process_table.html) entry of the parent process to 0.
Switch back to the user stack by resoting USER SP from the process table.

Return with 0.   /* success */
	
**Note:**  At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.

```

  

#### Questions:


1. What concurrency issue can occur if the inode is not locked before reading the lseek position?


2. What goes wrong if the LSEEK is stored in the File Status Table instead of the Open File table?


3. What goes wrong if the LSEEK is stored in the per-process resource table instead of the Open File table?


4. Which all file system calls set the FILE\_SIZE field in the inode status table?


5. If your OS code has no bugs, acquire\_inode() in the above code will never fail. Why?


  











































