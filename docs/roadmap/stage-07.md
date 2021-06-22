---
title: 'Stage 7 : ABI and XEXE Format (2 Hours)'
original_url: https://exposnitc.github.io/Roadmap.html
---

!!! note "Learning Objectives"
      - Familiarise with the Application Binary Interface(ABI) of eXpOS.
      -  Modify the INIT program to comply with the eXpOS ABI.
!!! info " Pre-requisite Reading"
      Read and Understand the eXpOS <b>Virtual Address Space Model</b> and <b> XEXE Executable File Format </b> from <a href="abi.html#xexe" target="_blank"> eXpOS ABI Documentation</a> before proceeding further.


In this stage we will rewrite the user program and OS startup code of Stage 6 in compliance with expos ABI.

#### Modifying INIT

The INIT program must be modified to comply with the XEXE executable format.
The executable format stipulates that the first 8 words of the file must contain a header.
The rest of the file contains the program instructions. The OS is expected to load the file
into logical pages starting from page 4. Thus the first disk block of the program is loaded
into logical address starting from 2048,
second (if the file size exceeds 512 words) to logical addresses starting from 2560
and so forth.

Since the first instruction starts after the 8 word header, the first instruction in the
program will be loaded into memory address 2056. Since each instruction requires two words,
the second instruction will start at memory address 2058 and so on. Thus the jump addresses
in the INIT program must be designed with this in mind.


The INIT program complying to ABI is given below. The code is given in bold and the
corresponding addresses are added for reference.
<pre><code>
2048<b>  0</b>
2049<b>  2056</b>
2050<b>  0</b>
2051<b>  0</b>
2052<b>  0</b>
2053<b>  0</b>
2054<b>  0</b>
2055<b>  0</b>
2056<b>  MOV R0, 1</b>
2058<b>  MOV R2, 5</b>
2060<b>  GE R2, R0</b>
2062<b>  JZ R2, 2074</b>
2064<b>  MOV R1, R0</b>
2066<b>  MUL R1, R0</b>
2068<b>  BRKP</b>
2070<b>  ADD R0, 1</b>
2072<b>  JMP 2058</b>
2074<b>  INT 10</b>
</code></pre>


####   Modifications to OS Startup Code
1) Load Library Code from disk to memory
```
loadi(63,13);
loadi(64,14);
```

The eXpOS ABI stipulates that the code for a shared library must be loaded to disk blocks 13
and 14 of the disk. During OS startup, the OS is supposed to load this code into memory pages
63 and 64. This <b>library code must be attached to logical page 0 and logical page 1 of each process</b>.
Thus, this code will be shared by every application program running on the operating system and is called the
<b>common shared library</b> or simply the library.

The library provides a common code interface for all system calls. This means, to invoke a
system call, the application can call the corresponding library function and the library will
in turn invoke the system call and return values back to the application. The library also
implements some functions like dynamic memory allocation and de-allocation from the heap
area.

<b>
The dynamic memory allocation functions of the library manage the heap memory of the
application program. The ABI stipulates that each application must be provided 2 pages of
memory for the heap. These two pages must be attached to logical pages 2 and 3 of the
application.
</b>


Note here that the library code is not part of the application's XEXE executable file. The
library code is "attached" to the address space of the application when the application is
loaded into memory for execution. Since the ABI stipulates the the library will be loaded to
logical pages 0 and 1, the application "knows" the logical address of the library routines
and will contain call to these routines, though the routines are not present in the
application's code.


Thus, the OS must do the following to ensure correct run time linkage of library code to each
application.

i. The library code must be pre-loaded to disk blocks 13 and 14 before OS startup.The library code can be found in the expl folder in eXpOs package.Load it into the XSM disk using the xfs-interface
```
load --library ../expl/library.lib
```

ii. During OS start-up, this code must be loaded to memory pages 63 and 64.

iii. When each application is loaded for execution, the logical pages 0 and 1 must be mapped to physical pages 63 and 64.

iv. Two physical pages must be allocated for the application's heap and attached to logical pages 2 and 3.
 
2) Modify the Page table entries according to ABI.

The <a href="support_tools-files/constants.html" target="_blank">SPL constant</a>PAGE_TABLE_BASE holds
the value 29696. A total of 16 page tables can be stored starting from this address.
Each page table will be 20 entries. For each user process, one page table will be allocated.

Here since we are running the first user program, we will use the first few entries of this
memory region for setting up the page table for the INIT process.

As noted, the first disk block of the INIT program (block 7) must be loaded to logical page 4.
Similarly, block 8 must be loaded to logical page 5. The ABI stipulates that two pages must be allocated for
the stack at logical pages 8 and 9.

The following code sets page table entries for logical page 4 and 5(for code area), logical
page 8 and 9(for user stack), logical pages 2 and 3(for heap) and logical pages 0 and 1(for
library). Since pages 0 to 75 are reserved for the use of the OS kernel, the first four free pages
(76,77,78 and 79) will be allocated for stack and heap area. See <a href="os_implementation.html" target="_blank">Memory Organisation.</a>
Note that the code and library pages must be kept read only where as stack and heap must be
read-write.(see <a href="arch_spec-files/paging_hardware.html" target="_blank"> page table</a>settings for details).

```
//Library
[PTBR+0] = 63;
[PTBR+1] = "0100";
[PTBR+2] = 64;
[PTBR+3] = "0100";

//Heap
[PTBR+4] = 78;
[PTBR+5] = "0110";
[PTBR+6] = 79;
[PTBR+7] = "0110";

//Code
[PTBR+8] = 65;
[PTBR+9] = "0100";
[PTBR+10] = 66;
[PTBR+11] = "0100";
[PTBR+12] = -1;
[PTBR+13] = "0000";
[PTBR+14] = -1;
[PTBR+15] = "0000";

//Stack
[PTBR+16] = 76;
[PTBR+17] = "0110";
[PTBR+18] = 77;
[PTBR+19] = "0110";
```

3) Since the total address space of a process is 10 pages, PTLR register must be set to value 10.
```
PTLR = 10;
```

4) The second entry of the header of an executable file will contain an entry point value. This
is the address of the first instruction to be executed when the program is run.

Hence, you must initialise IP to the second word in the header. Since the first code page is
loaded into memory page 65,
the address of the second word in header is calculated as (65 * 512) + 1. This value is
stored to the top of the user stack.
The machine on executing IRET instructions pops this value from the stack and sets IP to that
value.
```
SP = 8*512;
[76*512] = [65 * 512 + 1];
```

#### Making Things Work
1. Compile and load the modified OS startup Code.
2. Load the modified user program.
3. Run the machine in debug mode.

!!! assignment "Assignment 1"
      Change the user program to compute cubes of the first five numbers.