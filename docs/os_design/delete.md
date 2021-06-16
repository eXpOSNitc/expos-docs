---
title: 'Delete'
original_url: 'http://eXpOSNitc.github.io/os_design-files/delete.html'
---







Delete


































 



























  
  
  




Delete System Call
------------------


  

  

Arguments: Filename (String) 


Return Value: 




|  |  |
| --- | --- |
| 0 | Success/File does not exist |
| -1 | Permission denied |
| -2 | File is open |


***Description*** : The Delete operation takes as input a filename and deletes it. It returns with an error if any instance of the file is open in the system or if the file is not a DATA file. Delete command fails also if the file to be deleted does not belong to the current user and it has exclusive permissions. Otherwise, it deletes the root entry for the file name, invalidates the Inode Table entry for the file, releases the disk blocks allocated to the file and returns 0. 



  


![](../img/roadmap/delete.png)
  

Control flow diagram for *Delete* system call

  
  

#### **Algorithm**  :



```

Set the MODE\_FLAG in the [process table](process_table.html) entry to 4, 
indicating that the process is in the delete system call.

//Switch to Kernel Stack - See [Kernel Stack Management during System Calls](stack_smcall.html). 
Save the value of SP to the USER SP field in the [Process Table](process_table.html) entry of the process.
Set the value of SP to the beginning of User Area Page.

Find the index of the file in the [Inode Table](disk_ds.html#inode_table).
            
If file is not present in the [Inode Table](disk_ds.html#inode_table), return 0. 

If the file is not a DATA file, return -1.

**If** the [exclusive permission](../os_spec-files/multiuser.html) is set
	**if** the current user is not root and the current user does not own the file
		return -1. 

Acquire a lock on the file by calling the **acquire\_inode()** function in the [Resource Manager](../os_modules/Module_0.html) module.

Check if the the file open count is -1 in the  [File Status Table](./mem_ds.html#file_lock_status_table) . If not, release the lock and return -2.    
/* File is open, cannot be deleted */
 
**For** each disk block allocated to the file, **do** { 	/* Check [Inode Table](disk_ds.html#inode_table) */
	If the disk block is loaded into a buffer, and the DIRTY BIT is set, reset the dirty bit. 
	/* Check the [Buffer Table](../os_design-files/mem_ds.html#buffer_table) */ 

	Call the **release\_block()** function in the [Memory Manager](../os_modules/Module_2.html) module to free the disk block.        
}

Invalidate (set to -1) the Inode Table of the file.

Update the [Root file](disk_ds.html#root_file) by invalidating the entry for the file.

Release the lock on the file by calling the **release\_inode()** function in the [Resource Manager](../os_modules/Module_0.html) module.

Switch back to the user stack by reseting USER SP from the process table.
Set the MODE\_FLAG in the [process table](process_table.html) entry of the parent process to 0.

Return from system call with 0.    /* indicating success */

**Note:**  At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.
	     
```

  

#### Questions


1. Why are we not updating the [Open File Table](../os_design-files/mem_ds.html#file_table) when a file is being deleted?


2. Why can't an open file be deleted?


3. Why is the dirty bit in the buffer table cleared before the file is deleted?


4. Does disk blocks get freed anywhere else other than the delete system call?












































