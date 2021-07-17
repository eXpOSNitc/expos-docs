---
title: 'Kernel Stack Management in system calls, interrupts and kernel modules'
original_url: 'http://eXpOSNitc.github.io/os_design-files/stack_module.html'
hide:
    - navigation
---


Parts of the eXpOS kernel that implements code for certain standard repetitive tasks like scheduling, 
managing resources, buffer etc. are implemented
as separate subroutines called modules. A module may take several arguments and has a single return value. A module is
always invoked from some kernel routine like an interrupt/exception handler or some other module. Modules cannot be invoked by a program executing in the user mode. 



When a kernel routine invokes a module, the return address from the module gets pushed into the currently active
kernel stack. The functional and interface design of eXpOS
modules are presented  [here](../modules/index.md) . 

SPL lays down programming conventions regarding the invocation and programming of kernel modules. The  [SPL module programming conventions](../support-tools/spl.md)  (see Case c) documentation describes these conventions. 

A kernel module or an interrupt service routine can invoke another kernel module while it is executing. 
The invoked kernel module also uses the same kernel stack. 
 
Since the invocation is voluntary, execution context of the caller should be saved in its kernel stack
before transferring control to the invoked kernel module. 


The arguments to the kernel module are passed through the registers R1, R2 , etc. 
The return value will be stored in register R0.

Before returning control to the caller, the invoked module pops off the space used 
during its execution, from the stack. The caller restores
the register context upon return before resuming its execution.
 


!!! note
	RET instruction is used instead of IRET to return back to the kernel module.


  

###  **1. Actions done by caller before a call to the kernel module**

1. Save the registers in use to the kernel stack
2. Store the arguments argument\_1, argument\_2, argument\_3,... to R1, R2, ... respectively. 
3. Transfer control to the kernel module to be executed 

<div style="border: 1px solid var(--md-code-fg-color);padding: 1em">
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
 

###  **2. Actions done by the kernel module before return**

1. Store the return value to R0. 
2. Pop off the space used during its execution from the kernel stack 
3. Use RET instruction to transfer control back to the kernel module which invoked it 

<div style="border: 1px solid var(--md-code-fg-color);padding: 1em">
<img src="../../assets/img/stack-management/kernel_to_kernel_step2.png">
<pre><code>
<b>Pseudo code</b>	
....
// pop off the space used during 
	   its execution

// Move the return value to R0

RET	// return control to the module 
	   which invoked it
</code></pre>

<b>Fig.2. - Actions done by the kernel module before returning.</b>
</div>


###  **3. Actions done by the caller after returning from the kernel module**

1. Save the return value (present in R0) to a desired location, if necessary 
2. Restore the values of the registers in use from the kernel stack
