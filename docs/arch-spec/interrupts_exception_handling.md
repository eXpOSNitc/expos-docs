---
title: 'Interrupts and Exception handling'
original_url: 'http://eXpOSNitc.github.io/arch_spec-files/interrupts_exception_handling.html'
hide:
    - navigation
---


!!! warning "Important Note"
    _Througout the architecture documentation, we have used the terms kernel mode for previleged mode and user mode for unprevileged mode of machine execution. However, "kernel" and "user" are OS level abstractions and not connected with the hardware. Hence the above usage is incorrect technically. However since the kernel of an OS normally runs in the previliged mode and user programs execute in the unpreviliged mode, the (incorrect) terminology has been used._

XSM supports a total of 19 interrupts. Each interrupt is identified by its number between 0 and 18. Among these, Interrupt 0 is the exception handler, Interrupt 1 is the timer interrupt, Interrupt 2 is the disk controller interrupt and Interrupt 3 is the console interrupt. Interrupts 1, 2 and 3 are hardware interrupts. The interrupts 4 to 18 are software interrupts. Software interrupts occur when they are invoked by a program in execution. A program can invoke a software interrupt using the INT machine instruction. However, _hardware interrupts_ and the _exception handler_ cannot be invoked from user mode programs.

Associated with each interrupt/exception, there is an interrupt handler. When an interrupt occurs, the corresponding handler is executed. XSM specification reserves two contiguous memory pages for loading each interrupt handler according to the table given in [Memory Organisation](machine_organisation.html#content). When an interrupt/exception occurs, the machine transfers control to the beginning of the first page of the corresponding handler. It is the responsibility of the OS/Kernel programmer to store the interrupt handler routines in the disk and load them to the corresponding pages at the time of system startup.

Note: Internally XSM machine has an _interrupt vector table_ that maps each interrupt number to a corresponding address (of the interrupt handler). The vector table is stored starting from physical address 492 of the ROM memory. Locations 492,493,494 and 495 stores the addresses of exception handler, timer interrupt handler, disk interrupt handler and console interrupt handler. Location 496 contains the address of the first software interrupt handler - INT 4, location 497 contains address of INT 5 handler and so on. When the machine encounters an INT n instruction, the corresponding ROM location is searched for the handler address and IP is set to this value. Since the values are hard-coded in the ROM code of the XSM simulator given to you, you cannot change the addresses of these handlers. See [here](../arch_spec-files/machine_organisation.html#Boot ROM) for more details about Boot ROM and interrupt vector table.

!!! note
    XSM does not allow the INT instruction to be executed in kernel mode.


### **Timer Interrupt**

The XSM architecture includes a timer that can cause periodic interrupts during execution in unprivileged mode. The timer ticks with each unprivileged instruction executed and once the number of ticks reaches a threshold specified during boot-time (see --timer option of the [XSM simulator](../support_tools-files/xsm-simulator.html)), the tick counter is reset and a timer interrupt is raised. At that point, the machine executes the following actions:

1.  :red_circle: Increment the value of the SP register and push the value in the IP register into the memory address pointed to by SP. Since the machine is executing in unpreviliged mode, the address in SP is treated as a logical address and the machine performs [address translation](paging_hardware.html) to calculate the physical address corresponding to the SP value.
2.  Set IP to value stored in the interrupt vector table entry for the timer interrupt handler. The vector table entry for timer interrupt is located at physical address 493 in page 0 (ROM) of XSM and the value 2048 is preset in this location. Hence, the IP register gets value 2048 and the machine switches to privileged mode. Consequently, the next instruction will be fetched from physical address 2048, and the machine will continue execution in previliged mode (without peforming address translation).

!!! note
    :red_circle: If the value in the SP register after incrementing SP is an invalid address (i.e., not in the range 0 to PTLR\*512-1) then the machine generates an **illegal memory access exception** (see section below on exception handling). The machine will re-execute steps (1) and (2) immedietly after retrun to unprivileged mode, before executing any other instruction in unprivileged mode.

Thus the occurance of the timer interrupt results in machine execution to be transferred to the timer interrupt handler (INT 1) stored in page 4-5.

  

### **Disk Controller Interrupt**

The Disk Controller allows for imitating asynchronous disk access by the OS. Whenever the machine executes the LOAD/STORE instruction, the Disk Controller initiates a counter that ticks with each unprivileged instruction executed after the LOAD/STORE instruction. Once the counter reaches a threshold value specified during boot-time (see --disk option of the [XSM simulator](../support_tools-files/xsm-simulator.html)), the counter is reset and a disk interrupt (INT 2) is raised. At that point, the machine executes the following actions:

1.  :blue_circle: Increment the value of the SP register and push the value in the IP register into the memory address pointed to by SP. Since the machine is executing in unpreviliged mode, the address in SP is treated as a logical address and the machine performs [address translation](paging_hardware.html) to calculate the physical address corresponding to the SP value.
2.  Set IP to value stored in the interrupt vector table entry for the disk interrupt handler. The vector table entry for disk interrupt is located at physical address 494 in page 0 (ROM) of XSM and the value 3072 is preset in this location. Hence, the IP register gets value 3072 and the machine switches to privileged mode. Consequently, the next instruction will be fetched from physical address 3072, and the machine will continue execution in previliged mode (without peforming address translation).

!!! note
    :blue_circle: If the value in the SP register after incrementing SP is an invalid address (i.e., not in the range 0 to PTLR\*512-1) then the machine generates an **illegal memory access exception** (see section below on exception handling). The machine will re-execute steps (1) and (2) immedietly after retrun to unprivileged mode, before executing any other instruction in unprivileged mode.

Thus the occurance of the disk interrupt results in machine execution to be transferred to the disk interrupt handler (INT 2) stored in page 6-7. As noted above, the macros LOAD/STORE are used to send requests to the Disk Controller.

The Disk Controller does not support parallel input requests. Thus it is the OS Programmer's duty to ensure that multiple disk requests are not raised. That is, the OS must take care of ensuring that after a LOAD/STORE instruction is executed, another LOAD/STORE instruction is executed only after the device controller has raised the device interrupt, marking the completion of the first request.

  

### **Console Interrupt**

The XSM Architecture has a Console Device which acts as the IO interface for user interaction. When a program requires interacting with the user, the macros 'IN', 'INI' and 'OUT' are used to invoke the Console Device. Output (OUT instruction) is a synchronous process and works immediately. Whenever the machine executes the console input instruction (IN instruction), the Console Device initiates a counter that ticks with each unprivileged instruction executed after the IN instruction. Once the counter reaches a threshold value specified during boot-time (see --console option of the [XSM simulator](../support_tools-files/xsm-simulator.html)), the counter and the machine simulator waits for the user to enter some data into the console. When the user eventually enters the input, the counter is reset and the console interrupt (INT 3) is raised. At that point, the machine executes the following actions:

1.  :green_circle: Increment the value of the SP register and push the value in the IP register into the memory address pointed to by SP. Since the machine is executing in unpreviliged mode, the address in SP is treated as a logical address and the machine performs [address translation](paging_hardware.html) to calculate the physical address corresponding to the SP value.
2.  Set IP to value stored in the interrupt vector table entry for the console interrupt handler. The vector table entry for console interrupt is located at physical address 495 in page 0 (ROM) of XSM and the value 4096 is preset in this location. Hence, the IP register gets value 4096 and the machine switches to privileged mode. Consequently, the next instruction will be fetched from physical address 4096, and the machine will continue execution in previleged mode (without peforming address translation).

!!! note 
    :green_circle: If the value in the SP register after incrementing SP is an invalid address (i.e., not in the range 0 to PTLR\*512-1) then the machine generates an **illegal memory access exception** (see section below on exception handling). The machine will re-execute steps (1) and (2) immedietly after retrun to unprivileged mode, before executing any other instruction in unprivileged mode.

Thus the occurance of the console interrupt results in machine execution to be transferred to the console interrupt handler (INT 3) stored in page 8-9. As noted above, the macro instruction IN is used to send input requests to the Console device.

The Console Device does not support parallel input requests. Thus it is the OS Programmer's duty to ensure that multiple IN requests are not raised. Control is transferred to the user program by the interrupt routine only after the user inputs a word from the Console.

The INI instruction (which can be used only in debug mode) is a special instruction which allows synchronous console input where the machine doesn't raise an interrupt but waits for the user to enter the data before proceeding to the next instruction.

  

### **Race Conditions**

After the execution of an instruction in unpriviliged mode, suppose the machine finds that multiple interrupts are pending - say the disk, console and timer interrupts are simultaniously due, then the machine executes the interrupts in the following order - first timer, second disk and third console. After executing the first handler, the machine returns to unpreviliged mode and immedietely executes steps (1) and (2) in the next interrupt and so on till all pending interrupts are processed.

As noted above, if an exception occurs at the point of handling any of the above interrupts, the exception is handled first.

  

### **Exceptions**

Exceptions are anomalous situations which changes the normal flow of execution. The machine raises an exception when it runs in **user mode** and encounters an anomalous situation during program execution like division by zero or generation of an invalid address. All exceptions raise Interrupt 0.

The XSM Register set consists of four special registers for storing the details regarding exceptions. The exception registers are as shown below

1) **Exception IP (EIP)** : Stores the value of IP at the point where the exception occurred.
  
2) **Exception Page Number (EPN)** : This field is relevant when a **Page Fault Exception** occurs. The logical page number which caused a page fault exception is stored here.
  
3) **Exception Cause (EC)** : This field indicates a number which corresponds to the cause of the exception. Exceptions can be caused when the following events occur.
      
1. Page Fault : The value stored in the EC register for this exception is 0.
2. Illegal instruction : The value stored in the EC register for this exception is 1.
3. Illegal memory access : The value stored in the EC register for this exception is 2.
4. Arithmetic exception : The value stored in the EC register for this exception is 3.
  
4) **Exception Memory Address (EMA)** : Exception Memory Address register is relevant only in the case of **illegal memory access**. The illegal memory which was tried to be accessed is stored in the register. This field is relevant only when either the address referred to is outside the range 0 - 512\*(PTLR-1) or a write is attempted to a page which is read-only.


A detailed discussion on various conditions leading to the machine raising an exception are below:-

  

##### **Illegal instruction** 
occurs when one of the following conditions occur:-
    
1.  Destination of a MOV operation is a constant.
2.  A register/port not allowed in user mode is accessed.
3.  A privileged mode instruction is executed.
4.  There is an instruction that does not belong to XSM instruction set or an instruction is given with more/less operands than allowed - syntax error.
5.  INT n instruction - n is not in the valid range (4-18).
    
When one of the above events occur, the machine does the following:-  

1.  EIP is set to the value of the IP register, from which instruction that caused the exception was fetched.
2.  EPN contents are not valid for this exception.
3.  EC is set to value 1 corresponding to illegal instruction.
4.  EMA contents are not valid for this exception.
5. Set IP to value stored in the interrupt vector table entry for the exception handler. The vector table entry for exception handler is located at physical address 492 in page 0 (ROM) of XSM and the value 1024 is preset in this location. Hence, the IP register gets value 1024 and the machine switches to privileged mode. Consequently, the next instruction will be fetched from physical address 1024, and the machine will continue execution in previleged mode (without peforming address translation).
  
##### **Illegal Memory Access** 
occurs when one of the following conditions occur:-
    
1.  A MOV instruction has an address not in the range 0 to PTLR\*512-1. (Even indirect addressing as in MOV R0, \[R1\] can cause such addresses)
2.  RET/POP executed with SP not between 0 and PTLR\*512-1.
3.  CALL/INT/PUSH/hardware interrupt executed with SP not between -1 and PTLR\*512-2.
4.  JZ/JNZ/JMP Instruction is executed with IP value not in the range 0 to PTLR\*512-1.
5.  Write is attempted to a page whose [write permission bit](paging_hardware.html) in the page table entry has been set to 0.
  
When one of the above events occur, the machine does the following:-  

1.  EIP is set to the value of the IP register, from which instruction that caused the exception was fetched.
2.  EPN contents are not valid for this exception.
3.  EC is set to value 2 corresponding to illegal memory access.
4.  EMA is set to logical address that caused the illegal memory access.
5.  Set IP to value stored in the interrupt vector table entry for the exception handler. The vector table entry for exception handler is located at physical address 492 in page 0 (ROM) of XSM and the value 1024 is preset in this location. Hence, the IP register gets value 1024 and the machine switches to privileged mode. Consequently, the next instruction will be fetched from physical address 1024, and the machine will continue execution in previleged mode (without performing address translation).
  
##### **Arithmetic exception**
Occurs during DIV/MOD instruction with the second operator having value zero.  
      
When an arithmetic exception occurs, the machine does the following:-  

1.  EIP is set to the value of the IP register, from which instruction that caused the exception was fetched.
2.  EPN contents are not valid for this exception.
3.  EC is set to value 3 corresponding to arithmetic exception.
4.  EMA contents are not valid for this exception.
5.  Set IP to value stored in the interrupt vector table entry for the exception handler. The vector table entry for exception handler is located at physical address 492 in page 0 (ROM) of XSM and the value 1024 is preset in this location. Hence, the IP register gets value 1024 and the machine switches to privileged mode. Consequently, the next instruction will be fetched from physical address 1024, and the machine will continue execution in previleged mode (without performing address translation).
  
#####  **Page Fault** 
Occurs when **none** of the conditions above hold, and the [valid bit](paging_hardware.html) of the page referenced is set to 0.  
      
When one of the above events occur, the machine does the following:-  

1.  EIP is set to the value of the IP register, from which instruction that caused the exception was fetched.
2.  EPN contains the logical page number of the page accessed, that caused the exception.
3.  EC is set to value 0 corresponding to page fault.
4.  EMA contents are not valid for this exception.
5.  Set IP to value stored in the interrupt vector table entry for the exception handler. The vector table entry for exception handler is located at physical address 492 in page 0 (ROM) of XSM and the value 1024 is preset in this location. Hence, the IP register gets value 1024 and the machine switches to privileged mode. Consequently, the next instruction will be fetched from physical address 1024, and the machine will continue execution in previleged mode (without performing address translation).
    
 

### **Software Interrupts**

Software Interrupts are the primary mechanisms by which a user mode program transfers control to the corresponding interrupt handler that runs in the kernel mode. Software interrupt service routines typically contain the OS code for various system calls. Upon return from a software interrupt using the IRET instruction, execution resumes from the next instruction in the user mode program. A total of 15 software interrupts are available (Interrupt 4 - Interrupt 18). Note that **user mode programs cannot invoke the hardware interrupt routines**.

When an _INT n_ (n in the range 4-18) instruction occurs, the machine executes the following actions:

1.  :purple_circle: Increment the value of the SP register and push the value in the IP + 2 (logical address of the next instruction to be executed upon return from the interrupt handler) into the memory address pointed to by SP. Since the machine is executing in unpreviliged mode, the address in SP is treated as a logical address and the machine performs [address translation](paging_hardware.html) to calculate the physical address corresponding to the SP value.
2.  Set IP to value stored in the vector table entry for the corresponding interrupt. The vector table entry for _INT n_ is located at physical address _492 + n_ in page 0 (ROM) of XSM and the values are preset as specified in the [Boot ROM and Boot Block section](machine_organisation.html) of XSM Machine Organisation documentation. Hence, the IP register gets the value preset in the interrupt vector table and the machine switches to privileged mode. Consequently, the next instruction will be fetched from the preset value, and the machine will continue execution in previleged mode (without peforming address translation).

!!! note 
    :purple_circle: If the value in the SP register after incrementing SP is an invalid address (i.e., not in the range 0 to PTLR\*512-1) then the machine generates an **illegal memory access exception** (see section above on exception handling).

!!! note
    **INT instruction cannot be executed when the machine is executing in privileged mode.** (see [instruction set](instruction_set.html))
