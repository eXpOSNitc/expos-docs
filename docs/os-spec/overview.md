---
title: 'Spec Overview'
original_url: 'http://eXpOSNitc.github.io/os_spec-files/overview.html'
hide:
    - navigation
---


### Terminology

It is assumed that the reader has some working familiarity with the following terms and concepts. (The description of the machine used in this experiment is given [here](../arch-spec/index.md). However reading the description is NOT a prerequisite for this document.)

-   **Machine:** The hardware/machine (computer) on which the operating system is running.
-   **(Physical) Memory:** The physical memory (primary memory) of the machine.
-   **Word:** The fundamental unit of memory access/storage recognized by the eXpOS. A word is assumed to be able to store an integer or a character string.
-   **Page:** The memory is assumed to be divided into pages of contiguous memory words. It is assumed that the machine supports [paging](https://en.wikipedia.org/wiki/Paging) hardware.
-   **Disk:** The secondary storage where data and program files are stored. The operating system is also stored in the disk and is loaded from the disk to the memory at the time of bootstrap.
-   **Block:** The basic unit of disk access. A block can store a sequence of words. The number of words per block is hardware dependent.
-   **File:** Each file is a sequence of words, stored in the disk. The most important file types are **program** files (or **executable** files or application programs) and data files.
-   **Process:** An application program under execution is called a [process.](https://en.wikipedia.org/wiki/Process_%28computing%29)
-   **Kernel:** The core part of the eXpOS operating system that forms a layer between the hardware and application programs. The kernel essentially is a collection of routines residing in the memory of the machine. In this document, the term operating system normally refers to the [kernel.](https://en.wikipedia.org/wiki/Kernel_%28operating_system%29)
-   **System Calls:** These are kernel routines which application programs can invoke to do actions which only the OS reserves right to perform (Example: creating/modifying files or creating/destroying processes).
-   **Multiprogramming:** Multiple processes reside in the memory simultaneously and the OS time-shares the machine between the processes by scheduling[](https://en.wikipedia.org/wiki/Scheduling_%28computing%29). The processes are said to execute concurrently. An OS that supports concurrent execution of processes is called a multiprogramming OS.
-   **Timer:** The hardware device that interrupts the machine periodically. The scheduler is generally invoked by the [timer interrupt service routine](https://en.wikipedia.org/wiki/Interrupt_handler).
-   **User:** Any person logged in and currently using the system to run processes.
-   **Login:** The process which gives a user access to the system through username and password authentication.


### Primitive Concepts

The OS specification assumes a generic hardware model described below. The arrows show interaction between various components of the system.

![](../assets/img/hw_model.png)

The basic Machine model consists of memory, disk and the CPU. A small part of memory is assumed to contain a **bootstrap loader** stored permanently in ROM memory. These are machine instructions to load into the memory an **OS startup code** stored in a pre-defined area in the disk. The ROM code then transfers control to this newly loaded code. This code loads the operating system routines stored in (pre-defined areas of) the disk into memory and sets up the Operating system. This includes all the OS code for various system calls, the scheduler, the exception handler, device drivers etc. Further hardware support required like the timer, disk controller, Input-output system etc. are discussed later.

For eXpOS to work, the machine should support two **privilege levels** of program execution. These are called **the user mode** (unprivileged mode) and the **system mode** (privileged mode). User programs (or application programs) run in user mode whereas OS routines run in system mode. The collection of OS routines that run in system mode is called the **kernel** of the operating system. A user program in execution is called a **process**. (Sometimes the term "program" may be (ab)used to refer to the corresponding process). An application process has access only to a limited set of machine instructions and can only access a limited set of memory addresses called the **virtual address space** of the process. This restricted machine model provided by the OS (of course, using the support from the machine architecture) is called the **virtual machine model**.

The eXpOS logically divides the virtual address space of a process into **library, code, stack and heap** regions. eXpOS assumes that the machine provides **paging** hardware to implement the mapping of the virtual address space of a process into the physical memory of the machine. The following [link](../arch-spec/paging-hardware.md) discusses how such mapping is done. The discussion here assumes no segmentation support. (However, If the machine supports [segmented paging](https://en.wikipedia.org/wiki/Memory_segmentation#Segmentation_with_paging), the mapping can be done more easily and profitably.)

Data and program files are stored in the disk. The disk is typically divided into **blocks** and the machine provides instructions to transfer blocks into and out of the memory. These instructions can be accessed only in the system mode. The specific mechanisms available are hardware dependent. (The disk access model for [XSM](../arch-spec/index.md) architecture is discussed [here](../arch-spec/machine-organization.md#disk) ). Note that since processes run in user mode, they can access disk files only by invoking the designated system calls for the purpose.

User programs are generally stored as **executable files** in the disk. Typically the user writes the application programs in a high level language and a compiler generates the executable file. The eXpOS expects that executable files follow certain format and compilers must adhere to the format. This allows the eXpOS to figure out how much space must be allocated for library, stack, code and heap in the virtual address space when the program is loaded into memory for execution. The virtual machine model as well as the executable file format for eXpOS implementation in XSM are described in the eXpOS [application binary interface](../abi.md) documentation.

At the end of the bootstrap process, the OS startup code hand-creates the first user process called the **INIT process** in memory. Thereafter, new processes can be created by existing processes by invoking the OS system calls for the purpose. Recall that the system call routines would have been set up in the memory during the bootstrap process. The INIT process creates a special user process called the **shell process** by loading and executing a **shell program** from the disk. The shell program repetitively reads user commands from the input and executes programs specified by the user and the OS becomes functional. The specification of the INIT and the shell process are described in this [link](processmodel.md#special-processes-in-expos).

\* In the extended eXpOS specification, the INIT process is called the LOGIN process and is executed directly by the kernel. This process invokes the login system call to log a user in. Once a user is logged in, the shell process is created for the user and the original login process waits for the termination of the user shell, to log in the next user.

eXpOS treats the standard input and output devices just like special files. Hence user processes must use the system calls to read/write files to perform I/O operations. The underlying implementation details are hardware dependent and are left unspecified in the OS specification.

Finally, eXpOS assumes that the machine is equipped with a **hardware timer** device that can interrupt the machine at pre-defined regular intervals. The timer is crucial for multiprogramming. The timer interrupt handler is the eXpOS kernel's **scheduler** routine which is responsible for **timesharing** the machine between processes. Similarly, disk/input-output devices may require a handler for interrupt service routines. These are hardware dependent and hence left unspecified in the OS specification. More details can be found in [Section 6](misc.md).