---
title: eXpOS Specification
original_url: http://exposnitc.github.io/os_spec.html
---


### Who should read this document?
This document must be read by anyone wishing to write eXpOS application programs in a high level language or assembly language. This OS specification is prepared in a manner independent of programming language and target machine.

The document is also informative for system programmers like compiler designers who wishes to write the application programmer's interface for a high level language like ExpL to be run on eXpOS. The application binary interface ABI is the must-read document for the compiler designer.

Finally, this document must be read by anyone who wants to implement eXpOS on some machine because one needs to know the specification for the OS before getting started with its implementation!

### Introduction

This document gives application programmer's documentation for the eXperimental Operating System (eXpOS).

**eXpOS** is a tiny multiprogramming operating system. It has a very simple specification that allows a junior undergraduate computer science student to implement it in a few months, subject to availability of adequate hardware and programming platform support.

This specification is prepared from the perspective of the user/application programmer and is not hardware specific. Assumptions about the underlying hardware features necessary for the operating system to work are discussed in the first section of this document.

This document contains the following sections:




### [:link: Overview](./overview.md)

### [:link: eXpOS Abstractions](./expos-abstractions.md)

### [:link: The Logical File System : eXpFS](./expfs.md)

### [:link: Process Model](./processmodel.md)

### [:link: Synchronization and Access control](./synchronization.md)

### [:link: Miscellaneous](./misc.md)

### [:link: Multi-user Extension to eXpOS](./multiuser.md)

### Application Programmer's Interface (API)

#### [:link: High Level System Call Interface](./systemcallinterface.md)
#### [:link: High Level Library Interface](./dynamicmemoryroutines.md)


### [:link: eXpOS Shell specification](./shell-spec.md)