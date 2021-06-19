---
title: 'Delete System Call'
original_url: 'http://eXpOSNitc.github.io/os_design-files/delete.html'
hide:
    - navigation
    - toc
---

Arguments: Filename (String) 

Return Value: 

|  |  |
| --- | --- |
| 0 | Success/File does not exist |
| -1 | Permission denied |
| -2 | File is open |


#### Description
The Delete operation takes as input a filename and deletes it. It returns with an error if any instance of the file is open in the system or if the file is not a DATA file. Delete command fails also if the file to be deleted does not belong to the current user and it has exclusive permissions. Otherwise, it deletes the root entry for the file name, invalidates the Inode Table entry for the file, releases the disk blocks allocated to the file and returns 0. 

<figure>
	<img src="http://exposnitc.github.io/img/roadmap/delete.png">
	<figcaption>Control flow diagram for *Delete* system call</figcaption>
</figure>
  
  

#### Algorithm

<pre><code>
Set the MODE_FLAG in the <a href="process_table.html">process table</a> entry to 4, 
indicating that the process is in the delete system call.

//Switch to Kernel Stack - See <a href="stack_smcall.html">Kernel Stack Management during System Calls</a>. 
Save the value of SP to the USER SP field in the <a href="process_table.html">Process Table</a> entry of the process.
Set the value of SP to the beginning of User Area Page.

Find the index of the file in the <a href="disk_ds.html#inode_table" target="_blank">Inode Table</a>.
		
If file is not present in the <a href="disk_ds.html#inode_table" target="_blank">Inode Table</a>, return 0. 

If the file is not a DATA file, return -1.

<b>If</b> the <a href="../os_spec-files/multiuser.html">exclusive permission</a> is set
	<b>if</b> the current user is not root and the current user does not own the file
		return -1. 

Acquire a lock on the file by calling the <b>acquire_inode()</b> function in the <a href="../os_modules/Module_0.html">Resource Manager</a> module.

Check if the the file open count is -1 in the <a href="./mem_ds.html#file_lock_status_table" target="_blank"> File Status Table </a>. If not, release the lock and return -2.    
/* File is open, cannot be deleted */

<b>For</b> each disk block allocated to the file, <b>do</b> { 	/* Check <a href="disk_ds.html#inode_table" target="_blank">Inode Table</a> */
	If the disk block is loaded into a buffer, and the DIRTY BIT is set, reset the dirty bit. 
	/* Check the <a href="../os_design-files/mem_ds.html#buffer_table">Buffer Table</a> */ 

	Call the <b>release_block()</b> function in the <a href="../os_modules/Module_2.html">Memory Manager</a> module to free the disk block.        
}

Invalidate (set to -1) the Inode Table of the file.

Update the <a href="disk_ds.html#root_file" target="_blank">Root file</a> by invalidating the entry for the file.

Release the lock on the file by calling the <b>release_inode()</b> function in the <a href="../os_modules/Module_0.html">Resource Manager</a> module.

Switch back to the user stack by reseting USER SP from the process table.
Set the MODE_FLAG in the <a href="process_table.html">process table</a> entry of the parent process to 0.

Return from system call with 0.    /* indicating success */

</code></pre>
  
!!! note
	At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.

!!! question "Question 1"
	Why are we not updating the [Open File Table](../os_design-files/mem_ds.html#file_table) when a file is being deleted?

!!! question "Question 2"
	Why can't an open file be deleted?

!!! question "Question 3"
	Why is the dirty bit in the buffer table cleared before the file is deleted?

!!! question "Question 4"
	Does disk blocks get freed anywhere else other than the delete system call?

