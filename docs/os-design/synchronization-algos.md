---
title: 'System calls for Synchronization'
original_url: 'http://eXpOSNitc.github.io/os_design-files/synchronization_algos.html'
hide:
    - toc
---



### Wait system call

#### Arguments
Process Identifier of the process for which the current process has to wait.

#### Return Values

|  |  |
| --- | --- |
| 0 | Success |
| -1 | Given process identifier is invalid or it is the pid of the same process invoking wait |


#### Description
The current process is blocked till the process with PID given as argument
executes a Signal system call or exits. The system call will fail if a process attempts to wait for itself. The only data structure updated is [Process Table](process-table.md). The mode flag in the [Process Table](process-table.md) has to be set to Kernel mode when the process enters the system call and reset before exiting from the system call. 

#### Algorithm

<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 13.

Switch to the Kernel Stack. 	/* See <a href="../../os-design/stack-smcall/">kernel stack management during system calls</a> */
Save the value of SP to the USER SP field in the <a href="../../os-design/process-table/">Process Table</a> entry of the process.
Set the value of SP to the beginning of User Area Page.

<b>If</b> process is intending to wait for itself or for a non-existent process, return -1.    /* Check the status from Process table.  */ 
           
Change the status from (RUNNING,_ ) to (WAIT_PROCESS, Argument_PID ) in the <a href="../../os-design/process-table/" target="_blank">Process Table</a>.
             
Invoke the Scheduler by calling the <b>switch_context()</b> function in the <a href="../../modules/module-05/">Scheduler Module</a>.

/* The following code excutes only when scheduled again after the occurance of a signal/exit of the process waiting for. */

Restore SP to the USER SP stored in the process table.

Reset the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 0.

Return 0.  /* Success */
	
<b>Note: </b> At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.
</code></pre> 




### Signal system call

#### Arguments
None

#### Return Value: 

|  |  |
| --- | --- |
| 0 | Success |


#### Description
All processes waiting for the signalling process are resumed. The system call does not fail. The only data structure updated is [Process Table](process-table.md).The mode flag in the [Process Table](process-table.md) has to be set to Kernel mode when the process enters the system call and reset before exiting from the system call.

#### Algorithm

<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 14.

Wake up all processes waiting for the current process.
    Traverse through the <a href="../../os-design/process-table/" target="_blank">Process Table</a>
	    <b>If</b> the process is in state (<a href="constants.html" target="_blank">WAIT_PROCESS</a>, Pid) where Pid matches with the PID of the current process.
          	Change the status to (<a href="constants.html" target="_blank">READY</a>, _ ).

Reset the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 0.

Return 0.   /* Success */
</code></pre>