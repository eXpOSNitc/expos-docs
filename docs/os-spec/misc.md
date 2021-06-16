---
title: 'Miscellaneous'
original_url: 'http://eXpOSNitc.github.io/os_spec-files/misc.html'
---






Miscellaneous































 











Toggle navigation


















  

  

  







Miscellaneous
-------------


  









#### 
Timer interrupt handler





The hardware requirement specification for eXpOS assumes that the machine is equipped with a timer device that sends periodic hardware interrupts. The OS **scheduler** is invoked by the hardware timer interrupt handler. eXpOS specification suggest that a co-operative multitasking [round robin scheduling](http://en.wikipedia.org/wiki/Round-robin_scheduling) is employed. This means that a round robin scheduling is employed, but a process may go to **sleep** inside a system call when:


1. The resource which the process is trying to access (like a file or semaphore) is locked by another process (or even internally locked by another OS system call in concurrent execution).
2. There is a disk or I/O device access in a system call which is slow. If the wait for the device access is to be avoided, there must be hardware support from the device to send a hardware interrupt when device operation is finished. This allows the OS to put the process on sleep for now, continue scheduling the remaining processes in round robin fashion and then wake up the sleeping process when the device sends the interrupt. Such hardware support is desirable, but not necessary to implement eXpOS









#### 
Exception handler





If a process generates an illegal instruction, an invalid address (outside its virtual address space) or do a division by zero (or other faulty conditions which are machine dependent), the machine will generate an exception. The exception handler must terminate the process, wake up all processes waiting for it (or resources locked by it) and invoke the scheduler to continue round robin scheduling the remaining processes.


The exception handler is invoked when a page required by the process is not present in the memory. This condition is known as a [page fault](http://en.wikipedia.org/wiki/Page_fault). The module which handles **demand paging** (if the machine hardware supports demand paging) is invoked by the exception handler when there is a **page fault**. eXpOS specification does not require implementation of demand paging. However, most machines (including XSM) are equipped with hardware support for demand paging and using the feature can improve machine throughput considerably. A discussion of demand paging is given [here](http://en.wikipedia.org/wiki/Demand_paging).








#### 
Disk Controller





eXpOS treats the disk as a special **block device** and assumes that the hardware provides low level **block transfer routines** to transfer disk blocks to memory (pages) and back. The block transfer routines contain instructions to initiate block-memory transfer by the disk controller hardware. After initiating the disk-memory transfer, the block transfer routine normally returns to the calling program, which sleeps for the disk operation to complete. 


When the disk-memory transfer is complete, the disk controller raises a hardware interrupt. The interrupt service routine (handler) must be part of the OS code to be set up during the bootstrap. The disk interrupt handler is responsible for waking processes that went into sleep awaiting completion of the disk operation. 








#### 
Terminal and other Device Handlers





All other data handling devices (other than the disk) are treated as **stream devices**. This means that each device allows transfer of only one word from memory to the device or back at a time. Some devices may permit only write (like a printer) whereas some devices may permit only read. It is assumed that for each device there are associated **low level routines** that can be invoked by the OS to transfer data and control instructions. Some of these devices may raise a hardware interrupt when the transfer is complete. Thus, for each device that raises an interrupt, there must be a corresponding device interrupt handler. 


The details of how data is transferred between memory and specific devices are hardware dependent and are to be handled by the OS routines in an implementation specific way. Here we are concerned about the device interface to application programmers. 


For each device part of the hardware, the OS assigns a unique device identifier (**devid**) which is announced to the application programmer. (The device identifiers are specific to the particular installation). It is assumed that device identifiers are distinguishable from file handles. A user program can write a word into a device using the **write** system call. The **read** system call is used when the device allows a word to be read. [(System Call Interface)](systemcallinterface.html). **Read** and **Write** are the only system calls associated with devices. 


 
 The **standard input** and the **standard output** are two special stream devices with predefined identifiers STDIN = -1 and STDOUT = -2. Standard output permits only **Write** and standard input permits only **Read**. The Read operation typically puts the process executing the operation to sleep for console input from the user. When the user inputs data, the console device must send a hardware interrupt. The corresponding handler routine is called **terminal handler**. The terminal handler is responsible for waking up processes that are blocked for input console. 








#### 
eXpOS Library





The eXpOS library consists of a collection of high level (user level) routines. The library is part of the OS and is loaded into the memory at the time of boostrap. The OS loader (exec system call) links the library to the address space of a process if necessary. The executable header contains the information required for the loader to decide whether the library must be linked to the address space of a process when it is loaded for execution. The eXpOS library routines provide a unified interface for invoking system calls and dynamic memory management routines provided by the operating stystem. The interface hides the details of the interrupt service routines corresponding to the system calls from the application. See [high level library interface](dynamicmemoryroutines.html) for more details.








#### 
Idle Process





 Idle process is a user process created by the kernel during the bootstrap process. It executes an infinite loop. Its purpose is to ensure that there is atleast one user process for the scheduler to schedule. The OS will schedule the idle process when all the other user processes are in sleep state. Idle process is never swapped.








#### 
Init (Login) and Shell





  


The OS has an INIT program pre-loaded in the disk, which is loaded for execution at the time of bootstrap. The resulting process is the second process scheduled for execution (after the [IDLE process](../os_design-files/misc.html#idle)) and is called the INIT process. The INIT program is expected to run a login program that validates a user trying to log into the system using the *Login* system call. Hence, the INIT process is also called the **login process**. A **shell** is created upon successful login and the INIT (login) process waits for the exit of the shell to log in the next user. The shell program is typically designed to repeatedly wait for user commands (executable file names) and execute them. The algorithm design for a typical login process is given [here](../os_design-files/misc.html#login). The algorithm design for a typical eXpOS shell is given [here](../os_design-files/misc.html#shell).












[![](../img/spec_icon.jpg)](../os_spec.html)











































