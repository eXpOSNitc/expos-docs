---
title: 'XSM Instruction Set'
original_url: 'http://eXpOSNitc.github.io/arch_spec-files/instruction_set.html'
hide:
    - navigation
---


!!! note "Important Note"
    Througout the architecture documentation, we have used the terms kernel mode for previleged mode and user mode for unprevileged mode of machine execution. However, "kernel" and "user" are OS level abstractions and not connected with the hardware. Hence the above usage is incorrect technically. However since the kernel of an OS normally runs in the previliged mode and user programs execute in the unpreviliged mode, the (incorrect) terminology has been used.

Every instruction in XSM is 2 words long. The instructions provided by the XSM architecture can be classified into **unprivileged (user)** and **privileged (kernel)** instructions. The semantics of each instruction is different, depending on the mode in which the machine is running.


## Unprivileged Instructions

XSM provides a set of unprivileged instructions, which are the only instructions available when the machine is executing in the user mode. The machine can execute unprivileged instructions in kernel mode also, however, the instruction semantics will be different as explained in [Paging hardware](./paging-hardware.md). The unprivileged instructions are _Data Transfer Instructions_, _Arithmetic Instructions_, _Logical Instructions_, _Stack Instructions_, _Sub-routine instructions_, _Debug instructions_ and _Software interrupts_. Registers available in user mode are R0-R19, SP, BP and IP.

### [Data Transfer Instructions]

#### 1\. **Register Addressing** :  
_Syntax_ : MOV Ri, Rj  
_Semantics_ : Copies the contents of the register Rj to Ri.
  
#### 2\. **Immediate Addressing** :  
_Syntax_ : MOV Ri, INTEGER/STRING  
_Semantics_ : Copies the INTEGER/STRING to the register Ri.

#### 3\. **Register Indirect Addressing**:  
_Syntax_ : MOV Ri, \[Rj\]  
_Semantics_ : Copy contents of memory location pointed by Rj to register Ri.  
_Syntax_ : MOV \[Ri\], Rj  
_Semantics_ : Copy contents of Rj to the location whose address is in Ri.
  
#### 4\. **Direct Addressing** :  
_Syntax_ : MOV \[LOC\], Rj  
_Semantics_ : Copy contents of Rj to the memory address LOC.  
_Syntax_ : MOV Rj, \[LOC\]  
_Semantics_ : Copy contents of the memory location LOC to the register Rj.


For all the above instructions, Ri/Rj may be any register **except IP**.

!!! note
    Only registers R0-R19, SP and BP shall be used in code that executes in unpreviliged mode. An [exception](./interrupts-exception-handling.md#exceptions) (illegal instruction) will be generated otherwise.

### [Arithmetic Instructions]

Arithmetic Instructions perform arithmetic operations on registers containing integers. If the register contains a non-integer value, an exception (illegal instruction) is raised.

#### 1\. **ADD, SUB, MUL, DIV** and **MOD**  
_Syntax_ : OP Ri, Rj  
_Semantics_ : The result of Ri op Rj is stored in Ri.  
_Syntax_ : OP Ri, INTEGER  
_Semantics_ : The result of Ri op INTEGER is stored in Ri.
  
#### 2\. **INR, DCR**  
_Syntax_ : OP Ri  
_Semantics_ : Increments/Decrements the value of register Ri by 1.

  
  

For all the above instructions, Ri/Rj may be any register **except IP**.

!!! note
	Only registers R0-R19, SP and BP shall be used in code that executes in unpreviliged mode. An [exception](./interrupts-exception-handling.md#exceptions) (illegal instruction) will be generated otherwise.

### [Logical Instructions]

Logical instructions are used for comparing values in registers. Strings can also be compared according to the lexicographic ordering of ASCII. If one of the operands is a string, the other operand will also be considered as a string. The logical instructions are LT, GT, EQ, NE, GE and LE.

  
**LT, GT, EQ, NE, GE, LE**  
_Syntax_ : OP Ri, Rj  
_Semantics_ : Stores 1 in Ri if the value stored in Ri is less than/greater than/equal to/not equal to/greater than or equal to/less than or equal to that in Rj. Ri is set to 0 otherwise.  
  

For all the above instructions, Ri/Rj may be any register **except IP**.

!!! note
	Only registers R0-R19, SP and BP shall be used in code that executes in unpreviliged mode. An [exception](./interrupts-exception-handling.md#exceptions) (illegal instruction) will be generated otherwise.

### [Branching Instructions]

Branching is achieved by changing the value of the IP to the word address of the target instruction specified by 'target\_address'.

#### 1\. **JZ**  
_Syntax_ : JZ Ri, target\_address  
_Semantics_ : Jumps to target\_address if the contents of Ri is zero.
  
#### 2\. **JNZ**  
_Syntax_ : JNZ Ri, target\_address  
_Semantics_ : Jumps to target\_address if the contents of Ri is not zero.
  
#### 3\. **JMP**  
_Syntax_ : JMP target\_address  
_Semantics_ : Unconditional jump to target\_address.

  
For all the above instructions, Ri/Rj may be any register **except IP**.

!!! note
	Only registers R0-R19, SP and BP shall be used in code that executes in unpreviliged mode. An [exception](./interrupts-exception-handling.md#exceptions) (illegal instruction) will be generated otherwise.

### [Stack Instructions]

#### 1\. **PUSH**  
_Syntax_ : PUSH Ri  
_Semantics_ : Increment SP by 1 and copy contents of Ri to the location pointed to by SP.
  
#### 2\. **POP**  
_Syntax_ : POP Ri  
_Semantics_ : Copy contents of the location pointed to by SP into Ri and decrement SP by 1.

  
  

For all the above instructions, Ri/Rj may be any register **except IP**.

!!! note
	Only registers R0-R19, SP and BP shall be used in code that executes in unpreviliged mode. An [exception](./interrupts-exception-handling.md#exceptions) (illegal instruction) will be generated otherwise.

### [Subroutine Instructions]

The CALL instruction copies the address of the next instruction to be fetched(this value must be IP + 2 since each instruction is **two** memory words) on to location SP + 1. It also increments SP by one and transfers control to the instruction specified by the target\_address. The RET instruction restores the IP value stored at location pointed by SP, decrements SP by one and continues execution fetching the next instruction pointed to by IP.

####  1\. **CALL**  
_Syntax_ : CALL target\_address / Ri  
_Semantics_ : Increments SP by 1, transfers IP + 2 to location pointed to by SP and jumps to instruction specified by target\_address/Ri.  
    

For the CALL instruction, Ri/Rj may be any register **except IP**.
    
!!! note
	Only registers R0-R19, SP and BP shall be used in code that executes in unpreviliged mode. An [exception](./interrupts-exception-handling.md#exceptions) (illegal instruction) will be generated otherwise.
    
  
#### 2\. **RET**  
_Syntax_ : RET  

_Semantics_ : Sets IP to the value pointed to by SP and decrements SP.

### [Debug Instruction]

_Syntax_ : BRKP  

_Semantics_ : The machine when run in debug mode invokes the debugger when this intruction is executed. This instruction can be used for debugging system code.  
    

### [Software Interrupts]

_Syntax_ : INT n  

_Semantics_ : Generates an interrupt to the kernel with n (4 to 18) as a parameter. This involves a **change of mode from user to kernel mode**. It also disables the interrupts. The Stack Pointer is first incremented, the physical address of SP is calculated and the (virtual) address of the next instruction after the current value of IP is stored into that location (See [Address Translation](./paging-hardware.md)). After this, the execution mode is switched to Kernel mode. **Note that, INT can be invoked only from the User Mode.** The IP value must contain a virtual address and hence, the value pushed into stack is a virtual address and not a physical address. Finally, the IP value is set according to the value of n as specified [here](./machine-organization.md).  
    

### [NOP Instruction]

_Syntax_ : NOP  

_Semantics_ : Instruction that does nothing.  
    

  
  

## Privileged Instructions

Privileged instructions can be executed only in the kernel mode (both priviliged instructions and unpriviliged instructions can be executed in the kernel mode). It should be noted that all the addresses in the kernel mode should be **physical addresses**, whereas the user mode uses **logical addresses**, with address translation done using the [Paging hardware](./paging-hardware.md). Privileged Instructions are:

  

### [LOADI]

_Syntax_ : LOADI pagenum blocknum

_Semantics_ : This instruction loads the disk block specified by blocknum to the memory page specified by pagenum. Blocknum and pagenum should be numbers or registers containing numbers. **The machine will wait for the disk transfer to complete and continue execution of the next instruction only after the block transfer is completed by the disk controller.**

### [LOAD]

_Syntax_ : LOAD pagenum blocknum

_Semantics_ : This instruction initiates the transfer of the disk block specified by blocknum to the memory page specified by pagenum, using the disk controller. Blocknum and pagenum should be numbers or registers containing numbers. The machine proceeds to execute the next instruction without waiting for the completion of the block transfer. The disk controller raises the [disk interrupt](./interrupts-exception-handling.md) when the transfer is completed.

### [STORE]

_Syntax_ : STORE pagenum blocknum

_Semantics_ : This instruction initiates the transfer of the memory page specified by pagenum to the disk block specified by blocknum, using the disk controller. Blocknum and pagenum should be numbers or registers containing numbers. The machine proceeds to execute the next instruction without waiting for the completion of the block transfer. The disk controller raises the [disk interrupt](./interrupts-exception-handling.md) when the transfer is completed.

### [ENCRYPT]

_Syntax_ : ENCRYPT Ri

_Semantics_ : This instruction replaces the value in the register Ri with its encrypted value. The details of the encryption scheme used is left unspecified.

### [BACKUP]

_Syntax_ : BACKUP

_Semantics_ : This instruction is used to backup all the machine registers (except SP, IP, exception flag registers and ports) into the memory locations starting from the address pointed to by SP in the order : BP, R0 - R19. The value of SP gets incremented accordingly.

### [RESTORE]

_Syntax_ : RESTORE

_Semantics_ : This instruction is used to restore the backed up machine registers from memory. The registers are restored from contiguous memory locations starting from the address pointed to by SP in the order : R19-R0, BP. The value of SP gets decremented accordingly.

### [PORT]

_Syntax_ : PORT Ri, Pj  

_Semantics_ : Transfers the contents of port Pj to register Ri.

_Syntax_ : PORT Pi, Rj  

_Semantics_ : Transfers the contents of register Rj to port Pi.

### [IN]

_Syntax_ : IN  

_Semantics_ : IN initiates reading a word from the standard console. The machine proceeds to the execution of the next instruction without waiting for the console read to complete. When a word is read from the console, the console controller stores the word to the port P0 (which is reserved for the console input) and raises the [console interrupt](./interrupts-exception-handling.md).

### [INI]

_Syntax_ : INI  

_Semantics_ : INI initiates reading a word from the standard console. **This instruction gets enabled in the debug mode only.** The machine waits for the console read to complete before proceeding to the execution of the next instruction. When a word is read from the console, the console controller stores the word to the port P0. Console interrupt is not raised here.

### [OUT]

_Syntax_ : OUT  

_Semantics_ : Transfers the contents of P1 to the standard output immediately.

  

### [IRET]

_Syntax_ : IRET

_Semantics_ : This instruction is used to return control to a user mode program from an interrupt service routine/exception handler. This involves a change of mode from kernel to user mode. With the execution of the IRET instruction, interrupts are enabled. The address of the next instruction to be executed by the user program is popped from the stack and set to the IP Register, following which the Stack Pointer is decremented. Since the IP value must contain a virtual address while executing in User Mode, the value obtained from stack is treated as a virtual address and not a physical address (See [Address Translation](./paging-hardware.md)). Note that the machine switches to user mode just before the execution of the IRET instruction. Thus the address pointed to by SP is treated as a virtual address and the machine translates this address into physical address using the [page translation scheme](./paging-hardware.md), before popping the IP value.

### [HALT]

_Syntax_ : HALT

_Semantics_ : This instruction causes the machine to halt immediately.

  
  

##  <span style="color:red">NEXSM Additional Privileged Instructions</span>

!!! warning "Important Note"
    These instructions are available only on [NEXSM](./nexsm.md) (a two-core extension of XSM) machine. Additional Privileged Instructions in NEXSM are:
  

### TSL
_Syntax_ : TSL Rj, \[loc\]

_Semantics_ : The contents of the memory location \[loc\] is copied to register Rj. The value of \[loc\] is set to 1. This instruction is **atomic**. That is, when one of the cores is executing the TSL instruction, the **memory bus is locked** to avoid the other processor from simultaneously accessing \[loc\].

### START
_Syntax_ : START

_Semantics_ : If this instruction is executed by the primary while the machine is in reset mode, then secondary core starts parallel execution at the starting address of memory page 128 (physical address 65536). The START instruction is ignored if executed when the machine is in active mode.

### RESET
_Syntax_ : RESET

_Semantics_ : The instruction, when executed in active mode sets the machine to reset mode. The instruction is ignored if executed in reset mode.