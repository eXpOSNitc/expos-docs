---
title: Experimental File System (eXpFS)
original_url: https://exposnitc.github.io/os_spec-files/eXpFS.html
hide:
    - navigation
---

eXpOS assumes that the disk is a sequence of blocks, where each block can store a sequence of words.The number of words in a block is hardware dependent. Generally, the hardware comes with machine instructions to transfer a block from the disk to a contiguous space in memory and back.

The eXpFS logical file system provides a file abstraction that allows application programs to think of each data (or executable) file stored in the disk as a continuous stream of data (or machine instructions) without having to worry about the details of disk block allocation. Thus eXpFS hides the details of physical storage from application programs. eXpOS provides a sequence of file system calls through which application programs can create/read/write data files. These system calls are OS routines that does the translation of the user request into physical disk block operations.

In addition to the eXpOS system call interface, the eXpFS specification also requires that there is an external interface through which executable and data files can be loaded into the file system externally. The details of the external interface are implementation specific. The external interface for eXpOS implementation on the XSM machine is described in [XFS Interface](https://exposnitc.github.io/support_tools-files/xfs-interface.html).

In this section we discuss the abstract logical view provided by eXpFS to the eXpOS application programmer.


### eXpFS File System Organization

The eXpFS logical file system comprises of files organized in a single directory called the root. The root is also treated conceptually as a file. As noted already, every eXpFS file is a sequence of words. Associated with each eXpFS file there are three attributes - name, size and type, each attribute being one word long. The file name must be a string. Each file must have a unique name. The size of the file will be the total number of words stored in the file. (The maximum size of a file is operating system dependent).

:red_circle: In [extended eXpOS](http://exposnitc.github.io/os_spec-files/multiuser.html), a file has two additional attributes, username and permission.

There are three types of eXpFS files - the root, data files and executable files. Each file in eXpFS has an entry in the root called its root entry.

### The eXpFS Root File
The root file has the name root and contains _meta-data_ about the files stored in the file system. For each file stored in eXpFS, the root file stores three words of information - **file name, file-size and file-type**. (\* In [extended eXpOS](http://exposnitc.github.io/os_spec-files/multiuser.html), the root file stores two additional words - **user name** and **permission**.) This triple( \* In [extended eXpOS](http://exposnitc.github.io/os_spec-files/multiuser.html), 5-tuple) is called the **root entry** for the file. The first root entry is for the root itself. The order in which the remaining entries appear is not specified and can vary with the implementation. Example: If the file system stores two files - a data file, file.dat, of size 700 words and an executable file, **confirm this** program.xexe, of 1025 words, the root file will contain the following information.

|File name|File size|File type|User name|Permission|
|--- |--- |--- |--- |--- |
|root|512|ROOT|kernel|0|
|file.dat|700|DATA|username|0/1|
|program.xexe|1025|EXEC|kernel|unused|


The operations on the root file are **Open, Close, Read and Seek**. Since the operations on the root file is a subset of the operations on data files, with the same syntax and semantics, these operations are discussed together with other operations on data files.

\* The owner of the root file is set to kernel (userid = 0) and permission set to exclusive (0) during file system formatting (see also specification of [multi-user](http://exposnitc.github.io/os_spec-files/multiuser.html) extension to eXpOS.)

### eXpFS Data files
A data file is a sequence of words. The maximum number of words permissible in a file is defined by the constant MAX\_FILE\_SIZE. (It is a recommended programming convention to use the extension ".dat" for data files). eXpFS treats every file other than root and executable files (will be described later) as a data file. The Create system call automatically sets the file type field in the root entry for any file created through the create system call to DATA.

eXpOS allows an application program to perform the following operations (by invoking appropriate system calls) on data files: **Create**, **Delete**, **Open, Close, Read, Write, Seek**. Application programs can create only data files using the Create system call. In addition to this, data files may be loaded into the eXpFS file system using the external interface (see [XFS Interface](../support_tools-files/xfs-interface.html)). A detailed specification of the file system calls is given [here](systemcallinterface.html).

:red_circle: In [Multiuser](http://exposnitc.github.io/os_spec-files/multiuser.html) implementation of eXpOS, the username of a data file corresponds to the user who creates the file. Its permission can be either exclusive (0) or open (1) according to the value specified by the user at the time of creating the file.

:blue_circle: If a data file is externally loaded into the file system (see [XFS Interface](http://exposnitc.github.io/support_tools-files/xfs-interface.html)), the owner field is set to root (value = 1) and the access permission is set to open access (value = 1).


### eXpFS Executable files
These contain executable code for programs that can be loaded and run by the operating system. From the point of view of the eXpFS file system alone, executable files are just like data files except that file type is EXEC in the root entry. **eXpFS specification does not allow executable files to be created by application programs**. They can only be created externally and loaded using the external interface (see [XFS Interface](../support_tools-files/xfs-interface.html) for XSM architecture.)

:red_circle: In [Multiuser](http://exposnitc.github.io/os_spec-files/multiuser.html) implementation of eXpOS, the access permission field for executable files is not used (value = -1). By default, the owner of all excecutable files is set to 0 (kernel).

Executable files are essentially program files that must be loaded and run by the operating system. Hence the Operating system imposes certain structure on these files (called the **executable file format**). Moreover, the instructions must execute on the machine on which the OS is running. Thus, there is dependency on the hardware as well. Typically, an application program written in a high level language (like [ExpL](../support_tools-files/expl.html)) is compiled using a compiler that generates the executable file. The compiler generates executable file that is dependent on the operating system as well as the target machine.

An OS implementation on a particular machine specifies an **application binary interface (ABI)**. The eXpOS ABI for XSM machine is specified [here](../abi.html).

!!! note "Important Note"
    Application programs are typically written in a high level language like ExpL. A high level language implementation for an OS comes with an Application Programmers Interface (API) for the OS system calls. API describes the library functions which the application programs must invoke for each operating system call. The compiler will translate the library call to corresponding low level interrupt calls as specified in the ABI. Thus, application programmers need to know only API. A description of the [ExpL](../support_tools-files/expl.html) programming language and eXpOS [API](../os_design.html) are given. The ExpL compiler for eXpOS running on the XSM machine generates target code based on the ABI specification for eXpOS on XSM. Thus the ABI becomes the most important document for compiler back end design.

    The executable file format recognized by eXpOS is called the Experimental executable file ([XEXE](http://exposnitc.github.io/abi.html#xexe)) format. In this format, an executable file is divided into two sections. The first section is called header and the second section called the code (or text) section. The code section contains the program instructions. The header section contains information like the size of the text and data segments in the file, the space to be allocated for stack and heap areas when the program is loaded for execution etc. This information is used by the OS loader to map the file into a virtual address space and create a process in memory for executing the program.