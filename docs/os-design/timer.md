---
title: 'Timer Interrupt Handler'
original_url: 'http://eXpOSNitc.github.io/os_design-files/timer.html'
hide: 
    - navigation
    - toc
---

The hardware requirement specification for eXpOS assumes that the machine is equipped
with a timer device that sends periodic hardware interrupts. 
The timer interrupt handler internally invokes the eXpOS  [scheduler module](../modules/module-05.md) . 
 
<figure>
    <img src="http://exposnitc.github.io/img/roadmap/timer_interrupt.png">
    <figcaption>Control flow diagram for *Timer interrupt handler*</figcaption>
</figure>


### Algorithm:

<pre><code>
Switch to the Kernel Stack. 	/* See <a href="../../os-design/stack-smcall/">kernel stack management during system calls</a> */
Save the value of SP to the USER SP field in the <a href="../../os-design/process-table/">Process Table</a> entry of the process.
Set the value of SP to the beginning of User Area Page.

Backup the register context of the current process using the <a href="../../arch-spec/instruction-set/">BACKUP</a> instruction.


<details class="code-accordion"><summary>/* This code is relevant only when the Pager Module is implemented in Stage 27 */</summary>
<b>If</b> swapping is initiated, /* check <a href="../../os-design/mem-ds/#ss_table">System Status Table</a> */
{
    /* Call Swap In/Out, if necessary */

    <b>if</b> the current process is the Swapper Daemon and Paging Status is <a href="../support-tools/constants/">SWAP_OUT</a>,
        Call the <b>swap_out()</b> function in the <a href="../../modules/module-06/">Pager Module</a>.

    <b>else if</b> the current process is the Swapper Daemon and Paging Status is <a href="../support-tools/constants/">SWAP_IN</a>, 
        Call the <b>swap_in()</b> function in the <a href="../../modules/module-06/">Pager Module</a>.

    <b>else if</b> the current process is Idle,                          
        /* Swapping is ongoing, but the daemon is blocked for some disk operation and idle is being run now */
        /* Skip to the end to perform context switch. */
    
}

<b>else</b>           /* Swapping is not on now.  Check whether it must be initiated */
{
    <b>if</b> (MEM_FREE_COUNT < <a href="../support-tools/constants/">MEM_LOW</a>)	 	/* Check the <a href="../../os-design/mem-ds/#ss_table">System Status Table</a> */
        /* Swap Out to be invoked during next Timer Interrupt */
        Set the Paging Status in System Status Table to <a href="../support-tools/constants/">SWAP_OUT</a>.

    <b>else if</b> (there are swapped out processes)            /* Check SWAPPED_COUNT in <a href="../../os-design/mem-ds/#ss_table">System Status Table</a> */
        <b>if</b> (Tick of any Swapped Out process > <a href="../support-tools/constants/">MAX_TICK</a> or MEM_FREE_COUNT > <a href="../support-tools/constants/">MEM_HIGH</a>)
            /* Swap In to be invoked during next Timer Interrupt */
            Set the Paging Status in System Status Table to <a href="../support-tools/constants/">SWAP_IN</a>.

}
/* End of Stage 27 code for Swap In/Out management */
</details>
    
Change the state of the current process in its Process Table entry from RUNNING to READY.

Loop through the process table entires and increment the TICK field of each process.

Invoke the <a href="../../modules/module-05/" target="_blank">context switch module </a>.

Restore the register context of the process using <a href="../../arch-spec/instruction-set/">RESTORE</a> instruction.

Set SP as the user SP saved in the Process Table entry of the new process.
Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 0.
             
ireturn.
</code></pre>