---
title: Release quotes
original_url: https://exposnitc.github.io/release_quotes
hide:
    - navigation
---

!!! quote "05 April 2021"
    Website:  
    Add student feedback for 2020 batch.  
    Add bootstrap script that automatically pulls the latest version of code from the git repo.  
    Fixed a few typos.  
    Added link to Google Groups.  
    Created a repo to host user contributed content and added the link to the home page's sidebar.  
    Code:  
    Expl: Fixed linker error introduced by a breaking change in GCC10. Expl: Fixed strings containing colon getting parsed as labels.  
    xfs-interface: Allow specifying path to disk.xfs using --disk flag.
    
??? quote "23rd April 2020"
    Setup instructions for Debian, Red Hat based distros and arch linux added
    
??? quote "21st April 2020"
    
    The definitions for **User** and **Login** have been added to the terminologies in the overview section of OS specifications.
    
??? quote "22nd October 2019"
    
    The merge\_sort.expl program to be used in assignment 5, stage 27 has been modified to work properly. Each process is made to _wait_ for all the processes wth PID greater than itself inorer to prevent each process from closing leading to a reuse of PIDs.
    
??? quote "31st August 2019"
    
    The high level library interface contained a typo. The 3rd argument for **read** instruction was changed from _Memory Address (Buffer)_ to _variable name(to which data is to be read)_
    
??? quote "24th August 2019"
    
    The roadmap contained typos in stage 7 and stage 14. In stage 7, logical pages for heap were changed from 3 and 4 to 2 and 3. In stage 14 a typo of OS startup code was changed to boot module.
    
??? quote "4th August 2019"
    
    The project was failing to **_make_** on some operating systems. This was due to a dependency issue on some systems and has been fixed in the new release.  
    The _mem_ command in the XSM debug mode had an issue when called for a range of pages. It would just keep overwriting the contents of the mem file after writing a page and the mem file would contain the contents of only the last page in the range specified in the command call. Changes were made to the following directories:-
    
    *   **xsm:** The mem command was fixed and tested.
    
??? quote "2nd August 2019"
    
    The roadmap contained a typo in the assignment question _b_ of Stage 6. The memory locations 29714 in the question and 5160 in the answer has been corrected to 29706 and 51640 respectively.  
    The _rm_ command of the xfs-interface encountered segmentation faults upon execution. Changes were made to the following directories:-
    
    *   **xfs-interface:** The rm command was fixed and tested.
    
??? quote "22th April 2019"
    
    NEXSM (a dual-core extension of XSM) is introduced. Stage 28 (Multi-Core Extension) describing how the OS can be ported to a two-core extension of the XSM machine has been added. The documentation for [NEXSM architecture specification](arch_spec-files/nexsm.html) and [eXpOS Design for NEXSM machine](os_design-files/nexpos.html) have been added. The changes in the sub-directories are:-
    
    *   **expl:** Library is modified to include INT 19.
    *   **nespl:** Three new instructions, _start_, _reset_ and _tsl_, have been added.
    *   **nexfs-interface:** Commands for loading Bootstrap code for secondary core, software interrupt 19 and module 8-11 are added.
    *   **nexsm:** XSM machine is modified to simulate a two-core machine.
    
??? quote "20th January 2019"
    
    Stage 27 (Pager Module) has been modified. A swapper daemon is introduced as a new process similar to the idle program, with PID=15, and the Pager Module is called from the context of this process. To add fairness for the swapped out processes, if the TICK field of any swapped out process exceeds a threshold, that process is swapped in after swapping out another process in memory. The changes in the sub-directories are:-
    
    *   **xsm:** A few additional commands, including commands for displaying all the data structures, is added to the XSM debugger.
    
??? quote "5th November 2018"
    
    The changes in the sub-directories are:-
    
    *   **expl:** Modified the library (_library.lib_) to include INT 18 (Test0, Test1, Test2, Test3).
    
??? quote "26th October 2018"
    
    The _Execption Handler_ has been modified to allocate 2 heap pages when a page fault for a heap page occurs. In Stage 27 (Pager Module), _Get Free Page function_ in _Memory Manager_ and _Exit Process_ function in _Process Manager_ has been modified to call _Swap Out_ and _Swap In_ function, respectively.
    
??? quote "23th October 2018"
    
    A new asignment problem has been added to Stage 27 (Pager Module).
    
??? quote "20th October 2018"

    A new step has been added to the algorithm for Login and Logout system calls regarding the current userID in the system status table. The algorithm for Fork system call has been modified to allocate heap pages for parent process (if not yet assigned already), so that parent and child processes will still have a shared heap after Fork.
    
??? quote "14th October 2018"
    
    The code for the Stage 22 assignment problem ([Merge Sort](test_prog.html#test_program_14)) has been modified to avoid the stack overflow problem. A new assignment problem has been added to Stage 25 (File Write). The changes in the sub-directories are:-
    
    *   **expl:** Fixed a bug which caused an exception when function with more than one argument was called after an exposcall with more than one argument.
    *   **xfs-interface:** Fixed a bug which stored the file size of data files 1 more than the actual value.
    *   **xsm:** Fixed a bug in which the EIP value stored was 2 less than the actual value.
    
??? quote "4th October 2018"
    
    The _Fork_ system call had a problem - if a process forks, the parent first gets a PCB entry and then calls _Get Free Page_ function to allocate pages for Stack/User Area pages for the child. If the _Get Free Page_ causes the parent process to change the state to WAIT\_MEM, the PCB entry allocated for the child may also be given for another process. The problem has been fixed by modifying the _Get Pcb Entry_ function in _Process Manager_. Two new assignments has been added to Stage 22 (Semaphores). The changes in the sub-directories are:-
    
    *   **spl:** The constant ALLOCATED has been added to the [SPL pre-defined constants](support_tools-files/constants.html).
    
??? quote "20th September 2018"
    
    The algorithm for _Release Page_ function in _Memory Manager_ module has been modified to change the state of process from WAIT\_MEM to READY when a free page is available. Makefile for myexpos directory is updated for _make clean_. The changes in the sub-directories are:-
    
    *   **expl:**  
        a) Fixed a bug which caused return value of function to be overwritten when timer is called. The earlier version lowered the SP value before extracting return value from the call stack. If any interrupt occured in the meanwhile, the value in the stack was overwritten.  
        b) Modified DIV instruction such that it doesn't call INT 10 when divisor is 0.
    *   **spl:** Earlier SPL version used the register R20 when large expressions were compiled. However, the machine had only registers up to R19. Hence, "Illegal register usage" was reported by the simulator. The SPL compiler is modifed to use only registers upto R19.
    *   **xsm:** Validity check is conducted for page/block number in load/store instructions.
    
??? quote "17th September 2018"
    
    The exception/interrupt handling documentation has been modified. The simulator will no longer push IP on top of stack when an exception occurs, thus the code for exception handler must be modified as per the new documentation. The changes in the sub-directories are:-
    
    *   **expl:** Added line numbers during compilation errors. Fixed read(p.x) bug. After compilation of <filename>.expl, the target code is stored as both assemblycode.xsm and <filename>.xsm.
    *   **xfs-interface:** Fixed long string bug which caused "Illegal instruction" when large strings were used.
    *   **xsm:** Machine won't push IP on top of the stack when an exception occurs, anymore. XSM debugger will now show privilege mode and IP along with next instruction. Added usertable and watchpoint in XSM debugger. Fixed the --timer 1 bug which caused the timer to be called infinitely when timer is initialised as 1.