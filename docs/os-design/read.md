---
title: 'Read System Call'
original_url: 'http://eXpOSNitc.github.io/os_design-files/read.html'
hide: 
    - navigation
    - toc
---

### Arguments
File Descriptor(Integer) and a Buffer (a String/Integer variable) into which a word is to be read from the file


### Return Value

|  |  |
| --- | --- |
| 0 | Success |
| -1 | File Descriptor given is invalid |
| -2 | File pointer has reached the end of file |

### Description
The Read operation reads one word from the position pointed by the file pointer and stores it into the buffer. After each read operation, the file pointer advances to the next word in the file.

<figure>
	<img src="http://exposnitc.github.io/img/roadmap/FileRead.png">
	<figcaption>Control flow diagram for *Read* system call</figcaption>
</figure>

  
  

### Algorithm


<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 7, 
indicating that the process is in the read system call.

//Switch to Kernel Stack - See <a href="../../os-design/stack-smcall/">Kernel Stack Management during System Calls</a>. 
Save the value of SP to the USER SP field in the <a href="../../os-design/process-table/">Process Table</a> entry of the process.
Set the value of SP to the beginning of User Area Page.

<b>If</b> input is to be read from terminal    /* indicated by a file descriptor value of -1 */
	Call the <b>terminal_read()</b>function in the <a href="../../modules/module-04/" target="_blank">Device manager </a> Module .
			 
/* If not terminal, read from file. */
<b> else </b>

	If file descriptor is invalid, return -1.    /* File descriptor value should be within the range 0 to 7 (both included). */

	<details class="code-accordion"><summary>Locate the Per-Process Resource Table of the current process.</summary>
                Find the PID of the current process from the <a href="../../os-design/mem-ds/#ss_table" target="_blank">System Status Table</a>.
                Find the User Area page number from the <a href="../../os-design/process-table/#per_process_table" target="_blank">Process Table</a> entry.
                The  <a href="../../os-design/process-table/#per_process_table">Per-Process Resource Table</a> is located at the  <a href="constants.html" target="_blank">RESOURCE_TABLE_OFFSET</a> from the base of the <a href="../../os-design/process-table/#user_area" target="_blank"> User Area Page </a>.
	</details>
	If the Resource identifier field of the <a href="../../os-design/process-table/#per_process_table" target="_blank">Per Process Resource Table</a> entry is invalid or does not indicate a <a href="constants.html" target="_blank">FILE</a>, return -1.  
	/* No file is open with this file descriptor. */

	Get the index of the <a href="../../os-design/mem-ds/#file_table" target="_blank">Open File Table</a> entry from the Per Process Resource Table entry.

	Get the index of the <a href="../../os-design/disk-ds/#inode_table" target="_blank">Inode Table</a> entry from the Open File Table entry. 
	
	Acquire the Lock on the File by calling the <b>acquire_inode()</b> function in the <a href="../../modules/module-00/" target="_blank">Resource Manager</a> module.
	If acquiring the inode fails, return -1.

	Get the Lseek position from the Open File Table entry.
      
	Get the physical address curresponding to the logical address of Memory Buffer address given as input.

	<b>If</b> the File corresponds to Root file ( indicated by Inode index as INODE_ROOT)  
                  If the lseek value is equal to the root file size(480), <b>release_inode()</b> return -2. 

                  Read from the word at lseek position in memory copy of <a href="../../os-design/disk-ds/#root_file">root file</a> to the translated memory address. 
		  		  /* Use SPL Constant <a href="../support_tools-files/constants.html ">ROOT_FILE</a> */

                  Increment the Lseek position in the Open File Table.        
	<b> else </b>
		<b>If</b> lseek position is same as the file size, <b>release_inode()</b> and return -2.  /* End of file reached */

		<details class="code-accordion"><summary>Find the disk block number and the position in the block from which input is read.</summary>
			Get the block index from lseek position.   /* lseek/512 gives the index of the block */
			Get the disk block number corresponding to the block index from the <a href="../../os-design/disk-ds/#inode_table" target="_blank">Inode Table</a> .
            Get the offset value from lseek position.   /* lseek%512 gives the position to be read from.*/
      	</details>
		Read the data from the File Buffer by calling the <b>buffered_read()</b> function in the <a href="../../modules/module-03/" target="_blank">File Manager</a> module.

		Increment the Lseek position in the Open File Table.

	Release the Lock on the File by calling the <b>release_inode()</b> function in the <a href="../../modules/module-00/" target="_blank">Resource Manager</a> module.

Switch back to the user stack by resoting USER SP from the process table.
Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry of the parent process to 0.

Return 0.   /* success */

</code></pre>

!!! warning "Note"
	At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.





















