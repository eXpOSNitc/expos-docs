---
title: 'Low Level System Call Interface'
original_url: 'http://eXpOSNitc.github.io/os_design-files/Sw_interface.html'
---






Low Level System Call Interface















































[eXpOSNITC](index.html)


* [Home](../index.html)
* [Documentation](../documentation.html)
* [Roadmap](../Roadmap.html)
* [FAQ](../faq.html)
* [About Us](../About_us.html)












  

  

  







Low Level System Call Interface
-------------------------------


  


* If the file
 is created with permission set to [EXCLUSIVE](../support_tools-files/constants.html), then
 write and delete system calls will fail when executed by any
 user other than the owner or the root (see [here](../os_spec-files/multiuser.html)).
 



** These System Calls are available only on eXpOS running on [NEXSM](../arch_spec-files/nexsm.html) (a two-core extension of XSM) machine. 
 


  
   















































