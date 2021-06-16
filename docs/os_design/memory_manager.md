---
title: 'Memory Manager'
original_url: 'http://eXpOSNitc.github.io/os_design-files/memory_manager.html'
---





Memory Manager


































 

























  
  
  







Module 2: Memory Manager
------------------------


  

  


Getpage()
---------


  
  

**Arguments:** NIL 


**Return Value:**




|  |  |
| --- | --- |
| Page number of a free memory page | Success |
| -1 | Failure |


#### **Algorithm:**


 Run the second chance algorithm (if necessary)


If found,return the page number of a free memory page.


else, return -1.
 
 
Releasepage(page#)
------------------


  
  

**Arguments:** Memory page number


**Return Value:**




|  |  |
| --- | --- |
| 0 | Success |
| -1 | Failure |


#### **Algorithm:**


Release the page.


Update memory free list and system status table.


Return success.















































