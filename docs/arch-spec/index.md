---
title: XSM Architecture Specification
original_url: https://exposnitc.github.io/arch_spec.html
hide: 
    - toc
---

### Introduction

The Experimental String Machine (XSM) is a hypothetical interrupt driven uniprocessor machine. The basic unit of data which the machine handles is the **string**. A string is a sequence of characters terminated by the special character '\\0'. The length of a string is at most XSM\_WSIZE characters including the '\\0' character. (The value of XSM\_WSIZE is implementation dependent and is left unspecified in this documentation). The machine treats integers, characters or sequence of characters as strings.

The basic data storage components of the machine are **registers**, **memory** and the **disk**. The memory and the disk are organised as sequences of words. The word is the fundamental memory/disk storage element and each memory/disk word can store a string. In the following, we often (mis)use notation and use the term “word” to refer to the “string stored in the memory/disk word”.

!!! note "Important Note"
    _Througout the architecture documentation, we have used the terms kernel mode for previleged mode and user mode for unprevileged mode of machine execution. However, "kernel" and "user" are OS level abstractions and not connected with the hardware. Hence the above usage is incorrect technically. However since the kernel of an OS normally runs in the previliged mode and user programs execute in the unpreviliged mode, the (incorrect) terminology has been used._

This document contains the following sections:

#### [:link: Machine Organization](machine-organization.md)
#### [:link: Interrupts and Exception Handling](interrupts-exception-handling.md)
#### [:link: Instruction Set](instruction-set.md)
#### [:link: Paging Hardware and Address Translation](paging-hardware.md)
#### [:link: NEXSM (Two Core) Architecture Specification](nexsm.md)