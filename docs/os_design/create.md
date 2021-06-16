---
title: 'Create'
original_url: 'http://eXpOSNitc.github.io/os_design-files/create.html'
---







Create


































 



























  
  
  




Create System Call
------------------


  

  

Arguments: Filename (String), Permission (0 - exclusive/1 - open-access) 


Return Value:




|  |  |
| --- | --- |
| 0 | Success/File already exists |
| -1 | No free inode table entry |


***Description*** : The Create operation takes as input a filename. If the file already exists, then the system call returns 0 (success). Otherwise, it creates an empty file by that name, sets the file type to [DATA](constants.html), file size to 0, userid to that of the process (from the [process table](../os_design-files/process_table.html)) and permission as given in the input in the [Inode Table](disk_ds.html#inode_table). It also creates a root entry for that file.


  


#### **Algorithm**:



```

Set the MODE\_FLAG in the [process table](process_table.html) entry to 1, 
indicating that the process is in the create system call.

If the file is present in the system, return 0.   /* Check the [Inode Table](disk_ds.html#inode_table)  */ 
      
Find the index of a free entry in the Inode Table. 
If no free entry found, return -1.   /* Maximum number of files reached */
             
In the Inode Table entry found above, set FILE NAME to the given file name, FILE SIZE to 0 and FILE TYPE to [DATA](constants.html).
In the Inode Table entry, set the block numbers to -1.  /* No disk blocks are allocated to the file */

Set the USER ID to the USERID of the process /* See the [process table](../os_design-files/process_table.html) for user id */
Set the PERMISSION to the permission supplied as input.

In the [Root file](disk_ds.html#root_file) entry corresponding to the Inode Table index, 
set the FILE NAME, FILE SIZE, FILE TYPE, USERNAME and PERMISSION fields.

Set the MODE\_FLAG in the [process table](process_table.html) entry to 0.

Return from the system call with 0.  /* success */
	       

**Note:**  At each point of return from the system call, remember to reset the MODE FLAG.

```
 
 
Ouestions:

1. What would happen if we do not initilize the FILE OPEN COUNT in the File Status Table to -1?














































