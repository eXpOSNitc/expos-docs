---
title: 'Module 7: Boot Module'
original_url: https://eXpOSNitc.github.io/os_modules/Module_7.html
hide:
    - toc
---

This module is responsible for hand creating the INIT and SHELL processes. It loads the modules, interrupt routines and disk data structures which are required by eXpOS from disk to memory. It also initializes different memory data structures which are required to run the OS smoothly. Boot module is invoked only once by the OS Startup code at the time of booting.

#### Algorithm
