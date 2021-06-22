---
title: "About"
original_url: https://exposnitc.github.io/About_us.html
---

### eXpOS Philosophy

Any pedagogical operating system project offered as part of an undergraduate junior level operating system course needs to satisfy two requirements:

1. The student must be given as much depth and detail as possible about the central operating system concepts.
2. The quantity of work involved must not exceed what a student is able to do in a four month semester.

The problem before the teacher is to decide on how much compromise on (1) must be done in favour of (2). eXpOS is our stance in this matter.


There are three central principles that have been kept in mind in designing the eXpOS educational tool:

- [Separation of concerns](https://en.wikipedia.org/wiki/Edsger_W._Dijkstra)
- [Things shall be made as simple as possible, but no simpler](https://en.wikipedia.org/wiki/Albert_Einstein)
- ["Build to learn" rather than "learn to build"](https://en.wikipedia.org/wiki/Fred_Brooks)

These thoughts have translated into the following decisions:

1.  Keep the upward and downward interfaces of the OS kernel idealistically simple – This means:
    1.  The architecture platform on which the OS is implemented is kept simple to understand and program, yet capable of supporting virtual memory, interrupt driven disk/IO, time sharing, exception handling, demand paging etc.
    2.  The application programming interface ([API](http://exposnitc.github.io/os_spec.html)) (and the application binary interface [­(ABI)](http://exposnitc.github.io/abi.html) ) provided by the OS are kept simple and minimal.
2.  The [OS specification](os_spec.html) has been kept as simple as possible from the viewpoint of the OS programmer. The OS features are minimal, some of them being:
    1.  [co-operative multi-tasking](https://en.wikipedia.org/wiki/Cooperative_multitasking)
    2.  a simple single-directory file system where processes can create, write, read and delete data files
    3.  provision for processes to share files and memory
    4.  primitives for interprocess communication (binary semaphores) and process synchronization (signal-wait)
    5.  support for multiple users
    6.  demand-paged memory management
3.  The OS code has to be completely written by the student with no built-in code given, except for a bootstrap ROM code and code implementing an [application level library interface](abi.html#library). The programming support has been kept minimal to avoid high level programming tools hiding too many low level issues from the OS programmer. Essentially, the student has to do “low level programming” on a “high level hardware".
4.  The system is designed to help the student appreciate the functioning of a “sufficiently complex” operating system and **not** to help him/her gain experience with real operating systems programming. The architecture, the OS, the API, ABI etc. are all different from any of the existing real systems or standards in use, but designed to make the task of programming the OS as simple as possible.

---

Since the operating system kernel is a software that forms a layer between the hardware and the application program, the first major hurdle that a student faces while writing an OS is in understanding the complexities of the underlying hardware.

The eXpOS package simplifies this by providing a hypothetical simple-to-program hardware abstraction – the [XSM Machine](arch_spec.html). What makes XSM simple is that its memory words can store an arbitrary string or a number. This means that data formatting – one of the major technicalities while working with machines - is simplified. Further simplifications include the assumption that each disk block fits into exactly one memory page etc. The OS code can be written by programming the machine using a simple to learn [SPL language](support_tools-files/spl.html) (which is just an enriched XSM assembler).

The second interface of the OS is its upward interface – the interface to application programs. This interface, called the application binary interface ( [­ABI](abi.html) ), defines the low level system call interface between the application and the OS, the virtual address space model for an application, the format of executable files etc. The ABI too is kept minimal. It is easy to load executables into the memory. Only small programs are permitted. Parameter passing between applications and the system calls is also extremely simple.

The eXpOS [­ABI](abi.html) is too primitive to support application programs in the C programming language. Hence we provide a separate language (called [ExpL](support_tools-files/expl.html)) using which applications can be created and compiled. The ExpL compiler given to the student supports the eXpOS high level application program interface ([API](os_spec.html)). We note here that, implementing an ExpL compiler for the eXpOS ABI on the XSM machine would be an instructive exercise for an undergraduate compiler design laboratory. (See [ExpL compiler project](https://silcnitc.github.io).)

We are of the view that insisting the student to work with real systems diverts his/her attention to the details of various “formats, standards and interfaces" which often comes in the way of appreciating the underlying principles of OS design. eXpOS separates concerns by providing minimal interfaces that are just sufficient to achieve the required functionality.

The development methodology suggested is to start from scratch with a simple bootstrap loader. Routines for handling the timer, disk and I/O devices shall be added next. A simple program loader that can load and execute applications from the disk can be written at this point. Single process operation will be possible at this stage. Following this, modules to support multi-tasking, Interprocess communication and process synchronization can be added. A file system can now be built on top of this structure. Multi-user support may be added next and finally full scale virtual memory management with swapping and demand paging shall be implemented. (A final stage adding support for multiprocessor operation is also intended.) The [roadmap](Roadmap.html) guides the student systematically through these stages, asking him/her to follow the links and learn the concepts relevant to the OS modules developed in each stage.

---

There are two aspects associated with the design and implementation of each major component of an OS. – 1) A Policy and 2) An implementation Mechanism.

For example, the OS may specify a policy that each process is allowed it's own logical address space starting from 0 to a particular limit. Paging is a hardware mechanism that allows the OS to implement the policy. As another example, child processes inheriting open file instances from its parent process is a policy. The mechanism used by eXpOS to implement the policy is to keep a shared file seek position in an open file table.

The pedagogical strategy followed here is to keep policies excessively simple  so that the student can easily implement
the policy, once the implementation mechanism is understood.  For instance, in this project, size of the address space of
a process is fixed by the OS, the file system does not have a directory structure and so on.   To  quickly prepare the students
for the implementation, we provide detailed tutorials on various implementation mechanisms (like hardware paging) necessary to 
implement the policies.  Our belief is that once the student completes the implementation of a simple policy using a particular 
mechanism, she will be in a position to visualize the implementation of more sophisticated policies that uses similar mechanisms
 without actually going through another implementation project.

It is our belief that the experiment will provide the student with a feel for how the OS modules for process management, memory management, file management, device management, inter-process communication, process sychronization, demand paging and user management can be glued together to form a functional operating system. An appreciation for the Operating System's hardware interface, application interface and run time library linkage is also intended.

We had tried our best to ensure that the spirit of the subject matter is not lost. However there have been compromises. The multi-user support, the file system and device handling are very primitive. Address space of a process is small and cannot expand at run time. Going further in these directions would make it difficult for the project to be completed in a semester. Some of these extensions are not “in principle” hard, once the basic OS is built. However topics such as pre-emptive multitasking, fault tolerance, system security etc. are beyond the scope of this project.

---

The project presumes that the student has undergone a basic sophomore course in computer organization and data structures and has either completed or is currently undergoing a theory course in operating systems. The project does not require the student to be familar with the principles of compilers. It is not expected that the student has a high level of proficiency in programming or computer hardware. The required background on paging hardware, interrupts, run­time stack of application programs etc. are provided as reading material at appropriate places in the project roadmap. The parameter passing convention of ExpL as well as the system call interface are pretty simple so that students will have no serious difficulty in extracting parameters inside system calls and sending back return values to the application, despite not having undergone a compiler design course.

It must be emphasized that the project by no means a replacement to a theory course in operating systems,
but is only designed to suppliment it.

eXpOS evolved from an earlier version (called [XOS](http://xosnitc.github.io/)) which was successfully used for undergraduate instruction at the department of Computer Science and Engineering, NIT Calicut. eXpOS extends XOS with multi­user support, co­operative multi­tasking, interrupt based disk transfer and interprocess communication facility. Both these platforms were developed by teams of undergraduate CSE students of NIT Calicut through a series of undergraduate major projects.

### Authors
The content in the website and the documentation has been authored in the Department of Computer Science and Engineering, [National Institute of Technology, Calicut](http://nitc.ac.in) under the guidance of Dr. Murali Krishnan K. The project's activity started in the year 2010 and is currently under progress. Below is a list of co-authors and contributors to the project. The work evolved from an earlier version of the project called the [XOS project](https://xosnitc.github.io) under the guidance of Dr. Murali Krishnan K.

- **2018-2019**
    - Arun Joseph
    - Rohith Vishnumolakala
- **2017-2018**
    - Kandhala Naveena
    - Navaneeth Kishore
    - Sumedha Birajdar
- **2016-2017**
    - Akhil S
    - Karthika Aravind
    - N Ruthvik
    - Thallam Sai Sree Datta
- **2015-2016**
    - Anjana Babu
    - Christin V Jose
    - Kurian Jacob
    - Leny W V
    - Aleena Thomas
    - Reshma Sreekumar
    - Reshma Thomas
    - Nunnaguppala Surya Harsha
    - Vishnupriya Matha
- **2014-2015**
    - Kruthika Suresh Ved
    - Sikha V Manoj
    - Sonia V Mathew
    - Aswathy T Revi
    - Subhisha
    - Gautham R Warrier
    - Glen Martin
    - Govind R
- **2012-2013**
    - Shamil C M
    - Sreeraj S
    - Vivek Anand T Kallampally
- **2010-2012**
    - Ajeet Kumar
    - Albin Suresh
    - Avinash
    - Deepak Goyal
    - Jeril K George
    - K Dinesh
    - Mathew Kumpalamthanam
    - Naseem Iqbal
    - Nitish Kumar
    - Ramnath Jayachandran
    - Sathyam Doraswamy
    - Sumesh B
    - Yogesh Mishra
- **Technical Contributors**
    - Shajahan Fariz
    - Nikhil Sojan

### License
[![Creative Commons License](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc/4.0/)  
eXpOS by Dr. Murali Krishnan K, Department of Computer Science and Engineering, National Institute of Technology, Calicut is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](http://creativecommons.org/licenses/by-nc/4.0/). Based on a work at [https://github.com/eXpOSNitc](https://github.com/eXpOSNitc/)

### Acknowledgement
We thank GitHub for providing the free for use platform on which this tutoring system has been hosted. We also thank an uncountable collecton of individuals who have supported the work in one form or the other.