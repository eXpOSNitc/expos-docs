---
title: 'Module 5: Context Switch Module (Scheduler Module)'
original_url: https://eXpOSNitc.github.io/os_modules/Module_5.html
hide:
    - toc
---

Yields control from the current process and schedules the next process for execution.

|Function Number|Function Name|Arguments|
|--- |--- |--- |
| -  | Switch Context | Nil |

#### Switch Context

<pre><code>
Get the pid of the current process from <a href="../../os-design/process-table/">System Status Table</a>;

Push the BP register of the current process to the top of it's kernel stack. 
/* The ExpL application does not push the Base Pointer register (BP). See <a href="https://silcnitc.github.io/run_data_structures/run-time-stack.html">ExpL calling conventions</a>. 
Hence it is saved to the stop of the Kernel Stack */

Save the SP%512, PTBR and PTLR to the Kernel SP, PTBR and PTLR fields of the 
<a href="../../os-design/process-table/">Process Table</a> entry of the current process;  

<b>if</b> (PAGING_STATUS in the <a href="../../os-design/mem-ds/#ss_table">System Status Table</a> is not 0) /* Paging is ongoing */
    <b>If</b> the paging process is blocked     /* the paging process is executing a disk operation */
        Choose <a href="../../os-design/misc/#idle">Idle Process</a> for scheduling.
    <b>else</b>
        Choose the Swapper Daemon to be scheduled.
<b>else</b>
{
        Find the next non swapped process to schedule using the <a href="https://en.wikipedia.org/wiki/Round-robin_scheduling">Round Robin scheduling</a> technique, 
        excluding the Swapper Daemon;
        /* Check the SWAP_FLAG in the process table */
            If no process (that is not swapped out) is in  READY or CREATED state, select the Idle process;
}

Set the PTBR and PTLR registers to the corresponding values in the process table entry
of the new process;

Set the new PID in the System Status Table;

if (the new Process is in CREATED state){ 		/* The process has just been forked from a parent process */

        Set SP to the value of UserSP field in the Process table entry of the new process;
    Set BP to the value stored at the beginning of the kernel stack.	
    /* BP value of the process is saved to the beginning of the kernel stack by Fork() system call at process creation. */

        Set the state of the new process as (RUNNING, - );

    Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry 0.
        Use ireturn statement to transfer control back to user mode;
}

Set the state of the new process as (RUNNING, - );

Read the KPTR field and the UArea Page number from the Process table entry of the
new process;

Set SP to UArea_Page * 512 + KPTR;

Restore the BP register of the new process from the top of it's kernel stack.

return;
</code></pre>