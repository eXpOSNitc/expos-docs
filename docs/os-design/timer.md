---
title: 'Timer Interrupt Handler'
original_url: 'http://eXpOSNitc.github.io/os_design-files/timer.html'
---







Timer Interrupt Handler


































 



























  
  
  




Timer Interrupt Handler
-----------------------


  

  

*Description:* The hardware requirement specification for eXpOS assumes that the machine is equipped
 with a timer device that sends periodic hardware interrupts. 
 The timer interrupt handler internally invokes the eXpOS  [scheduler module](../os_modules/Module_5.html) . 
 


  


![](../img/roadmap/timer_interrupt.png)
  

Control flow diagram for *Timer interrupt handler*

  
  

#### Algorithm:



```

Switch to the Kernel Stack. 	/* See [kernel stack management during system calls](stack_smcall.html) */
Save the value of SP to the USER SP field in the [Process Table](process_table.html) entry of the process.
Set the value of SP to the beginning of User Area Page.

Backup the register context of the current process using the [BACKUP](../arch_spec-files/instruction_set.html) instruction.


[/* This code is relevant only when the Pager Module is implemented in Stage 27 */](#collapse1)

**If** swapping is initiated, /* check [System Status Table](../os_design-files/mem_ds.html#ss_table) */
{
 /* Call Swap In/Out, if necessary */

 **if** the current process is the Swapper Daemon and Paging Status is [SWAP\_OUT](../support_tools-files/constants.html),
 Call the **swap\_out()** function in the [Pager Module](../os_modules/Module_6.html).

 **else if** the current process is the Swapper Daemon and Paging Status is [SWAP\_IN](../support_tools-files/constants.html), 
 Call the **swap\_in()** function in the [Pager Module](../os_modules/Module_6.html).

 **else if** the current process is Idle, 
 /* Swapping is ongoing, but the daemon is blocked for some disk operation and idle is being run now */
 /* Skip to the end to perform context switch. */
 
}

**else** /* Swapping is not on now. Check whether it must be initiated */
{
 **if** (MEM\_FREE\_COUNT < [MEM\_LOW](../support_tools-files/constants.html)) /* Check the [System Status Table](../os_design-files/mem_ds.html#ss_table) */
 /* Swap Out to be invoked during next Timer Interrupt */
 Set the Paging Status in System Status Table to [SWAP\_OUT](../support_tools-files/constants.html).

 **else if** (there are swapped out processes) /* Check SWAPPED\_COUNT in [System Status Table](../os_design-files/mem_ds.html#ss_table) */
 **if** (Tick of any Swapped Out process > [MAX\_TICK](../support_tools-files/constants.html) or MEM\_FREE\_COUNT > [MEM\_HIGH](../support_tools-files/constants.html))
 /* Swap In to be invoked during next Timer Interrupt */
 Set the Paging Status in System Status Table to [SWAP\_IN](../support_tools-files/constants.html).

}
/* End of Stage 27 code for Swap In/Out management */
    
Change the state of the current process in its Process Table entry from RUNNING to READY.

Loop through the process table entires and increment the TICK field of each process.

Invoke the [context switch module](../os_modules/Module_5.html) .

Restore the register context of the process using [RESTORE](../arch_spec-files/instruction_set.html) instruction.

Set SP as the user SP saved in the Process Table entry of the new process.
Set the MODE\_FLAG in the [process table](process_table.html) entry to 0.
             
ireturn.

```











































