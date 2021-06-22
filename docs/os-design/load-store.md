---
title: 'Load/Store'
original_url: 'http://eXpOSNitc.github.io/os_design-files/load_store.html'
hide:
    - navigation
    - toc
---

### Steps to Load/Store

1) In the [Disk Status Table](mem-ds.md#ds_table), do the following steps


* Set the Status bit to 1.   /* Shows disk is busy */
* Set the Load/Store bit to 0 (load) / 1 (store).
* Set the Page Number field to the number of the page being stored / to which the disk block is loaded.
* Set the PID to the PID of the process invoking the disk-memory transfer. If the load/store instruction was invoked by scheduler, set the PID to **-(pid)** where **pid** is the identifier of the process for which load/store operation was initiated.


2) Issue the load/store machine instruction.














































