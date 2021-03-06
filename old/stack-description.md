---
title: 'Kernel Stack Management in system calls, interrupts and kernel modules'
original_url: 'http://eXpOSNitc.github.io/os_design-files/stack_description.html'
hide:
    - navigation
---

This document is a tutorial explaining how the eXpOS kernel must manage the kernel stack. The document is
specific to the implementation of eXpOS on the XSM machine. 
There are three different situations where the eXpOS kernel needs to do careful stack management:
1. A user program invokes a system call
2. An Exception / Interrupt occurs when a user process is executing
3. A kernel module invokes another kernel module

The calling conventions followed here correspond to the one given in the [SPL documentation](../support-tools/spl.md).


!!! warning "Important Note"
	Whenever the kernel stack pointer of a process is saved in the KPTR field of the process table, the **offset of SP register within the user area page** will be stored (and **not** the physical address of the kernel stack pointer). The page number of the user area page is stored in the USER AREA PAGE NUMBER field in the process table. Thus, the value of the offset can be calculated by the fomula *offset = SP – (512 * USER AREA PAGE NUMBER)*.

	The purpose of storing the offset (instead of the physical address) in the KPTR field is to allow the OS to relocate the user area page to another physical memory page. Thus, if the user area page is swapped out, it can be swapped back later to a different physical memory page.

### System Call Invocation

An application program must push the input parameters to a system call through the user stack. The return value of the system
call is also passed back to the application through the user stack. For the calling conventions followed in eXpOS, see [ABI](../abi.md).


If the application program is written in ExpL, then the ExpL compiler will generate code for pushing arguments into the user
stack (if you are writing directly in assembly language, then your code must explicitly contain the code to do these). The system call module must be designed so as to access these arguments from the user stack of the process, do the processing
required and store the return value into the appropriate place in the user stack before returning to the user mode. 
The system call module must also change the stack to its own (kernel) stack upon entry and switch back to the user stack at the time
of return.

Please note that the description below does not apply to the [stack management during context switch](./timer-stack-management.md) which is discussed elsewhere.


####  **1. Actions done by the user process before executing an INT instruction**

1. Push the registers in use to the stack
2. Push the system call number into the stack
3. Push the arguments
4. Push one space for the return value
5. Invoke the INT machine instruction corresponding to the system call

!!! note
	The XSM Machine, on execution of INT instruction, pushes the return adress (IP + 2 value) on to the user stack.
  
<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/stack-management/actions_of_process_upon_encountering_sys_call.png">
<pre><code>
<b>Pseudo code</b>
.... 			// Code to push registers
PUSH System_Call_Number	// Push system call number
PUSH Argument_1		// Push the arguments to the stack
PUSH Argument_2
PUSH Argument_3
PUSH R0			//  Push an empty space for return value
INT number		//  Invoke the corresponding INT 
			   		instruction
</code></pre>
</div>
  
  

#### **2. Actions done by the System call service routine upon entry**

1. Compute the physical address of the top of the user stack.
2. Extract the system call number and the arguments. (Note : The convention is to extract the system call number to register R0, and arguments to              R1,R2, and R3 in that order from the caller's stack)
3. Switch the stack from user to kernel  
    1. Transfer the current SP register to User stack pointer field of the process table.
    2. Compute the physical address of the kernel stack pointer.
    3. Transfer the physical address of the kernel stack pointer to the SP register.
4. Identify the system call using the system call number and transfer control to the system call code
<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/stack-management/actions_of_process_upon_encountering_sys_call.png">
<pre><code>
<b>Pseudo code</b>
... 
MOV R4,	physicalSP  // Compute physicalSP 		      
MOV R0, [R4 - 4]    // Extracting the system call number
MOV R1, [R4 - 3]    // Extracting the values of the arguments
MOV R2, [R4 - 2]
MOV R3, [R4 - 1]			 

// Switching the stack

MOV UPTR, SP
MOV R4, User Area Page Number*512
ADD R4, KPTR  
MOV SP, R4 
...
</code></pre>
</div>



#### **3. Actions done by the System call service routine before returning from the system call**

1. Store the return value in the user stack
2. Pop off all the contents from the kernel stack and store the logical address of the top of kernel stack to the KPTR field of the process table
3. Point the stack pointer (SP) to top of the user stack
4. Return to the user program using the IRET machine instruction


<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/stack-management/actions_of_kernel_returning_from_sys_call_step3.png">
<pre><code>
<b>Pseudo code</b>
....		   
MOV R4, physicalSP
		
MOV [R4 - 1], return value 	    
		// store the return value in the 
		   space alloted in the user stack
MOV R4, User Area Page Number*512 
		// find the physical address 
        	   of the user area page
MOV R5, SP
SUB R5,R4
MOV KPTR,R5	// logicalSP = 
		   SP - (UAreaPgNo * 512)	
MOV SP, UPTR	// move the value of USER STACK 
		   POINTER TO SP
IRET		// return to the user program
....
</code></pre>
</div>



#### **4. Actions done by the process after returning from a system call**

1. Save the return value
2. Pop off the arguments and the system call number from the stack
3. Restore the register context and resume execution.

<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/stack-management/actions_of_process_aftr_return_sys_call.png">
<pre><code>
<b>Pseudo code</b>

....
POP R0			// Pop and save the return 
		           value
POP Argument\_3		
POP Argument\_2
POP Argument\_1		// Pop and discard the 
			   arguments
POP System\_Call\_Number	// Pop and discard the 
			   system call number 
....			// Code to restore the 
			   register context and 
			   resume execution
</code></pre>
</div>

### Exception/Interrupt Handler

A hardware interrupt/exception can occur while an application program is executing.
It can be the exception handler, timer interrupt routine, disk interrupt routine or the 
console interrupt routine. Since the application does not have control over the transfer 
to the interrupt module, it would not have saved its context. Thus in this case the kernel 
module must save the register context of the application in its own stack before using the 
registers and must restore the context before returning to the application. 
The kernel stack is used to store the execution context of the user process. 
This context is restored before the return from the kernel module. 
(The [backup](../arch-spec/instruction-set.md#backup) and [restore](../arch-spec/instruction-set.md#restore) instructions of the XSM machine facilitate this).


!!! note
	If an exception is caused by error conditions ( such as stack overflow, invalid stack pointer value, arithmetic exceptions etc.), the user program will be terminated. This is not dealt with in this tutorial. The tutorial describes the stack management only in the case of page fault exception (since this does not result in termination of the user program).

*The XSM machine pushes the return address (IP+2 value) to the user stack before transferring the control to the Interrut Service Routine* 
  

####  **1. Actions done by the kernel upon entering the interrupt service routine**

1. Switch from the user stack to the kernel stack
2. Save the values of the machine registers in the kernel stack using BACKUP machine instruction.
3. Transfer control to the interrupt routine code


<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<b>Execution context before an interrupt/exception:</b>
<img src="../../assets/img/stack-management/execn_context_b4_interrupt.png">
</div>

<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/stack-management/aftr_interrupt_step1a.png">
<pre><code>
<b>Pseudo code</b>	
....
MOV UPTR, SP	// Save the current SP register to 
		   User stack pointer field of the 
		   process table.
MOV SP, User Area Page Number*512 + KPTR
	// Set kernel stack
		   

<b>(Note: Registers should not be used explicitly here
 for calculations as they are not backed up yet.)</b>

</code></pre>
<b>Fig.1.a. - Switch from the user stack to the kernel stack</b>
</div>

<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/stack-management/aftr_interrupt_step1b.png">
<pre><code>
<b>Pseudo code</b>
....
BACKUP		// machine instruction to save the 
		   register context
....
</code></pre>
<b>Fig.1.{b,c} - Use the BACKUP machine instruction to save the values of the machine registers in the kernel stack and transfer control to the interrupt routine code</b>
</div>



  

####  **2. Actions done by the kernel before returning from the interrupt routine**
1. Restore the values of the machine registers using RESTORE machine instruction
2. Store the logical address of the current kernel stack top to the KPTR field
3. Set the value of SP to the top of the user stack
4. Transfer control back to the user process


<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/stack-management/aftr_interrupt_step2a.png">
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
<img src="../../assets/img/stack-management/aftr_interrupt_step2b.png">
<pre><code>
<b>Pseudo code</b>

....
MOV KPTR, User Area Page Number*512 - SP 
		// find the physical address 
        	   of the user area page
MOV SP, UPTR	// point SP to the user stack

IRET		// return to the user process
....

<b>(Note: Again, registers should not be used 
 explicitly in the calculations as it will 
 overwrite the restored register context)</b>
	
</code></pre>
<b>Fig.3. - Switch the stack and Transfer the control back to the user process</b>
</div>


### Invocation of a kernel module from another kernel module

A kernel module or an interrupt service routine can invoke another kernel module while it is executing. 
Since the invocation is voluntarily, execution context of the callee should be saved in the kernel stack
before transferring control to the invoked kernel module. 
The arguments to the kernel module are passed through the registers R0, R1, R2. 
The invoked kernel module also uses the same kernel stack. 

The return value will be stored in register R0. 
Before returning control to the callee, the invoked module pops off the space used 
during its execution, from the stack. The callee restores
the register context upon return before resuming its execution.


!!! note
	RET instruction is used instead of IRET to return back to the kernel module.


####  **1. Actions done by callee before executing the call to a kernel module**

1. Save the registers in use to the kernel stack
2. Store the arguments argument\_1, argument\_2, argument\_3,... to R0, R1, R2, ... respectively
3. Transfer control to the kernel module to be executed 

<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/stack-management/kernel_to_kernel_step1a.png">
<pre><code>
<b>Pseudo code</b>	
			
....		// save the registers in use
MOV R0, argument\_1
MOV R1, argument\_2
MOV R2, argument\_3
...
		// store the arguments
CALL MODULE\_N 
		// invoke the kernel 
		   module
....
</code></pre>
<b>Fig.1. - Save the registers in use to the kernel stack, store the values of arguments to registers R0, R1, R2,.. in that order and transfer control to the kernel module to be executed</b>
</div>

####  **2. Actions done by the kernel module before returning**
1. Pop off the space used during its execution from the kernel stack
2. Use RET instruction to transfer control back to the kernel module which invoked it 


<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/stack-management/kernel_to_kernel_step2.png">
<pre><code>
<b>Pseudo code</b>	
....
POP R0	// pop off the space used during 
...	   its execution

RET	// return control to the module 
	   which invoked it

</code></pre>
<b>Fig.2. - Actions done by the kernel module before returning.</b>
</div>