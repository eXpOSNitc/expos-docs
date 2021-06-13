---
title: FAQ
hide:
  - navigation
  - toc
---

!!! question "1. What is eXpOS? What is its purpose?"
    <p>eXpOS stands for eXperimental Operating System. The <a href="os_spec.html" target="_blank">eXpOS
    specification</a> describes a very simple multi-user multi-tasking operating system. </p>
    <p>eXpOS is not intended to be used as a practical operating system. It is designed with the
    following intentions:
    <ol>
    <li>To have a multi-tasking OS specification that can be comprehended by a junior undergraduate
    student in computer science who is undergoing a first course in Operating System such that
    he/she will be able to implement the OS in two or three months. This educational package comes
    with enough guidance and support tools as well as documentation to allow the student to achieve
    this goal without the supervision of a specialist teacher.</li>
    <li>The student will write the complete code for the OS from scratch. He/She will not be building
    the OS on top of a given code base. The only programming support provided will be a compiler
    for a programming language (called SPL) in which the OS kernel will be written. </li>
    </ol>
    </p>


!!! question "2. Who will benefit by implementing eXpOS?"
    If you are a non-expert in computer science – like an undergraduate student or some non-specialist
    systems enthusiast – and you have a basic understanding of programming, and computer organization,
    implementing eXpOS will help you to get a feel of some of the core ideas involved in implementing a
    multi-tasking operating system on a single processor. You will learn how to:
    
    - Initally load the operating system from secondary storage to memory – <b>Bootstrapping</b>.
    - Manage several processess in memory simultaneously – <b>Process Management</b>. 
    - Handle allocation and de-allocation of memory to processes – <b>Memory Management</b> (includes
    virtual memory management).
    - Manage organization of data and program files in secondary storage – <b>File Management</b>.
    - Implement a mechanism to allow multiple processes to share files/memory – <b>Resource Sharing</b>.
    - Realize primitives that help application programs to avoid inconsistency when resources are
    shared by several processes executing concurrently – <b>Process Sychronization</b>.
    - Handling multiple users with different privileges over resources shared among them – <b>Multi-user
    Capability.</b>
    
    The experiment is akin to guiding a third year aerospace engineering student to build a small
    unmanned flight in two months. (The flight will not be usable outside the laboratory!)


!!! question "3. What are the OS concepts that eXpOS will help me to comprehend better than – say just learning from a text book?"
    Please see FAQ 2.

!!! question "4. What are the prerequisites for doing the eXpOS project?"
    The project presumes that the student has undergone a basic sophomore course in computer
    organization and data structures and has either completed or is currently undergoing a theory
    course in operating systems. The project does not require the student
    to be familar with the principles of compilers. It is not expected that the student has a high
    level of proficiency in programming or computer hardware. The required background on paging
    hardware, interrupts, run­time stack of application programs etc. are provided as reading material
    at appropriate places in the project roadmap.


!!! question "5. Who must not be spending time on eXpOS?"
    <p>People who want to learn about operating systems, but who belong to the following category are not
    advised to proceed with eXpOS:</p>
    <ol>
    <li>You are a confident programmer comfortable with reading and understanding professionally
    written code – like the source code of linux. In this case, more sophisticated packages like <a
    href="http://minix3.org/">Minix</a> allow you to do real hard stuff. However, this is not for
    novices. </li>
    <li>You are not an expert; you want to try out the things listed in FAQ 2, but you do not want to
    do dirty work at a low level. (Although you can avoid assembly language programming in the eXpOS
    project, you still will have to get into quite a bit of “low level” architectural details). We
    suggest you to look for alternatives like <a href="https://en.wikipedia.org/wiki/Not_Another_Completely_Heuristic_Operating_System"
    target="_blank">NACHOS</a>. </li>
    </ol>


!!! question "6. Can eXpOS be actually be used in a real application?"
    Please see FAQ 2.


!!! question "7. What are the important OS concepts I miss out when working with eXpOS?"
    <p>What you learn is very little compared to what is needed to become an OS expert. So, listing out
    everything is impossible. But here are some important misses: </p>
    <ol>
    <li>The XSM machine allows you to store a character string in a memory word. No real machine
    architecture permits you to do such stuff. This is made possible just because XSM is a software
    simulated. However, XSM makes your data manipulation job much simpler without getting bogged down
    by details of data formatting. It is in principle possible to implement eXpOS on “more real”
    machines like <a href="http://en.wikipedia.org/wiki/MIPS_instruction_set" target="_blank">MIPS</a>.
    However, this would involve considerably more time and effort. </li>
    <li>The project involves very little work involving input-ouput, device interfacing, security or
    networking. Moreover the file system and multi-user support are very primitive. The methods
    studied won't scale up when there is <a href="https://en.wikipedia.org/wiki/Computer_multitasking#Preemptive_multitasking"
    target="_blank"> pre-emptive multitasking </a>. </li>
    </ol>


!!! question "8. What are the system requirements for working on the eXpOS package?"
    <p>We expect you to have a Linux/Unix Machine with Lex/Flex and Yacc/Bison software packages
    installed. (For Flex/Bison installation on your Linux system, see <a href="http://en.kioskea.net/faq/30635-how-to-install-flex-and-bison-under-ubuntu"
    target="_blank">link</a>). Once you have these, you can download the eXpOS package by following
    instructions at <a href="./support_tools-files/setting-up.html" target="_blank"> Setting Up</a>.</p>


!!! question "9. What are the contents of the eXpOS package?"
    <p>The eXpOS package available <a href="./support_tools-files/setting-up.html" target="_blank">here</a>
    comes with the following: </p>
    <ol>
    <li>A simulator for the <a href="arch_spec.html" target="_blank">Experimental String Machine (XSM)</a>
    on which you implement eXpOS. The machine consists of a CPU, Memory and a disk and a small
    Input-Ouput subsystem.</li>
    <li>A compiler (into the XSM machine) for the <a href="support_tools-files/spl.html" target="_blank">System
    Programmer's Language (SPL)</a> using which you will be writing all your code for implementing
    eXpOS. SPL is a simple programming language which essentially is an extended assembler for the
    XSM machine, specifically designed for the eXpOS package.</li>
    <li>A compiler (into the XSM machine) for the <a href="support_tools-files/expl.html" target="_blank">Experimental
    String Language (ExpL)</a>. This language is used for writing application programs that can run
    on top of eXpOS. You will be using this language for writing some of the user level programs of
    the OS including the shell. Test programs that are used to test your OS will also be written in
    ExpL.</li>
    <li>An interface tool called <a href="support_tools-files/xfs-interface.html" target="_blank">XFS-interface</a>
    that allows you to transfer data files and executable programs from your Unix/Linux system into
    the hard disk of the XSM machine.</li>
    <li>You also download the source code of all the above tools and their formal specification
    documents, the sample test programs testing your OS, some help etc. </li>
    </ol>


!!! question "10. I have downloaded the eXpOS package. How can I get started with the work?"
    <p>The best way is to follow the eXpOS roadmap. It is a journey taken one simple step at a time. You
    will be provided with links to learn the concepts on a “learn when needed” way. Just go ahead
    following this <a href="Roadmap.html" target="_blank">link</a>.</p>


!!! question "11. What differenciates eXpOS from other educational packages like NACHOS?"
    <p>It is difficult to answer this question for all similar packages available elsewhere, but here is
    a comparison with NACHOS. </p>
    <p>NACHOS learning system asks you to implement OS software that allows application programs in the
    noff executable format, running on a the software simulation of a MIPS machine, to invoke system
    calls. However, the OS code you write really doesn't run on the MIPS machine! Your code is actually
    C code running on your Linux/Unix machine. When an application program invokes an OS system call,
    the MIPS simulator transfers control to a corresponding “stub” function in the simulating
    environment. You must write C code in the stub to do “whatever is expected from the OS” to satisfy
    the calling application program invoking the system call. Since the MIPS machine is simulated, your
    code has access to its memory, registers etc. Thus you can implement the system call, put return
    values in appropriate memory locations on the simulated MIPS machine and transfer control back to
    the calling program. </p>
    <p>In eXpOS, the OS and the application programs run in the same machine as is the case in real
    systems. The compromise made in achieving this goal was to make the machine “unreal” and the OS
    simple enough so that additional complexity is manageable for a short term project. </p>


!!! question "12. What is the difference between eXpOS and XOS?"
    <p><a href="http://xosnitc.github.io/" target="_blank">XOS</a> is an earlier version of this project.
    XOS did not support blocking system calls.</p>
    <p> This means that a process will never do a context switch while it is running in the kernel mode.
    However eXpOS, system calls may block in the kernel mode and other processes could be scheduled.
    The version of XSM provided with eXpOS has the necessary hardware support for doing this.</p>
    <p> The addition of this single feature makes the eXpOS substantially more complex than XOS. This is
    because a blocked process might have made partial updates to some OS data structures before
    blocking and a newly scheduled process, while executing in the kernel mode, must be careful not to
    modify these data structures and leave the OS in an inconsistent state. </p>
    <p> Apart from the above feature, eXpOS adds support for semaphores, shared memory, file locking etc.
    There is also limited multi-user support. However, the additional complexity introduced by these
    features is minor. </p>


!!! question "13. How do I write OS code and load the OS in the eXpOS system?"
    You have to write your OS code from your Linux/Unix system in a custom programming language called
    SPL that comes with the eXpOS package, compile the code and install the target code into the hard
    disk of the XSM machine. The xfs-interface tool allows you to do this pre-loading. Your OS code
    must include set up code that will be executed when the system is started. This code must load the
    rest of the OS into memory during bootstrap.


!!! question "14. How do I write application programs that run on eXpOS?"
    Application programs must be compiled in the Linux/Unix environment outside and pre-loaded into
    the XSM machine's disk. The ExpL language allows applications to be written and compiled into the
    eXpOS executable format called the <a href="abi.html#xexe" target="_blank"> XEXE </a> format.


!!! question "15. What is meant by user mode and kernel mode?"
    In a multitasking OS like Linux, there are two types of programs running. Firstly, there are
    application programs that users write. These are called "user mode programs". Secondly, there are
    "kernel mode programs" which constitute the OS code. These routines implement the system call
    interface for application programs and other OS functions like process, memory, file and device
    management etc. 
    
    User mode programs can execute only a restricted instruction set and has access only to a limited
    memory (called the virtual address space). These programs must invoke OS system calls to do tasks
    which involve capacity beyond their limited instruction set. Kernel mode programs on the other hand
    have full access to the machine instruction set.

    Any machine supporting eXpOS needs to recognize and support two modes of program execution. The OS
    must be designed such that the machine switches to kernel mode when a user mode program invokes a
    system call and goes back to user mode when the system call returns. This requires architecture
    support. XSM machine is equipped with the necessary hardware support.


!!! question "16. Why do you need two programming languages in the eXpOS package – the SPL and ExpL?"
    We need separate programming systems for writing user mode programs and kernel mode programs
    because these languages serve different purposes. The high level language - ExpL provided with the
    package can be used for writing application programs that run on top of the operating system.
    However, ExpL does not support low level programming necessary to write the OS. The SPL language
    (which is essentially an enriched XSM assembly language) must be used to write the OS modules.



!!! question "17. What is eXpOS Library?"
    The ExpOS library is a piece of code that provides a generic interface for application programs to
    access OS services like system calls and dynamic memory management routines.

    ExpL permits applications to invoke OS routines only through the library interface. The compiler
    simply translates the library call to a low level library call. However, ExpL compiler will not
    attach the library to the application at compile time. The OS loader must attach the library to the
    application at run time.


!!! question "18. What is XFS interface?"
    XFS interface is a tool that permits you to transfer programs and data files between your host
    system and the XSM machine's simulated hard disk. The tool is capable of handling various eXpOS
    file types (like OS modules, application programs, data files, library etc.) and store them in the
    XSM disk, updating the disk data structures appropriately.

!!! question "19. My friend has implemented eXpOS after downloading the package and following the roadmap. I want to write a program and test his implementation. How to do it?"
    You must write your code in ExpL language in your Unix/Linux machine, compile it using the ExpL
    compiler that comes with the eXpOS package and load the target executable file into the XSM
    machine's disk using the xfs-interface tool. Now start the machine (assuming that your friend has
    already written his OS routines in SPL, compiled it using the SPL compiler and loaded it into the
    disk) so that her OS boots up and runs the shell program. From the shell, you will be able to type
    in the name of your executable program and execute it, just like in bash.


!!! question "20. I am a teacher and wants to use eXpOS for laboratory instruction. How should I proceed?"
    You are welcome use eXpOS. You may also fork the project on GitHub and customize the project to
    your own needs subject to the <a href="http://creativecommons.org/licenses/by-nc/4.0/">Creative
    Commons</a> license conditions.
    Pro Tip: Suppose your institution has the name ABC University, to host your project on GitHub as
    exposabc.github.io, create a GitHub account by the name eXpOSABC, fork this project, rename your
    repository to exposabc.github.io, and host your website using <a href="https://pages.github.com/">GitHub
    Pages</a>
