---
title: 'Module 0: Resource Manager'
original_url: https://eXpOSNitc.github.io/os_modules/Module_0.html
---

This module is responsible for allocating and releasing the different resources. Note that the Terminal and Disk devices are freed by the corresponding interrupt handlers.

|Function Number|Function Name|Arguments|Return Value|
|--- |--- |--- |--- |
|ACQUIRE_BUFFER = 1|Acquire Buffer|Buffer Number, PID|NIL|
|RELEASE_BUFFER = 2|Release Buffer|Buffer Number, PID|0 or -1|
|ACQUIRE_DISK = 3|Acquire Disk*|PID|NIL|
|ACQUIRE_INODE = 4|Acquire Inode|Inodeindex, PID|0 or -1|
|RELEASE_INODE = 5|Release Inode|Inodeindex, PID|0 or -1|
|ACQUIRE_SEMAPHORE = 6|Acquire Semaphore|PID|Semaphore Table Index or -1|
|RELEASE_SEMAPHORE = 7|Release Semaphore|Semaphore Table Index, PID|0 or -1|
|ACQUIRE_TERMINAL = 8|Acquire Terminal|PID|NIL|
|RELEASE_TERMINAL = 9|Release Terminal|PID|0 or -1|

*Release function for the disk is implimented in the disk interrupt handler.

![](http://eXpOSNitc.github.io/img/os-modules/ResourceManager.png)

### Acquire Buffer

_**Description**_: Acquire the buffer corresponding to buffer number given as input. Assumes a valid PID and a valid buffer number are given.  

<pre><code>
while ( Buffer is locked ){   /* Check the Locking PID field in the [Buffer Status Table](/os_design-files/mem_ds.html#buffer_table) \*/
    Set state of the process as ( WAIT\_BUFFER , Buffer Number );
    Call the **switch\_context()** function from the [Scheduler Module](Module_5.html).
}
</code></pre>

Lock the Buffer by setting the PID of the current process in the Locking PID field
in the [Buffer Status Table](/os_design-files/mem_ds.html#buffer_table) ;

return;

Called by BufRead and BufWrite functions in the [File Manager](Module_3.html).

### Release Buffer

_**Description**_ : Release the buffer corresponding to buffer number given as input. Assumes a valid PID and a valid buffer number are given.  
  

If PID given as input is not equal to the LOCKING PID in the [Buffer Status Table](/os_design-files/mem_ds.html#buffer_table), return -1.

Free the lock in the the [Buffer Status Table](/os_design-files/mem_ds.html#buffer_table) entry corresponding to
the buffer Number; /\* Set Locking PID field to -1 \*/

loop through the process table{ 
       if (the process state is ( WAIT\_BUFFER , Buffer Number ) ){
             Set state of process as (READY , \_ )
         } 
}
return 0;

Called by BufRead and BufWrite functions in the [File Manager](Module_3.html).

### Acquire Disk

_**Description**_ : Locks the disk device. Assumes that a valid PID is given as input.  
  

while ( disk is locked ){        /\* Check the _Status_ field in the [Disk Status Table](../os_design-files/mem_ds.html#ds_table). \*/
    Set state of the process as ( WAIT\_DISK , - );
    Call the **switch\_context()** function from the [Scheduler Module](Module_5.html).
}

Lock the disk by setting PID and the status field in the [Disk Status Table.](../os_design-files/mem_ds.html#ds_table)

return;

Called by BufRead and BufWrite functions in the [File Manager](Module_3.html) and the exception handler for swap-in.

### Acquire Inode

_**Description**_ : Locks the Inode entry corresponding to the inodeindex given as input. Assumes a valid PID and a valid inode index are given.  
  

while ( inode is locked ){   /\* Check the Lock field in the [File Status Table](../os_design-files/mem_ds.html#file_lock_status_table). \*/
    Set state of the process as ( WAIT\_FILE , Inode Index );
    Call the **switch\_context()** function from the [Scheduler Module](Module_5.html).
} 

If inode becomes invalid, return -1. /\* File was deleted by the time the inode was acquired \*/

Lock the Inode by setting the Lock field in the [File Status Table](../os_design-files/mem_ds.html#file_lock_status_table) 
to the PID of the current process.;

return 0;

Called by Delete, Read, Write and Seek system calls.

### Release Inode

_**Description**_ : Frees the lock of the inode entry corresponding to the inodeindex given as input. Assumes a valid PID and a valid inode index are given.  
  

If PID given as input is not equal to the LOCKING PID in the [File Status Table](../os_design-files/mem_ds.html#file_lock_status_table), return -1.

Free the lock in the File Status Table corresponding to the inode index;       /\* Set the Lock field to -1 \*/

loop through the process table{ 
       if (the process state is ( WAIT\_FILE, Inode Index ) ){
             Set state of process as (READY , \_ )
         } 
}
return 0;

Called by Read, Write and Seek system calls.

### Acquire Semaphore

_**Description**_ : Acquires a semaphore and returns it's semaphore number. Assumes a valid PID is given as input. Returns -1 upon failure.  
  

 

Find the index of a free entry in [Semaphore table](../os_design-files/mem_ds.html#sem_table). If no free entry, return -1.
/\* Free entry is indicated by a Process Count of 0. \*/ 

Set the PROCESS\_COUNT to 1 and LOCKING\_PID to -1.

Return the Semaphore table index.   /\* success \*/

Called by the [Semget system call](../os_design-files/semaphore_algos.html#semget).

### Release Semaphore

_**Description**_ : Releases a semaphore. Assumes a valid PID and semaphore table index are given as input.  
  

 
If ( semaphore is locked by the current process)   /\*Check the Locking PID in the [Semaphore table](../os_design-files/mem_ds.html#sem_table)\*/
	Set the Locking PID to -1.  /\* Unlock the semaphore before release \*/
	loop through the process table{ /\*wake up processes blocked by the semaphore \*/
       		if (the process state is ( WAIT\_SEMAPHORE, SEMTABLEINDEX ) ){
             	Set state of process as (READY , \_ )
         	} 
	}

Decrement the process count of the semaphore in the semaphore table.
/\* When the count becomes 0, the semaphore is free. \*/
	     

Called by the [Semrelease](../os_design-files/semaphore_algos.html#semrelease) and exit system call.

### Acquire Terminal

_**Description**_ : Locks the Terminal device. Assumes a valid PID is given as input.  
  

while ( Terminal device is locked ){    /\* Check the Status field in the [Terminal Status Table](../os_design-files/mem_ds.html#ts_table) \*/
    Set state of the process as ( WAIT\_TERMINAL , - );
    Call the **switch\_context()** function from the [Scheduler Module](Module_5.html).
}
    
Lock the Terminal device by setting the Status and PID fields in the [Terminal Status Table](../os_design-files/mem_ds.html#ts_table).

return;

Called by the Terminal Read and Terimnal Write functions of the [Device Manager Module](Module_4.html).

### Release Terminal

_**Description**_ : Frees the Terminal device. Assumes a valid PID is given as input.  

If PID given as input is not equal to the LOCKING PID in the [Teminal Status Table](../os_design-files/mem_ds.html#ts_table), return -1.

Release the lock on the Terminal by updating the Terminal Status Table.;

loop through the process table{ 
if (the process state is ( WAIT\_TERMINAL , - ) ){
        Set state of process as (READY , \_ )
    } 
}

Return 0


Called by the Terimnal Write function in the [Device Manager Module](Module_4.html).