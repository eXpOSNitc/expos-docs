---
title: 'Process State Transitions'
original_url: 'http://eXpOSNitc.github.io/os_design-files/state_diag.html'
hide:
    - navigation
    - toc
---




Process State Transition Diagram in eXpOS
-----------------------------------------


  

  

The state transitions that a process in eXpOS can undergo are shown in the following diagram. The events that cause each transition are explained below the diagram.


![](../assets/img/state_trans.png)
  

The events that cause the transitions:


**A** :
    CREATED -> RUNNING: The Scheduler has scheduled the process for execution for the first time.


**B** :


RUNNING -> WAIT\_TERMINAL : The process is either waiting for access to the terminal or for data to be inputted through terminal.


RUNNING -> WAIT\_DISK : The process is either waiting for access to the disk or for the disk operation to finish.


**C** :


RUNNING -> WAIT\_SEMAPHORE : The semaphore which the process is trying to use, is found to be locked.


RUNNING -> WAIT\_FILE : The file which the process is trying to read/write, is found to be locked.


RUNNING -> WAIT\_BUFFER : The buffer which the process is trying to use, is found to be locked.


RUNNING -> WAIT\_MEM : The process requires a free memory page but there are none in the memory.


**D** :


RUNNING -> WAIT\_PROCESS : The process is waiting for another process to either exit or to signal it.


**E** :


RUNNING -> TERMINATED: The process has either completed execution or has invoked an Exit System Call.


**F** :


WAIT\_SEMAPHORE -> READY : The semaphore for which the process was waiting, is now unlocked.


WAIT\_FILE -> READY : The file for which the process was waiting, is now unlocked.


WAIT\_BUFFER -> READY : The buffer for which the process was waiting, is now unlocked.


WAIT\_MEM -> READY : There are free pages in memory.


**G** :


WAIT\_TERMINAL -> READY : The input data has been read from terminal and terminal is free to be used by any process.


WAIT\_DISK -> READY : The disk operation is complete.


**H** :


WAIT\_PROCESS -> READY : The process has either received a signal from the process it was waiting for or the latter has exited the system.


**I** :


RUNNING -> READY : Context switch caused by the timer interrupt routine.
**J** :


READY -> RUNNING : The Scheduler has scheduled the process for execution.


**K** :


ALLOCATED -> CREATED : When a PCB entry is allocated for a process that is being newly created by the Fork system call, its state is set to ALLOCATED. The state is changed to CREATED, once the Fork system call completes the creation of the process.


  

!!! note
    The process can go from any state other than running state to the swapped state. A process, once swapped out will not be be swapped back into memory unless it's state becomes READY. 


!!! note
    A process may be unexpectredly TERMINATED due to various reasons like exceptions, logout, shutdown etc.










  

  







































