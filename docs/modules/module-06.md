---
title: 'Module 6: Pager Module'
original_url: 'http://eXpOSNitc.github.io/os_modules/Module_6.html'
---

This module is responsible for swapping in and out processes. Swap-out is initiated from the timer interrupt when the free memory is critically low. Similiarly, if there is enough memory available in the system, swap-in is initiated by the timer.

| Function Number | Function Name | Arguments | Return Value |
| --- | --- | --- | --- |
| SWAP\_OUT = 1 | Swap Out | PID | NIL |
| SWAP\_IN = 2 | Swap In | PID | NIL |

<img src="http://exposnitc.github.io/img/os-modules/Pager.png">

### Swap Out

#### Description
Invoked when the physical memory is critically low. The function chooses a process to swap out, and free it's memory by moving it to the disk. PID of the currently running process is passed as an argument.  


<figure>
<img src="http://exposnitc.github.io/img/roadmap/swap_out.png">
<figcaption>Control flow diagram for *Swap Out*</figcaption>
</figure>

<pre><code>
Choose a process to swap out. (other than the IDLE, Shell or INIT)
	Loop through the <a href="../os_design-files/process_table.html">Process Table</a> and find a non-swapped process that is in the WAIT_PROCESS state.
	If there are no non-swapped processes in the WAIT_PROCESS state, find a non-swapped process in the WAIT_SEMAPHORE state.
	If there are no non-swapped processes in the WAIT_PROCESS and WAIT_SEMAPHORE state, 
            find process with the highest TICK which is not running, terminated, allocated or swapped.

If no such process exists, 
        set the PAGING_STATUS back to 0 and return.

Set the TICK field of the process table entry of the selected process to 0.
/* When the process goes to swap, TICK starts again */

Call the <b>release_page()</b> function in the <a href="../os_modules/Module_2.html">Memory Manager</a> module to deallocate the valid code pages of the process.
Invalidate the <a href="../os_design-files/process_table.html#per_page_table">Page table</a> entry correpsonding to the code pages.

<b>For</b> each heap page that is not shared and is valid {	/* Shared heap pages are not swapped out. */
	Get a free swap block by calling the <b>get_swap_block()</b> function in the <a href="../os_modules/Module_2.html">Memory Manager</a> module.
	Store the disk block number in the <a href="../os_design-files/process_table.html#disk_map_table">Disk Map Table</a> entry of the process curresponding to the heap page.
	Use the <b>disk_store()</b> function in the <a href="../os_modules/Module_4.html">Device Manager</a> module to write the heap page to the block found above
	Call the <b>release_page()</b> function in the <a href="../os_modules/Module_2.html">Memory Manager</a> module to deallocate the page.
	Invalidate the Page table entry correpsonding to the page.
}

Get two free swap block by calling the <b>get_swap_block()</b> function in the <a href="../os_modules/Module_2.html">Memory Manager</a> module.

Use the <b>disk_store()</b> function in the <a href="../os_modules/Module_4.html">Device Manager</a> module to write the two stack pages to the disk blocks found above.

Call the <b>release_page()</b> function in the <a href="../os_modules/Module_2.html">Memory Manager</a> module to deallocate the two pages.

Update the Disk Map Table entry of the process to store the disk block numbers of the stack.

Invalidate the Page table entries correpsonding to the two stack pages.

Set the SWAP_FLAG field in the process table entry of the process to 1.

In the <a href="../os_design-files/mem_ds.html#ss_table">System Status Table</a>, increment the SWAP_COUNT and reset the PAGING_STATUS back to 0.	
/* The scheduler can now resume normal scheduling */ 

return;
</code></pre>

Called by the timer interrupt.  
  

!!! question
	What is the reasoning behind the order of choosing the process to swap out? Why is a process in WAIT\_PROCESS swapped out ahead of a process waiting for the terminal? What about processes waiting for the disk?   

  
  

### Swap In


#### Description 
Invoked when the physical memory is high enough that a process can be swapped in. If a suitable process is found, it is loaded back to the main memory. PID of the currently running process is passed as an argument.  

<figure>
<img src="http://exposnitc.github.io/img/roadmap/swap_in.png">
<figcaption>Control flow diagram for *Swap In*</figcaption>
</figure>
  
  
<pre><code>
/* Find if any swapped out process can be made ready to run if brought into memory. */
Loop through the <a href="../os_design-files/process_table.html">Process Table</a> and find the <b>swapped</b> process in the READY state with the highest TICK.
If there is no such process in the READY state, reset the PAGING_STATUS field to 0 and Return.

Set the TICK field of the process table entry of the selected process to 0.

<b>For</b> each heap page that is swapped out {	/* Check the <a href="../os_design-files/process_table.html#disk_map_table">Disk Map Table</a>. */
	Call the <b>get_free_page()</b> function in the <a href="../os_modules/Module_2.html">Memory Manager</a> module to allocate a memory page.
	Get the disk block number in the <a href="../os_design-files/process_table.html#disk_map_table">Disk Map Table</a> entry of the process corresponding to the heap page.
	Use the <b>disk_load()</b> function in the <a href="../os_modules/Module_4.html">Device Manager</a> module to copy the heap page found above to the memory.
	Free the swap block by calling the <b>release_block()</b> function in the <a href="../os_modules/Module_2.html">Memory Manager</a> module.
	Set the Page table entry correpsonding to the page. Reference bit is set to 0, valid bit and write bit are set to 1.
    Invalidate the Disk Map Table entry corresponding to the heap page.
}

Get two free memory pages by calling the <b>get_free_page()</b> function in the <a href="../os_modules/Module_2.html">Memory Manager</a> module.

Use the <b>disk_load()</b> function in the <a href="../os_modules/Module_4.html">Device Manager</a> module to load the two stack pages to the memory allocated above.

Set the Page table entries correpsonding to the two stack pages. The pages are valid, unreferenced and writable.

Call the <b>release_block()</b> function in the <a href="../os_modules/Module_2.html">Memory Manager</a> module to deallocate the two swap blocks.

Invalidate the Disk Map Table entry of the process corresponding to the pages.

Set the SWAP_FLAG field in the process table entry of the process to 0.

In the <a href="../os_design-files/mem_ds.html#ss_table">System Status Table</a>, decrement the SWAP_COUNT and reset the PAGING_STATUS back to 0.	
/* The scheduler can now resume normal scheduling */ 

return;
</code></pre>


Called by timer interrupt.  
  

!!! question "Question 1" 
	Is it possible that there are processes waiting for memory, even when MEM\_FREE\_COUNT > MEM\_HIGH? 

!!! question "Question 2"
	Why are code pages not loaded back to memory when the process is swapped in?
  
  


  