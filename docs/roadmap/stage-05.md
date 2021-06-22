---
title: 'Stage 5 : XSM Debugging (2 Hours)'
original_url: https://exposnitc.github.io/Roadmap.html
---

!!! note "Learning Objectives"
    Getting familiarised with the XSM Debugger.

!!! info "Pre-requisite Reading"
     Read and understand the [Debugger Specification](../support-tools/xsm-simulator.md)

In this stage you will write an SPL program with a **breakpoint** statement. The breakpoint statement translates to the [BRKP](../arch-spec/instruction-set.md) machine instruction and is used for debugging. If the XSM machine is run in the [Debug mode](../support-tools/xsm-simulator.md) , on encountering the BRKP instruction, the machine simulator will suspend the program execution and allow you to inspect the values of the registers, memory, os data structures etc. Execution resumes only after you instruct the simulator to proceed.

1)  Write an SPL code to generate odd numbers from 1 to 10. Add a debug instruction in between :

```
alias counter R0;
counter = 0;
while(counter <= 10) do
  if(counter%2 != 0) then
    breakpoint;
  endif;
  counter = counter + 1;
endwhile;
```

2) Compile the program using the SPL compiler.

3) Load the compiled xsm code as OS startup code into the XSM disk using the XFS interface.

4) Run the machine in debug mode.

```
cd $HOME/myexpos/xsm
./xsm --debug
```

5)  The Machine pauses after the execution of the first BRKP instruction.
View the contents of registers using the command
```
reg
```

Enter the following command

```
mem 1
```

This will write the contents of memory page 1 to the file mem inside the xsm folder (if xsm is run from any other directory then the file mem will be created in that directory). Open this file and view the contents.  

Use the following command step to the next instruction.

```
s
```

6)  Press c to continue execution till the BRKP instruction is executed again. You can see that the content of R0 register changes during each iteration.

```
c
```