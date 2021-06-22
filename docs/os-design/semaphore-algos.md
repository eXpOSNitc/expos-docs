---
title: 'Semaphore System Calls'
original_url: 'http://eXpOSNitc.github.io/os_design-files/semaphore_algos.html'
hide:
    - navigation
---

### Semget system call
#### Argument
None

#### Return Value 

| Value | Description |
| --- | --- |
| SEMID (Integer)  | Success, returns a semaphore descriptor(SEMID) |
| -1 | Process has reached its limit of resources  |
| -2 | Number of semaphores has reached its maximum |


#### Description
This system call is used to obtain a binary [semaphore](https://en.wikipedia.org/wiki/Semaphore_(programming)). eXpOS has a fixed number of semaphores.
The semaphores of a process are shared with it's child processes. Data Structures updated are [Per Process Resource Table](process-table.md#per_process_table) and [Semaphore table](mem-ds.md#sem_table).

The mode flag in the [Process Table](process-table.md) has to be set to Kernel mode when the process enters the system call and must be reset before exiting from the system call.

<figure>
    <img src="http://exposnitc.github.io/img/roadmap/semget.png">
    <figcaption>Control flow diagram for *Semget* system call</figcaption>
</figure>

#### Algorithm


<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/" target="_blank">Process Table</a> to 17 and <a href="../../os-design/stack-smcall/">switch</a> to kernel stack.

Find the index of a free entry in the <a href="../../os-design/process-table/#per_process_table" target="_blank">Per Process Resource Table</a>. /* This will be our semaphore descriptor */
If no free entry, then return -1.

Resource Identifier field of the per-process resource table entry is set to 1 to indicate that the resource is a semaphore.

Acquire a semaphore by calling the <b>acquire_semaphore()</b> function in the <a href="../../modules/module-00/">Resource Manager</a> Module.

/* acquire_semaphore() module function acquires a semaphore by making an entry in the <a href="../../os-design/mem-ds/#sem_table">Semaphore Table</a> and 
returns the index of the entry. If there are no free semaphores, it returns -1 */

If there are no free semaphores, return -2.
             
Store the index of the Semaphore table entry in the Per Process Resource Table entry.   /*Attach the semaphore to the process.*/
             
Switch back to the user stack by resoring the USER SP from the process table.

Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry of the parent process to 0.

Return the Per-process Resource Table entry index.   /* Semaphore Descriptor */

</code></pre>

!!! note
    At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.



### Semrelease system call

#### Arguments
Semaphore Descriptor (Integer)

#### Return Value

|  |  |
| --- | --- |
| 0 | Success |
| -1 | Semaphore Descriptor is invalid |


#### Description
This system call is used to release a semaphore descriptor held by the process. Data Structures updated are [Per Process Resource Table](process-table.md#per_process_table) and [Semaphore table](mem-ds.md#sem_table). The mode flag in the [Process Table](process-table.md) has to be set to Kernel mode when the process enters the system call and reset before exiting from the system call.


  

<figure>
    <img src="http://exposnitc.github.io/img/roadmap/semrelease.png">
    <figcaption>Control flow diagram for *Semrelease* system call</figcaption>
</figure>
  

#### Algorithm

<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/" target="_blank">Process Table</a> to 18 and <a href="../../os-design/stack-smcall/">switch</a> to kernel stack.

<b>If</b> Semaphore descriptor is not valid or the entry in the <a href="../../os-design/process-table/#per_process_table" target="_blank">Per Process Resource Table</a> is not valid, return -1. 
/* The descriptor is invalid if not in the range 0 - 7, or if the resource identifier field of the table entry is not 1 */

Invoke the release_semaphore() function in the <a href="../../modules/module-00/">Resource Manager</a> Module.
             
Invalidate the Per-Process resource table entry.   /* Set to -1 */ 
               
Switch back to the user stack by restoring the USER SP from the process table.

Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry of the parent process to 0.

Return 0.
</code></pre>

!!! note
    At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.

### SemLock system call


#### Arguments
Semaphore Descriptor (Integer)


#### Return Value

|  |  |
| --- | --- |
| 0 | Success or the semaphore is already locked by the current process |
| -1 | Semaphore Descriptor is invalid |


#### Description
This system call is used to lock the semaphore. If the semaphore is already locked by some other process, then the calling process goes to sleep and wakes up only when the semaphore is unlocked. Otherwise, it locks the semaphore and continues execution. Data Structures updated are [Process Table](process-table.md) and [Semaphore table](mem-ds.md#sem_table).


The mode flag in the [Process Table](process-table.md) has to be set to Kernel mode when the process enters the system call and reset before exiting from the system call.


  

#### Algorithm
<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/" target="_blank">Process Table</a> to 19 and <a href="../../os-design/stack-smcall/">switch</a> to kernel stack.

<b>If</b> Semaphore descriptor is not valid or the entry in the <a href="../../os-design/process-table/#per_process_table" target="_blank">Per Process Resource Table</a> is not valid, return -1. 
/* The descriptor is invalid if not in the range 0 - 7, or if the resource identifier field of the table entry is not 1 */
             
<b>while</b> the semaphore is locked by a process other than the current process <b>do</b>    /* Check the Locking PID field in the <a href="../../os-design/mem-ds/#sem_table" target="_blank">Semaphore table</a> */
              Change the <a href="../../os-design/process-table/#state" target="_blank">state</a> of the current process to (<a href="constants.html" target="_blank">WAIT_SEMAPHORE</a>, Semaphore table index of the locked semaphore).
              Invoke the <b>switch_context()</b> function in the <a href="../../modules/module-05/">Scheduler Module</a>.
<b>endwhile</b>

/* Reaches here when the semaphore becomes free for locking */

Change the Locking PID to PID of the current process in the <a href="../../os-design/mem-ds/#sem_table" target="_blank">Semaphore Table </a>.

Reset the mode flag in the <a href="../../os-design/process-table/" target="_blank">Process Table</a> to 0 and switch back to the user stack.

Return 0.   /* success */

</code></pre>

!!! note
    At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.


### SemUnLock system call


#### Arguments
Semaphore Descriptor (Integer)


#### Return Value




|  |  |
| --- | --- |
| 0 | Success |
| -1 | Semaphore Descriptor is invalid |
| -2 | Semaphore was not locked by the calling process |


#### Description
This system call is used to unlock a semaphore that was previously locked by the calling process. It wakes up all the processes which went to sleep trying to lock the semaphore while the semaphore was locked by the calling process. Data Structures updated are [Process Table](process-table.md) and [Semaphore table](mem-ds.md#sem_table). 


The mode flag in the [Process Table](process-table.md) has to be set to Kernel mode when the process enters the system call and reset before exiting from the system call.


#### Algorithm

<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/" target="_blank">Process Table</a> to 20 and <a href="../../os-design/stack-smcall/">switch</a> to kernel stack.

<b>If</b> Semaphore descriptor is not valid or the entry in the <a href="../../os-design/process-table/#per_process_table" target="_blank">Per Process Resource Table</a> is not valid, return -1. 
/* The descriptor is invalid if not in the range 0 - 7, or if the resource identifier field of the table entry is not 1 */
         
<b>If</b> semaphore is locked. /* Check the Locking PID in the <a href="../../os-design/mem-ds/#sem_table">Semaphore table</a> */

              <b>If</b> current process has not locked the semaphore, return -2.   /* The semaphore is locked by some other process.*/

              Set the Locking PID to -1.   /* Unlock the semaphore. */

              Loop through the process table and change the <a href="../../os-design/process-table/#state">state</a> to (READY, _ ) for all the processes 
	      in the state (<a href="constants.html" target="_blank">WAIT_SEMAPHORE</a>, Semaphore table index of the locked semaphore). 

Reset the MODE_FLAG in the <a href="../../os-design/process-table/" target="_blank">Process Table</a> to 0 and switch back to the user stack. 

Return 0.   /* success */
</code></pre>

!!! note
    At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.