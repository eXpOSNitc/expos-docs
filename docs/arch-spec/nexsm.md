---
title: 'NEXSM (Two Core) Architecture Specification'
original_url: 'http://eXpOSNitc.github.io/arch_spec-files/nexsm.html'
hide:
    - navigation
---
  

NEXSM is an extension of the XSM architecture with a dual-core feature. The machine has two identical cores with the same set of internal registers sharing a common memory. All registers in XSM are present in both the cores. Additionally, NEXSM cores contain an extra register called the **core flag**. A few additional privileged instructions provide primitives for synchronization between the two cores. One of the processors is called the **primary core** and the other called the **secondary core**. The machine can operate in two modes – **active mode** and **reset mode**. **In the reset mode, the secondary is non-functional.** The mode in which the machine operates can be controlled by the primary using a pair of special privileged instructions – START and RESET.

  

#### **Additional Registers**

The only additional register in NEXSM that is not present in XSM is the core flag (CORE). The core flag is a **read-only machine register**. The contents of the core flag are set to 0 in the primary core and 1 in the secondary core. The core flag allows a program to test whether it is currently executing in the primary or the secondary.

Usage Example: JZ CORE, \[Address\] /\*\* Tests the value of CORE and branches \*\*/

  

#### **Dual-Core Bootstrap**

1.  When powered on, the machine starts in **reset** mode. The primary core starts execution and the secondary core is non-functional. Here, the functioning is similar to XSM.
2.  The secondary core starts execution when the primary core executes a START instruction.
3.  Upon execution of the START instruction, the machine enters the **active** mode. The START instruction sets the IP value of the secondary to physical address **65536 (page 128)** and secondary is powered on.
4.  Normally, when the machine is powered on, the primary executes a bootstrap code which loads the initialization code for the secondary into memory page 128 before executing START.
5.  When the machine is running in active mode, if a RESET instruction is executed by either the primary or the secondary, then the machine goes back to reset mode and the secondary stops execution.

**Note:** The START instruction is ignored if executed in active mode. Similarly, the RESET instruction is ignored when executed in reset mode.

  

#### **Memory Organization**

NEXSM machine has 144 memory pages (as against 128 pages of XSM). The memory organization of pages 0 to 127 are exactly as in XSM. The organization of the remaining 16 pages are as:

1.  Page 128 and 129 are reserved for loading the **bootstrap** code for the second core.
2.  Pages 130 and 131 are reserved for an additional **software interrupt INT 19**.
3.  Pages 132 to 143 are available as free memory.

  

#### **Disk Organization**

NEXSM has 16 additional free blocks of disk space, with block numbers 512 to 527.

  

#### **Additional Privileged mode Instructions**

  
1\. **Test and Set Lock**  
_Syntax:_ TSL Rj, \[loc\]  
_Semantics:_ The contents of the memory location \[loc\] is copied to register Rj. The value of \[loc\] is set to 1. This instruction is **atomic**. That is, when one of the cores is executing the TSL instruction, the **memory bus is locked** to avoid the other processor from simultaneously accessing \[loc\].  
  
2\. **Dual-core initialization**  
_Syntax:_ START  
_Semantics:_ If this instruction is executed by the primary while the machine is in reset mode, then secondary core starts parallel execution at the starting address of memory page 128 (physical address 65536). The START instruction is ignored if executed when the machine is in active mode.  
  
3\. **Reset instruction**  
_Syntax:_ RESET  
_Semantics:_ The instruction, when executed in active mode sets the machine to reset mode. The instruction is ignored if executed in reset mode.

  

#### **Interrupts and Exceptions**

The way NEXSM machine enters privileged mode is similar to XSM. Switch from unprivileged mode to privileged mode happens only when a software/hardware interrupt or exception occurs. The following are the details.

1.  The disk and the terminal interrupts apply to the primary core only.
2.  Software interrupts, exceptions and timer interrupt applies to both the cores.
3.  As with XSM, when a core enters protected mode, interrupts are disabled (on the core). The memory addresses of all interrupt/exception handlers in NEXSM are exactly those in XSM.
4.  NEXSM permits an additional software interrupt INT19 (address 66560, pages 130 and 131).