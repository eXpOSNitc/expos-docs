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
<a target="_blank" href="../os-design/misc/#swapper" style="position: absolute; height: 62px; width: 120px; margin-top: 10px; margin-left: 260px"></a>
<a target="_blank" href="../os-spec/shell-spec/" style="position: absolute; height: 62px; width: 100px; margin-top: 10px; margin-left: 410px"></a>
<a target="_blank" href="../os-spec/shell-spec/" style="position: absolute; height: 62px; width: 100px; margin-top: 10px; margin-left: 540px"></a>
<a target="_blank" href="../os-design/misc/#idle" style="position: absolute; height: 62px; width: 120px; margin-top: 90px; margin-left: 20px"></a>
<a target="_blank" href="../os-design/misc/#login" style="position: absolute; height: 62px; width: 200px; margin-top: 90px; margin-left: 180px"></a>
<a target="_blank" href="../os-design/misc/#shell" style="position: absolute; height: 62px; width: 220px; margin-top: 90px; margin-left: 420px"></a>
<a target="_blank" href="../os-design/exe-handler/" style="position: absolute; height: 60px; width: 80px; margin-top: 230px; margin-left: 750px"></a>
<a target="_blank" href="../os-design/timer/" style="position: absolute; height: 60px; width: 80px; margin-top: 230px; margin-left: 830px"></a>
<a target="_blank" href="../os-design/disk-interrupt/" style="position: absolute; height: 60px; width: 80px; margin-top: 230px; margin-left: 910px"></a>
<a target="_blank" href="../os-design/term-handler/" style="position: absolute; height: 60px; width: 80px; margin-top: 230px; margin-left: 990px"></a>
<a target="_blank" href="../modules/module-03/" style="position: absolute; height: 60px; width: 200px; margin-top: 378px; margin-left: 140px"></a>
<a target="_blank" href="../modules/module-01/" style="position: absolute; height: 60px; width: 200px; margin-top: 378px; margin-left: 380px"></a>
<a target="_blank" href="../modules/module-02/" style="position: absolute; height: 60px; width: 200px; margin-top: 378px; margin-left: 620px"></a>
<a target="_blank" href="../modules/module-06/" style="position: absolute; height: 60px; width: 200px; margin-top: 378px; margin-left: 860px"></a>
<a target="_blank" href="../modules/module-04/" style="position: absolute; height: 60px; width: 440px; margin-top: 470px; margin-left: 140px"></a>
<a target="_blank" href="../modules/module-05/" style="position: absolute; height: 60px; width: 440px; margin-top: 470px; margin-left: 620px"></a>
<a target="_blank" href="../modules/module-00/" style="position: absolute; height: 68px; width: 760px; margin-top: 580px; margin-left: 100px"></a>
<a target="_blank" href="../modules/module-00/" style="position: absolute; height: 260px; width: 60px; margin-top: 380px; margin-left: 40px"></a>
<a target="_blank" href="../modules/module-07/" style="position: absolute; height: 68px; width: 170px; margin-top: 580px; margin-left: 890px"></a>
<a target="_blank" href="../arch-spec/machine-organization/#BootROM" style="position: absolute; height: 68px; width: 120px; margin-top: 730px; margin-left: 790px"></a>
<a target="_blank" href="../os-design/misc/#os_startup" style="position: absolute; height: 68px; width: 120px; margin-top: 730px; margin-left: 950px"></a>
</div>

## System Calls

<div style="background: url(https://exposnitc.github.io/img/os-design/SystemCalls.png); height: 442px; width: 1032px" ;="">
<a target="_blank" href="../os-design/shutdown/" style="position: absolute; height: 60px; width: 190px; margin-top: 52px; margin-left: 20px"></a>
<a target="_blank" href="../os-design/create/" style="position: absolute; height: 30px; width: 150px; margin-top: 110px; margin-left: 240px"></a>
<a target="_blank" href="../os-design/delete/" style="position: absolute; height: 33px; width: 150px; margin-top: 150px; margin-left: 240px"></a>
<a target="_blank" href="../os-design/open/" style="position: absolute; height: 30px; width: 150px; margin-top: 190px; margin-left: 240px"></a>
<a target="_blank" href="../os-design/close/" style="position: absolute; height: 30px; width: 150px; margin-top: 230px; margin-left: 240px"></a>
<a target="_blank" href="../os-design/read/" style="position: absolute; height: 30px; width: 150px; margin-top: 270px; margin-left: 240px"></a>
<a target="_blank" href="../os-design/write/" style="position: absolute; height: 30px; width: 150px; margin-top: 312px; margin-left: 240px"></a>
<a target="_blank" href="../os-design/seek/" style="position: absolute; height: 30px; width: 150px; margin-top: 350px; margin-left: 240px"></a>
<a target="_blank" href="../os-design/fork/" style="position: absolute; height: 30px; width: 150px; margin-top: 113px; margin-left: 440px"></a>
<a target="_blank" href="../os-design/exec/" style="position: absolute; height: 33px; width: 150px; margin-top: 150px; margin-left: 440px"></a>
<a target="_blank" href="../os-design/exit/" style="position: absolute; height: 30px; width: 150px; margin-top: 190px; margin-left: 440px"></a>
<a target="_blank" href="../os-design/proc-misc/#getpid" style="position: absolute; height: 30px; width: 150px; margin-top: 230px; margin-left: 440px"></a>
<a target="_blank" href="../os-design/proc-misc/#getppid" style="position: absolute; height: 30px; width: 150px; margin-top: 270px; margin-left: 440px"></a>
<a target="_blank" href="../os-design/synchronization-algos/#wait" style="position: absolute; height: 30px; width: 150px; margin-top: 113px; margin-left: 640px"></a>
<a target="_blank" href="../os-design/synchronization-algos/#signal" style="position: absolute; height: 33px; width: 150px; margin-top: 150px; margin-left: 640px"></a>
<a target="_blank" href="../os-design/semaphore-algos/#semget" style="position: absolute; height: 30px; width: 150px; margin-top: 190px; margin-left: 640px"></a>
<a target="_blank" href="../os-design/semaphore-algos/#semrelease" style="position: absolute; height: 30px; width: 150px; margin-top: 230px; margin-left: 640px"></a>
<a target="_blank" href="../os-design/semaphore-algos/#semlock" style="position: absolute; height: 30px; width: 150px; margin-top: 270px; margin-left: 640px"></a>
<a target="_blank" href="../os-design/semaphore-algos/#semunlock" style="position: absolute; height: 30px; width: 150px; margin-top: 315px; margin-left: 640px"></a>
<a target="_blank" href="../os-design/multiusersyscalls/#newusr" style="position: absolute; height: 30px; width: 150px; margin-top: 113px; margin-left: 840px"></a>
<a target="_blank" href="../os-design/multiusersyscalls/#remusr" style="position: absolute; height: 33px; width: 150px; margin-top: 150px; margin-left: 840px"></a>
<a target="_blank" href="../os-design/multiusersyscalls/#setpwd" style="position: absolute; height: 30px; width: 150px; margin-top: 190px; margin-left: 840px"></a>
<a target="_blank" href="../os-design/multiusersyscalls/#getuid" style="position: absolute; height: 30px; width: 150px; margin-top: 230px; margin-left: 840px"></a>
<a target="_blank" href="../os-design/multiusersyscalls/#getuname" style="position: absolute; height: 30px; width: 150px; margin-top: 270px; margin-left: 840px"></a>
<a target="_blank" href="../os-design/multiusersyscalls/#login" style="position: absolute; height: 30px; width: 150px; margin-top: 312px; margin-left: 840px"></a>
<a target="_blank" href="../os-design/multiusersyscalls/#logout" style="position: absolute; height: 30px; width: 150px; margin-top: 350px; margin-left: 840px"></a>
</div>

## Data Structures

<div style="background: url(http://exposnitc.github.io/img/os-design/DataStructures_new.png); height: 671px; width: 671px; margin-bottom:30px" ;="">
<a target="_blank" href="../os-design/disk-ds/#inode-table" style="position: absolute; height: 30px; width: 150px; margin-top: 83px; margin-left: 50px"></a>
<a target="_blank" href="../os-design/disk-ds/#disk-free-list" style="position: absolute; height: 30px; width: 150px; margin-top: 123px; margin-left: 50px"></a>
<a target="_blank" href="../os-design/disk-ds/#root-file" style="position: absolute; height: 32px; width: 150px; margin-top: 168px; margin-left: 50px"></a>
<a target="_blank" href="../os-design/disk-ds/#user-table" style="position: absolute; height: 32px; width: 150px; margin-top: 208px; margin-left: 50px"></a>
<a target="_blank" href="../os-design/process-table/" style="position: absolute; height: 32px; width: 290px; margin-top: 113px; margin-left: 310px"></a>
<a target="_blank" href="../os-design/process-table/#user_area" style="position: absolute; height: 32px; width: 290px; margin-top: 233px; margin-left: 310px"></a>
<a target="_blank" href="../os-design/mem-ds/#open-file-table" style="position: absolute; height: 32px; width: 290px; margin-top: 325px; margin-left: 310px"></a>
<a target="_blank" href="../os-design/mem-ds/#file-inode-status-table" style="position: absolute; height: 32px; width: 290px; margin-top: 365px; margin-left: 310px"></a>
<a target="_blank" href="../os-design/mem-ds/#semaphore-table" style="position: absolute; height: 32px; width: 290px; margin-top: 405px; margin-left: 310px"></a>
<a target="_blank" href="../os-design/mem-ds/#disk-status-table" style="position: absolute; height: 32px; width: 290px; margin-top: 445px; margin-left: 310px"></a>
<a target="_blank" href="../os-design/mem-ds/#system-status-table" style="position: absolute; height: 30px; width: 290px; margin-top: 485px; margin-left: 310px"></a>
<a target="_blank" href="../os-design/mem-ds/#terminal-status-table" style="position: absolute; height: 30px; width: 290px; margin-top: 525px; margin-left: 310px"></a>
<a target="_blank" href="../os-design/mem-ds/#memory-free-list" style="position: absolute; height: 30px; width: 290px; margin-top: 562px; margin-left: 310px"></a>
<a target="_blank" href="../os-design/mem-ds/#buffer-table" style="position: absolute; height: 30px; width: 290px; margin-top: 602px; margin-left: 310px"></a>
<a target="_blank" href="../os-design/process-table/#per-process-page-table" style="position: absolute; height: 32px; width: 135px; margin-top: 155px; margin-left: 310px"></a>
<a target="_blank" href="../os-design/process-table/#per-process-disk-map-table" style="position: absolute; height: 32px; width: 137px; margin-top: 155px; margin-left: 460px"></a>
<a target="_blank" href="../os-design/process-table/#per-process-resource-table" style="position: absolute; height: 32px; width: 135px; margin-top: 195px; margin-left: 310px"></a>
<a target="_blank" href="../os-design/process-table/#kernel_stack" style="position: absolute; height: 32px; width: 137px; margin-top: 195px; margin-left: 460px"></a>
</div>


## [:link: Process State Transition Diagram in eXpOS](./state-diag.md)
## [:link: eXpOS Design for NEXSM (Two Core) Machine](./nexpos.md)
### [:link: Access Lock Table](./mem-ds.md)
### [:link: Access Control Module](../modules/module-08.md)