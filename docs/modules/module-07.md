---
title: 'Module 7: Boot Module'
original_url: https://eXpOSNitc.github.io/os_modules/Module_7.html
hide:
    - toc
---

This module is responsible for hand creating the INIT and SHELL processes. It loads the modules, interrupt routines and disk data structures which are required by eXpOS from disk to memory. It also initializes different memory data structures which are required to run the OS smoothly. Boot module is invoked only once by the OS Startup code at the time of booting.

#### Algorithm

<pre><code>

Load the following from the disk to the memory - 
Exception handler, Timer interrupt handler, Disk interrupt handler, Console (terminal) interrupt handler, 
Library, Interrupt routines [4 - 17] and Modules [0 - 6]. 
/* Module 7 (boot module) and IDLE process will be loaded by OS startup code */


Load the following disk data structures to the memory pages of their memory copies - 
Disk free list, Root file, Inode table and User table.

See <a href="../../os-implementation/" target="_blank">disk/memory organization</a>.


/* Initialize the INIT (Login) process as follows - */

Load only the first code page of INIT process from the disk to the memory.

<details class="code-accordion"><summary>Initialize the Page table for INIT process (PID = 1)</summary>
    Use <a href="../../support-tools/constants/" target="_blank">PAGE_TABLE_BASE</a> + 20 as starting address for the page table of INIT process.
    Set the memory pages 63 and 64 for library entries in the <a href="../../os-design/process-table/#per_page_table" target="_blank">page table</a>. Set "0100" as auxiliary information for library pages. <!--the reference bit to 0, valid bit to 1, write bit to 0.-->
    Set the first code page entry to 65 (See <a href="../../os-implementation/" target="_blank">memory organization</a>) and auxiliary information for valid code pages as "0100". <!--Set valid bit to 1 and write bit to 0.-->  
    Set the first stack page entry to 66 and auxiliary information to "0110".<!--valid bit to 1, write bit to 1. Set second stack page entry to -1 and valid bit to 0.-->
    Set remaining code pages, remaining stack page and heap pages entries to -1 and auxiliary information to "0000".
</details>
<details class="code-accordion"><summary>Initialize the process table for INIT process.</summary>
    Initialize the fields of <a href="../../os-design/process-table/" target="_blank">process table</a> as - TICK as 0, PID as 1, USERID as 0, STATE as CREATED,
    USER AREA PAGE NUMBER as 77 (allocated from free user space), KPTR to 0, UPTR to 4096 (starting of first user stack page), 
    PTBR to PAGE_TABLE_BASE + 20 and PTLR as 10.
</details>
Store the IP value (from the header of the INIT) on top of first user stack page [66*512] = [65*512+1].


/* Initialize the SHELL process */

Load the code pages of SHELL process from the disk to the memory.

<details class="code-accordion"><summary>Initialize the Page table for SHELL process (PID = 2)</summary>
    Use <a href="../../support-tools/constants/" target="_blank">PAGE_TABLE_BASE</a> + 40 as starting address for the page table of SHELL process.
    Set the memory pages 63 and 64 for library entries in the <a href="../../os-design/process-table/#per_page_table" target="_blank">page table</a>.
    Set "0100" as auxiliary information for library pages. <!--the reference bit to 0, valid bit to 1, write bit to 0.-->
    Set the code page entries to 67 and 68 (See <a href="../../os-implementation/" target="_blank">memory organization</a>) and auxiliary information for valid code pages as "0100". <!--Set valid bit to 1 and write bit to 0.-->  
    Allocate two memory pages 78 and 79 for user stack.
    Set the two stack page entries to allocated memory pages and auxiliary information to "0110".<!--valid bit to 1, write bit to 1. Set second stack page entry to -1 and valid bit to 0.-->
    Set remaining code pages and heap pages entries to -1 and auxiliary information to "0000".
</details>
<details class="code-accordion"><summary>Initialize the process table for SHELL process.</summary>
    Initialize the fields of <a href="../../os-design/process-table/" target="_blank">process table</a> as - TICK as 0, PID as 2, USERID as 0, STATE as TERMINATED,
    USER AREA PAGE NUMBER as 80 (allocated from free user space), KPTR to 0, UPTR to 4096 (starting of first user stack page), 
    PTBR to PAGE_TABLE_BASE + 40 and PTLR as 10.
</details>
Store the IP value (from the header of the SHELL) on top of first user stack page [78*512] = [67*512 +1].    

Initialize <a href="../../os-design/process-table/#disk_map_table" target="_blank">Disk Map Table</a> for shell. First two code page entries with 9, 10 and all other entries to -1.


/* Initialize all memory data structures */

Set the states of all processes (other than INIT, IDLE, SHELL and Swapper Daemon) in the <a href="../../os-design/process-table/" target="_blank">process table</a> to TERMINATED.
Reset the status field in the <a href="../../os-design/mem-ds/#ts_table" target="_blank">terminal status table</a> and <a href="../../os-design/mem-ds/#ds_table" target="_blank">disk status table</a> to 0.
Initialize the <a href="../../os-design/mem-ds/#mem_free_list" target="_blank">memory free list</a> by setting 0 (free) for free entries and 1 for allocated pages.
// presently 82 memory pages are allocated

Initialize the fields of <a href="../../os-design/mem-ds/#ss_table" target="_blank">System Status Table</a>. MEM_FREE_COUNT as 45, WAIT_MEM_COUNT as 0, SWAPPED_COUNT as 0, PAGING_STATUS as 0.

Invalidate <a href="../../os-design/process-table/#per_process_table" target="_blank">Per Process Resource Table</a> of INIT and SHELL processes (all entries are set to -1).

Store 0 in the PROCESS_COUNT field for all entries in <a href="../../os-design/mem-ds/#sem_table" target="_blank">Semaphore Table</a>.

Initialize BLOCK NUMBER to -1, DIRTY BIT to 0 and LOCKING PID to -1 for the four buffer pages in the <a href="../../os-design/mem-ds/#buffer_table" target="_blank">Buffer table</a>.

Set FILE OPEN COUNT and LOCKING PID to -1 for all entries in the <a href="../../os-design/mem-ds/#file_lock_status_table" target="_blank">File Status Table</a>. 

Set the INODE INDEX to -1 in the <a <a href="../../os-design/mem-ds/" target="_blank">Open File Table</a> for all entries.


</code></pre>
