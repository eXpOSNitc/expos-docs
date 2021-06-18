---
title: 'Module 8: Access Control Module'
original_url: http://exposnitc.github.io/os_modules/Module_8.html
---

This module contains the functions that manages access locks.

|Function Number|Function Name|Arguments|Return Value|
|--- |--- |--- |--- |
|ACQUIRE_KERN_LOCK = 1|Acquire Kernel Lock|NIL|NIL|
|ACQUIRE_SCHED_LOCK = 2|Acquire Scheduler Lock|NIL|NIL|
|ACQUIRE_GLOCK = 3|Acquire Glock (Unused)|NIL|NIL|
|RELEASE_LOCK = 4|Release Lock|LockVarAddress|NIL|

### Acquire Kernel Lock
Acquires KERN_LOCK which is a common access variable to be set before running any critical kernel code (except the scheduler). Before executing any kernel module/interrupt handler, KERN_LOCK is set (by invoking this function) so that the other core waits till the critical action is completed. After completing the critical kernel code, the ReleaseLock function is used to release KERN_LOCK.

<pre><code>
if (core is SECONDARY_CORE){
    if (PAGING_STATUS or LOGOUT_STATUS is on){
        // <a href="../os_design-files/nexpos.html" target="_blank">eXpOS design</a>  does not permit a process 
        // to execute critical code on the secondary core when paging or logout is ongoing.

        Set the state of current process to READY

        Call the <b>switch_context()</b> function of the Scheduler Module.
        <b>/* Scheduler Module requires appropriate modifications 
            before running on the <a href="../arch_spec-files/nexsm.html" target="_blank">NEXSM machine</a> */</b>
    }
}

while ( tsl (KERN_LOCK) == 1 ){
    continue;
}

return;
</code></pre>


Called by all system calls, exception handler and timer interrupt handler.


### Acquire Scheduler Lock
Acquires SCHED_LOCK which is an access variable to be set before running the scheduler. This ensures that if one core has set SCHED_LOCK, the other core will not enter the Scheduler module until the first core completes the scheduling action. After completing the scheduling action, the ReleaseLock function is used to release SCHED_LOCK.
```
while ( tsl (SCHED_LOCK) == 1 ){
    continue;
}
    
return;
```
Called by the Scehduler module.

### Acquire Glock

Acquires GLOCK which is a general purpose lock variable that is currently left unused.
```
while ( tsl (GLOCK) == 1 ){
    continue;
}
    
return;
```

### Release Lock
Releases the access lock provided as the argument.
```
Store 0 to the address LockVarAddress.
return;
```

Called by all system calls, exception handler, timer interrupt handler and scheduler.