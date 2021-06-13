---
title: Roadmap
---

This roadmap is divided into stages. Each stage is to be done in sequential order. You will build eXpOS incrementally. Links are provided throughout the document for further reference. There are two kinds of links. The contents of the important links must be read immediately before proceeding with the roadmap. The informative links may be clicked for more information about a particular concept. However this information may not be necessary at that point and you may proceed with the roadmap without visiting these links.

It is very important that you proceed with the roadmap on a regular schedule and not get lost in the links. Hence, an approximate amount of time (in hours) which you are expected to spend on each stage is noted along with the stage. If you find that reading a particular documentation/link takes too much time, skip it for the time being and come back to it only when needed.

!!!note "Preparatory Stages:"
    The preparatory stages help you to get familiarized with the disk bootstrap loading process, disk access mechanism, file-system specification, debugger, paging hardware, interrupt handling mechanism, program loading, library linkage and function calling conventions, application binary interface (ABI), context switching between applications and so forth. You will need 2-3 weeks to complete these stages.

[:octicons-link-external-16: Stage 1 : Setting up the System](#){ .stage-link }
[:octicons-link-external-16: Stage 2 : Understanding the Filesystem (2 Hours)](#){ .stage-link }
[:octicons-link-external-16: Stage 3 : Bootstrap Loader (2 Hours)](#){ .stage-link }
[:octicons-link-external-16: Stage 4 : Learning the SPL Language (2 Hours)](#){ .stage-link }
[:octicons-link-external-16: Stage 5 : XSM Debugging (2 Hours)](#){ .stage-link }
[:octicons-link-external-16: Stage 6 : Running a user program (4 Hours)](#){ .stage-link }
[:octicons-link-external-16: Stage 7 : ABI and XEXE Format (2 Hours)](#){ .stage-link }
[:octicons-link-external-16: Stage 8 : Handling Timer Interrupt (2 Hours)](#){ .stage-link }
[:octicons-link-external-16: Stage 9 : Handling kernel stack (4 Hours)](#){ .stage-link }
[:octicons-link-external-16: Stage 10 : Console output (4 Hours)](#){ .stage-link }
[:octicons-link-external-16: Stage 11 : Introduction to ExpL (4 Hours)](#){ .stage-link }
[:octicons-link-external-16: Stage 12 : Introduction to Multiprogramming (4 Hours)](#){ .stage-link }

!!!note "Intermediate Stages"
    In these stages, you will come across more advanced hardware features like, disk interrupt handling and exception handling. You will be implementing some basic kernel subsystems that will be used throughout the project. You will modularize your kernel into functional subsystems for resource management, memory management, device management, etc. You will implement a primitive user interface (Shell) and the final version of the OS loader (Exec system call). The amount of implementation details given in the road map will gradually diminish and many details will be left to be worked out by you. You wil need 3-4 weeks to complete these stages.

[:octicons-link-external-16: Stage 13 : Boot Module (4 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 14 : Round robin scheduler (4 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 15 : Resource Manager Module (4 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 16 : Console Input (6 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 17 : Program Loader (6 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 18 : Disk Interrupt Handler (6 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 19 : Exception Handler (6 Hours)](#){.stage-link}


!!!note "Final Stages"
    Stage 20-Stage 27 are the final stages of the project where you will implement all the system calls stipulated in the ABI documentation. Typically 5-6 weeks will be needed to complete these stages. At the end of the twentieth stage, basic system calls for process creation and termination – Fork, Exec and Exit will be completed. The next two stages take up system calls implementing signals and semaphores. The next three stages address the implementation of the file system. The subsequent stages add multi-user support and virtual memory support. (An advanced stage (Stage 28) describing how the OS can be ported to a two-core extension of the XSM machine has been added subsequently.)

[:octicons-link-external-16: Stage 20 : Process Creation and Termination (12 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 21 : Process Synchronization (4 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 22 : Semaphores (4 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 23 : File Creation and Deletion (6 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 24 : File Read (12 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 25 : File Write (12 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 26 : User Management (12 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 27 : Pager Module (18 Hours)](#){.stage-link}
[:octicons-link-external-16: Stage 28 : Multi-Core Extension (12 Hours)](#){.stage-link}
