---
title: 'Stage 8 : Handling Timer Interrupt (2 Hours)'
original_url: https://exposnitc.github.io/Roadmap.html
---

!!! info "Learning Objectives"
      - Run the XSM machine with Timer enabled.
      - Familiarise with timer interrupt handling.

!!! abstract "Pre-requisite Reading"
      Read and understand the <a href="Tutorials/xsm_interrupts_tutorial.html" target="_blank"> XSM tutorial on Interrupts and Exception handling</a> before proceeding further. (Read only the Timer Interrupt part).

**Try to solve the following question that tests your understanding.**

!!! question 
    Suppose the XSM machine was executing in unprivileged mode and just after
    instruction at logical address 3000 was fetched and executed, the machine found that
    the timer interrupt was pending. Suppose that at this time, the values of the
    some of the machine registers were as the following :

    ```
    IP: 3000,
    PTBR: 29696,
    SP 5000
    ```

    ??? question "Which physical memory location will contain the physical page number to which return address will be stored by the machine before transferring control to the timer interrupt handler?"
        29714 (Why?) It is absolutely necessary that you read the <a href="http://exposnitc.github.io/Tutorials/xsm_unprivileged_tutorial.html" target="_blank">XSM unprivileged mode execution tutorial</a>if you are not able to solve this question yourself.
    ??? question "Suppose further that the memory location 29714 contains value 35. What will be the physical memory address to which the XSM machine will copy the value of the next instruction to be executed?"
        18313 (Again if you are not able to solve the problem yourself, you must read the <a href="http://exposnitc.github.io/Tutorials/xsm_unprivileged_tutorial.html" target="_blank">XSM unprivileged mode execution tutorial</a>)
    ??? question "What will be the value stored into the location 18313 by the machine?"
        3002 This is the (logical) address of the next instruction to be executed after return from the interrupt handler. Note the each XSM instruction occupies two words in memory and hence the next instruction's address is at 3002 (and not 3001).
    ??? question "What value will the SP and IP registers contain after the execution of the INT instruction?"
        SP=5001 and IP=2048
    ??? question "What will be the physical address from which the machine will fetch the next instruction?"
        2048 Since the machine switches to privileged mode once the interrupt handler is entered, the next instruction will be fetched from the address pointed to by IP register without performing address translation.


If the XSM simulator is run with the the timer set to some value - say 20, then every time the
machine completes execution of 20 instructions in user mode, the timer device will send a
hardware signal that interrupts machine execution. The machine will push the IP value of the
next user mode instruction to the stack and pass control to the the timer interrupt handler at
physical address 2048.

eXpOS design given <a href="os_implementation.html" target="_blank">here</a>
requires you to load a timer interrupt routine into two pages of memory starting at memory address 2048 (pages
4 and 5). The routine must be written by you and loaded into disk blocks 17 and 18 so that the
OS startup code can load this code into memory pages 4 and 5.

In this stage, we will run the machine with timer on and write a simple timer interrupt handler.


#### Modifications to OS Startup Code

OS Startup code used in the previous stage has to be modified to
load the timer interrupt routine from disk blocks 17 and 18 to memory pages 4 and 5.

```
loadi(4, 17);
loadi(5, 18);
```

#### Timer Interrupt

We will write the timer interupt routine such that it just prints "TIMER" and returns to the
user program.
```
print "TIMER";
ireturn;
```
1) Save this file in your UNIX machine as $HOME/myexpos/spl/spl_progs/sample_timer.spl

2) Compile this program using the SPL compiler.

3) Load the compiled XSM code as the timer interrupt into the XSM disk using XFS Interface.
```
cd $HOME/myexpos/xfs-interface
./xfs-interface
# load --int=timer $HOME/spl/spl_progs/sample_timer.xsm
# exit
```

4) Recompile and reload the OS Startup code.

5) Run the XSM machine with timer enabled.

```
cd $HOME/myexpos/xsm
./xsm --timer 2
```