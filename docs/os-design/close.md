---
title: 'Close System Call'
original_url: 'http://eXpOSNitc.github.io/os_design-files/close.html'
hide:
    - navigation
    - toc
---


Arguments: File Descriptor (Integer) 

Return Value:

|  |  |
| --- | --- |
| 0 | Success |
| -1 | File Descriptor given is invalid |


#### Description 
The Close system call closes an open file. The file descriptor ceases to be valid once the close system call is invoked. 

<figure>
<img src="http://exposnitc.github.io/img/roadmap/close.png">
<figcaption>Control flow diagram for *Close* system call</figcaption>
</figure>
  
  

#### Algorithm
<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 3, 
indicating that the process is in the close system call.

//Switch to Kernel Stack - See <a href="../../os-design/stack-smcall/">Kernel Stack Management during System Calls</a>. 
Save the value of SP to the USER SP field in the <a href="../../os-design/process-table/">Process Table</a> entry of the process.
Set the value of SP to the beginning of User Area Page.

If file descriptor is invalid, return -1. &nbsp;&nbsp; /* File descriptor value should be within the range 0 to 7 (both included). */

Locate the Per-Process Resource Table of the current process.
	Find the PID of the current process from the <a href="../../os-design/mem-ds/#ss_table" target="_blank">System Status Table</a>.
	Find the User Area page number from the <a href="../../os-design/process-table/#per_process_table" target="_blank">Process Table </a>entry.
	The <a href="../../os-design/process-table/#per_process_table">Per-Process Resource Table</a> is located at the  <a href="constants.html" target="_blank">RESOURCE_TABLE_OFFSET</a> from the base of the <a href="../../os-design/process-table/#user_area" target="_blank"> User Area Page</a>

If the Resource identifier field of the <a href="../../os-design/process-table/#per_process_table" target="_blank">Per Process Resource Table</a> entry is invalid or does not indicate a <a href="constants.html" target="_blank">FILE</a>, return -1.   

/* No file is open with this file descriptor. */

Get the index of the <a href="../../os-design/mem-ds/#file_table" target="_blank">Open File Table</a> entry from Per-Process Resource Table entry.

Call the <b>close()</b> function in the <a href="../../modules/module-03/">File Manager module</a> with the Open File Table index as arguement.

Invalidate the <a href="../../os-design/process-table/#per_process_table" target="_blank">Per-Process Resource Table</a> entry.

Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 0.
Switch back to the user stack.

Return from system call with 0. &nbsp;&nbsp; /* success */
</code></pre>

!!! note
	At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.
  
!!! question "Question"
	Why did we not check if the file is locked?












































