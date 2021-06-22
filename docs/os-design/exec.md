---
title: 'Exec System Call'
original_url: 'http://eXpOSNitc.github.io/os_design-files/exec.html'
hide: 
    - navigation
    - toc
---

### Arguments
File Name (String) of the executable file (which must be of [XEXE format](../abi.md#xexe))


### Return Value

|  |  |
| --- | --- |
| -1 | File not found or file is of invalid type |


### Description
Exec destroys the present process and loads the executable file given as input into a new memory address space. A successful Exec operation results in the extinction of the invoking process and hence never returns to it. All open instances of file and semaphores of the parent process are closed. However, the newly created process will inherit the PID of the calling process.

The data structures that are modified in this system call are [Process Table](process-table.md), [Memory Free List](mem-ds.md#mem_free_list), [Disk Free List](disk-ds.md#disk_free_list), [Open File Table](mem-ds.md#file_table), [Semaphore Table](mem-ds.md#sem_table), [System Status Table](mem-ds.md#ss_table), [Resource Table](process-table.md#per_process_table) and the [Disk Map Table](process-table.md#disk_map_table).

The mode flag in the [Process Table](process-table.md) has to be set to Kernel mode when the process enters the system call and reset before exiting from the system call.


  
<figure>
    <img src="http://exposnitc.github.io/img/roadmap/exec3.png">
    <figcaption>Control flow diagram for *Exec* system call</figcaption>
</figure>
 
  

### Algorithm
<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 9 indicate that the process is in exec system call.

//Switch to the Kernel Stack. see <a href="../../os-design/stack-smcall/">kernel stack management during system calls</a>
Save the value of SP to the USER SP field in the <a href="../../os-design/process-table/">Process Table</a> entry of the process.
Set the value of SP to the beginning of User Area Page.

/* Check for the file entry in <a href="../../os-design/disk-ds/#inode_table" target="_blank">Inode Table</a>. */
<b>If</b> filename is invalid, return -1.
<b>If</b> file not found in system or file type is not EXEC, return -1 

Call the exit_process() function in the <a href="../../modules/module-01/">Process Manager Module</a> to deallocate resources of the current process.

Reacquire the same User Area Page of the old process manually by incrementing 
the <a href="../../os-design/mem-ds/#mem_free_list">Mem Free List</a> and decrementing MEM_FREE_COUNT in the <a href="../../os-design/mem-ds/#ss_table">System Status Table</a>.

/* exit_process() in the previous step deallocated the user area page, and 
hence we immediately reclaim the page for loading the new program.  Since the page
storing the kernel context has been de-allocated, it is unsafe  
to invoke the memory manager module for allocating a fresh user area page (why?) */

Set SP to User Area Page Number * 512 - 1 /* Start fresh in the new kernel stack */

Initilize the <a href="../../os-design/process-table/#per_process_table">Per-process Resource Table</a> by setting all entries to -1.	

In the <a href="../../os-design/process-table/">Process Table</a> entry of the current process, set the Inode Index field to the 
index of Inode Table entry for the file and set the state as RUNNING.

Acquire two memory pages for user stack by invoking the <b>get_free_page()</b> function in the <a href="../../modules/module-02/">memory manager</a> module.

Obtain the disk block number of the first code page from the inode entry of the file passed as argument.

Load the first code page into memory by invoking the <b>get_code_page()</b> function in the <a href="../../modules/module-02/">Memory Manager module</a>.
	
<details class="code-accordion"><summary>Set the Page Table and Disk Map Table entries of the process.</summary>
                Set the Page Table entries for library. Set the valid bit to 1 and write bit to 0.
                /* Since the ExpL compler uses the library for even basic operations like read/write, 
                the library flag is ignored, and we link the library to all loaded programs */

                Invalidate the page table entries for heap. &nbsp;&nbsp; 
                /* Memory will be allocated when page fault occurs */

                Set the page table entry for the first code page to the 
                page loaded eariler. Set it's valid bit to 1 and write bit to 0.
		        Other code pages are set to invalid and unreferenced.

                Set the page table entry for the stack page to the 
                pages found earlier. Set the valid bit and write bit to 1.

                Set the code pages in the <a href="../../os-design/process-table/#disk_map_table">Disk Map Table</a> to the Block numbers by refering 
                to the <a href="../../os-design/disk-ds/#inode_table" target="_blank">Inode Table</a>. Other fields are set to -1.
</details>
Obtain the entry point IP value from the header of the new process and set it to the beginning  of user stack(logical address 4096).
Set SP to the logical address of the user stack.

Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to back to 0.

ireturn from system call to newly loaded process.
<code></pre>

!!! note
    At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.

