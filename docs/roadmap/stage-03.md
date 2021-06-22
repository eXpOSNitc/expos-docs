---
title: 'Stage 3 : Bootstrap Loader (2 Hours)'
original_url: https://exposnitc.github.io/Roadmap.html
---

!!! note "Learning Objectives"
       - Use the XSM Instruction set to write a small *OS startup* code.
       - Load your *OS startup code* into the *boot block* of the disk and get this code executed on bootstrap.

!!! abstract "Pre-requisite Reading"
       - Have a quick look at <a href="arch_spec-files/machine_organisation.html" target="_blank"> XSM Machine Organisation </a>. (Do not spend more than 15 minutes).
       - Have a quick look at <a href="arch_spec-files/instruction_set.html" target="_blank">XSM Instruction set</a>. (Do not spend more than 15 minutes).
       - It is absolutely necessary to read the <a href="Tutorials/xsm-instruction-cycle.html" target="_blank"><b>XSM privileged mode execution tutorial</b></a> before proceeding further.


When the XSM machine is started up, the <a href="arch_spec-files/machine_organisation.html#Boot ROM" target="_blank">
ROM Code </a>, which resides in page 0 of the memory, is executed. It is hard-coded into the machine. 
That is, the ROM code at physical address 0 (to 511) is "already there" when machine starts up.
The ROM code is called the "Boot ROM" in OS literature. Boot ROM code does the following operations :

1. Loads block 0 of the disk to page 1 of the memory (physical address 512).
2. After loading the block to memory, it sets the value of the register <a href="arch_spec-files/machine_organisation.html" target="_blank">
IP</a>(Instruction Pointer) to 512 so that the next instruction is fetched from location 512 (page 1 in memory starts from location 512).


In this stage, you will write a small assembly program to print "HELLO_WORLD" using XSM Instruction set 
and load it into block 0 of the disk using XFS-Interface as the <b>OS Startup Code</b>.
As described above, this OS Startup Code is loaded from disk block 0 to memory page 1 by the ROM Code 
on machine startup and is then executed.

*The steps to do this are explained in detail below.*

1) Create the assembly program to print "HELLO_WORLD".
The assembly code to print "HELLO_WORLD" :
```
MOV R0, "HELLO_WORLD"
MOV R16, R0
PORT P1, R16
OUT
HALT
```
Save this file as `$HOME/myexpos/spl/spl_progs/helloworld.xsm`.

2) Load the file as OS Startup code to `disk.xfs`using XFS-Interface.  
Invoke the XFS interface and use the following command to load the OS Startup Code
```
cd $HOME/myexpos/xfs-interface
./xfs-interface
# load --os $HOME/myexpos/spl/spl_progs/helloworld.xsm
# exit
```

Note that the `--os` option loads the file to Block 0 of the XFS disk.

3) Run the machine  
```
cd $HOME/myexpos/xsm
./xsm
```

The machine will halt after printing "HELLO_WORLD".

```
HELLO_WORLD
Machine is halting.
```

!!! note 
       The XSM simulator given to you is an assembly language interpeter for XSM.
       Hence, it is possible to load and run assembly language programs on 
       the simulator (unlike real systems where binary programs need to be supplied).


??? question "If the OS Startup Code is loaded to some other page other than Page 1, will XSM work fine?"
       No. This is because after the execution of the ROM Code, IP points to *512* which is the 1<sup>st</sup>
       instruction of Page 1. So if the OS Startup Code is not loaded to Page 1, it results in an <a href="./arch_spec-files/interrupts_exception_handling.html" target="_blank">exception</a> and leads to system crash.

!!! assignment "Assignment 1"
       Write an assembly program to print numbers from 1 to 20 and run it as the OS Startup code.
