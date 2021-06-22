---
title: 'Module 4: Device Manager'
original_url: 'http://eXpOSNitc.github.io/os_modules/Module_4.html'
---


Handles Terminal I/O and Disk operations (Load and Store).

| Function Number | Function Name | Arguments | Return Value |
| --- | --- | --- | --- |
| DISK\_STORE = 1 | Disk Store | PID, Page Number, Block Number | NIL |
| DISK\_LOAD = 2 | Disk Load | PID, Page Number, Block Number | NIL |
| TERMINAL\_WRITE = 3 | Terminal Write | PID, Word | NIL |
| TERMINAL\_READ = 4 | Terminal Read | PID, Address | NIL |

![](http://exposnitc.github.io/img/os-modules/DeviceManager.png)

### Disk Store


 ***Description*** : Stores the contents of the page into the disk block. A valid PID as input is assumed.  
  

<pre><code>
Acquire the lock on the disk device by calling the Acquire_Disk() function
in the <a href="../../modules/module-00/">Resource Manager</a> module;

Set the LOAD/STORE BIT, PAGE NUMBER and BLOCK NUMBER in the <a href="../../os-design/mem-ds/#ds_table">Disk Status Table</a>.

Use the store statement to store the memory page to disk;

Set the state as (WAIT_DISK, - );

Call the <b>switch_context()</b> function from the <a href="../../modules/module-05/">Scheduler Module</a>.

return;
</code></pre>


Called by Shutdown, Buffer Read and Buffer Write.  

###  Disk Load


 ***Description*** : Loads the contents of the disk block to the page. A valid PID as input is assumed.  
  


<pre><code>
Acquire the lock on the disk device by calling the Acquire_Disk() function
in the <a href="../../modules/module-00/">Resource Manager</a> module;

Reset the LOAD/STORE BIT, set PAGE NUMBER and BLOCK NUMBER in the <a href="../../os-design/mem-ds/#ds_table">Disk Status Table</a>.

Use the load statement to load the disk block to memory;

Set the state as (WAIT_DISK, - );

Call the <b>switch_context()</b> function from the <a href="../../modules/module-05/">Scheduler Module</a>.

return;
</code></pre>


Called by the Buffer Read, Buffer Write functions, exec system call (to load the first code page) 
and the exception handler (demand paging).   
   


Note: The bootstrap code must use *loadi* statement and not this function.

###  Terminal Write


 ***Description*** : Reads a word from the Memory address provided to the terminal. Assumes a valid PID is given.  

<pre><code>
    Acquire the lock on the terminal device by calling the Acquire_Terminal() function
    in the <a href="../../modules/module-00/">Resource Manager</a> module;
    
    Use the print statement to print the contents of the word
    to the terminal;

    Release the lock on the terminal device by calling the Release_Terminal() function
    in the <a href="../../modules/module-00/">Resource Manager</a> module;
  
    return;
</code></pre>

Called by the Write system call.

###  Terminal Read


  

 ***Description*** : Reads a word from the terminal and stores it to the memory address provided. Assumes a valid PID is given.  
  

<pre><code>
Acquire the lock on the disk device by calling the Acquire_Terminal() function
in the <a href="../../modules/module-00/">Resource Manager</a> module;

Use the read statement to read the word from the terminal;

Set the state as (WAIT_TERMINAL, - );

Call the <b>switch_context()</b> function from the <a href="../../modules/module-05/">Scheduler Module</a>.

Copy the word from the <b>Input Buffer</b> of the <a href="../../os-design/process-table/">Process Table</a> of the process corresponding to PID
to the memory address provided.

return;
</code></pre>
Called by the Read system call.

!!! note
    The Terminal Interrupt Handler will transfer the contents of the input port P0 to the Input Buffer of the process.  
