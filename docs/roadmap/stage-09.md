---
title: 'Stage 9 : Handling kernel stack (4 Hours)'
original_url: https://exposnitc.github.io/Roadmap.html
---

!!! info "Learning Objectives"
    - Get introduced to setting up process table entry for a user program.
    - Familiarise with the management of kernel stack in hardware interrupt handlers.
!!! abstract "Pre-requisite Reading"
     Read and understand the <a href="os_design-files/stack_interrupt.html" target="_blank">Kernel Stack Management during Interrupts</a>before proceeding further.


eXpOS requires that when the OS enters an interrupt handler that runs in kernel mode,
the interrupt handler must switch to a different stack. This requirement is to prevent user
level “hacks” into the kernel through the stack. In the previous stage, though you entered the timer
interrupt service routine in the kernel mode, you did not change the stack. In this stage,
this will be done.

To isolate the kernel from the user stack, the OS kernel must maintain two stacks for
a program - **a user stack and a kernel stack**. 
In eXpOS, one page called the <a href="os_design-files/process_table.html#user_area">user area page</a>
is allocated for each process. A part of the space in this page will be used for the kernel stack
(some other process information also will be stored in this page).


Whenever there is a transfer of program control from the user mode to kernel during interrupts
(or exceptions), the interrupt handler will change the stack to the kernel stack of the program
(that is, the SP register must point to the top of the kernel stack of the program). Before the
machine returns to user mode
from the interrupt, the user stack must be restored (that is, the SP register must point to the
top of the user
stack of the program).

Once we have two stacks for a user program, we need to design some data structure in memory to
store the SP values of the two stacks. This is because the SP register of the machine can store only
one value.

eXpOS requires you to maintain a <a href="os_design-files/process_table.html" target="_blank">
Process Table </a>,where data such as value of the kernel stack pointer, user stack pointer etc. pertaining to
each process is stored.


For now, we just have one user program in execution. Hence we will need just one process table
entry to be created. Each process table entry contains several fields. But for now, we are only interested
in storing only 1) user stack pointer and 2) the memory page allocated as user area for the program.


The process table starts at page number 56 (address 28672). The process table has space for 16
entries, each having 16 words. Each entry holds information pertaining to one user process. Since we have
only one process, we will use the first entry (the first 16 words starting at address 28672). Among these, we
will be updating only entries for user stack pointer (word 13) and user area page number (word 11)
in this stage.

You will modify the previous stage code so that the user program is allocated a user area page.
You will also create a process table entry for the program where you will make the necessary entries.

#### Modifications to the OS Startup Code

1) Set the User Area page number in the <a href="os_design-files/process_table.html" target="_blank">
Process Table</a> entry of the current process. Since the first available free page is 80,
the User Area page is allocated at the physical page number 80.
The <a href="support_tools-files/constants.html" target="_blank">SPL constant</a>PROCESS_TABLE points to 
the starting address(28672) of the Process Table.
```
[PROCESS_TABLE + 11] = 80;
```

2) As we are using the first Process Table entry, the PID will be 0. eXpOS kernel is expected to
store the PID in the PID field of the process table.
```
[PROCESS_TABLE + 1] = 0;
```

3) The kernel maintains a data structure called <a href="os_design-files/mem_ds.html#ss_table" target="_blank">
System Status Table</a> where the PID of the currently executing user process is maintained.
This makes it easy to keep track of the current PID whenever the machine enters any kernel
mode routine. The System Status Table is stored starting from memory address 29560. The second field of
this table must be set to the PID of the process which is going to be run in user mode.

Set the current PID field in the System Status Table. The <a href="support_tools-files/constants.html" target="_blank">
SPL constant </a> SYSTEM_STATUS_TABLE points to the starting address of the System Status Table.

```
[SYSTEM_STATUS_TABLE + 1] = 0;
```

4) The kernel stack pointer for the process need not be set now as <b>all interrupt handlers assume that the kernel stack is empty when the handler is entered from user mode</b>. Thus whenever an interrupt handler is entered from user mode, the kernelstack pointer will be initialized assuming that the stack is empty. (See <a href="os_design-files/stack_interrupt.html" target="_blank"> Kernel Stack Management during hardware interrupts and exceptions </a>).The KPTR value will be used in later stages when kernel modules invoke each other.

####   Timer Interrupt

1) Save the current value of User SP into the corresponding Process Table entry.
Obtain the process id of the currently executing process from <a href="os_design-files/mem_ds.html#ss_table" target="_blank">System Status Table</a>.
This value can be used to get the <a href="os_design-files/process_table.html" target="_blank">Process Table</a>
entry of the currently executing process.<br/>
    
!!! caution "Important Note"
    Registers R0-R15 are user registers.
    Since you have not saved the register values
    into the stack yet, you should be careful not to write any code that alters these registers
    till the user context is saved into the stack. Registers R16-R19 are marked for kernel use and
    hence the kernel can modify them. The SPL compiler will use these registers to translate your SPL
    code.

```
[PROCESS_TABLE + ( [SYSTEM_STATUS_TABLE + 1] * 16) + 13] = SP;
```

2) Set the SP to beginning of the kernel stack.User Area Page number is the 11th word of the Process Table.
The initial value of SP must be set to this `address*512 - 1`.
```
// Setting SP to UArea Page number * 512 - 1
SP = [PROCESS_TABLE + ([SYSTEM_STATUS_TABLE + 1] * 16) + 11] * 512 - 1;
```

3) Save the user context to the kernel stack using the <a href="arch_spec-files/instruction_set.html#backup" target="_blank">Backup</a> instruction.

```
backup;
```

4) Print "timer".

```
print "TIMER";
```

5)Restore the user context from the kernel stack and set SP to the user SP saved in Process
Table, before returning to user mode.

```
restore;
SP = [PROCESS_TABLE + ( [SYSTEM_STATUS_TABLE + 1] * 16) + 13];
```
  
6) Use ireturn statement to switch to user mode.

```
ireturn;
```

!!! assignment "Assignment 1"
    Print the process id of currently executing
    process in timer interrupt before returning to user mode.
    You can look up this value from the System Status Table.

