---
title: 'Resource Manager'
original_url: 'http://eXpOSNitc.github.io/os_design-files/resource_manager.html'
---





Resource Manager


































 

























  
  
  







Module 0: Resource Manager
--------------------------


  

  


Acquire(resource\_id,argument)
------------------------------


  
  

**Arguments:** resource\_id, argument 


 If the resource is either Disk or Terminal, argument = NIL. If the resource is Inode table, argument = Inode index.


**Return Value:**




|  |  |
| --- | --- |
| 0 | Success |
| -1 | Failure |


#### **Algorithm:**


If resource\_id is that of:


     Case 1: Disk - Blocks for the disk. 


                              return success.


     Case 2: Inode - Blocks for the Inode and sets Klock. 


                              return success.


     Case 3: Terminal - Blocks for the Terminal. 


                                      return success.



Release(Inode)
--------------


  
  

**Arguments:** Inode 


**Return Value:**




|  |  |
| --- | --- |
| 0 | Success |
| -1 | Failure |


#### **Algorithm:**


Release Klock on the inode and wake up all processes blocked for the Inode.    /* Terminal and Disk are released by interrupt handlers */ 














































