---
title: 'SPL Specification'
original_url: 'http://eXpOSNitc.github.io/support_tools-files/spl.html'
---

**SPL** or _System Programmer's Language_ in reality is not a high level programming language, but an enriched assembly language programming system for writing protected mode programs for the XSM machine. This language is useful for implementation of an OS on top of the XSM machine. The language is minimalistic and consists only of very basic constructs. Programming using SPL requires an understanding of the underlying [XSM architecture](../arch-spec/index.md).

Each SPL program is considered as a **module**. A module consists of a maximum of 1024 words which includes both the space allocated for code and data. Particular class of modules called **Interrupt Service Routines** can be invoked from the application by the INT instruction. Other modules can only be invoked from the kernel. The SPL compiler translates an SPL source program to a target XSM assembly module. [(See Loading modules into the disk architecture)](xfs-interface.md).

This specification defines the syntax and semantics of the basic constructs of the SPL language and also specifies the programming conventions recommended in using the langugage. The default SPL compiler provided as part of the eXpOS package is designed to follow the programming conventions specified in this document.


## Lexical Elements
### Comments and White Spaces

SPL allows only single line comments. Comments start with the character sequence // and stop at the end of the line. 
White spaces in the program including tabs, newline and horizontal spaces are ignored.


### Keywords

The following are the reserved words in SPL and it cannot be used as identifiers.

```
alias 	define	encrypt	breakpoint	inline
halt	goto	call	return	ireturn
backup	restore	readi	read	print
loadi	load	store	do	while
endwhile	break	continue	if	then
else 	endif	tsl*	start*	reset*
```


*\** These keywords are available only on eXpOS running on [NEXSM](../arch-spec/nexsm.md) (a two-core extension of XSM) machine.
 
### Operators and Delimiters

The following are the operators and delimiters in SPL
 
```
(	)	;	[	]	/	*	+	-	%	:
>	<	>=	<=	!=	==	=	&&	||	!
```

### Registers and Ports

SPL allows the use of 25 registers (`R0`-`R15`, `BP`, `SP`, `IP`, `PTBR`, `PTLR`, `EIP`, `EC`, `EPN`, `EMA`) and 4 ports (`P0`-`P3`). `P0` and `P1` are used for standard input and standard output respectively.


### Identifiers

Identifiers are used as symbolic names for constants and aliases for registers.
Identifiers should start with an alphabet but may contain alphabets, digits and/or underscore ( \_ ). 
No other special characters are allowed in identifiers.

*Examples:* 

**Valid :** var1, new\_page 

**Invalid :**  9blocks, $n etc.


### Literals

Integer and String literals are permitted in SPL.

An integer literal is a sequence of digits representing an integer. 
Negative integers are represented with a negative sign preceding the sequence of digits. eg. `3`, `-512`, `1024`

A string literal is a sequence of characters which are enclosed within double quotes (" ").eg.  `"alice"`


### Labels

SPL supports labels which are used along with goto and call. Labels follow the same naming convention as that of the identifiers.  

```
eg. label1:
.
.
.
goto label1
```









## Registers and Ports

SPL provides a fixed set of registers and ports are provided. 
The register set in SPL contains 29 registers. There is a direct mapping between these registers and the machine registers in XSM. There are 4 ports supported.

| Name                                                 | Register/Port |
| ---------------------------------------------------- | ------------- |
| Program Registers                                    | R0 - R15      |
| Reserved Registers **(For the use of SPL compiler)** | R16 - R19     |
| Base Pointer                                         | BP            |
| Stack Pointer                                        | SP            |
| Instruction Pointer                                  | IP            |
| Page Table Base Register                             | PTBR          |
| Page Table Length Register                           | PTLR          |
| Exception Instruction Pointer                        | EIP           |
| Exception Cause                                      | EC            |
| Exception Page Number                                | EPN           |
| Exception Memory Address                             | EMA           |
| Input Port                                           | P0            |
| Output Port                                          | P1            |
| Unused Ports                                         | P2, P3        |
| Core Flag :red_circle:                               | CORE          |

:red_circle: This is an extra read-only register available only on [NEXSM machine](../arch-spec/nexsm.md) (a two-core extension of XSM).
 
### Aliasing
Any register/port can be referred to by using a different name. A name is assigned to a particular register/port using the **alias** keyword. 
Each register/port can be assigned to only one alias at any particular point of time. However, a register/port can be reassigned to a different alias at a later point. 
Aliasing can also be done inside the **if** and **while** block. However, an alias defined within the **if** and **while** blocks will only be valid within the block. No two registers/ports can have the same alias name simultaneously.



## Constants

Symbolic names for values can be defined in an SPL module using the **define** keyword. They will be visible only inside the module. 
Unlike aliasing, two or more names can be assigned to the same value. A constant can only be defined once in a program.


### Predefined Constants

SPL provides a set of predefined constants defined in the file **splconstants.cfg**. 

The standard SPL implementation comes with a set of [pre-defined constants](constants.md) included in the *splconstants.cfg* file specifically tuned for the implementation of eXpOS on the XSM architecture. These constants are mostly the starting addresses of various OS data structures/handlers in the memory which are specified in the [implementation](../os-implementation.md) of the eXpOS. 
 
Users can also define constants which are visible in all 
SPL modules by including the definition in the *splconstants.cfg* file. If a constant defined in the *splconstants.cfg* file is re-defined in a module, the local definition will override the global definition. These predefined constants' definitions can be over-ruled by assigning different values explicitly by the user using the **define** keyword.
 

## Expressions

An expression specifies the computation of a value by applying operators to operands. SPL supports arithmetic and logical expressions.


### Arithmetic Expressions

Registers, constants and two or more arithmetic expressions connected using arithmetic operators are categorized as arithmetic expressions. 
SPL provides five arithmetic operators, viz., **+, -, *, /** (Integer Division) and **%** (Modulo operator) through which arithmetic expressions may be combined. 
Expression syntax and semantics are similar to standard practice in programming languages and normal rules of precedence, associativity and paranthesization hold.

Examples:
```
(5*R4) + 3 
10 % 4
```

### Logical Expressions
Logical expressions may be formed by combining arithmetic expressions using relational operators. 
The relational operators supported by SPL are **>, <, >=, <=, !=, ==**.
Standard meanings apply to these operators. A relational operator will take in two arguments and return 1 if the relation is valid and 0 otherwise.   

The relational operators can also be applied to strings.  <, >, <=, >=  compares two strings lexicographically. !=  and == checks for equality in the case of strings. If one of the operands is a string, the other operand will also be considered as a string.

Examples:
```
 "adam" < "apple" // This returns 1 
 "hansel" == "gretel" // This returns 0 
 "3" == 3 // This returns 1, as 3 will be treated as "3" 
```

Logical expressions themselves may be combined using logical operators, && (logical and) , || (logical or) and ! (not).


### Addressing Expressions
Memory of the machine can be directly accessed in an SPL program. 
A word in the memory is accessed by specifying the addressing element, i.e. memory location within **[ ]**. 
This corresponds to the value stored in the given address. An arithmetic expression or an addressing expression can be used to specify the address.  

Examples:
```
[1024], [R3], [R5+[R7]+128], [INODE\_TABLE + R2] etc.
```


## Statements

Statements control the execution of the program. All statements in SPL are terminated with a semicolon **( ; )** .


### Define Statement

The **define** statement is used to define a symbolic name for a value. Define statements should be used **before any other statement** in an SPL program. 
The keyword **define** is used to associate a literal to a symbolic name.  

**SYNTAX :** `define constant_name value;`;
```
    define DISK\_BLOCK 437;
```

### Alias Statement

An **alias** statement is used to associate a register/port with a name. Alias statements can be used anywhere in the program.  

**SYNTAX :** `alias alias_name register_name;`
```
    alias counter R0;
```

### Breakpoint Statement
The **breakpoint** statement is used to debug the program. The program when run in the [debug mode](xsm-simulator.md) pauses the execution at this instruction.  

**SYNTAX :** `breakpoint;`

This statement translates to [BRKP machine instruction](../arch-spec/instruction-set.md).


### Assignment Statement

The SPL assignment statement assigns the value of an expression/value stored in a memory address to a register/memory address. **=** is the assignment operator used in SPL. The operand on the right hand side of the operator is assigned to the left hand side. 
   
 **SYNTAX :**  `Register / Alias / [Address] = Register / Port / Number / String / Expression / [Address];`

```
R2 = P0;   
[PTBR + 3] = [1024] + 10;   
R1 = "hello world";             
```

### If Statement
**If** statement specifies the conditional execution of two branches according to the value of a logical expression. 
If the expression evaluates to 1, the **if** branch is executed, otherwise the **else** branch is executed. The **else** part is optional.   

**SYNTAX :**    
<pre><code>
<b>if</b> (logical expression) <b>then</b>
        statements;  
<b>else</b>
        statements;  
<b>endif</b>;
</code></pre>

### While Statement

**While** statement iteratively executes a set of statements based on a condition. 
The condition is defined using a logical expression. 
The statements are iteratively executed as long as the condition is true.  

**SYNTAX :** 

<pre><code>
<b>while</b> (logical expression) <b>do</b>
    statements;
<b>endwhile</b>;
</code></pre>

### Break Statement
**Break** statement when used inside a while loop block, stops the execution of the loop in which it is used and passes the control of execution to the next statement after the loop. 
This statement cannot be used anywhere else other than while loop.  

**SYNTAX :** `break;`


### Continue Statement
**Continue statement** when used inside a while loop block, skips the current iteration of the loop and passes the control to the next iteration after checking the loop condition.   

**SYNTAX :** `continue;`


### ireturn Statement
**ireturn** statement or the Interrupt Return statement is used to pass control from a kernel mode interrupt service routine to the user mode program which invoked it.  

**SYNTAX :**  `ireturn  ;`

The **ireturn** is generally used at the end of an interrupt code. This statement translates to [IRET machine instruction](../arch-spec/instruction-set.md).


### Read/Print Statements

The **read** and **print** statements are used as standard input and output statements. The **read** statement initiates the transfer of a string from the console to the standard input port P0 using the IN machine instruction. The machine proceeds to execute the next instruction without waiting for the completion of the string transfer.

!!! note
    String read or printed must not exceed 10 characters.

The **print** statement outputs value of a register or an integer/string literal or value of a memory location.  

**SYNTAX :** 
`read;` 

`print** Register / Number / String / Expression / [Address];`


### Readi Statement

The **readi** statement reads a value from the standard input device and stores it in a register using the INI machine instruction (which can be used only in debug mode).

!!! note
    String read must not exceed 10 characters.

**SYNTAX :** `readi Register;`

### Load/Store Statements

Loading and storing between the disk and the memory of the XSM machine can be accomplished using **load** and **store** statements in SPL. The machine proceeds to execute the next instruction without waiting for the completion of the block transfer. 
**load** statement loads the block specified by *block\_number* from the disk to the the page specified by the *page\_number* in the memory. 
**store** statement stores the page specified by *page\_number* in the memory to the the block specified by the *block\_number* in the disk.
The *page\_number* and *block\_number* can be specified using arithmetic expressions.

 **SYNTAX :** 
 ```
 load (page_number, block_number);
 store (page_number, block_number);
 ```


### Loadi Statement

Loading from the disk to the memory of the XSM machine can also be accomplished using **loadi** statement in SPL. But here, the machine will continue execution of the next instruction only after the block transfer is completed.
**loadi** statement loads the block specified by *block\_number* from the disk to the the page specified by the *page\_number* in the memory.
The *page\_number* and *block\_number* can be specified using arithmetic expressions.

**SYNTAX :** `loadi (page\_number, block\_number);`

### Multipush Statement

Multipush statement is used to push a sequence of registers into the memory locations starting from the address pointed to by SP. The registers are pushed in the order in which they are specified in the statement.

**SYNTAX :** `multipush (Register1, Register2, ...);`

### Multipop Statement

Multipop statement is used to pop a sequence of registers from the memory locations starting from the address pointed to by SP. The registers are popped in the reverse order in which they are specified in the statement.

**SYNTAX :** `multipop (Register1, Register2, ...);`

### Backup Statement

The **backup** statement is used to backup all the machine registers (except SP, IP, exception flag registers and ports) into the memory locations starting from the address pointed to by SP in the order : BP, PTBR, PTLR, R0 - R19. The value of SP gets incremented accordingly.


**SYNTAX :** `backup;`

This statement translates to the [BACKUP machine instruction](../arch-spec/instruction-set.md).


### Restore Statement

The **restore** statement is used to restore the backed up machine registers from the memory. The registers are restored from contiguous memory locations starting from the address pointed to by SP in the order : R19-R0, PTLR, PTBR, BP. The value of SP gets decremented accordingly. 


**SYNTAX :** `restore;`

This statement translates to the [RESTORE machine instruction](../arch-spec/instruction-set.md).


### Encrypt Statement

The **encrypt** statement replaces the value in the register Ri with its encrypted value. 

**SYNTAX :** `encrypt Ri;`

This statement translates to the [ENCRYPT machine instruction](../arch-spec/instruction-set.md).


### Goto Statement

The **goto** statement transfers control to the specified labelled statement.


**SYNTAX :** `goto label / INT_n / MOD_n / constants;` (See [SPL constants](constants.md))
```
goto label1;
goto INT\_7;
goto MOD\_2;
goto MEMORY\_MANAGER;
```

!!! note
    label should be defined within the module.


### Call Statement

The **call** statement saves procedure linking information on the stack and branches to the procedure specified by the argument.

**SYNTAX :** `call label / INT_n / MOD`_n / constants;` (See [SPL constants](constants.md))

```
call swap\_func;
call INT\_7;
call MOD\_2;
call MEMORY\_MANAGER;
```

!!! note
    label should be defined within the module.

Call statement translates to the [CALL machine instruction](../arch-spec/instruction-set.md).


### Return Statement

The **return** statement is used to transfer the control from a subroutine to the calling program in the kernel mode and the return address is popped from the stack.

**SYNTAX :** `return;`

This statement translates to the [RET machine instruction](../arch-spec/instruction-set.md).

### Halt Statement

The **halt** statement is used to halt the machine.  

**SYNTAX :** `halt;`

This statement translates to [HALT machine instruction](../arch-spec/instruction-set.md).


### Inline Statement

The **inline** statement is used to give XSM machine instructions directly within an SPL program.  

**SYNTAX :** `inline "MACHINE INSTRUCTION"`;
  
```
inline "JMP 11776";
```


## Functions

SPL does not provide explicit support for functions. However, a label can be defined at the beginning of the code for a function and the code can be invoked using the **call** instruction using the label. This allows use of functions inside a module. Labels defined in one module will not be visible in other modules.

If parameters are to be passed to a function, it has to be explictly passed either using agreed upon registers or using a stack.

A function loaded at a particular known location in memory (either specified directly by the memory address or using a pre-defined constant) can be invoked by a call to the corresponding memory address. However, it is recommended to follow the conventions discussed below in inter-module calls. 

```
call swap;
call MOD\_4;
call 511;  /* Transfers control to the first page in memory */  
```

## SPL Interrupt Handler and Module Programming Conventions

Each SPL System Call Handler/Interrupt Handler/Module is designed to occupy a maximum of two pages of continuous memory in the XSM machine. (Sometimes, the generic term "module" is abused to indicate all types of routines of the above categories, though we avoid this usage here). 
They contain protected mode code that carries out certain functions as determined by the OS programmer.
The following suggests certain programming conventions which are recommend while designing SPL modules and interrupt handlers.

These routines may be entered as a result of:   
1. A **system call handler** is entered upon execution of a software interrupt from an application (user mode) program.   
2. A **hardware interrupt/exception**  is executed when the machine raises a corresponding hardware signal/exception while an application was executing.
3. A  **module**  may invoked from another module or Interrupt handler.  

**Case a: (Software Interrupts)** In this case, the arguments to the module are passed through the **application program** stack.
The return values are also passed through the same stack.  **The convention is that the application must save the state 
of its registers before making the call** . (For instance, the eXpL compiler will save the caller context in the user stack
before invoking a software interrupt). Thus, the interrupt routine need not concern itself about saving the 
context of the application and can use the registers R0-R15 without saving them. 
However, the application is not expected to save the SP register before the call, 
and the module must save it for future return.

**In this case the kernel module must switch to the kernel stack and not use the application's stack.**
This is to avoid potential user level “hacks” into the interrupt modules through the stack.

![](../assets/img/memory_management.png)


**Case b: (Hardware Interrupts)** This case applies to the exception handler, timer interrupt routine, disk interrupt routine and the console interrupt routine. 
The difference here from *Case a)* is that the application does not have control over the transfer to the interrupt module, and hence would not have saved its context. 
**Thus, in this case, the module must save the register context of the application in its own stack** (or elsewhere in the memory) before using the registers and must restore the context before returning to the application.

In this case also the module is expected to allocate its own stack in the memory and not use the application's stack.

**Case c: (Modules)** In this case, since the caller and the callee are both executing in protected mode, the same stack can be used. Here, the recommended parameter passing convention is to use R1, R2... for argument\_1, argument\_2, argument\_3... The return value of the module may be stored in R0.

This convention is recommended instead of using the stack for passing arguments for improving efficiency. 

As in the previous cases, the caller must save the values of the registers in use into the stack
before the call. 


!!! note
    The SPL compiler given here uses the constants (given in  [*splconstants.cfg*](constants.md)  file) MOD\_0 to MOD\_7 as starting address of eXpOS kernel modules. eXpOS kernel loads these modules into various pre-defined memory pages of the XSM machine on startup. 
    In addition to these, all interrupt service routines can be programmed as SPL modules and loaded to the corresponding 
    interrupt service routine locations in memory. 
 

## <span style="color:red">SPL Specification for NEXSM</span>

The following additonal instructions are available in SPL when running on the [NEXSM machine](../arch-spec/nexsm.md), which is a two core extension for XSM. 

### TSL Expression

The contents of the memory location specified by ADDRESS is returned and the value at ADDRESS is set to 1.
**SYNTAX :** `tsl (ADDRESS)`

*Examples:*
```
while( tsl(KERN\_LOCK) == 1 ) do 
     continue; 
endwhile;
``` 
This statement translates to a sequence of instructions that uses the [TSL machine instruction](../arch-spec/nexsm.md#instr).
 


### START Statement

The **start** instruction when executed from primary core of the [NEXSM machine](../arch-spec/nexsm.md) will start the secondary core into parallel execution.

**SYNTAX :** `start;`

This statement translates to the [START machine instruction](../arch-spec/nexsm.md#instr).
 
### RESET Statement

The **reset** instruction when executed from primary core of the [NEXSM machine](../arch-spec/nexsm.md) will freeze the secondary core.

**SYNTAX :** `reset;`

This statement translates to the [RESET machine instruction](../arch-spec/nexsm.md#instr).
 