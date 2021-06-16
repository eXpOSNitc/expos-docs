---
title: 'Disk Interrupt Handler'
original_url: 'http://eXpOSNitc.github.io/os_design-files/disk_interrupt.html'
---







Disk Interrupt Handler


































 



























  
  
  






Disk Interrupt Handler
----------------------


  

  

*Description*: Hardware sends an interrupt on completion of a [load/store operation](../arch_spec-files/instruction_set.html). This interrupt is handled by the Disk Interrupt Handler. The data structure updated is the [Disk Status Table](mem_ds.html#ds_table).


#### Algorithm:



```

Switch to the Kernel Stack. 	/* See [kernel stack management during system calls](stack_smcall.html) */
Save the value of SP to the USER SP field in the [Process Table](process_table.html) entry of the process.
Set the value of SP to the beginning of User Area Page.

Backup the register context of the current process using the [BACKUP](../arch_spec-files/instruction_set.html) instruction.


In the Disk Status Table, set the STATUS field to 0, indicating that the disk is no longer busy.

[Wake up all processes waiting for the disk.](#collapse2)
                  1. Search the [Process table](process_table.html) for processes in ([WAIT\_DISK](constants.html), \_ ) state.
 2. Change the state of the processes to ([READY](constants.html), \_ ).

Restore the register context of the process using [RESTORE](../arch_spec-files/instruction_set.html) instruction.

Restore SP to the value stored in USER SP field of the process table.

ireturn;

```



  
  













































