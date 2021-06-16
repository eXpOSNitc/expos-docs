---
title: 'Terminal Interrupt Handler'
original_url: 'http://eXpOSNitc.github.io/os_design-files/term_handler.html'
---







Terminal Interrupt Handler


































 



























  
  
  






Terminal Interrupt Handler
--------------------------


  

  

*Description*: The Read operation for terminal input, puts the process executing the operation to sleep while the input is being read. Once input data is read, the terminal device sends a hardware interrupt, which is handled by the terminal handler. The terminal handler is responsible for waking up processes that are blocked for input console. 


The data structures modified are [Terminal Status Table](mem_ds.html#ts_table) and [Process Table](process_table.html).


  

#### Algorithm:



```

Switch to the Kernel Stack. 	/* See [kernel stack management during system calls](stack_smcall.html) */
Save the value of SP to the USER SP field in the [Process Table](process_table.html) entry of the process.
Set the value of SP to the beginning of User Area Page.

Backup the register context of the current process using the [BACKUP](../arch_spec-files/instruction_set.html) instruction.

Set the status field in [Terminal Status Table](mem_ds.html#ts_table) to 0 to indicate that the terminal is free.

Using the PID field of the Terminal Status Table, locate the [Process Table](process_table.html) entry of the process that read the data.

Copy the word read from the standard input to the **Input Buffer** field in the Process Table entry.

Release lock on the terminal by calling **release\_terminal()** function in the [Resource Manager](../os_modules/Module_0.html) Module.

Restore the register context of the process using [RESTORE](../arch_spec-files/instruction_set.html) instruction.

Restore SP to the value stored in USER\_SP field of the process table entry of the process.

ireturn;

```

#### Questions:


1. When interrupts or system calls are invloked, the mode changes from user to kernel. Registers are backed up using the BACKUP instruction in the case of interrupts and not in the case of system calls. Why?




  
  











































