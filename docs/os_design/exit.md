---
title: 'Exit system call'
original_url: 'http://eXpOSNitc.github.io/os_design-files/exit.html'
---

### Arguments
None

### Return Value
None

### Description
Exit system call terminates the execution of the process which invoked it and destroys its memory address space. The calling application ceases to exist after the system call and hence the system call never returns.

Data structures modified are [Memory Free List](mem_ds.html#mem_free_list), [Disk Free List](disk_ds.html#disk_free_list), [Open File Table](mem_ds.html#file_table), [Semaphore Table](mem_ds.html#sem_table), [System Status Table](mem_ds.html#ss_table), [Resource Table](process_table.html#per_process_table) and the [Disk Map Table](process_table.html#disk_map_table).


![](../img/roadmap/exit.png)
Control flow diagram for *Exit* system call
  

### Algorithm

<pre><code>
Set the MODE_FLAG in the <a href="process_table.html">process table</a> entry to 10.

//Switch to the Kernel Stack. see <a href="stack_smcall.html">kernel stack management during system calls</a>
Save the value of SP to the USER SP field in the <a href="process_table.html">Process Table</a> entry of the process.
Set the value of SP to the beginning of User Area Page.

Invoke the <b>exit_process()</b> function from the <a href="../os_modules/Module_1.html">Process Manager</a> module.

/* exit_process() releases all the memory pages of the process including the page holding kernel stack.
Still, as exit_process is non-blocking, the kernel stack page will not be allocated to another process.
This makes it possible to make a final call from the process to the scheduler. There is no return to
the process after the following scheduler invocation. */ 

Invoke the <b>context_switch()</b> function in the <a href="../os_modules/Module_5.html">Scheduler Module</a>.
	
</code></pre>  