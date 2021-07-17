---
title: 'High Level Library Interface'
original_url: 'http://eXpOSNitc.github.io/os_spec-files/dynamicmemoryroutines.html'
hide:
    - navigation
---

## High Level Library Interface
The High Level Library Interface is a unified Application Programming Interface (API) to access system call routines and dynamic memory management functions from application programs. The ExpL language allows applications to access the OS routines only through the library interface. The syntax for the call to the library function in ExpL is :

```
t = exposcall(fun_code, arg1, arg2, arg3);
```

Depending on the fun_code the control is transferred to the [system call routines](systemcallinterface.md) and the dynamic memory management functions (see below) .

<table class="table table-bordered" style="text-align: center;" id="syscalltable">
<thead>
<tr class="success">
<th style="text-align: center;">Library Function / System Call </th>
<th style="text-align: center;">Function Code</th>
<th style="text-align: center;">Argument 1</th>
<th style="text-align: center;">Argument 2</th>
<th style="text-align: center;">Argument 3</th>
<th style="text-align: center;"> Return value </th>
</tr>
</thead><tbody>
<tr>
<td rowspan="2">Create</td>
<td rowspan="2">"Create"</td>
<td rowspan="2">File Name</td>
<td rowspan="2">Permission <img alt="🔴" class="twemoji" src="https://twemoji.maxcdn.com/v/latest/svg/1f534.svg" title=":red_circle:"></td>
<td rowspan="2">-</td>
<td>0 - Success/File already exists
</tr>
<td>-1 - No free inode table entry</tr>
</tr>

<tr>
<td rowspan="4">Open</td>
<td rowspan="4">"Open"</td>
<td rowspan="4">File Name</td>
<td rowspan="4">-</td>
<td rowspan="4">-</td>
<td> File Descriptor - Success
</tr>
<td>-1 - File Not found or file is not data file or root file</tr>
<td>-2 - System has reached its limit of open files</tr>
<td>-3 - Process has reached its limit of resources</tr>
</tr>


<tr>
<td rowspan="2">Close</td>
<td rowspan="2">"Close"</td>
<td rowspan="2">File Descriptor</td>
<td rowspan="2">-</td>
<td rowspan="2">-</td>
<td>0 - Success
</tr>
<td>-1 - File Descriptor is invalid</tr>
</tr>

<tr>
<td rowspan="3">Delete</td>
<td rowspan="3">"Delete"</td>
<td rowspan="3">File Name</td>
<td rowspan="3">-</td>
<td rowspan="3">-</td>
<td>0 - Success/File does not exist
</tr>
<td>-1 - Permission Denied</tr>
<td>-2 - File is open</tr>
</tr>
<tr>
<td rowspan="4">Write</td>
<td rowspan="4">"Write"</td>
<td rowspan="4">File Descriptor (-2 for terminal)</td>
<td rowspan="4">Word to be written</td>
<td rowspan="4">-</td>
<td>0 - Success
</tr>
<td>-1 - File Descriptor given is invalid</tr>
<td>-2 - No disk space</tr>
<td>-3 - Permission denied</tr>
</tr>
<tr>
<td rowspan="3">Read</td>
<td rowspan="3">"Read"</td>
<td rowspan="3">File Descriptor (-1 for terminal)</td>
<td rowspan="3">Variable name (to which data is to be read)</td>
<td rowspan="3">-</td>
<td>0 - Success
</tr>
<td>-1 - File Descriptor given is invalid</tr>
<td>-2 - File pointer has reached the end of file</tr>
</tr>

<tr>
<td rowspan="3">Seek</td>
<td rowspan="3">"Seek"</td>
<td rowspan="3">File Descriptor</td>
<td rowspan="3">Offset</td>
<td rowspan="3">-</td>
<td>0 - Success
</tr>
<td>-1 - File Descriptor is invalid</tr>
<td>-2 - Offset moves File pointer outside file</tr>
</tr>


<!--- -->

<tr>
<td rowspan="3">Fork</td>
<td rowspan="3">"Fork"</td>
<td rowspan="3">-</td>
<td rowspan="3">-</td>
<td rowspan="3">-</td>
<td>PID - Success (in parent process)
</tr>
<td>0 - Success (in child process)</tr>
<td>-1 - Failure (in parent process), Number of processes has reached maximum limit </tr>
</tr>
<tr>
<td rowspan="2">Exec</td>
<td rowspan="2">"Exec"</td>
<td rowspan="2">File Name</td>
<td rowspan="2">-</td>
<td rowspan="2">-</td>
<td>-1 - File not found or file is not executable
</tr>
<td>-2 - Out of memory or disk swap space</td>
</tr>

<tr>
<td>Exit</td>
<td>"Exit"</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>-</td>
</tr>

<tr>
<td>Getpid</td>
<td>"Getpid"</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>current PID - Success</td>
</tr>

<tr>
<td>Getppid</td>
<td>"Getppid"</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>parent PID - Success</td>
</tr>

<tr>
<td rowspan="2">Wait</td>
<td rowspan="2">"Wait"</td>
<td rowspan="2">Process Identifier</td>
<td rowspan="2">-</td>
<td rowspan="2">-</td>
<td>0 - Success
</tr>
<td>-1 - Given PID is invalid or it is PID of invoking process</tr>
</tr>

<tr>
<td>Signal</td>
<td>"Signal"</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>0 - Success</td>
</tr>

<tr>
<td rowspan="3">Semget</td>
<td rowspan="3">"Semget"</td>
<td rowspan="3">-</td>
<td rowspan="3">-</td>
<td rowspan="3">-</td>
<td>SEMID - Success
</tr>
<td>-1 - Process has reached its limit of resources</tr>
<td>-2 - Number of semaphores has reached its maximum</td>
</tr>

<tr>
<td rowspan="2">Semrelease</td>
<td rowspan="2">"Semrelease"</td>
<td rowspan="2">Semaphore Descriptor</td>
<td rowspan="2">-</td>
<td rowspan="2">-</td>
<td>0 - Success
</tr>
<td>-1 - Invalid SEMID</tr>
</tr>

<tr>
<td rowspan="2">SemLock</td>
<td rowspan="2">"SemLock"</td>
<td rowspan="2">Semaphore Descriptor</td>
<td rowspan="2">-</td>
<td rowspan="2">-</td>
<td>0 - Success or semaphore is already locked by the current process
</tr>
<td>-1 - invalid SEMID </tr>
</tr>
<tr>
<td rowspan="3">SemUnLock</td>
<td rowspan="3">"SemUnLock"</td>
<td rowspan="3">Semaphore Descriptor</td>
<td rowspan="3">-</td>
<td rowspan="3">-</td>
<td>0 - Success
</tr>
<td>-1 - Invalid SEMID</tr>
<td>-2 - Semaphore was not locked by the calling process</tr>
</tr>

<tr>
<td>Shutdown</td>
<td>"Shutdown"</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>-1 - Permission denied</td>
</tr>
<tr>
<td rowspan="4">Newusr</td>
<td rowspan="4">"Newusr"</td>
<td rowspan="4">User name</td>
<td rowspan="4">Password</td>
<td rowspan="4">-</td>
<td>0 - Success
</tr>
<td>-1 - User already exists</tr>
<td>-2 - Permission denied</tr>
<td>-3 - No. of users have reached the system limit.</tr>
</tr>
<tr>
<td rowspan="4">Remusr</td>
<td rowspan="4">"Remusr"</td>
<td rowspan="4">User name</td>
<td rowspan="4">-</td>
<td rowspan="4">-</td>
<td>0 - Success
</tr>
<td>-1 - User does not exist</tr>
<td>-2 - Permission denied</tr>
<td>-3 - Undeleted files exist for the user</tr>
</tr>
<tr>
<td rowspan="3">Setpwd</td>
<td rowspan="3">"Setpwd"</td>
<td rowspan="3">User name</td>
<td rowspan="3">New Password</td>
<td rowspan="3">-</td>
<td>0 - Success
</tr>
<td>-1 - Unauthorised attempt to change password</tr>
<td>-2 - The user does not exist.</tr>
</tr>
<tr>
<td rowspan="2">Getuname</td>
<td rowspan="2">"Getuname"</td>
<td rowspan="2">User ID</td>
<td rowspan="2">-</td>
<td rowspan="2">-</td>
<td>User Name - Success
</tr>
<td>-1 - Invalid User ID</td>
</tr>
<tr>
<td rowspan="2">Getuid</td>
<td rowspan="2">"Getuid"</td>
<td rowspan="2">User name</td>
<td rowspan="2">-</td>
<td rowspan="2">-</td>
<td>User ID - Success
</tr>
<td>-1 - Invalid username</td>
</tr>
<tr>
<td rowspan="3">Login</td>
<td rowspan="3">"Login"</td>
<td rowspan="3">User name</td>
<td rowspan="3">Password</td>
<td rowspan="3">-</td>
<td>0 - Success
</tr>
<td>-1 - Invalid username or password</tr>
<td>-2 - Permission denied</tr>
</tr>
<tr>
<td>Logout</td>
<td>"Logout"</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>-1 - permission denied</td>
</tr>

<tr>
<td>Test0</td>
<td>"Test0"</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>-</td>
</tr>

<tr>
<td>Test1</td>
<td>"Test1"</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>-</td>
</tr>

<tr>
<td>Test2</td>
<td>"Test2"</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>-</td>
</tr>

<tr>
<td>Test3</td>
<td>"Test3"</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>-</td>
</tr>

<tr>
<td style="color:red">Test4 <img alt="🔵" class="twemoji" src="https://twemoji.maxcdn.com/v/latest/svg/1f535.svg" title=":blue_circle:"></td>
<td>"Test4"</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>-</td>
</tr>

<tr>
<td style="color:red">Test5 <img alt="🔵" class="twemoji" src="https://twemoji.maxcdn.com/v/latest/svg/1f535.svg" title=":blue_circle:"></td>
<td>"Test5"</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>-</td>
</tr>

<tr>
<td style="color:red">Test6 <img alt="🔵" class="twemoji" src="https://twemoji.maxcdn.com/v/latest/svg/1f535.svg" title=":blue_circle:"></td>
<td>"Test6"</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>-</td>
</tr>

<tr>
<td style="color:red">Test7 <img alt="🔵" class="twemoji" src="https://twemoji.maxcdn.com/v/latest/svg/1f535.svg" title=":blue_circle:"></td>
<td>"Test7"</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>Unspecified</td>
<td>-</td>
</tr>

<tr class="active">
<td rowspan="2">Initialize</td>
<td rowspan="2">"Heapset"</td>
<td rowspan="2">-</td>
<td rowspan="2">-</td>
<td rowspan="2">-</td>
<td>0 - Success
</tr>
<td style="background-color: rgb(245,245,245);">-1 - Failure</tr>
</tr>
<tr class="active">
<td rowspan="2">Alloc</td>
<td rowspan="2">"Alloc"</td>
<td rowspan="2">Size</td>
<td rowspan="2">-</td>
<td rowspan="2">-</td>
<td>Allocated address in Heap - Success
</tr>
<td style="background-color: rgb(245,245,245);">-1 - No allocation</tr>

</tr>
<tr class="active">
<td rowspan="2">Free</td>
<td rowspan="2">"Free"</td>
<td rowspan="2">Pointer</td>
<td rowspan="2">-</td>
<td rowspan="2">-</td>
<td>0 - Success
</tr>
<td style="background-color: rgb(245,245,245);">-1 - Failure</tr>
</tr>
</tbody>
</table>

:red_circle: If the file is created with EXCLUSIVE permissions, then write and delete system calls will fail when executed by any user other than the owner or the root (see here).

:blue_circle: These System Calls are available only on eXpOS running on NEXSM (a two-core extension of XSM) machine.

!!! note
    According to syntax of exposcall(), it needs four arguments. These arguments are func_code, arg1, arg2, arg3. func_code is necessary for every exposcall() to recognize the Library function/System call. The remaining number of arguments varies according to Library interface specification of the corresponding func_code. Even if exposcall() is invoked with more number of arguments than required for a particular Library function/System call, they are ignored.

Examples to use above mentioned Library functions/system calls :

1) To open a file named example.dat, ExpL library interface call is

```
   fd=exposcall("Open","example.dat");
```
Here return value is stored in variable fd, which is file descriptor for file example.dat on success.

2) From above example, variable 'fd' contains file descriptor for file example.dat. To write the value stored in variable 'num' to this file, ExpL library interface call is

```
   temp=exposcall("Write",fd,num);     //return value stored in temp
```

To write to terminal, use -2 as first argument. Note that expressions such as 2 + 3, num * 34 are not valid as second argument for write system call.
```
    temp=exposcall("Write",fd,num+2); //Invalid library interface call
```

3) Alloc is a library function, which is predefined in ExpL library. It is a dynamic memory management routine. It allocates memory for variables of user defined type in ExpL. ExpL library interface call to allocate memory for variable 'data', which requires 3 words of memory is
```
   data=exposcall("Alloc",3);
```

**The present library routine alloc allocates 8 words for any variable irrespective of the size mentioned in its alloc exposcall(). So, do not define a user defined type having more than 8 fields. Remember to call library function Intialize using exposcall() once before invoking first alloc in any ExpL program.**

The description of the system calls can be seen [here](systemcallinterface.md). The dynamic memory management routines are described below.




## Dynamic Memory Routines

### Initialize
Arguments: None

Return Value:
<table class="table table-bordered">
<tr>
<td>0</td>
<td>Success</td>
</tr>
<tr>
<td>-1</td>
<td>Failure</td>
</tr>
</table>

Description: Intitalizes the heap data structures and sets up the heap area of the process.
It is the applications responsibility to invoke Initialize() before the first use of
Alloc(). The behaviour of Alloc() and Free() when invoked
without an Intialize() operation is undefined. Any memory allocated before an Intialize()
operation will be reclaimed for future allocation. 

### Alloc

Arguments: Size (Integer)

Return Value:

<table class="table table-bordered">
<tr>
<td>Allocated address in Heap</td>
<td>Success</td>
</tr>
<tr>
<td>-1</td>
<td>No allocation</td>
</tr>
</table>

Description: The Alloc operation takes size (integer) as an input and when successful,
allocates contiguous words (in the heap) equal to the size specified and returns the address
of the allocated memory.The present implementation of library routine alloc allocates 8
words for any variable irrespective of the size mentioned in its alloc exposcall(). So, do
not define a user defined type having more than 8 fields.

### Free
Arguments: Pointer (Integer)

Return Value:
<table class="table table-bordered">
<tr>
<td>0</td>
<td>Success</td>
</tr>
<tr>
<td>-1</td>
<td>Failure</td>
</tr>
</table>
Description: The Free operation takes a pointer (i.e., an integer memory address) of a
previously allocated memory block and returns it to the heap memory pool. If the pointer
does not correspond to a valid reference to the beginning of a previously allocated memory
block, the behaviour of Free is not defined.