---
title: 'Kernel Stack Management in system calls, interrupts and kernel modules'
original_url: 'http://eXpOSNitc.github.io/os_design-files/stack_smcall.html'
hide:
    - navigation
---



This document is a tutorial explaining how the eXpOS kernel must manage the kernel stack during system calls. The document is specific to the implementation of eXpOS on the XSM machine. 
 
Since the user program has control over the transfer to the system call module, it is expected to save its register context (in the user stack) before the system call and restore the context after returing from the system call.

The application program must also pass the parameters to the system call through the user stack. The return value of the system call is also passed back to the application through the user stack. For the calling conventions followed in eXpOS, see [ABI](http://exposnitc.github.io/abi.html).

If the application program is written in ExpL, then the ExpL compiler will generate code for saving and restoring the context
and pushing arguments into the user stack (if you are writing directly in assembly language, then your code must explicitly contain the code to do these). 

The system call module must be designed so as to access these arguments from the user stack of the process, do the processing
required and store the return value into the appropriate location in the user stack before returning to the user mode. 
The system call module must also change the stack to its kernel stack upon entry and switch back to the user stack at the time
of return.





!!! note
	The algorithms described in the [design page](../os_design.html) stipulates that each system call sets the [MODE flag](process_table.html) to the appropriate [system call number](Sw_interface.html) and switches to the kernel stack.
  
	However, if the same (software) interrupt contains multiple system calls,
	code duplication can be avoided by
	setting the MODE flag and switching to kernel stack immediately upon entry
	into the interrupt handler, before control is transferred to the appropriate
	system call function.


	The interrupt handler can reset the MODE flag and switch back to the user stack
	after return from the system call function,
	before returning to user mode.


###  **1. Actions done by the user process before executing an INT instruction**

1. Push the registers in use to the stack
2. Push the system call number into the stack
3. Push the arguments
4. Push an empty space for the return value
5. Invoke the INT machine instruction corresponding to the system call

<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="http://exposnitc.github.io/img/Stack_Management/Kernel_sw1.png">
<pre><code>
<b>Pseudo code</b>

.... 			// Code to push registers
PUSH System\_Call\_Number	// Push system call number
PUSH Argument\_1		// Push the arguments to the stack
PUSH Argument\_2
PUSH Argument\_3
PUSH R0			// Push an empty space for return value
INT number		// Invoke the corresponding INT 
			       instruction
</code></pre>
</div>

!!! note
	The XSM Machine, on execution of INT instruction, pushes the return adress (IP + 2 value) on to the user stack.*
  
 

### **2. Actions done by the System call service routine upon entry**

1. Extract the system call number and the arguments from the user stack.
2. Set the MODE field in process table entry of the process to the system call number.
3. Switch from the user stack to the kernel stack.
4. Identify the system call using the system call number and transfer control to the system call code


  

<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="http://exposnitc.github.io/img/Stack_Management/Kernel_sw2.png">
<pre><code>
<b>Pseudo code</b>

... 
syscallNumber <- address\_translate(UserSP - 5);
Argument\_1    <- address\_translate(UserSP - 4);
Argument\_2    <- address\_translate(UserSP - 3);
Argument\_3    <- address\_translate(UserSP - 2);

// Switching the stack

UPTR <- UserSP
SP   <- User Area Page Number * 512 - 1
...

</code></pre>
</div>


### **3. Actions done by the System call service routine before returning from the system call**

1. Store the return value in the user stack
2. Set the stack pointer (SP) to top of the user stack 
3. Set the MODE field in process table entry of the current process to 0.
4. Return to the user program using the IRET machine instruction

<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="http://exposnitc.github.io/img/Stack_Management/Kernel_sw1.png">
<pre><code>
<b>Pseudo code</b>
....		   

// store the return value in the 
       space alloted in the user stack

Address\_RetVal <- address\_translate(UPTR - 1);
		
[Address\_RetVal] <- return value 	    

// move the value of User Stack 
       Pointer TO SP
		
MOV SP, UPTR	

// return to the user program

IRET		
</code></pre>
</div>

!!! note
	Note that the figure shows the KPTR pointing to top of the kernel stack. However, we have not written any 
	code to set the value of KPTR. This is because the kernel stack is assumed to be empty on entering a kerenl module from
	the user mode. Therefore, when the kernel mode is entered the next time, SP will be initialised to point to the 
	beginning of the kernel stack.
	
  


### **4. Actions done by the process after returning from a system call**


1. Save the return value
2. Pop off the arguments and the system call number from the stack
3. Restore the register context and resume execution.

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