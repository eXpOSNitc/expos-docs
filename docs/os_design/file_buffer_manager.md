---
title: 'File buffer Manager'
original_url: 'http://eXpOSNitc.github.io/os_design-files/file_buffer_manager.html'
---





File buffer Manager


































 

























  
  
  







Module 3: File Buffer Manager
-----------------------------


  

  

The buffer manager hides the buffer from the system call routine and uses device manager routines Dread and Dwrite below.



Bufwrite(disk#,offset,data)
---------------------------


  
  

**Arguments:** Disk block number, offset, data 


#### **Algorithm:**


Wait for the buffer and lock it.


If the disk block number is not present in the buffer already, use Dread routine of device manager module to read contents from the disk block to the buffer cache; if necessary by replacing existing page.


Write data to the offset.



Bufread(disk#,offset,data)
--------------------------


  
  

**Arguments:** Disk block number, offset, data 


#### **Algorithm:**


 Wait for the buffer and lock it.
If the disk block number is not present in the buffer already, use Dread routine of device manager module to read contents from the disk block to the buffer cache; if necessary by replacing existing page.


Return data at the offset.

















































