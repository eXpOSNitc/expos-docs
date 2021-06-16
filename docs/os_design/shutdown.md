---
title: 'Shutdown'
original_url: 'http://eXpOSNitc.github.io/os_design-files/shutdown.html'
---







Shutdown


































 



























  
  
  




Shutdown system call
--------------------


  

  

Arguments: None


Return Value: -1 on error or NIL


*Description*: The shut down system call is used to halt the system. It can be invoked only from shell of the root user. It terminates all the running processes, commits back the disk data (inode table, disk free list, root file, user table and dirty disk buffers) and halts the system.


  


![](../img/roadmap/shutdown.png)
  

Control flow diagram for *Shutdown* system call

  
  

#### Algorithm:



```
  
Set the MODE\_FLAG in the [process table](process_table.html) entry to 21, 
indicating that the process is in the shutdown system call.
	
//Switch to the Kernel Stack. see [kernel stack management during system calls](stack_smcall.html)
Save the value of SP to the USER SP field in the [Process Table](process_table.html) entry of the process.
Set the value of SP to the beginning of User Area Page.

If the current process is not the shell, return -1.	/* Shell process has the PID 2 */
If the current user is not the root, return -1.

Kill all user processes except the idle, login and the current process(shell) by calling the 
**kill\_all()** function in the [Process Manager](../os_modules/Module_1.html) module.

Loop through the [Buffer Table](../os_design-files/mem_ds.html#buffer_table)
	If the buffer is dirty
		Commit changes to the disk by calling the **disk\_store()** function in the [Device Manager](../os_modules/Module_4.html) module.

Commit the inode table, root file, user table and disk free list to the disk by calling the 
**disk\_store()** function in the [Device Manager](../os_modules/Module_4.html) Module.

Halt the system. 
               
```











































