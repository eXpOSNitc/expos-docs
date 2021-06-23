---
title: 'Kernel Stack Management During Context switch'
original_url: 'http://eXpOSNitc.github.io/os_design-files/timer_stack_management.html'
hide:
    - navigation
---

Context switch involves switching a machine from executing one process to executing another even before the former is completed. This involves saving the state of all volatile data like registers, PTBR, BP, etc. (in other words the "context") and, then loading the context of a new process or starting a new process from scratch which will have its own context. This technique allows the machine to concurrently execute multiple processes.


eXpOS maintains a kernel stack for each application process. Before a context switch, the context of the outgoing process must be saved into its kernel stack. The previously saved context of the incoming process must be restored from the kernel stack of that process. 



 This document specifies how stack management has to be performed during a context switch. There are two situations that can result in a context switch:


1. The time slice of a process executing in the user mode expires and a timer interrupt is raised. The timer interrupt routine invokes the scheduler module(MOD\_5) to perform a context switch.


2. While executing in the kernel mode (inside a system call or the exception handler), a process has to wait for some event to happen (ex: wait for a resource like disk, terminal etc) and hence voluntarily invokes the scheduler(MOD\_5) to schedule itself out. 
 



  

 **Case 1 : Saving and Restoring the context during timer interrupt.**
  
   

 The Timer ISR saves the user context of the process from which it was entered, into the kernel stack of that process. (see  [Kernel Stack Management during Interrupts](stack-interrupt.md)  for more details). The Timer ISR then calls the scheduler module. The scheduler module determines which process must be run next, and changes the 
 machine's stack to the kernel stack of the new processes. This stack is expected to contain the previously saved context of the 
 new process. The scheduler is reponsible for resuming execution of the new process.



 If the new process was scheduled out earlier by the timer interrupt, then the scheduler will return to the instruction in the 
 timer interrupt after the call to the scheduler. When the timer ISR returns to the
 user mode, the new process will resume execution because the execution context restored by the timer ISR at the time
 of return to user mode will
 be from the kernel stack of the new process. More details will be explained below. 





 Note: We will write the Timer ISR in such a way that it does not use any registers. So, we need not store and restore any additional kernel level context inside the timer ISR before or after invoking the scheduler module.
 


  

 **Case 2 : Saving and Restoring the context during blocking system calls.**
  
   

 In this case, the scheduler modules was invoked from some other kernel code - typically some blocking system call, exception
handler etc. Here, it is the responsibility of the calling module/handler to save its context (registers in use) in its kernel stack 
before invoking the scheduler module. Later, when the scheduler returns to this handler/module, the handler/module should restore the context and resume execution. See the  [Kernel Stack management during module calls](stack-module.md) for more details.




In spite of the above convention, **the ExpL compiler fails to save the value of BP register before making a system call.** To solve this problem, a patch is added to the scheduler so that the scheduler saves the current value of BP register to the kernel stack of the process being scheduled out. 



  

##  Scheduler Module



The scheduler module is responsible for performing the actual context switch. Context switch happens by a change of SP, PTBR and PTLR registers. We store these register values of the old process to its Process Table and restore SP, PTBR and PTLR values from the Process Table of the new process. 




!!! warning "Important Note"
	The **offset of SP register within the user area page**  will be stored in the KPTR field of the process table(and **not** the physical address of the kernel stack pointer). The value of the offset can be calculated by the fomula `offset = SP – (512 * USER AREA PAGE NUMBER)`
	The purpose of storing the offset (instead of the physical address) is to allow the OS to relocate the user area page to another physical memory page during swapping. 



 After switching the registers, the scheduler module executes the return instruction resulting in IP value being set from the top of the kernel stack of the new process (except for one special case which we will see below). This transfers control to the next instruction in the kernel handler/module in the new process.
 

### **Actions done by the scheduler:**

1) Save register BP to the kernel stack of current process.  

2) Save the current kernel stack pointer offset in the KPTR field of the process table.  

3) Save the current PTBR and PTLR values in the process table of the leaving process. (This operation is redundant)

4) Find the pid of the next process to be scheduled.

5) Restore the PTBR, PTLR and kernel stack pointer (KPTR) values from the process table of the entering process.

6) Restore register BP from the top of kernel stack of entering process.  

7) Identify whether the state* of the new process is a READY/CREATED from the state field of the process table. (A process that has never been scheduled for execution previously will be in CREATED state. The fork system call creates the child process in the CREATED state.)


####  **Case 1 : The new process is in READY state**

8) Compute the physical address corresponding to the offset stored in KPTR field of the process table entry of the new process, and store this to SP.

 
<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/kernel_mode_timer_step2.i.a.png">
<pre><code>			
...
						
MOV R4, User Area Page Number*512
	// find the physical address of the user
	   area page 
ADD R4, KPTR
	// find the value of the kernel stack 
	   pointer using the formula 512*user 
	   area page number + KERNEL STACK POINTER
MOV SP, R4	
	// store the physical address of the kernel 
	   stack pointer in SP

...
</code></pre>
<b>Fig.2.a - Setting the kernel SP from the offset value in the KPTR field of the process table.</b>
</div>

9) return instruction is executed and control goes back to the Interrupt routine or kernel module that called the scheduler.
 
 

####  **Case 2 : The new process is in CREATED state**



8) Set SP to the address stored in the UPTR field of the process table of the new process.


<div style="padding: 1em;border: 1px solid var(--md-code-fg-color);">
<img src="../../assets/img/user_mode_timer_step2c.png">
<pre><code>
...
						
MOV SP, UPTR

IRET

...
</code></pre>
<b>Fig.2.a - Setting the kernel SP from the offset value in the KPTR field of the process table.</b>
</div>


9) `ireturn` statement is executed. (In this case, the scheduler directly kicks off execution of the new process in user mode.)
  
  

!!! note
	A process may invoke the scheduler for several reasons. As noted earlier as Case 1, one reason is that the time slice of the process is finished. Other possibilities (handled under Case 2) includes waiting for disk, terminal, semaphore, file etc. Before calling the scheduler a process must set the STATE field of the process table entry to indicate the correct reason for invoking the scheduler. Note that the scheduler cannot set the STATE field as only the caller will know the cause.

   
  







































