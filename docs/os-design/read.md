---
title: 'Read'
original_url: 'http://eXpOSNitc.github.io/os_design-files/read.html'
---







Read


































 



























  
  
  




Read System Call
----------------


  

  

Arguments: File Descriptor(Integer) and a Buffer (a String/Integer variable) into which a word is to be read from the file


Return Value:






|  |  |
| --- | --- |
| 0 | Success |
| -1 | File Descriptor given is invalid |
| -2 | File pointer has reached the end of file |

***Description*** : The Read operation reads one word from the position pointed by the file pointer and stores it into the buffer. After each read operation, the file pointer advances to the next word in the file.



  


![](../img/roadmap/FileRead.png)
  

Control flow diagram for *Read* system call

  
  

#### **Algorithm**:



```

Set the MODE\_FLAG in the [process table](process_table.html) entry to 7, 
indicating that the process is in the read system call.

//Switch to Kernel Stack - See [Kernel Stack Management during System Calls](stack_smcall.html). 
Save the value of SP to the USER SP field in the [Process Table](process_table.html) entry of the process.
Set the value of SP to the beginning of User Area Page.

**If** input is to be read from terminal    /* indicated by a file descriptor value of -1 */
	Call the **terminal\_read()**function in the [Device manager](../os_modules/Module_4.html)  Module .
			 
/* If not terminal, read from file. */
 **else** 

	If file descriptor is invalid, return -1.    /* File descriptor value should be within the range 0 to 7 (both included). */

	[Locate the Per-Process Resource Table of the current process.](#collapse5a)

 Find the PID of the current process from the [System Status Table](./mem_ds.html#ss_table).
 Find the User Area page number from the [Process Table](process_table.html#per_process_table) entry.
 The [Per-Process Resource Table](../os_design-files/process_table.html#per_process_table) is located at the [RESOURCE\_TABLE\_OFFSET](constants.html) from the base of the  [User Area Page](./process_table.html#user_area) .
 
	If the Resource identifier field of the [Per Process Resource Table](process_table.html#per_process_table) entry is invalid or does not indicate a [FILE](constants.html), return -1.  
	/* No file is open with this file descriptor. */

	Get the index of the [Open File Table](mem_ds.html#file_table) entry from the Per Process Resource Table entry.

	Get the index of the [Inode Table](./disk_ds.html#inode_table) entry from the Open File Table entry. 
	
	Acquire the Lock on the File by calling the **acquire\_inode()** function in the [Resource Manager](../os_modules/Module_0.html) module.
	If acquiring the inode fails, return -1.

	Get the Lseek position from the Open File Table entry.
      
	Get the physical address curresponding to the logical address of Memory Buffer address given as input.

	**If** the File corresponds to Root file ( indicated by Inode index as INODE\_ROOT)  
                  If the lseek value is equal to the root file size(480), **release\_inode()** return -2. 

                  Read from the word at lseek position in memory copy of [root file](../os_design-files/disk_ds.html#root_file) to the translated memory address. 
		  /* Use SPL Constant [ROOT\_FILE](../support_tools-files/constants.html ) */

                  Increment the Lseek position in the Open File Table.        
	 **else** 
		**If** lseek position is same as the file size, **release\_inode()** and return -2.  /* End of file reached */

		[Find the disk block number and the position in the block from which input is read.](#collapse8)
	 Get the block index from lseek position.   /* lseek/512 gives the index of the block */
 Get the disk block number corresponding to the block index from the [Inode Table](disk_ds.html#inode_table) .
 Get the offset value from lseek position.   /* lseek%512 gives the position to be read from.*/
 
		Read the data from the File Buffer by calling the **buffered\_read()** function in the [File Manager](../os_modules/Module_3.html) module.

		Increment the Lseek position in the Open File Table.

	Release the Lock on the File by calling the **release\_inode()** function in the [Resource Manager](../os_modules/Module_0.html) module.

Switch back to the user stack by resoting USER SP from the process table.
Set the MODE\_FLAG in the [process table](process_table.html) entry of the parent process to 0.

Return 0.   /* success */
	
**Note:**  At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.
  
```

  

#### Questions:



  











































