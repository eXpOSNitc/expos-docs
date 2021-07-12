---
title: 'Kernel Stack Management in Hardware Interrupts or Exceptions'
original_url: 'http://eXpOSNitc.github.io/os_design-files/stack_interrupt.html'
hide:
    - navigation
---

This document is a tutorial explaining how the eXpOS kernel must manage the kernel stack during events such as a hardware interrupt or an exception. The document is specific to the implementation of eXpOS on the XSM machine. 

A hardware interrupt/exception can occur while an application program is executing.Since the application does not have control over the transfer to the interrupt module, it would not have saved its context. 

Thus in this case the Interrupt Service Routine must save the register context of the application in the kernel stack of the current process, perform the required operations and must restore the context before returning to the application. 
The  **[kernel stack](process-table.md#user-area)**  is used to store the execution context of the user process. (The [backup](../arch-spec/instruction-set.md#backup) and [restore](../arch-spec/instruction-set.md#restore) instructions of the XSM machine facilitate this).


### Actions done by the XSM machine on receiving an interrupt/ exception
On Receiving an interrupt or exception, the XSM machine does 3 things: 

1. Pushes the return address (IP+2 value) to the user stack.
2. Switches mode of execution from user to kernel.
3. Transfers the control to the Interrut Service Routine or Exception Handler 


<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<b>Execution context just after interrupt/exception:</b>
<img src="../../assets/img/stack-management/Kernel_interrupt1.png">
</div>


!!! note
	1.The page number of the user area page is stored in the UArea Page Number field in the process table.
	
	2.The offset of SP register within the user area page will be stored (and not the physical address of the kernel stack pointer) in the  field of the process table. The purpose of storing the offset (instead of the physical address) in the KPTR field is to allow the OS to relocate the user area page to another physical memory page. On entering a kernel module from the user process, the kernel stack will be empty and hence KTPR will be 0.
	
	3.When executing in user mode, the kernel stack is empty and hence the KPTR value is assumed to be zero. 

####  **1. Actions done by the kernel upon entering the interrupt service routine**
1. Switch from the user stack to the kernel stack. This involves storing the value of SP to UPTR field of the Process Table entry and setting the value of SP to User Area Page Number * 512 -1 as kernel stack is assumed to be empty on entering a kernel module from user process.
2. Save the values of the machine registers in the kernel stack using BACKUP machine instruction. 
3. Continue execution of the interrupt routine code

<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/stack-management/Kernel_interrupt2.png">
<pre><code>
<b>Pseudo code</b>
....
MOV UPTR, SP	// Save the current SP register to 
		   User stack pointer field of the 
		   process table.
MOV SP, User Area Page Number*512 - 1
	// Set kernel stack
		   

<b>(Note: Registers should not be used explicitly here
 for calculations as they are not backed up yet.)</b>
</code></pre>
<b>Fig.1.a. - Switch from the user stack to the kernel stack</b>
</div>

<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/stack-management/Kernel_interrupt3.png">
<pre><code>
<b>Pseudo code</b>

....
BACKUP		// machine instruction to save the 
		   register context
....

</code></pre>
<b>Fig.1.b - Use the BACKUP machine instruction to save the values of the machine registers in the kernel stack.</b>
</div>


####  **2. Actions done by the kernel before returning from the interrupt routine**

1. Restore the values of the machine registers using RESTORE machine instruction
2. Set the value of SP to the top of the user stack 
3. Transfer control back to the user process

<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/stack-management/Kernel_interrupt4.png">
<pre><code>
<b>Pseudo code</b>

....
RESTORE		// machine instruction to restore
 		   the register context
....

</code></pre>
<b>Fig.2.a - Use the RESTORE machine instruction to restore the values of the machine registers</b>
</div>


<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/stack-management/Kernel_interrupt5.png">
<pre><code>
<b>Pseudo code</b>
....

MOV SP, UPTR	// point SP to the user stack

IRET		// return to the user process
....

<b>(Note: Again, registers should not be used 
 explicitly in the calculations as it will 
 overwrite the restored register context)</b>
</code></pre>
<b>Fig.3. - Switch the stack and transfer the control back to the user process</b>
</div>


!!! note
	If an exception is caused by error conditions ( such as stack overflow, invalid stack pointer value, arithmetic exceptions etc.), the user program will be terminated. This is not dealt with in this tutorial. However the procedure described above should be followed while handling page fault exception (since this does not result in termination of the user program).


  
   











































