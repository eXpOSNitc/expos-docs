---
title: eXpOS Design
original_url: https://exposnitc.github.io/os_design.html
hide: 
    - navigation
    - toc
---

## Introduction
This document specifies the high level system design on eXpOS along with the specification of Data Structures and Algorithms used in eXpOS.

Data Structures can be classified into - Memory Data Structures (In-core) and Disk Data Structures. The Disk Data Structures are loaded to memory by the OS startup code and stored back when system terminates.

Algorithms specified in this document can fall into any of the five categories - File System Calls, Process System Calls, System Calls related to access control and synchronization, Multiuser System Calls and Hardware Interrupts and Exception Handler.

## High Level Design

<div style="background: url(http://exposnitc.github.io/img/os-design/os_design_detailed.png); height: 819px; width: 1206px" ;="">
<a target="_blank" href="os_design-files/misc.html#swapper" style="position: absolute; height: 62px; width: 120px; margin-top: 10px; margin-left: 260px"></a>
<a target="_blank" href="os_spec-files/shell_spec.html" style="position: absolute; height: 62px; width: 100px; margin-top: 10px; margin-left: 410px"></a>
<a target="_blank" href="os_spec-files/shell_spec.html" style="position: absolute; height: 62px; width: 100px; margin-top: 10px; margin-left: 540px"></a>
<a target="_blank" href="os_design-files/misc.html#idle" style="position: absolute; height: 62px; width: 120px; margin-top: 90px; margin-left: 20px"></a>
<a target="_blank" href="os_design-files/misc.html#login" style="position: absolute; height: 62px; width: 200px; margin-top: 90px; margin-left: 180px"></a>
<a target="_blank" href="os_design-files/misc.html#shell" style="position: absolute; height: 62px; width: 220px; margin-top: 90px; margin-left: 420px"></a>
<a href="#syscallsdiag" style="position: absolute; height: 60px; width: 130px; margin-top: 230px; margin-left: 35px"></a>
<a href="#syscallsdiag" style="position: absolute; height: 60px; width: 120px; margin-top: 230px; margin-left: 165px"></a>
<a href="#syscallsdiag" style="position: absolute; height: 60px; width: 120px; margin-top: 230px; margin-left: 285px"></a>
<a href="#syscallsdiag" style="position: absolute; height: 60px; width: 120px; margin-top: 230px; margin-left: 405px"></a>
<a href="#syscallsdiag" style="position: absolute; height: 60px; width: 120px; margin-top: 230px; margin-left: 525px"></a>
<a target="_blank" href="os_design-files/exe_handler.html" style="position: absolute; height: 60px; width: 80px; margin-top: 230px; margin-left: 750px"></a>
<a target="_blank" href="os_design-files/timer.html" style="position: absolute; height: 60px; width: 80px; margin-top: 230px; margin-left: 830px"></a>
<a target="_blank" href="os_design-files/disk_interrupt.html" style="position: absolute; height: 60px; width: 80px; margin-top: 230px; margin-left: 910px"></a>
<a target="_blank" href="os_design-files/term_handler.html" style="position: absolute; height: 60px; width: 80px; margin-top: 230px; margin-left: 990px"></a>
<a target="_blank" href="os_modules/Module_3.html" style="position: absolute; height: 60px; width: 200px; margin-top: 378px; margin-left: 140px"></a>
<a target="_blank" href="os_modules/Module_1.html" style="position: absolute; height: 60px; width: 200px; margin-top: 378px; margin-left: 380px"></a>
<a target="_blank" href="os_modules/Module_2.html" style="position: absolute; height: 60px; width: 200px; margin-top: 378px; margin-left: 620px"></a>
<a target="_blank" href="os_modules/Module_6.html" style="position: absolute; height: 60px; width: 200px; margin-top: 378px; margin-left: 860px"></a>
<a target="_blank" href="os_modules/Module_4.html" style="position: absolute; height: 60px; width: 440px; margin-top: 470px; margin-left: 140px"></a>
<a target="_blank" href="os_modules/Module_5.html" style="position: absolute; height: 60px; width: 440px; margin-top: 470px; margin-left: 620px"></a>
<a target="_blank" href="os_modules/Module_0.html" style="position: absolute; height: 68px; width: 760px; margin-top: 580px; margin-left: 100px"></a>
<a target="_blank" href="os_modules/Module_0.html" style="position: absolute; height: 260px; width: 60px; margin-top: 380px; margin-left: 40px"></a>
<a target="_blank" href="os_modules/Module_7.html" style="position: absolute; height: 68px; width: 170px; margin-top: 580px; margin-left: 890px"></a>
<a target="_blank" href="arch_spec-files/machine_organisation.html#Boot ROM" style="position: absolute; height: 68px; width: 120px; margin-top: 730px; margin-left: 790px"></a>
<a target="_blank" href="os_design-files/misc.html#os_startup" style="position: absolute; height: 68px; width: 120px; margin-top: 730px; margin-left: 950px"></a>
</div>

## System Calls

<div style="background: url(https://exposnitc.github.io/img/os-design/SystemCalls.png); height: 442px; width: 1032px" ;="">
<a target="_blank" href="os_design-files/shutdown.html" style="position: absolute; height: 60px; width: 190px; margin-top: 52px; margin-left: 20px"></a>
<a target="_blank" href="os_design-files/create.html" style="position: absolute; height: 30px; width: 150px; margin-top: 110px; margin-left: 240px"></a>
<a target="_blank" href="os_design-files/delete.html" style="position: absolute; height: 33px; width: 150px; margin-top: 150px; margin-left: 240px"></a>
<a target="_blank" href="os_design-files/open.html" style="position: absolute; height: 30px; width: 150px; margin-top: 190px; margin-left: 240px"></a>
<a target="_blank" href="os_design-files/close.html" style="position: absolute; height: 30px; width: 150px; margin-top: 230px; margin-left: 240px"></a>
<a target="_blank" href="os_design-files/read.html" style="position: absolute; height: 30px; width: 150px; margin-top: 270px; margin-left: 240px"></a>
<a target="_blank" href="os_design-files/write.html" style="position: absolute; height: 30px; width: 150px; margin-top: 312px; margin-left: 240px"></a>
<a target="_blank" href="os_design-files/seek.html" style="position: absolute; height: 30px; width: 150px; margin-top: 350px; margin-left: 240px"></a>
<a target="_blank" href="os_design-files/fork.html" style="position: absolute; height: 30px; width: 150px; margin-top: 113px; margin-left: 440px"></a>
<a target="_blank" href="os_design-files/exec.html" style="position: absolute; height: 33px; width: 150px; margin-top: 150px; margin-left: 440px"></a>
<a target="_blank" href="os_design-files/exit.html" style="position: absolute; height: 30px; width: 150px; margin-top: 190px; margin-left: 440px"></a>
<a target="_blank" href="os_design-files/proc_misc.html#getpid" style="position: absolute; height: 30px; width: 150px; margin-top: 230px; margin-left: 440px"></a>
<a target="_blank" href="os_design-files/proc_misc.html#getppid" style="position: absolute; height: 30px; width: 150px; margin-top: 270px; margin-left: 440px"></a>
<a target="_blank" href="os_design-files/synchronization_algos.html#wait" style="position: absolute; height: 30px; width: 150px; margin-top: 113px; margin-left: 640px"></a>
<a target="_blank" href="os_design-files/synchronization_algos.html#signal" style="position: absolute; height: 33px; width: 150px; margin-top: 150px; margin-left: 640px"></a>
<a target="_blank" href="os_design-files/semaphore_algos.html#semget" style="position: absolute; height: 30px; width: 150px; margin-top: 190px; margin-left: 640px"></a>
<a target="_blank" href="os_design-files/semaphore_algos.html#semrelease" style="position: absolute; height: 30px; width: 150px; margin-top: 230px; margin-left: 640px"></a>
<a target="_blank" href="os_design-files/semaphore_algos.html#semlock" style="position: absolute; height: 30px; width: 150px; margin-top: 270px; margin-left: 640px"></a>
<a target="_blank" href="os_design-files/semaphore_algos.html#semunlock" style="position: absolute; height: 30px; width: 150px; margin-top: 315px; margin-left: 640px"></a>
<a target="_blank" href="os_design-files/multiusersyscalls.html#newusr" style="position: absolute; height: 30px; width: 150px; margin-top: 113px; margin-left: 840px"></a>
<a target="_blank" href="os_design-files/multiusersyscalls.html#remusr" style="position: absolute; height: 33px; width: 150px; margin-top: 150px; margin-left: 840px"></a>
<a target="_blank" href="os_design-files/multiusersyscalls.html#setpwd" style="position: absolute; height: 30px; width: 150px; margin-top: 190px; margin-left: 840px"></a>
<a target="_blank" href="os_design-files/multiusersyscalls.html#getuid" style="position: absolute; height: 30px; width: 150px; margin-top: 230px; margin-left: 840px"></a>
<a target="_blank" href="os_design-files/multiusersyscalls.html#getuname" style="position: absolute; height: 30px; width: 150px; margin-top: 270px; margin-left: 840px"></a>
<a target="_blank" href="os_design-files/multiusersyscalls.html#login" style="position: absolute; height: 30px; width: 150px; margin-top: 312px; margin-left: 840px"></a>
<a target="_blank" href="os_design-files/multiusersyscalls.html#logout" style="position: absolute; height: 30px; width: 150px; margin-top: 350px; margin-left: 840px"></a>
</div>

## Data Structures

<div style="background: url(http://exposnitc.github.io/img/os-design/DataStructures_new.png); height: 671px; width: 671px; margin-bottom:30px" ;="">
<a target="_blank" href="os_design-files/disk_ds.html#inode_table" style="position: absolute; height: 30px; width: 150px; margin-top: 83px; margin-left: 50px"></a>
<a target="_blank" href="os_design-files/disk_ds.html#disk_free_list" style="position: absolute; height: 30px; width: 150px; margin-top: 123px; margin-left: 50px"></a>
<a target="_blank" href="os_design-files/disk_ds.html#root_file" style="position: absolute; height: 32px; width: 150px; margin-top: 168px; margin-left: 50px"></a>
<a target="_blank" href="os_design-files/disk_ds.html#user_table" style="position: absolute; height: 32px; width: 150px; margin-top: 208px; margin-left: 50px"></a>
<a target="_blank" href="os_design-files/process_table.html" style="position: absolute; height: 32px; width: 290px; margin-top: 113px; margin-left: 310px"></a>
<a target="_blank" href="os_design-files/process_table.html#user_area" style="position: absolute; height: 32px; width: 290px; margin-top: 233px; margin-left: 310px"></a>
<a target="_blank" href="os_design-files/mem_ds.html#file_table" style="position: absolute; height: 32px; width: 290px; margin-top: 325px; margin-left: 310px"></a>
<a target="_blank" href="os_design-files/mem_ds.html#file_lock_status_table" style="position: absolute; height: 32px; width: 290px; margin-top: 365px; margin-left: 310px"></a>
<a target="_blank" href="os_design-files/mem_ds.html#sem_table" style="position: absolute; height: 32px; width: 290px; margin-top: 405px; margin-left: 310px"></a>
<a target="_blank" href="os_design-files/mem_ds.html#ds_table" style="position: absolute; height: 32px; width: 290px; margin-top: 445px; margin-left: 310px"></a>
<a target="_blank" href="os_design-files/mem_ds.html#ss_table" style="position: absolute; height: 30px; width: 290px; margin-top: 485px; margin-left: 310px"></a>
<a target="_blank" href="os_design-files/mem_ds.html#ts_table" style="position: absolute; height: 30px; width: 290px; margin-top: 525px; margin-left: 310px"></a>
<a target="_blank" href="os_design-files/mem_ds.html#mem_free_list" style="position: absolute; height: 30px; width: 290px; margin-top: 562px; margin-left: 310px"></a>
<a target="_blank" href="os_design-files/mem_ds.html#buffer_table" style="position: absolute; height: 30px; width: 290px; margin-top: 602px; margin-left: 310px"></a>
<a target="_blank" href="os_design-files/process_table.html#per_page_table" style="position: absolute; height: 32px; width: 135px; margin-top: 155px; margin-left: 310px"></a>
<a target="_blank" href="os_design-files/process_table.html#disk_map_table" style="position: absolute; height: 32px; width: 137px; margin-top: 155px; margin-left: 460px"></a>
<a target="_blank" href="os_design-files/process_table.html#per_process_table" style="position: absolute; height: 32px; width: 135px; margin-top: 195px; margin-left: 310px"></a>
<a target="_blank" href="os_design-files/process_table.html#kernel_stack" style="position: absolute; height: 32px; width: 137px; margin-top: 195px; margin-left: 460px"></a>
</div>


## [:link: Process State Transition Diagram in eXpOS](./state_diag.md)
## [:link: eXpOS Design for NEXSM (Two Core) Machine](./nexpos.md)
### [:link: Access Lock Table](./mem_ds.md)
### [:link: Access Control Module](../modules/module_08.md)