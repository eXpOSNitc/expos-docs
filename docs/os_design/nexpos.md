---
title: 'eXpOS Design for NEXSM (Two Core) Machine'
original_url: 'http://eXpOSNitc.github.io/os_design-files/nexpos.html'
---






eXpOS Design for NEXSM (Two Core) Machine































 
















[eXpOSNITC](index.html)


* [Home](../index.html)
* [Documentation](../documentation.html)
* [Roadmap](../Roadmap.html)
* [FAQ](../faq.html)
* [About Us](../About_us.html)











  

  

  







eXpOS Design for NEXSM (Two Core) Machine
-----------------------------------------


  

  


[NEXSM](../arch_spec-files/nexsm.html) is an extension of the XSM architecture with a dual-core feature. The machine has two identical cores with the same set of internal registers sharing a common memory. All registers in XSM are present in both the cores. Additionally, NEXSM cores contain an extra register called the **core flag**. A few additional privileged instructions provide primitives for synchronization between the two cores. One of the processors is called the **primary core** and the other called the **secondary core**. The machine can operate in two modes – **active mode** and **reset mode**. **In the reset mode, the secondary is non-functional.** The mode in which the machine operates can be controlled by the primary using a pair of special privileged instructions – START and RESET.
 


  

#### **Modifications to User Interface**



 The user interface is eXpOS undergoes no change.
 


  

#### **Modifications to Application Interface**



 The application interface specification of the eXpOS undergoes minor modification when moving to NEXSM. The version of eXpOS running on NEXSM supports an additional software interrupt INT 19. There are four system calls that gets mapped to INT 19 routine. These are:
 





|  |  |
| --- | --- |
| **System Call Name** | **System Call Number** |
| Test4 | 100 |
| Test5 | 101 |
| Test6 | 102 |
| Test7 | 103 |






 The **high level library interface** to these new system calls is specified [here](../os_spec-files/dynamicmemoryroutines.html).
 



 The **low level system call interface** to these new system calls is specified [here](Sw_interface.html).
 



 Currently, these system calls are unused. They could be used for testing future enhancements to the system.
 


  

#### **Modifications to OS Design**



 The design of eXpOS undergoes changes when ported to the two-core machine.
 


  

#### **Disk Organization**



 NEXSM disk has 16 additional disk blocks (block numbers 512 to 527). The OS uses these blocks for loading the following handlers:
 





|  |  |
| --- | --- |
| **Block Number** | **Contents** |
| 512-513 | Secondary Bootstrap Loader |
| 514-515 | INT 19 handler |
| 516-517 | Module 8 |
| 518-519 | Module 9 |
| 520-521 | Module 10 |
| 522-523 | Module 11 |
| 524-527 | Unused |






 Disk organization is given [here](../os_implementation.html).
 


  

#### **Memory Organization**



 NEXSM has 16 additional pages of memory (pages 128 to 144). The first four new pages are reserved by the machine. These are:
 

|  |  |
| --- | --- |
| **Page Number** | **Contents** |
| 128-129 | Secondary bootstrap loader (bootstrap loader for secondary core) |
| 130-131 | Software interrupt, INT 19 (currently INT19 is unused) |






 Four new system calls, Test4, Test5, Test6 and Test7 are added to eXpOS and all these calls are directed to INT19 (see details [here](../os_spec-files/dynamicmemoryroutines.html)). Currently the functionality of these system calls are unspecified. These are left so for testing future enhancements and conducting experiments on the system.
 



 From among the remaining 12 available pages, eXpOS reserves the next eight pages for storing OS code as follows:
 

|  |  |
| --- | --- |
| **Page Number** | **Contents** |
| 132-133 | Module 8 ([Access Control Module](../os_modules/Module_8.html)) |
| 134-135 | Module 9 (TestA Module) |
| 136-137 | Module 10 (TestB Module) |
| 138-139 | Module 11 (TestC Module) |
| 140-143 | Reserved for future use |






 The present design does not use Module 9, Module 10 and Module 11. Module 8 is called **Access Control Module**. This module contains code for synchronization between the two cores. Module 9, Module 10 and Module 11 are called TestA Module, TestB Module and TestC Module, respectively. These modules are left free to provide space for testing enhancements and conducting experiments on the system. The remaining four pages (140-143) are also not used. 
 


  

#### **Design Policies**



 The fundamental issue to be resolved while extending the OS to a two core machine is to ensure *that concurrent updates of OS data structures from the two cores do not leave the OS in an inconsistent state*. Here we impose a few simple to implement design level restrictions on the level of parallelism permitted so that a simple and comprehensible design is possible. The constraints imposed are the following:
 



***Policy 1:** Atomicity constraints:*



1. 
 A single process will never be scheduled simultaneously on both the cores. The scheduler will be designed to ensure this policy.
2. 
 Only one core will run scheduler code that involves updates to kernel data structures at a given time. This makes implementation of the first policy straight-forward.
3. 
 Only one core will be executing critical kernel code at a time. Upon entry into a system call the kernel checks whether the other core is running critical kernel code. If that is the case, then the kernel waits for the other core to finish the critical code before proceeding.



 Atomicity is ensured using **access locks**. The kernel maintains a few access locks which will be set before executing critical code. **Before executing any critical code, the kernel checks whether the other core has acquired the access lock and waits for the release of the lock before proceeding.** When the access lock is available, the kernel sets the access lock when available and proceeds to the critical code. This procedure ensures that only one core executes critical code.
 



***Policy 2:** Hold and Wait constraints:* A process, after acquiring an access lock will quickly perform the required action (like updating a kernel data structure) and release the lock immediately, before being scheduled out. Moreover, a second access lock will be acquired only after releasing the first. These constraints ensure that there will be no hold and wait or circular wait for access locks.
 



 It is not very difficult to see that adherence to the above policies is sufficient to ensure the consistency of the OS.
 


  

#### **Implementation of Access Locking**



 Atomicity of access locking is implemented using the hardware mechanism provided by the [NEXSM machine](../arch_spec-files/nexsm.html) ([TSL instruction](../arch_spec-files/nexsm.html#instr)). The details follow.
 


  

#### **OS Data Structures**



 The OS uses essentially the same data structures in the single processor eXpOS system. However, to ensure atomicity of the resource acquire functions (of the resource manager module), as well as access/updates of OS data structures, an additional layer of access locking, is introduced as explained above. The OS maintains an **Access Lock Table** in memory with the following fields to hold the additional locks.
 


  

#### **Access Lock Table**





|  |  |
| --- | --- |
| **Field** | **Function** |
| KERN\_LOCK | Common access lock to be set before running any critical kernel code other than scheduling. Before performing any kernel function, this lock must be set by the kernel module/interrupt handler so that the other core waits till the critical action is completed. |
| SCHED\_LOCK | Access lock to run the Scheduler Module. If one core has set the SCHED\_LOCK in the Scheduler Module, the other core runs in a busy loop until execution of the Scheduler Module is completed. |
| GLOCK | A general purpose lock variable that is left unused for future use. |






 The design ensures that before running the scheduler, a process releases KERN\_LOCK. The scheduler must set SCHED\_LOCK before starting the scheduling process and reset the lock after scheduling actions are completed.
 



 The [Access Lock table](mem_ds.html#al_table) is allocated eight words of memory and is stored in memory locations 29576-29583, of which the last five words are unused. (see [memory organization](../os_implementation.html)). 
 


  

#### **Access Control Module**



 The [access control module](../os_modules/Module_8.html) contains functions that implement atomic set and reset operations on the kernel lock variables. The following are functions present in the access control module:
 


1. AcquireKernLock()
2. AcquireSchedLock()
3. AcquireGLock()
4. ReleaseLock(LockVarAddress)


 The AccessLock functions can be implemented using the TSL instruction to ensure that locking is **atomic**. The general locking logic in SPL would be the following:
 



```

Acquire****Lock() {
    ....
    .... 
    while (tsl (LockVariableAddress) == 1) 
       continue;
    endwhile; 
}
```


 The [SPL extension](../support_tools-files/spl.html#nexsm) of NEXSM provides [constants](../support_tools-files/constants.html#nexsm) for identifying the access control variables in the Access Lock Table. Constants for invoking the new modules – TestA, TestB, TestC and the Access Control Module, etc., are also provided.
 


  

#### **Other Design Modifications**



 In two core operation, it might be required that both the cores schedule the IDLE process simultaneously. However, this goes against our previously stated design principle of not allowing the same process to be scheduled simultaneously on both the cores. To handle this contingency, a new process called IDLE2 with (PID=14) is created. The scheduler will be modified to run IDLE2 on the secondary core whenever it finds that no other process can be scheduled. The standard IDLE (PID=0) will be scheduled under similar circumstances in the primary core. The primary will never execute IDLE2 and the secondary will never run IDLE (PID=0).
 



 IDLE2 is run on the secondary when:
   
 1. No other process is ready, **OR**
  
 2. The OS is running the [pager module](../os_modules/Module_6.html) or if [logout system call](multiusersyscalls.html#logout) is being executed in the primary.
 



 In the present design, the scheduler will run [LOGIN](misc.html#login), [SHELL](misc.html#shell) and the [Swapper Daemon](misc.html#swapper) processes only from the primary. The [pager module](../os_modules/Module_6.html) also will be run only from the primary. These constraints simplify implementation of the kernel, but are neither necessary nor very efficient. 
 


  

#### **Boot Procedure**



 NEXSM specification stipulates that the secondary code bootstraps from the physical address 65536 (page 128) upon execution of the START instruction from the primary. Hence, **the bootstrap routine of the primary core must transfer the bootstrap code of the secondary from disk block (see [disk organization](../os_implementation.html)) to memory page 128 before issuing the START instruction**. The START instruction is issued at the end of normal bootstrap by the primary (see [OS Startup code](misc.html#os_startup)).
 



 The secondary bootstrap code will schedule the IDLE2 process for execution (setting its state appropriately) and from there normal two core execution starts.
 


  

#### **Implementation**



 The major changes to be made to the single core eXpOS kernel are the following:
 

1. 
 Upon entry into a system call or exception handler, either from an application or from the scheduler, *AcquireKernLock()* must be invoked. The lock must be released before invoking the scheduler or switch back to user mode using *ReleaseLock(KERN\_LOCK)*.
2. 
 The scheduler module must be modified to set *AcquireSchedLock()* before initiating scheduling actions. Upon completion of scheduling actions, the scheduler must release the lock invoking *ReleaseLock(SCHED\_LOCK)* before setting any process into execution.
3. *Swapper daemon* will be invoked only from the primary core by the timer interrupt handler (as done in eXpOS). When the scheduler running on the second core finds that pager daemon was initiated from the primary (check PAGING\_STATUS in [system status table](mem_ds.html#ss_table)), it will simply schedule IDLE2.
4. 
 The *Logout system call* will be invoked only from primary core as the shell process will be scheduled to run only on the primary. When the scheduler running on the second core finds that logout/shutdown system call is initiated, from the primary (check LOGOUT\_STATUS in [system status table](mem_ds.html#ss_table)), it will simply schedule IDLE2.

  


 A detailed description of the changes required to the eXpOS kernel are outlined in the Stage 28 page of the [Roadmap](../Roadmap.html).
 












































