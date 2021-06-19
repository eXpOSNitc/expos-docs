---
title: 'Disk Interrupt Handler'
original_url: 'http://eXpOSNitc.github.io/os_design-files/disk_interrupt.html'
hide:
    - navigation
    - toc
---

#### Description
Hardware sends an interrupt on completion of a [load/store operation](../arch_spec-files/instruction_set.html). This interrupt is handled by the Disk Interrupt Handler. The data structure updated is the [Disk Status Table](mem_ds.html#ds_table).


#### Algorithm


<pre><code>
Switch to the Kernel Stack. 	/* See <a href="stack_smcall.html">kernel stack management during system calls</a> */
Save the value of SP to the USER SP field in the <a href="process_table.html">Process Table</a> entry of the process.
Set the value of SP to the beginning of User Area Page.

Backup the register context of the current process using the <a href="../arch_spec-files/instruction_set.html">BACKUP</a> instruction.


In the Disk Status Table, set the STATUS field to 0, indicating that the disk is no longer busy.

Wake up all processes waiting for the disk.
    1. Search the <a href="process_table.html" target="_blank">Process table</a> for processes in (<a href="constants.html" target="_blank">WAIT_DISK</a>, _ ) state.
    2. Change the state of the processes to (<a href="constants.html" target="_blank">READY</a>, _ ).

Restore the register context of the process using <a href="../arch_spec-files/instruction_set.html">RESTORE</a> instruction.

Restore SP to the value stored in USER SP field of the process table.

ireturn;
</code></pre>