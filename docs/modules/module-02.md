---
title: 'Module 2: Memory Manager'
original_url: http://exposnitc.github.io/os_modules/Module_2.html
---

This module handles allocation and deallocation of memory pages. The memory free list entry denotes the number of processes using(sharing) the memory page. Unused pages are therefore indicated by 0 in the corresponding entry in memory free list.

| Function Number    | Function Name  | Arguments         | Return Value            |
| ------------------ | -------------- | ----------------- | ----------------------- |
| GET_FREE_PAGE = 1  | Get Free Page  | NIL               | Free Page number        |
| RELEASE_PAGE = 2   | Release Page   | Page Number       | NIL                     |
| GET_FREE_BLOCK = 3 | Get Free Block | NIL               | Free Block Number or -1 |
| RELEASE_BLOCK = 4  | Release Block  | Block Number, PID | NIL                     |
| GET_CODE_PAGE = 5  | Get Code Page  | Block Number      | Page Number             |
| GET_SWAP_BLOCK = 6 | Get Swap Block | NIL               | Block Number            |


![](../assets/img/modules/MemoryManager.png)

### Get Free Page
Returns the page number of a free page.

<pre><code>
Increment WAIT_MEM_COUNT field in the <a href="../../os-design/mem-ds/#system-status-table">System Status Table</a>

while ( memory is full ){   /* Check the MEM_FREE_COUNT in the System Status Table */

        Set state of the process as ( WAIT_MEM , ____);
        Call the <b>switch_context()</b> function from the <a href="../../modules/module-05/">Scheduler Module</a>.
}

// There is a free page available for use.
Decrement the WAIT_MEM_COUNT field and decrement the MEM_FREE_COUNT field in the System Status Table.

loop through entries in the <a href="../../os-design/mem-ds/#memory-free-list">Memory Free List</a>{
/* Available pages for user processes are from 76- 127. See <a href="../../os-implementation/">Memory Organisation</a>. */
    if ( a free entry is found ){
            Set the Memory Free List entry as 1;
            Return the corresponding page number;
    }
}
</code></pre>

Called by fork and exec system calls. Also called by exception handler on page fault. 

### Release Page 
Decrements the entry corresponding to page in memory free list.

<pre><code>
Decrement the entry corresponding to the page in the <a href="../../os-design/mem-ds/#memory-free-list">Memory Free List</a>;

<b>If</b> Mem Free List entry becomes 0, increment the MEM_FREE_COUNT field in the <a href="../../os-design/mem-ds/#system-status-table">System Status Table</a>

loop through the process table{ 
    if (the process state is ( WAIT_MEM , _ ) ){
        Set state of process as (READY , _ )
    }
}

return;
</code></pre>
Called by the Free page table and Free UArea Page functions.

!!! note
    Do not clear the contents of the page. A page may be shared by multiple processes and a call to release may not make the page free.

### Get Free Block
Returns the block number of a free disk block. Returns -1 if disk is full.

<pre><code>
loop through entries in the <a href="../../os-design/disk-ds/#disk-free-list">Disk Free List</a> from <a href="../../support-tools/constants/">DISK_FREE_AREA</a> to <a href="../../support-tools/constants/">DISK_SWAP_AREA</a> - 1{ 	/* User Block, not preallocated to the OS or swap area */
    if ( a free entry is found ){
            Set the Disk Free List entry as 1;
            Return the corresponding block number;
    }
}
return -1;
</code></pre>

###  Release Block
Decrements the entry corresponding to the disk block in the disk free list.

<pre><code>
    Set the Disk Free List entry corresponding to the block to 0.
    
    return;
</code></pre>

### Get Code Page 
Loads a single code page to memory given the block number of the page in the disk. It takes the block number and PID as an argument.

<pre><code>
/* If the required code page is already loaded by some other process, we simply increment the share count in the <a href="../../os-design/mem-ds/#memory-free-list">Mem Free List</a> */

Loop though code page entries in the <a href="../../os-design/process-table/#per-process-disk-map-table">disk map table</a> of all processes
    If (the block number in the Disk Map Table entry matches the 
    block to be loaded, and it's corresponding <a href="../../os-design/process-table/#per-process-page-table">page table</a> entry is set to VALID) {
        <b>increment the share count</b> of the page in the <a href="../../os-design/mem-ds/#memory-free-list">Mem Free List</a>.
        return the physical page number
    }

/* The code page is not in memory, and has to be loaded from disk */

Get a free memory page by calling the <b>get_free_page()</b> function.
Load the disk block into memory page by calling the <b>disk_load()</b> function in the <a href="../../modules/module-04/">Device Manager</a> Module.
Return the memory page number to which the code block has been loaded.
</code></pre>

###  Get Swap Block
Returns the block number of a free disk block in the swap area.

<pre><code>
loop through entries in the <a href="../../os-design/disk-ds/#disk-free-list">Disk Free List</a> from <a href="../../support-tools/constants/">DISK_SWAP_AREA</a> to <a href="../../support-tools/constants/">DISK_SIZE</a> - 1{ 	/* swap area */
    if ( a free entry is found ){
            Set the Disk Free List entry as 1;
            Return the corresponding block number;
    }
}
return -1;
</code></pre>