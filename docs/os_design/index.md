---
title: eXpOS Design
original_url: https://exposnitc.github.io/os_design.html
todo: true
---

## Introduction
This document specifies the high level system design on eXpOS along with the specification of Data Structures and Algorithms used in eXpOS.

Data Structures can be classified into - Memory Data Structures (In-core) and Disk Data Structures. The Disk Data Structures are loaded to memory by the OS startup code and stored back when system terminates.

Algorithms specified in this document can fall into any of the five categories - File System Calls, Process System Calls, System Calls related to access control and synchronization, Multiuser System Calls and Hardware Interrupts and Exception Handler.

## High Level Design