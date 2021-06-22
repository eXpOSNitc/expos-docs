---
title: "Kernel Module Interface"
original_url: https://exposnitc.github.io/os_modules/Module_Design.html

---

These routines are invoked from within system calls/interrupts/exception handler. A user program is not allowed to call a kernel module directly.

While executing a blocking system call, a process may block inside a module. In that case, the module will invoke the scheduler to execute other processes. The OS, in fact, is designed in such a way that blocking can happen only inside modules. Each module may contain calls to other modules (made through the CALL instruction). A module returns to its caller using the RET instruction. Modules may also be called from interrupt/exception handlers. Note that a process remains in the kernel mode through out the execution (as well as entry and exit) of a module.

A module may implement several functions. Each function within a module is identified by a function number which must be passed as an argument to the module through register R1. Other arguments must be passed through registers R2, R3 etc. in that order. The return value from a module must be passed through register R0. (See SPL documentation on module calling conventions [here](../support-tools/spl.md). )

The kernel modules and the functions present in each module are described below.

### [module-0 : Resource Manager](module-00.md)

| Function Number | Function Name     | Arguments          |
| --------------- | ----------------- | ------------------ |
| 1               | Acquire Buffer    | Buffer Number, PID |
| 2               | Release Buffer    | Buffer Number, PID |
| 3               | Acquire Disk*     | PID                |
| 4               | Acquire Inode     | Inodeindex, PID    |
| 5               | Release Inode     | Inodeindex, PID    |
| 6               | Acquire Semaphore | PID                |
| 7               | Release Semaphore | PID                |
| 8               | Acquire Terminal  | PID                |
| 9               | Release Terminal  | PID                |

*Release function for the disk is implimented in the disk interrupt handler.


### [module-1 : Process Manager](module-01.md)

| Function Number | Function Name       | Arguments |
| --------------- | ------------------- | --------- |
| 1               | Get Pcb Entry       | NIL       |
| 2               | Free User Area Page | PID       |
| 3               | Exit Process        | PID       |
| 4               | Free Page Table     | PID       |
| 5               | Kill All            | PID       |

### [module-2 : Memory Manager](module-02.md)
| Function Number | Function Name  | Arguments         |
| --------------- | -------------- | ----------------- |
| 1               | Get Free Page  | NIL               |
| 2               | Release Page   | Page Number       |
| 3               | Get Free Block | NIL               |
| 4               | Release Block  | Block Number      |
| 5               | Get Code Page  | Block Number, PID |
| 6               | Get Swap Block | NIL               |


### [module-3 : File Manager](module-03.md)
| Function Number | Function Name  | Arguments                                 |
| --------------- | -------------- | ----------------------------------------- |
| 1               | Buffered Write | Disk Block Number, Offset, Word           |
| 2               | Buffered Read  | Disk Block Number, Offset, Memory Address |
| 3               | Open           | File Name                                 |
| 4               | Close          | File Table Index                          |


### [module-4 : Device Manager](module-04.md)
| Function Number | Function Name  | Arguments                      |
| --------------- | -------------- | ------------------------------ |
| 1               | Disk Store     | PID, Page Number, Block Number |
| 2               | Disk Load      | PID, Page Number, Block Number |
| 3               | Terminal Write | PID, Word                      |
| 4               | Terminal Read  | PID, Address                   |


### [module-5 : Context Switch Module (Scheduler Module)](module-05.md)
| Function Number | Function Name  | Arguments |
| --------------- | -------------- | --------- |
| -               | Switch Context | Nil       |

### [module-6 : Pager Module](module-06.md)
| Function Number | Function Name | Arguments |
| --------------- | ------------- | --------- |
| 1               | Swap Out      | Nil       |
| 2               | Swap In       | Nil       |

### [module-7 : Boot Module](module-07.md)
| Function Number | Function Name | Arguments |
| --------------- | ------------- | --------- |
| -               | -             | Nil       |
