---
title: 'Write'
original_url: 'http://eXpOSNitc.github.io/os_design-files/write.html'
---






Write


































 



























  
  
  




Write System Call
-----------------


  

  

Arguments: File Descriptor(Integer) and the word to be written


Return Value:




|  |  |
| --- | --- |
| 0 | Success |
| -1 | File Descriptor given is invalid |
| -2 | No disk space / File Full |
| -3 | Permission denied |


Description: The file descriptor is used to identify an open instance of the file. The Write operation writes the word given as argument to the position pointed by the file pointer of the file. After each Write operation, the file pointer advances to the next word in the file. Root file and Executable files cannot be written.


* In addition to this in  [Multiuser](http://exposnitc.github.io/os_spec-files/multiuser.html) implementation, data files which are created with exclusive permission, cannot be written into by any user other than the owner, root or kernel.



  


![](../img/roadmap/FileWrite.png)
  

Control flow diagram for *Write* system call

  
  

#### **Algorithm**:



```

Set the MODE\_FLAG in the [process table](process_table.html) entry to 5, 
indicating that the process is in the write system call.

//Switch to Kernel Stack - See [Kernel Stack Management during System Calls](stack_smcall.html). 
Save the value of SP to the USER SP field in the [Process Table](process_table.html) entry of the process.
Set the value of SP to the beginning of User Area Page.

**If** the word is to be written to STDOUT (terminal device)    /* indicated by a file descriptor value of -2 */
	     Call the **terminal\_write()**function in the [Device manager](../os_modules/Module_4.html)  Module .
	     Switch back to the user stack by restoring USER SP from the process table.
             Set the MODE\_FLAG in the [process table](process_table.html) entry of the parent process to 0.
             Return 0.   /* success */
			 
/* If not terminal, write to file. */

If file descriptor is invalid, return -1.    /* File descriptor value should be within the range 0 to 7 (both included). */

[Locate the Per-Process Resource Table of the current process.](#collapse5a)
 Find the PID of the current process from the [System Status Table](./mem_ds.html#ss_table).
 Find the User Area page number from the [Process Table](process_table.html#per_process_table) entry.
 The [Per-Process Resource Table](../os_design-files/process_table.html#per_process_table) is located at the [RESOURCE\_TABLE\_OFFSET](constants.html) from the base of the  [User Area Page](./process_table.html#user_area) .

If the Resource identifier field of the [Per Process Resource Table](process_table.html#per_process_table) entry is invalid or does not indicate a [FILE](constants.html), return -1.   
/* No file is open with this file descriptor. */

Get the index of the [Open File Table](mem_ds.html#file_table) entry from the Per Process Resource Table entry.

Get the index of the [Inode Table](./disk_ds.html#inode_table) entry from the Open File Table entry. 

If the current user is not root and the current user does not own the file and 		/* Check the [process table](../os_design-files/process_table.html) entry */
the exclusive permission is set, return -3. 

Acquire the Lock on the File by calling the **acquire\_inode()** function in the [File Manager](../os_modules/Module_0.html) module.  
If acquiring the inode fails, return -1.

Get the Lseek position from the Open File Table entry.

**If** lseek position is same as the [MAX\_FILE\_SIZE](support_tools-files/constants.html), **release\_inode()** and return -2.  /* Maximum file size of 2048 reached*/

[If the Lseek position is a multiple of 512 and the same as File size in the inode table](#collapse8a)	/* New block to be allocated */ 
 Get a free disk block by calling the **get\_free\_block()** function in the [Memory Manager](../os_modules/Module_2.html) module.

 If no free disk block is found **release\_inode()** and return -2. 

 Set the new disk block found in the corresponding (lseek / 512) disk block field in the [Inode table](./disk_ds.html#inode_table) entry. 

[Find the disk block number and the position in the block from which input is to be written.](#collapse8)

 Get the block index from lseek position.   /* block index = lseek / block size (512) */
 Get the disk block number corresponding to the block index from the [Inode Table](disk_ds.html#inode_table) .
 Get the offset value from lseek position.   /* offset = lseek % the block size (512) */
Write the word to the File Buffer by calling the **buffered\_write()** function in the [Buffer Manager](../os_modules/Module_3.html) module.

If Lseek equals file size, increment file size in the inode table entry and also in the memory copy of the [root file](disk_ds.html#root_file).

Increment the Lseek position in the Open File Table entry.

Release the Lock on the File by calling the **release\_inode()** function in the [Resource Manager](../os_modules/Module_0.html) module.

Switch back to the user stack by restoring USER SP from the process table.
Set the MODE\_FLAG in the [process table](process_table.html) entry of the parent process to 0.

Return 0.   /* success */
	
**Note:**  At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.
  
```

  

#### Questions:


1. What happens when the "root" is being written into?


2. Which data structure constrains the max file size to 2048 words?


3. What modification to the file data stuctures will enable files exceeding the max file size?



  











































