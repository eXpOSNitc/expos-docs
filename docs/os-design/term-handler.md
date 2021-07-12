---
title: 'Terminal Interrupt Handler'
original_url: 'http://eXpOSNitc.github.io/os_design-files/term_handler.html'
hide:
    - navigation
---

### Description
The Read operation for terminal input, puts the process executing the operation to sleep while the input is being read. Once input data is read, the terminal device sends a hardware interrupt, which is handled by the terminal handler. The terminal handler is responsible for waking up processes that are blocked for input console. 

The data structures modified are [Terminal Status Table](mem-ds.md#terminal-status-table) and [Process Table](process-table.md).


  

### Algorithm

<pre><code>
Switch to the Kernel Stack. 	/* See <a href="../../os-design/stack-smcall/">kernel stack management during system calls</a> */
Save the value of SP to the USER SP field in the <a href="../../os-design/process-table/">Process Table</a> entry of the process.
Set the value of SP to the beginning of User Area Page.

Backup the register context of the current process using the <a href="../../arch-spec/instruction-set/">BACKUP</a> instruction.

Set the status field in <a href="../../os-design/mem-ds/#terminal-status-table" target="_blank">Terminal Status Table</a> to 0 to indicate that the terminal is free.

Using the PID field of the Terminal Status Table, locate the <a href="../../os-design/process-table/" target="_blank">Process Table</a> entry of the process that read the data.

Copy the word read from the standard input to the <b>Input Buffer</b> field in the Process Table entry.

Release lock on the terminal by calling <b>release_terminal()</b> function in the <a href="../../modules/module-00/">Resource Manager</a> Module.

Restore the register context of the process using <a href="../../arch-spec/instruction-set/">RESTORE</a> instruction.

Restore SP to the value stored in USER_SP field of the process table entry of the process.

ireturn;
</code></pre>


!!! question 
    When interrupts or system calls are invloked, the mode changes from user to kernel. Registers are backed up using the BACKUP instruction in the case of interrupts and not in the case of system calls. Why?




  
  











































