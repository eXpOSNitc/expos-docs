---
title: 'Miscellaneous'
original_url: 'http://eXpOSNitc.github.io/os_design-files/misc.html'
---







Miscellaneous


































 



























  
  
  




OS Startup Code
---------------


  

  

*Description*: OS Startup Code is loaded from disk to memory by the ROM Code on machine startup. Its main function is to prepare the machine for executing the processes. It initializes data structures, loads root file, disk free list, etc into the memory. OS startup code invokes [Boot Module](../os_modules/Module_7.html) to help the booting.


  

#### Algorithm:



```


  Load IDLE process and boot module from disk to memory. See [disk/memory organization](../os_implementation.html).
  Set SP to (user area page number of idle) * 512 + 1 and invoke module 7. //running the boot module in the context of idle.

  // after returning from the boot module


  /* Initialize the IDLE process.*/

  [Initialize the Page table for IDLE process (PID = 0)](#collapse2)

 Initialize the Page table base register (PTBR) to [PAGE\_TABLE\_BASE](../support_tools-files/constants.html) and PTLR to 10.
 Set the [page table](../os_design-files/process_table.html#per_page_table) entries for library and heap to -1. Set auxiliary information for these pages to "0000". 
 // idle doesn't invoke any library function. 
 Set the first code page entry to 69 (See [memory organization](../os_implementation.html)). Set auxiliary information for valid code pages to "0100". 
 Set remaining code page entries to -1 and auxiliary information to "0000".
 Set the first stack page entry to 70 and auxiliary information for this page to "0110".
 Set second stack page entry to -1 and auxiliary information to "0000".
  [Initialize the process table for IDLE process.](#collapse4)

 Initialize the fields of [process table](../os_design-files/process_table.html) as - TICK, PID and USERID as 0, STATE as RUNNING,
 USER AREA PAGE NUMBER as 76 (allocated from free user space), KPTR to 0, UPTR to 4096 (starting of first user stack page),
 PTBR to PAGE\_TABLE\_BASE and PTLR as 10.
  Store the IP value (from the header of the IDLE) on top of first user stack page [70*512] = [69*512 +1].


  /* Initialize the Swapper Daemon (not relevant before Stage 27) */

  [Initialize the Page table for Swapper Daemon (PID = 15)](#collapse2a)
  
 /* Swapper Daemon is identical to Idle and shares the code for Idle */
 Initialize the Page table base register (PTBR) to [PAGE\_TABLE\_BASE](../support_tools-files/constants.html) + 20*15 and PTLR to 10.
 Set the [page table](../os_design-files/process_table.html#per_page_table) entries for library and heap to -1. Set auxiliary information for these pages to "0000". 
 // swapper doesn't invoke any library function. 
 Set the first code page entry to that of Idle (See [memory organization](../os_implementation.html)). Set auxiliary information for valid code pages to "0100". 
 Set remaining code page entries to -1 and auxiliary information to "0000".
 Set the first stack page entry to 81 and auxiliary information for this page to "0110".
 Set second stack page entry to -1 and auxiliary information to "0000".
  [Initialize the process table for Swapper Daemon.](#collapse4a)
  
 Initialize the fields of [process table](../os_design-files/process_table.html) as - TICK, USERID as 0, PID as 15, STATE as CREATED,
 USER AREA PAGE NUMBER as 82 (allocated from free user space), KPTR to 0, UPTR to 4096 (starting of first user stack page),
 PTBR to PAGE\_TABLE\_BASE + 20*15 and PTLR as 10.  
  Store the IP value (from the header of the IDLE whose code is shared by Swapper) on top of first user stack page [81*512] = [69*512 +1].


  /* Initialize the IDLE2 (not relevant before Stage 28) */

  [Initialize the Page table for IDLE2 (PID = 14)](#collapse2b)
  
 /* IDLE2 is identical to Idle and shares the code for Idle */
 Initialize the Page table base register (PTBR) to [PAGE\_TABLE\_BASE](../support_tools-files/constants.html) + 20*14 and PTLR to 10.
 Set the [page table](../os_design-files/process_table.html#per_page_table) entries for library and heap to -1. Set auxiliary information for these pages to "0000". 
 // swapper doesn't invoke any library function. 
 Set the first code page entry to that of Idle (See [memory organization](../os_implementation.html)). Set auxiliary information for valid code pages to "0100". 
 Set remaining code page entries to -1 and auxiliary information to "0000".
 Set the first stack page entry to 83 and auxiliary information for this page to "0110".
 Set second stack page entry to -1 and auxiliary information to "0000".
  [Initialize the process table for IDLE2.](#collapse4b)
  
 Initialize the fields of [process table](../os_design-files/process_table.html) as - TICK, USERID as 0, PID as 14, STATE as RUNNING,
 USER AREA PAGE NUMBER as 84 (allocated from free user space), KPTR to 0, UPTR to 4096 (starting of first user stack page),
 PTBR to PAGE\_TABLE\_BASE + 20*14 and PTLR as 10.  

  
  Set the Page table base register (PTBR) to [PAGE\_TABLE\_BASE](../support_tools-files/constants.html) and PTLR to 10.

  Schedule IDLE process for excecution. (Return to user mode.)


```

  

#### Questions


1. why is the disk transfer (loading all the routines and data structures) done synchronously?







  
  
  




Shell Process
-------------


  

  

*Description*: It is created by the init process to act like a console. It accepts a command from the console. If the commnad is halt, shell shutdown the system using Shutdown system call. If the given command is built in shell command, corresponding system call will be executed with after reading suitable arguments from the console. If the command is a executable file, shell 
 forks itself and Exec the file given as command. These steps are repeated to accept and execute other files from the console.


Typically in eXpOS, the shell process acts as the init process.


* In  [Multiuser](http://exposnitc.github.io/os_spec-files/multiuser.html) implemention of eXpOS, the login process acts as the init process, which then executes the shell process with PID = 2.


Complete ExpL code for Shell program is provided [here](../test_prog.html#test_program_7).


  

#### Algorithm:



```
   **while** TRUE **do**

      command = read from console command to be executed. 
      **if** command == halt
         invoke shutdown system call.
      **endif**

      **if** command is built in shell command //eg- Logout, Remusr, Newusr etc 
         Read the required arguments from the console according to the built in shell command
         Invoke the corresponding system call with arguments.
      **else**
         childPID = fork(); 

         **if** (childPID == 0) /*Only child process will do the exec */
            Execute given command using *Exec* system call.
         **else**
            Wait for child to finish execution.   /* Using Wait system Call*/
         **endif**
      **endif** 
   
    **endwhile**
             
```






  
  
  




Idle Process
------------


  

  

*Description*: It is a user program which is created and executed by the bootstrap loader. It is stored in the disk and will be loaded to memory by the bootstrap loader. The main purpose of the idle process is to run as a background process in an infinite loop. This is demanded by the OS so that the scheduler will always have a process to schedule. The page table and process table for the idle process will be set up by the bootstrap loader. The PID of the idle process is fixed to be 0.


  

#### Algorithm:



```
   **while** TRUE **do**  //infinite loop

   **endwhile**
```






  
  
  




INIT/Login Process
------------------


  

  

*Description*: The login process is the first process scheduled for execution. It is used to login a user.The login process waits invoking the (terminal) read system call for a username and password to be input from the console. The login process executes the [Login system call](http://exposnitc.github.io/os_spec-files/systemcallinterface.html#multiusersystemcalls) with the username and the password as the arguments. The login system call verifies the user and creates a new [shell process](http://exposnitc.github.io/os_design-files/misc.html#shell).The original login process waits inside the login system call for the shell to exit. Upon exit of the shell, the login process proceeds to log in the next user. The login process is the init process in [Multiuser](http://exposnitc.github.io/os_spec-files/multiuser.html) extension to eXpOS.


  

#### Algorithm:



```
   **while** TRUE **do**

      username = read from console
      password = read from console
      Retval = Login (username, password)             
      **if** Retval = -1
         Write to console "Invalid credentials"             
      **else if** Retval = -2
         Write to console "Permission denied"             
      **endif**

   **endwhile**
```






  
  
  




Swapper Daemon
--------------


  

  

*Description*: It is a user program which is created by the bootstrap loader. This process uses the same code of the Idle process and hence has no file in the disk associated with it. The main purpose of the swapper daemon is to serve as a user program such that the OS performs swap-in and swap-out operations in the kernel context of this process. The PID of the swapper daemon is fixed to be 15.


  

#### Algorithm:


Identical to the Idle Process and runs with the code of the Idle Process.







  
  
  




OS Startup Code for Secondary Core*
-----------------------------------


  

  

* This is only relevant for Stage 28. 
 *Description*: OS Startup Code for the secondary core is loaded from disk to memory by the [Boot Module](../os_modules/Module_7.html). Its main function is to prepare the secondary core of the machine for executing the processes.


  

#### Algorithm:



```

Store the IP value (from the header of the IDLE whose code is shared by Swapper) on top of first user stack page [83*512] = [69*512 + 1]

Set SP to 8*512

Set the Page table base register (PTBR) to [PAGE\_TABLE\_BASE](../support_tools-files/constants.html) + 14*20 and PTLR to 10.

Schedule IDLE2 process for excecution. (Return to user mode)

```






  
  
  




IDLE Process for Secondary Core*
--------------------------------


  

  

* This is only relevant for Stage 28. 
 *Description*: It is a user program which is created by the bootstrap loader. This process uses the same code of the Idle process and hence has no file in the disk associated with it. The main purpose of the idle process is to run as a background process in an infinite loop in the secondary core. This is demanded by the OS so that the scheduler will always have a process to schedule in the secondary core, even if it schedules the IDLE in the primary core. The page table and process table for the init process will be set up by the bootstrap loader. The PID of the idle process is fixed to be 14.


  

#### Algorithm:


Identical to the Idle Process and runs with the code of the Idle Process.






  

  







































