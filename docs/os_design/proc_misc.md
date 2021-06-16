---
title: 'Process System Calls'
original_url: 'http://eXpOSNitc.github.io/os_design-files/proc_misc.html'
hide:
    - navigation
---

### Getpid system call

#### Arguments
None

#### Return Value

|  |  |
| --- | --- |
| PID | Success |


#### Description
Returns the process identifier of the invoking process. The system call does not fail. 


#### Algorithm:

<pre><code>
Find the PID of the current process from the <a href="process_table.html">Process Table</a>.

Return the PID of current process.

</code></pre>

### Getppid system call

#### Arguments
None

#### Return Value

|  |  |
| --- | --- |
| PPID | Success |


#### Description
Returns to the calling process the value of the process identifier of its parent. The system call does not fail. 
  

#### Algorithm

<pre><code>

Find the PPID of the current process from the <a href="process_table.html">Process Table</a>.

Return the PPID.

</code></pre>








  
  
  








































