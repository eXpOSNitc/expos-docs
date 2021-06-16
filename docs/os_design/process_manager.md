---
title: 'Process Manager'
original_url: 'http://eXpOSNitc.github.io/os_design-files/process_manager.html'
---





Process Manager


































 

























  
  
  







Module 1: Process Manager
-------------------------


  

  


GetPcbEntry()
-------------


  
  

**Arguments:** NIL 


**Return Value:**




|  |  |
| --- | --- |
| Index of the free process table entry | Success |
| -1 | Failure |


#### **Algorithm:**


Search the process table for a free entry.


If found, return index of the free entry.


else, return -1.
 
 
FreePcbEntry(PID)
-----------------


  
  

**Arguments:** Process Identifier( PID ) 


**Return Value:**




|  |  |
| --- | --- |
| 0 | Success |
| -1 | Failure |


#### **Algorithm:**


Release files, semaphores and locks if any.


Release pages, swap blocks, and any other resources held by the process.


**Note:** Must not be invoked if the process is blocked. 















































