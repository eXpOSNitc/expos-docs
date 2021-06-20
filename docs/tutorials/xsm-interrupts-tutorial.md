---
title: XSM Interrupts and Exception Handling
original_url: https://exposnitc.github.io/Tutorials/xsm_interrupts_tutorial.html
---

We have seen that an application program can transfer control to a privileged mode
trap handler using the INT instruction.  Hardware interrupts (or simply interrupts) are useful
to transfer control into handlers that must be run on the occurrence of hardware events.

XSM machine supports three hardware interrupts - timer interrupt, disk interrupt and console
interrupt.  Associated with each interrupt, there is
an interrupt handler routine.   These handler routines are called

<b>timer interrupt handler, disk interrupt handler and the console interrupt handler</b>
respectively.
The addresses of these handlers are stored in locations 493, 494 and 495 of the ROM and are preset to
values 2048, 3072 and 4096.  Thus, the OS bootstrap code must load the timer interrupt handler into
memory starting from 2048, disk interrupt handler from address 3072 and console interrupt handler from 4096.

### Timer Interrupt

XSM has a timer device which can be set to interrupt the machine at regular intervals of time.
You can run the XSM simulator with the option `--timer`:
```
xsm  --timer 10
```

Then, every time the machine completes executing ten instructions in unprivileged mode, the machine does the following actions:

1. *Push the IP value into the top of the stack.
2. Set IP to value stored in the interrupt vector table entry for the timer interrupt
  handler.  The vector table entry for timer interrupt is located at physical address 493 in page 0
  (ROM) of XSM and the  value 2048 is preset in this location.  Hence, the IP register gets value 2048.
  The machine then switches to to privileged mode and address translation is disabled.
  Hence, next instruction will be fetched from physical address 2048. (See Boot ROM and Boot block section in <a href="../arch_spec-files/machine_organisation.html" target="_blank"> XSM Machine Organisation </a> documentation)


!!! note "* Note"
    If the value in the SP register after incrementing SP is an invalid address (i.e., not in the range 0 to PTLR*512-1)
    then the machine generates an <b>illegal memory access exception</b> (see section below on exception handling).  The machine will re-execute steps (1) and (2) immedietly after retrun to unprivileged mode, before executing any other instruction in unprivileged mode. 

Note that the action is similar to the INT instruction except that the application does not invoke the timer handler using the INT instruction.  In fact, the application does not have any control over the process.
<b>Interrupts are disabled when machine runs in the privileged mode so that there are no race conditions.</b>
After returning from the timer interrupt handler, the next entry into the handler occurs only after the machine
executes another ten instructions in user mode.

The timer device can be used to ensure that privileged code gets control of the machine at regular
intervals of time.  This is necessary to ensure that an application once started is not allowed to run
"forever."  In a time-sharing environment, <b>the timer handler invokes the scheduler of
the OS to do a context switch</b> to a different process when one process has completed its time quantum.

!!! note "Important Note"
    In real machines, timer, disk and console are devices that are external to the CPU.
    (This is why the <a href="http://exposnitc.github.io/arch_spec-files/machine_organisation.html" target="_blank"> XSM machine model </a> draws them outside the machine's CPU).
    Such devices are generally attached to <a href="https://simple.wikipedia.org/wiki/Device_controller" target="_blank"> programmable device-controllers </a> in the computer system's <a href="https://en.wikipedia.org/wiki/Motherboard" target="_blank"> mother-board </a> containing the CPU.
    These devices are typically either I/O mapped (via ports) or
    <a href="https://en.wikipedia.org/wiki/Memory-mapped_I/O" target="_blank"> memory mapped </a>
    and the exact configuration is determined by the hardware
    manufacturer. The hardware manufacturer supplies a <a href="https://en.wikipedia.org/wiki/Device_driver" target="_blank">device driver software </a> for each of these device controller. The device driver software is typically loaded into memory
    along with the OS kernel during machine bootstrap. Thus, the device drivers run as part of the kernel.
    Each device driver contains a set of functions that can be invoked from the OS kernel.  These
    device driver functions in turn contain code that issues commands to the
    respective device controller. Finally, the device controller contains the
    software and hardware necessary to make the device physically behave in the required way
    based on the commands received.

    <img src="https://exposnitc.github.io/img/os-design/xsm_machine_model.jpg">
    Thus, in a real systems, the OS loads into the memory
    the timer device's driver during bootstrap.
    (Here, the driver is assumed to have been pre-loaded into the disk.  However modern systems also permit drivers to be loaded at run time without re-booting the OS)
    After this, some kernel boot code will invoke the appropriate
    functions of the device driver to perform initial configuration of
    the timer device so as to interrupt the machine at regular intervals of time.
    The timer device will have some output wire that (after passing through
    several intermediate hardware circuits) connects to some interrupt pin of
    the CPU.  The OS bootstrap code will instruct the device driver to configure the device in such manner that
    the device sends a signal to the interrupt pin at regular intervals of time.  Each time
    such signal is received,  the CPU saves the next
    instruction's IP value to the stack and transfers control to the interrupt routine.

    Thus, it is important to understand that the XSM machine is a software simulated machine
    and hence deviates from real systems.  No real life CPU comes with hardware that counts
    the number of instructions and invoke the timer interrupt handler after a pre-set number of
    instructions as XSM machine does.  The same comment holds for the disk and the console interrupts as well.

### Disk and Console Interrupts


The other two interrupt handlers are associated with the disk and the console.
The XSM privileged instructions load(page_num,block_num) and store(block_num, page_num) are used for transfer of data from disk to memory and memory to disk.  The actual data transfer involves time delay as disk access is slow. <b>On encountering a load/store instruction, the XSM machine will start a disk transfer, increment IP by two and fetch the next instruction without waiting for the data transfer to be completed. When the actual disk-memory data transfer is completed, the disk controller will raise the disk interrupt.</b> Similarly, the IN instruction initiates a console input but will not suspend machine execution till some input is read.  Machine execution proceeds to the next instruction in the program.  When the user enters data, the data is transferred to port P0, and a console interrupt is raised by the console device.


After the execution of each instruction in unprivileged mode, the machine checks whether a pending
disk/console/timer interrupt.  If so, the machine does the following actions:

1.  **\***Push the IP value into the top of the stack.
2.  Set IP to value stored in the interrupt vector table entry for the timer interrupt handler. The vector table entry for timer interrupt is located at physical address 493 in page 0 (ROM) of XSM and the value 2048 is preset in this location. Hence, the IP register gets value 1. The machine then switches to to privileged mode and address translation is disabled. Hence, next instruction will be fetched from physical address 2048. (See Boot ROM and Boot block section in [XSM Machine Organisation](../arch_spec-files/machine_organisation.html) documentation)

!!! note
    If the value in the SP register after incrementing SP is an invalid address (i.e., not in the range 0 to PTLR\*512-1) then the machine generates an **illegal memory access exception** (see section below on exception handling). The machine will re-execute steps (1) and (2) immedietly after retrun to unprivileged mode, before executing any other instruction in unprivileged mode.

<!--pushes the address of the next instruction to the
stack and transfers control to the interrupt handler</b> (just as in the case of the timer interrupt).
As noted previously, the OS must load the disk interrupt handler into the two pages starting at memory page
 6 (address 3072), and console interrupt handler into the two pages starting at memory page 8 (address 4096).
 This is normally done during OS start-up.-->

<b>The XSM machine enables interrupts only when the machine is executing in unprivileged mode.</b>(If a previously initiated load/store/IN operation is completed while XSM is running in privileged mode,
the machine waits for next transition to unprivileged mode before processing the interrupt.)</p>

### Exception handling in XSM 

What must happen when an application running in unprivileged mode contains an illegal instruction or a
divide by zero instruction or an instruction that tries to write data into a logical address outside its
address space?

Clearly, the machine must not halt, for otherwise, one application will be able to halt the whole system. The correct action must be to transfer control to some privileged mode handler. This privileged mode handler is the <b>exception handler</b>.   The exception handler code must start at memory address 1024. (page 2).

While an application is running in unprivileged mode on the XSM machine, if any of the following events occur,
the XSM machine raises an exception.


a) **Illegal Memory Access:** Occurs when any address generated by the application lies outside its logical address space. This also occurs when the process tries to write into pages whose [Write access bit](../arch_spec-files/paging_hardware.html) is not set in the page table. Recall that the logical page number generated for a valid instruction should be between 0 and the value of (512 \* PTLR) - 1.  
b) **Illegal instructions:** Occurs when an application tries to execute an instruction not belonging to the instruction set or when an operand/data in an instruction is not legal. (Example: MOV 4 R0, MOV IP, 4)  
c) **Arithmetic exception:** Occurs when there is a division/modulus by zero. (Example: DIV R0, 0)  
In all the above cases, the typical action is for the exception handler code is to pass control to other privileged mode OS routines to terminate the application and schedule other applications. d) **Page fault:** This is the most significant exception handling function that must be understood clearly. A page fault occurs if an instruction contains an address whose logical page number is within the range 0 to PTLR-1 and the [valid bit](../arch_spec-files/paging_hardware.html) in the corresponding page table entry is set to to 0.

Page fault exception can occur either during instruction fetch or operand fetch. Suppose during execution of an application, the value of IP reaches value – say 3000. The next fetch will try to translate the logical address 3000 to physical address using the page table. The logical page number corresponding to address 3000 is 3000 DIV 512 = 5. The machine must look up the page table entry corresponding to logical page 5. If the valid bit for this entry is set to 0, the page reference is invalid. In this case, the machine will raise an exception.

The second possibility for a page fault to occur is during operand fetch. Suppose an instruction is successfully fetched – say MOV R0, \[5000\]. To execute the instruction, the machine will try to translate the logical address 5000 using page table. As in the previous case, if the page is not valid, then the machine raises an exception.

Page fault exception allows the OS to delay allocation of memory pages to a program in execution till the program actually tries to access the page. The OS can set the valid bit of unallocated pages in the address space of the process to 0 and wait for the program to generate a page fault when (and if) the program tries to access the page. The page fault handler can be designed to attach the required memory pages to the program (often loading the page from the disk) so that the program can resume execution. Such "lazy" allocation minimizes memory usage and will help the OS to concurrently accomodate more programs in memory than what would be possible without deploying such lazy allocation. This technique is called [demand paging](https://en.wikipedia.org/wiki/Demand_paging).


When the machine raises an exception, the following occurs:  
  
1\. IP is set to value 1024 and machine switches to privileged mode. Thus, the next instruction will be fetched from the exception handler.  
  
2\. The machine sets several CPU registers with values that describe (to the exception handler) the cause of the exception. These are explained below:  
  
a) **EIP** (Exception IP): The logical IP value of the unprivileged mode instruction that caused the exception is stored in this register. For example, if the instruction MOV R0, \[5000\], fetched from IP=3000 caused an exception because the logical page corresponding to address 5000 (logical page 8) was invalid, the EIP will be loaded with value 3000.  
  
b) **EPN** (Exception Page Number): _The contents of this register are valid only in the case of a page fault exception._ The logical page number that caused the page fault is stored in this register. In the above example, if MOV R0, \[5000\] caused a page fault because logical page 8 was invalid, then EPN will have value 8. Note that if the instruction fetch caused a page fault (say IP=3000), then EPN would have contained value 5.  
  
c) **EC** (Exception Cause): The EC register will indicate the cause of the exception – values are set as below.  
  
(i) Page Fault: The value stored in the EC register for this exception is 0.  
  
(ii) Illegal instruction: The value stored in the EC register for this exception is 1.  
  
(iii) Illegal memory access: The value stored in the EC register for this exception is 2.  
  
(iv) Arithmetic exception: The value stored in the EC register for this exception is 3.  
  
d) **EMA** (Exception memory address): _The value of this register is relevant only in the case of illegal memory access._ The illegal memory which was tried to be accessed is stored in the register. Either the address referred to is outside the range 0 - 512\*(PTLR-1) or a write is attempted to a page which is [read-only](../arch_spec-files/paging_hardware.html).  
  
**The [XSM interrupt/exception handling documentation](../arch_spec-files/interrupts_exception_handling.html) gives a more detailed technical description of the actions performed by the machine when interrupts or exceptions occur. You may have a quick look at the documentation now, but refer to relevant sections of the documentation only as and when required.**