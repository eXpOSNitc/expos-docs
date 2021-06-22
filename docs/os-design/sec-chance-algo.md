---
title: 'Second Chance Algorithm'
original_url: 'http://eXpOSNitc.github.io/os_design-files/sec_chance_algo.html'
hide:
    - navigation
    - toc
---

### Second Chance Algorithm

The page replacement technique used in eXpOS is a modified version of the [Second Chance Algorithm](http://en.wikipedia.org/wiki/Page_replacement_algorithm#Second-chance). This algorithm uses the [reference bits](process-table.md#per_page_table) in the Page Table. The page to be replaced is selected by first searching the **per-process page tables** of all processes. **Only [valid](process-table.md#per_page_table) pages are searched. The pages which are shared between multiple processes and shared library pages are skipped in the search.** The first valid unshared page with Reference bit as 0 is selected. While searching for the page with reference bit 0, the reference bit of every page table entry that is traversed during the search, is set to 0. This gives the page which is accessed recently a second chance before getting replaced. 


  

#### Algorithm

<pre><code>
Scan the Page Tables of all processes (except the idle process) for a page with Valid bit 1 and Reference bit 0.

Pages shared among multiple processes and shared library pages are skipped in the scan 
    /* shared pages have a number greater than 1 in its <a href="mem_ds.html#mem_free_list">Memory Free List</a> entry */

While scanning, the reference bit of any page, with valid bit 1 and reference bit 1, is set to 0. 

If an unshared page with reference bit 0 and valid bit 1 is found, it is selected as page to be replaced.


Return the page number and the PID.
</code></pre>