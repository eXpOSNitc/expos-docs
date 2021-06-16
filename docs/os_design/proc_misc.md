---
title: 'Process System Calls'
original_url: 'http://eXpOSNitc.github.io/os_design-files/proc_misc.html'
---







Process System Calls


































 


























  
  
  




Getpid system call
------------------


  

  

Arguments: None


Return Value: 




|  |  |
| --- | --- |
| PID | Success |


*Description*: Returns the process identifier of the invoking process. The system call does not fail. 


  

#### Algorithm:



```

Find the PID of the current process from the [Process Table](process_table.html).

Return the PID of current process.

```





  
  
  


  
  
  




Getppid system call
-------------------


  

  

Arguments: None


Return Value: 




|  |  |
| --- | --- |
| PPID | Success |


*Description*: Returns to the calling process the value of the process identifier of its parent. The system call does not fail. 
  

#### Algorithm:



```

Find the PPID of the current process from the [Process Table](process_table.html).

Return the PPID.

```








  
  
  








































