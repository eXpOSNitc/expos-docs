---
title: 'Module 0: Resource Manager'
original_url: https://eXpOSNitc.github.io/os_modules/Module_0.html
---

This module is responsible for allocating and releasing the different resources. Note that the Terminal and Disk devices are freed by the corresponding interrupt handlers.

| Function Number       | Function Name     | Arguments                  | Return Value                |
| --------------------- | ----------------- | -------------------------- | --------------------------- |
| ACQUIRE_BUFFER = 1    | Acquire Buffer    | Buffer Number, PID         | NIL                         |
| RELEASE_BUFFER = 2    | Release Buffer    | Buffer Number, PID         | 0 or -1                     |
| ACQUIRE_DISK = 3      | Acquire Disk*     | PID                        | NIL                         |
| ACQUIRE_INODE = 4     | Acquire Inode     | Inodeindex, PID            | 0 or -1                     |
| RELEASE_INODE = 5     | Release Inode     | Inodeindex, PID            | 0 or -1                     |
| ACQUIRE_SEMAPHORE = 6 | Acquire Semaphore | PID                        | Semaphore Table Index or -1 |
| RELEASE_SEMAPHORE = 7 | Release Semaphore | Semaphore Table Index, PID | 0 or -1                     |
| ACQUIRE_TERMINAL = 8  | Acquire Terminal  | PID                        | NIL                         |
| RELEASE_TERMINAL = 9  | Release Terminal  | PID                        | 0 or -1                     |

*Release function for the disk is implimented in the disk interrupt handler.

![](../assets/img/modules/ResourceManager.png)

### Acquire Buffer

_**Description**_: Acquire the buffer corresponding to buffer number given as input. Assumes a valid PID and a valid buffer number are given.  

<pre>
<code>
while ( Buffer is locked ){   /* Check the Locking PID field in the <a href="../../os-design/mem-ds/#buffer_table" target="_blank">Buffer Status Table</a> */
    Set state of the process as ( WAIT_BUFFER , Buffer Number );
    Call the <b>switch_context()</b> function from the <a href="../module-05/">Scheduler Module</a>.
}

Lock the Buffer by setting the PID of the current process in the Locking PID field
in the <a href="../../os-design/mem-ds/#buffer_table" target="_blank">Buffer Status Table</a> ;

return;
</code>
</pre>

Called by BufRead and BufWrite functions in the [File Manager](./module-03.md).

### Release Buffer

_**Description**_ : Release the buffer corresponding to buffer number given as input. Assumes a valid PID and a valid buffer number are given.  
  
<pre><code>
If PID given as input is not equal to the LOCKING PID in the <a href="../../os-design/mem-ds/#buffer_table" target="_blank">Buffer Status Table</a>, return -1.

Free the lock in the the <a href="../../os-design/mem-ds/#buffer_table" target="_blank">Buffer Status Table</a> entry corresponding to 
the buffer Number; /* Set Locking PID field to -1 */
loop through the process table{ 
       if (the process state is ( WAIT_BUFFER , Buffer Number ) ){
             Set state of process as (READY , _ )
         } 
}
return 0;
</code></pre>

Called by BufRead and BufWrite functions in the [File Manager](./module-03.md).

### Acquire Disk

_**Description**_ : Locks the disk device. Assumes that a valid PID is given as input.  

<pre><code>
while ( disk is locked ){  /* Check the <i>Status</i> field in the <a href="../../os-design/mem-ds/#ds_table" target="_blank">Disk Status Table</a>. */
    Set state of the process as ( WAIT_DISK , - );
    Call the <b>switch_context()</b> function from the <a href="../module-05/">Scheduler Module</a>.
}

Lock the disk by setting PID and the status field in the <a href="../../os-design/mem-ds/#ds_table" target="_blank">Disk Status Table.</a>

return;
</code></pre>

Called by BufRead and BufWrite functions in the [File Manager](./module-03.md) and the exception handler for swap-in.

### Acquire Inode

_**Description**_ : Locks the Inode entry corresponding to the inodeindex given as input. Assumes a valid PID and a valid inode index are given.  
  
<pre><code>
while ( inode is locked ){   /* Check the Lock field in the <a href="../../os-design/mem-ds/#file_lock_status_table" target="_blank">File Status Table</a>. */
    Set state of the process as ( WAIT_FILE , Inode Index );
    Call the <b>switch_context()</b> function from the <a href="../module-05/">Scheduler Module</a>.
} 

If inode becomes invalid, return -1. /* File was deleted by the time the inode was acquired */

Lock the Inode by setting the Lock field in the <a href="../../os-design/mem-ds/#file_lock_status_table" target="_blank">File Status Table</a> 
to the PID of the current process.;

return 0;
</code></pre>

Called by Delete, Read, Write and Seek system calls.

### Release Inode

_**Description**_ : Frees the lock of the inode entry corresponding to the inodeindex given as input. Assumes a valid PID and a valid inode index are given.  
  
<pre><code>
If PID given as input is not equal to the LOCKING PID in the <a href="../../os-design/mem-ds/#file_lock_status_table" target="_blank">File Status Table</a>, return -1.

Free the lock in the File Status Table corresponding to the inode index;       /* Set the Lock field to -1 */

loop through the process table{ 
       if (the process state is ( WAIT_FILE, Inode Index ) ){
             Set state of process as (READY , _ )
         } 
}
return 0;
</code></pre>
Called by Read, Write and Seek system calls.

### Acquire Semaphore

_**Description**_ : Acquires a semaphore and returns it's semaphore number. Assumes a valid PID is given as input. Returns -1 upon failure.  

<pre> <code>
Find the index of a free entry in <a href="../../os-design/mem-ds/#semaphore-table" target="_blank">Semaphore table</a>. If no free entry, return -1.
/* Free entry is indicated by a Process Count of 0. */ 

Set the PROCESS_COUNT to 1 and LOCKING_PID to -1.

Return the Semaphore table index. /* success */
</code></pre>

Called by the [Semget system call](../os-design/semaphore-algos.md#semget).

### Release Semaphore

_**Description**_ : Releases a semaphore. Assumes a valid PID and semaphore table index are given as input.  
  
<pre><code>
If ( semaphore is locked by the current process) /*Check the Locking PID in the <a href="../../os-design/mem-ds/#semaphore-table" target="_blank">Semaphore table</a>*/
	Set the Locking PID to -1. /* Unlock the semaphore before release */
	loop through the process table{ /*wake up processes blocked by the semaphore */
       		if (the process state is ( WAIT_SEMAPHORE, SEMTABLEINDEX ) ){
             	Set state of process as (READY , _ )
         	} 
	}

Decrement the process count of the semaphore in the semaphore table.
/* When the count becomes 0, the semaphore is free. */

</code></pre>
	     
Called by the [Semrelease](../os-design/semaphore-algos.md#semrelease) and exit system call.

### Acquire Terminal

_**Description**_ : Locks the Terminal device. Assumes a valid PID is given as input.  
  

<pre><code>
while ( Terminal device is locked ){    /* Check the Status field in the <a href="../../os-design/mem-ds/#ts_table" target="_blank">Terminal Status Table</a> */
    Set state of the process as ( WAIT_TERMINAL , - );
    Call the <b>switch_context()</b> function from the <a href="../module-05/">Scheduler Module</a>.
}
    
Lock the Terminal device by setting the Status and PID fields in the <a href="../../os-design/mem-ds/#ts_table" target="_blank">Terminal Status Table</a>.

return;
</code></pre>
Called by the Terminal Read and Terimnal Write functions of the [Device Manager Module](./module-04.md).

### Release Terminal

_**Description**_ : Frees the Terminal device. Assumes a valid PID is given as input.  

<pre><code>
If PID given as input is not equal to the LOCKING PID in the <a href="../../os-design/mem-ds/#ts_table">Teminal Status Table</a>, return -1.

    Release the lock on the Terminal by updating the Terminal Status Table.;

    loop through the process table{ 
       if (the process state is ( WAIT_TERMINAL , - ) ){
             Set state of process as (READY , _ )
         } 
    }

    Return 0
 
</code></pre>

Called by the Terimnal Write function in the [Device Manager Module](./module-04.md).