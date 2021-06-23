---
title: 'Module 1: Process Manager'
original_url: 'http://eXpOSNitc.github.io/os_modules/Module_1.html'
---

This module contains functions that manage the different aspects related to processes.

| Function Number | Function Name | Arguments | Return Value |
| --- | --- | --- | --- |
| GET\_PCB\_ENTRY = 1 | Get Pcb Entry | NIL | Index of Free PCB.  |
| FREE\_USER\_AREA\_PAGE = 2 | Free User Area Page | PID | NIL |
| EXIT\_PROCESS = 3 | Exit Process | PID | NIL |
| FREE\_PAGE\_TABLE = 4 | Free Page Table | PID | NIL |
| KILL\_ALL = 5 | Kill All | PID | NIL |


![](../assets/img/modules/ProcessManager.png)

###  Get PCB entry
Returns a Free PCB index. Returns -1 if PCB is full.  

<pre><code>
loop through the <a href="../../os-design/process-table/">Process Table</a>{
        if ( process table entry is free )
            Set the PID to index of the entry
            Set the STATE to (ALLOCATED, - )
    Set PTBR to PAGE_TABLE_BASE + 20*index 	/* See <a href="../../os-implementation/#collapse2">Memory Organisation</a> */
    Set PTLR to 10. 						/* <a href="../../abi/">Address space</a> of processes in eXpOS has 10 pages */
    return index;
}

return -1;
</code></pre>


Called by Fork system call.


###  Free User Area Page
Frees all the resources in the Resource Table inside the User Area page. Also frees the User Area page.  

!!! note
    The function should be called only when no file/buffer/terminal resource is locked by the process.  
<pre><code>
/* If the user are page is swapped out, it has to be swapped back first. */

Get the User Area Page number from the <a href="../../os-design/process-table/">process table</a> entry
corresponding to the PID;

loop through the <a href="../../os-design/process-table/#per_process_table">Resource Table</a>{
        if ( the resource table entry is valid )
        if (the resource is a file)
                Close the corresponding file by calling the Close() function in the 
        <a href="../../modules/module-03/">File Manager</a> Module.
        if (the resource is a semaphore)
                Release the semaphore by calling the Release Semaphore() function in the 
        <a href="../../modules/module-00/">Resource Manager</a> Module.
        Invalidate the resource table entry.
}

Free the User Area page by calling the release_page()
function in the <a href="../../modules/module-02/">Memory Manager</a> module;
    
return;	
</code></pre>

!!! warning "Note"
    The user area page holding the return address for the call to free_user_area_page()  
    has been released! Neverthless the return address and the saved context of the calling process 
    will not be lost. This is because release_page() is non blocking and hence the page will never be 
    allocated to another process before control transfers back to the caller.  The calling function 
    gets "time" to either invoke the scheduler using the same stack page or to reallocate the same page 
    again for a different purpose.  

Called by the exit\_process function.




### Exit Process

Terminate the process whose PID is provided.  
  

!!! note
    The function should be called only when no file/terminal/disk/buffer resource is locked by the process.  
  

<pre><code>
<b>if</b> (the current process is not in the exec system call)	// check MODE_FLAG
{
    <b>loop</b> though the <a href="../../os-design/process-table/">process table</a> entries
{
        /* Wake up all processes waiting for the current process */
        <b>if</b>( process is waitng for the current process ) 		/* indicated by the STATE = (WAIT_PROCESS, PID ) */
        Set STATE of the process to (READY, - )
    /* Set the children of the process as Orphan */
    <b>if</b>( process has PPID as that of the current process)
        Set PPID to -1.
    }
}

Free the <a href="../../os-design/process-table/#per_page_table">Page Table</a> entry corresponding to the process by
invoking the Free_Page_Table() function; 

Free the User Area Page corresponding to the process by calling
the Free_User_Area_Page() function;  
/* After the User Area Page has been deallocated, the process is executing without a kernel stack.
    Hence the process should immmediately be scehduled out */

Set the state of process as (TERMINATED , - )

return;
/* Note that the return statement is executing using a deallocated stack page. See note after free_user_area_page() */ 
</code></pre>

Called by exec system call, exit system call, exception handler, shutdown and logout.

!!! question "Question"
    Why is the loop in the beginning not executed when called from exec system call?


###  Free Page Table

Free the page table entry and the used pages. The Disk Map table entries are also freed.  

<pre><code>
Invalidate the <a href="../../os-design/process-table/#per_page_table">page table</a> entries corresponding to the shared library pages;

loop through the other <a href="../../os-design/process-table/">page table</a> entries{
        if ( the entry is valid ){
            free the corresponding page by 
            invoking the release_page() function 
            in the <a href="../../modules/module-02/">Memory Manager module</a>;
        }
        Invalidate the page table entry;
}

Loop through the <a href="../../os-design/process-table/">Disk Map Table</a> entries of the process  
    if (the entry is valid and is stack or heap)
    call release_block() function in the <a href="../../modules/module-02/">Memory Manager</a> Module.
    set the entry to -1.
return;
</code></pre>

Called by the exit\_process function.

### Kill All
Kills all the processes except the current process, idle and init/login*.  

<pre><code>
/* Lock all files to ensure that no processes are in the middle of a file operation */
<b>For</b> each valid entry in the <a href="../../os-design/disk-ds/#inode_table">Inode table</a>	
	Acquire lock on the file by calling the <b>acquire_inode()</b> function in the <a href="../../modules/module-00/">Resource Manager</a> module.

<b>For</b> each pid from 2 to MAX_PROC_NUM - 1 	/* PID 0 is idle and 1 is init */
{
    /* This code is relevant only when the Pager Module is implemented in Stage 27 */
    <b>If</b> pid == PID of Swapper Daemon         /* Swapper Daemon must not be TERMINATED */
          continue;
    <b>If</b> pid != pid of the current process AND state of the process in the process table entry is not TERMINATED
	  Call <b>exit_process()</b> function from the <a href="../../modules/module-01/">Process Manager</a> Module.
}

<b>For</b> each valid entry in the Inode table
	Release lock on the file by calling the <b>release_inode()</b> function in the Resource Manager module.

return;
</code></pre>

Called by shutdown and logout system call.

!!! note
    The init process will be the login process in the multi user extension of eXpOS

