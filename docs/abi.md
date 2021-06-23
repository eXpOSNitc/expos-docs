---
title: Application Binary Interface (ABI)
original_url: https://exposnitc.github.io/abi.html
hide:
    - navigation
---

An application binary interface (ABI) is the interface between a user program and the kernel.

The eXpOS ABI defines the following:

- The **machine model** - that is, the instruction set and the virtual memory address space to which an application/compiler generating executable file must generate target code for. This is very much architecture specific.
 
- A logical division of the memory address space into **regions** - _text, stack, heap and library_ and the low level (assembly/machine level) system call interface. This part is dependent on both the OS and the architecture.
  
- The **file format** to be followed for executable files by the compiler (the XEXE executable file format). This part is generally OS specific and architecture independent. Compilers must generate executable files adhering to this format.
  
- A **low level system call interface** which gives the specification of the software interrupt instruction (trap) corresponding to each system call and the order in which arguments must be passed to the system call through the application program's stack.This part is architecture dependent.
  
- The **low level runtime library interface :** The low level runtime library interface consists of user level routines which provide a layer of abstraction between the low level system call interface and the application program by providing a unified interface for all system calls, hiding low level interrupt details from the application. (Applications however, may choose to bypass this layer and directly invoke the low level system calls.) In addition to the system call interface, application level dynamic memory allocator and deallocator functions are also part of the eXpOS library.


###  XSM User Level Instruction Set
XSM Instruction set describes the target language in which a compiler must generate an executable file. Instructions are classified into privileged and unprivileged instructions. Since application programs run in the user mode, they can make use of only unprivileged instructions.

You can read more about the XSM user level instruction set [here](./virtual-machine-spec.md).

### Virtual Address Space Model

The (virtual) address space of any eXpOS process is logically divided into four parts namely _Shared Library, Heap, Code and Stack_.  

![](./assets/img/process_model.png)

**Shared library** can be shared by more than one executable file. The maximum size of this memory region is X\_LSIZE.

!!! note
    eXpOS provides a library that provides a unified interface for system calls and dynamic memory allocation/deallocation routines. The library is pre-loaded into memory at the time of OS startup and is linked to the address space of a process when an executable program is loaded into the memory for execution if required (as determined by the Library flag in the [executable file](abi.md#xexe)) . The eXpOS implementation for the XSM architecture discussed here sets X\_LSIZE to 1024 words. Thus the shared library will be loaded into the region between memory addresses 0 and 1023 in the address space of the process.

**Heap** is the portion of the address space of a process reserved as the memory pool from which dynamic memory allocation is done by the allocator routines in the shared library (for example, memory allocated via malloc in C). The maximum size of this memory region is X\_HSIZE. Library functions access this portion of memory for dynamic memory allocation and deallocation. The eXpOS execution semantics specify that when a process executes the Fork system call, this region will be shared between the parent process and the child process. The eXpOS implementation for the XSM architecture discussed here sets X\_HSIZE to 1024 words. Thus the heap region will be between memory addresses 1024 and 2047 in the address space of the process.

**Code** contains the header and code part of the XEXE executable file, which is loaded by the eXpOS loader from the file system when the Exec system call is executed. The first eight words of the executable file contains the header. The rest of the code region contains the XSM instructions. The total size of code section cannot exceed X\_CSIZE. The eXpOS implementation for the XSM architecture discussed here sets X\_CSIZE to 2048 words. Hence, the code region will be between memory addressess 2048 and 4095 in the address space of the process.

**Stack** is the space reserved for the runtime stack of the process. Parameters and local variables associated with functions in a program are allocated in the stack. In the XSM architecture, the stack grows upwards and the maximum stack size is X\_SSIZE. Global variables are normally allocated in the stack as the executable file format does not support a separate [Data region](http://en.wikipedia.org/wiki/Data_segment). The eXpOS implementation for the XSM architecture discussed here sets X\_SIZE to 1024 words.Thus the stack will occupy the region between memory address 4096 and 5119 in the address space of the process.

A description of the user level address space provided by XSM is given [here](./virtual-machine-spec.md).

### XEXE Executable File Format

Executable files in eXpOS must be in the [XEXE format](./os-spec/expfs.md) as eXpOS executes only files of such format.

An XEXE executable file in eXpOS consists of two parts:

-   1\. Header
-   2\. Code

![](./assets/img/exe_file.jpeg)

  

The maximum size of the file (including the header) is limited by the constant EXE\_SIZE. The eXpOS implementation for the XSM architecture discussed here sets EXE\_SIZE to 2048 words.

The first eight words of an executable file are reserved for the header which describes the features of file. The structure of the header is :

![](./assets/img/header.png)

**XMAGIC** is a number indicating the type of executable file. All XEXE files will have magic number 0. For more on Magic Number, click [here](http://en.wikipedia.org/wiki/File_format#Magic_number).

**Entry point** contains the virtual address in memory of the first instruction to be executed (entry point) of the program after the OS loader has loaded it. During loading, the program counter must be initialized to this address.

**Text Size**, **Data Size**, **Heap Size** and **Stack size** indicates the sizes of Text, Data, Heap and Stack regions to be allocated by the OS loader when the file is loaded for execution.

!!! note
    The present eXpOS virtual address space model requires that the data and stack must be in the same memory area and must be managed by the compiler / application program (this means that the program must contain the code to initialize the value of the stack pointer). The value of Data Size field is ignored. Moreover, the eXpOS loader ([exec system call](os-spec/systemcallinterface.md#processsystemcalls)) sets the size of text region to 2048 words and stack region to 1024 words in memory irrespective of the values present in the header.

If the **Runtime Library** must be included when the file is loaded, the Library Flag is set to 1 in the executable file. If this flag is not set then neither memory is allocated for the heap nor the library linked to the address space of the process by the eXpOS loader at execution time.

In summary, the eXpOS loader maps an executable file into its virtual address according to the following table :

|Region|Start Address|End Address|
|--- |--- |--- |
|Library*|0|1023|
|Heap*|1024|2047|
|Code**|2048|4095|
|Stack†|4096|5119|


\* If Library Flag is set to 1 in the executable header.

\*\* The eXpOS loader sets IP to the value specified in the program header.

† The eXpOS loader does not gurentee that the values of SP and BP are initialised to the base address of the stack region. Hence the executable program must contain code to initialise these registers.


### Low Level System Call Interface

The **Low level system call interface** describes the conventions to be followed by application programs that invoke [eXpOS system calls](./os-spec/systemcallinterface.md) on the XSM architecture. The interface describes the software interrupt instruction (trap) corresponding to each system call and the calling conventions for passing arguments and extracting return values of the system call through the application program's stack. This part is architecture dependent.

!!! note
    If a high level language like [ExpL](https://silcnitc.github.io) is used for writing application programs, then the application programs will be using the [high level library interface](./os-spec/dynamicmemoryroutines.md) for invoking system calls. The ExpL compiler is responsible for generating assembly language code to translate the call to a corresponding library call using the low level library interface. The ExpL library which is pre-loaded into the system memory during eXpOS boot up contains assembly language code that redirects the library call to the corresponding eXpOS system call using the low level system call interface described here. If you write assembly language application programs as user programs, then you can use the low level system call interface directly bye-passing the library.

#### System Calls
For an application program, there are two stages in executing a system call:

1) **Before the system call** : The calling application must set up the arguments in the (user) stack before executing the trap instruction.
	    
!!! note "Important Note"
    The calling application is supposed to save its register context into the stack before making a system call.The system call is not expected to save the user context of the calling application.  However, the [ExpL calling convention](https://silcnitc.github.io/run_data_structures/run-time-stack.html)(unfortunately) does not save the Base Pointer Register (BP) before the call. Hence, the OS implementation must be careful to save the value of the register.

2) **After the system call** : The return value of the system call must be extracted from the stack.

##### Invoking a system call
A user program invokes a system call by first pushing the system call number and then the arguments into the stack and then invoking the **INT** machine instruction corresponding to the system call. The eXpOS ABI stipulates that the number of arguments pushed into the stack is fixed at three.
<pre><code>
PUSH System_Call_Number     // Push system call number
PUSH Argument_1             // Push argument 1 to the stack
PUSH Argument_2             // Push argument 2 to the stack
PUSH Argument_3             // Push argument 3 to the stack
<b>PUSH R0                     // Push an empty space for RETURN VALUE</b>
INT number                  // Invoke the corresponding INT instruction.
                            // The number can be any number between 4 and 18
</code></pre>

A system call invocation using the high level application programmer's interface of a programming language like ExpL compiles to a set of machine instructions (see the instructions to the left). They are the stack operations that must be performed by the user program before the INT instruction is executed.

<!-- IMAGE -->
![](./assets/img/system_call_stack1.png){ align=left width=40% }
The arguments must be pushed into the stack in such a way that the last argument comes on the top. An additional push instruction ('PUSH R0') is inserted to have an empty space in the stack for the return value. The system call implementation must ensure that the return value is stored in this space. The system call number is also pushed to the stack. The interrupt routine needs this value to identify the system call. The figure to the left shows the data stored in process stack just before an INT instruction.

<!-- IMAGE LEFT  -->
![](./assets/img/system_call_stack2.png){ align=right width=40%}
The INT instruction in XSM will push the value of IP + 2 on to the stack. This is the address of the instruction immediately following the INT instruction in the user program. Each instruction is 2 words, hence IP is incremented by 2. Upon execution of the IRET instruction from the system call, execution resumes from this value of IP. The INT instruction changes mode from **User** mode to **Kernel** mode and passes control to the Interrupt Routine corresponding to the system call. The figure to the right shows the contents of the stack immediately after the execution of the INT instruction.

##### After return from the system call
The IRET instruction transfers control back to the user program to the instruction immediately following the INT instruction. The following machine instructions are present after the INT instruction in the ExpL compiled machine code given in the previous step.
```
POP Ri           // Pop and save the return value into some register Ri
POP Rj           // Pop and discard argument 3
POP Rj           // Pop and discard argument 2
POP Rj           // Pop and discard argument 1
POP Rj           // Pop and discard the system call number
// Now the stack is popped back to the state before call
```
The machine code to the left pops the values from the stack. The system call number and arguments were inputs to the system call and hence they may be discarded now. The return value which is stored in the stack by the system call is fetched and used by the user program by popping out to some register.



##### System calls and their translation

Associated with each system call, there is a system call number and interrupt routine number. The system call number is used to identify a system call. The interrupt routine number denotes the number of the interrupt routine which handles the system call. An interrupt routine may handle more than one system call.

**Mapping of system calls to interrupt numbers and corresponding system call interface specification with details of arguments and return values of system calls are given in the [eXpOS Low Level System Call Interface](./os-design/sw-interface.md) Documentation.**


### Low Level Runtime Library Interface

The eXpOS library consists of a collection of user level routines provided as part of the operating system. These routines are loaded to the memory during OS start up and can be linked to the address space of any user process by the OS loader (exec system call). The OS loader will link these routines to the shared library region of the address space (see address space) if the library flag in the header of the executable file being loaded is set to 1 (see xexe).

The library provides a **uniform interface** through which an application program can invoke system calls and dynamic memory allocation / deallocation routines by providing the function code and the arguments. The interface hides the details of the interrupt service routines corresponding to the **system calls** from the application, thereby making them architecture independent. The library also provides user level routines for **dynamic memory management (allocation and de-allocation)** from the _heap region_ of the application.

![](./assets/img/memory_management.png)  

The library routine is linked to **virtual address 0** of the address space of a process by the OS loader and requires four arguments (function code and three arguments to the system call / memory management routine) to be passed through the stack. The routine invokes the corresponding low level system call / memory management routine and returns to the user program the return value of the system call / memory management routine through the stack. The figure to the side shows the contents of the stack immediately before a call to this library routine.

The invocation details for the system calls and the dynamic memory management routines using the library interface can be seen in the [**eXpOS High Level Library Interface**](./os-spec/dynamicmemoryroutines.md) documentation.

#### Invoking a library module
<pre><code>
PUSH Function_Code          // Push Function Code
PUSH Argument_1             // Push argument 1 to the stack
PUSH Argument_2             // Push argument 2 to the stack
PUSH Argument_3             // Push argument 3 to the stack
<b>PUSH R0                  // Push an empty space for RETURN VALUE</b>
CALL 0                  	// Pass the control to virtual address 0.
// (eXpOS loader links the library to virtual address 0)
</code></pre>
A library module invocation using the high level application programmer's interface of a programming language like ExpL compiles to a set of machine instructions (see the instructions to the right). They are the stack operations that must be performed by the user program before the CALL instruction is executed.

#### After return from the library module

The following machine instructions are present after the CALL instruction in the ExpL compiled machine code given in the previous step.
```
POP Ri           // Pop and save the return value into some register Ri
POP Rj           // Pop and discard argument 3
POP Rj           // Pop and discard argument 2
POP Rj           // Pop and discard argument 1
POP Rj           // Pop and discard the function code
// Now the stack is popped back to the state before call
```
The machine code to the left pops the values from the stack. The function code and arguments were inputs to the library module and hence they may be discarded now. The return value which is stored in the stack by the system call is fetched and used by the user program by popping out to some register.

!!! note 
    If application programs are written in a high level language like ExpL, the [exposcall()](./os-spec/dynamicmemoryroutines.md) function will be used to make system calls/invoke dynamic memory routines. The programmer does not have to worry about the library interface specified here because the ExpL compiler will automatically generate assembly code that translate the high level call to a low level call to the library using the above interface and retrieve return values from the call. eXpOS pre-loads the library into the memory at boot time. The library re-directs system call requests to the OS through the low level system call interface. Dynamic memory mangement functions are implemented as part of the library itself.