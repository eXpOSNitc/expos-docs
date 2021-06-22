---
title: eXpOS Implementation
original_url: https://exposnitc.github.io/os_implementation
todo: true
hide:
    - navigation
---

## Introduction
This document discusses the mapping of various eXpOS data structures to the XSM machine's disk and memory. The implementation of eXpOS on XSM discussed in the project modularises the code of system calls into smaller module functions. An interface description of the module functions is given here. The document also outlines the useage of kernel stack of user processes.


### Disk Organization

|Block Number|Contents|Number of Blocks|
|:---: |:---: |:---:|
|0 - 1|Bootstrap|2|
|2|Disk Free List|1|
|3 - 4|Inode + User Table *|2|
|5|Root File **|1|
|6|Reserved for future use|1|
|7 - 8|Init/Login Code|2|
|9 - 10|Shell Code|2|
|11 - 12|Idle Code|2|
|13 - 14|Library|2|
|15 - 16|Exception Handler|2|
|17 - 18|Timer Interrupt Routine|2|
|19 - 20|Disk Controller Interrupt Routine|2|
|21 - 22|Console Interrupt Routine|2|
|23 - 24|Interrupt 4 Routine: Create, Delete|2|
|25 - 26|Interrupt 5 Routine: Seek, Open, Close|2|
|27 - 28|Interrupt 6 Routine: Read|2|
|29 - 30|Interrupt 7 Routine: Write|2|
|31 - 32|Interrupt 8 Routine: Fork|2|
|33 - 34|Interrupt 9 Routine: Exec|2|
|35 - 36|Interrupt 10 Routine: Exit|2|
|37 - 38|Interrupt 11 Routine: Getpid, Getppid, Wait, Signal|2|
|39 - 40|Interrupt 12 Routine: Logout|2|
|41 - 42|Interrupt 13 Routine: Semget, Semrelease|2|
|43 - 44|Interrupt 14 Routine: SemLock, SemUnLock|2|
|45 - 46|Interrupt 15 Routine: Shutdown|2|
|47 - 48|Interrupt 16 Routine: Newusr, Remusr, Setpwd, Getuname, Getuid|2|
|49 - 50|Interrupt 17 Routine: Login|2|
|51 - 52|Interrupt 18 Routine: Test0, Test1, Test2, Test3|2|
|53 - 54|Module 0: Resource Manager|2|
|55 - 56|Module 1: Process Manager|2|
|57 - 58|Module 2: Memory Manager|2|
|59 - 60|Module 3: File Manager|2|
|61 - 62|Module 4: Device Manager|2|
|63 - 64|Module 5: Context Switch Module (Scheduler Module)|2|
|65 - 66|Module 6: Pager Module|2|
|67 - 68|Module 7: Boot Module|2|
|69 - 255|User Blocks|187|
|256 - 511|Swap Area|256|
|512 - 513|Secondary Bootstrap *|2|
|514 - 515|Interrupt 19 Routine: Test4, Test5, Test6, Test8 *|2|
|516 - 517|Module 8: Access Control Module *|2|
|518 - 519|Module 9: TestA (Unused) *|2|
|520 - 521|Module 10: TestB (Unused) *|2|
|522 - 523|Module 11: TestC (Unused) *|2|
|524 - 527|Unallocated *|4|


### Memory Organization
The Memory layout of the XSM machine is as follows :




### [:link: Kernel Module Interface](./modules/index.md)

### Kernel Stack Management
#### [:link: Kernel Stack Management during System Calls](/broken.md)
#### [:link: Kernel Stack Management during Hardware interrupts or exceptions](/broken.md)
#### [:link: Kernel Stack Management during Module calls](/broken.md)
#### [:link: Kernel Stack Management during Context Switch](/broken.md)

### [:link: eXpOS Procees management implementation](./tutorials/process_management_implementation.md)

### [:link: eXpOS File-System and implementation](./tutorials/filesystem_implementation.md)

### [:link: eXpOS Multi-User implementation](./tutorials/multiuser_implementation.md)