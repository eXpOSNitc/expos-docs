---
title: Multi-user Implementation Tutorial
original_url: http://exposnitc.github.io/Tutorials/multiuser_implementation.html
---

!!! note "Prerequisites"
    It is necessary to read the following documentations before starting with this tutorial.
    
    1. User level specification of [eXpOS multi-user model](../os-spec/multiuser.md).
    2. [Multi-user system call specification](../os-spec/systemcallinterface.md#multiuser-system-calls).
    3. Specification of [Shell commands and system utilities](../os-spec/shell-spec.md).

eXpOS implements a very primitive support for multiple users to login into the system. eXpOS supports only one terminal. Hence, only one user is permitted to login into the system at one time and another user can login only after the current user logs out. The OS permits only a maximum of 16 users to be created. Of these 16, two are default users - the **kernel** and the **root**.

The OS maintains a single disk data structure, the [user table](../os-design/disk-ds.md#user-table) - for storing information pertaining to the users in the system. The user table contains 16 entries. Each entry contains just two fields - a **username** and an **encrypted password**. The OS maintains one entry per user. The OS also assigns a **user-id** to each user. The user-id of a user is the index of the user’s entry in the user table. (Hence there is no field for storing the user-id of a user in the user table.) Thus, the first entry in the user table corresponds to user-id = 0, the next user has userid = 1 and so on. The user table is stored in 32 words of disk block 4 in the disk. Note that the user table appears at the end of the Inode table in the disk. (See [disk organization](../os-implementation.md)).

eXpOS assumes that the machine provides some kind of password encryption mechanism. The XSM machine provides the [ENCRYPT](../arch-spec/instruction-set.md) to convert a text password to encrypted form. (The SPL instruction [encrypt](../support-tools/spl.md) gets translated to the above machine instruction).

When the xfs-disk is formatted using the [FDISK command](../support-tools/xfs-interface.md) of the XFS-interface, the user table is initialized with valid entries for the two default users - kernel and the root. The first two entries of the user table are assigned to kernel and root. Consequently, the user-id of kernel is 0 and the user-id of root is 1. All other entries are initialized to -1 (invalid entry).

Among the two default users, **kernel is a non-loggable user**. Hence, kernel has no password set initially by FDISK. The root user is assigned a default password “root” (without quotes) by FDISK. This means that the **encrypted form of the string “root”** (without quotes) is stored in the user table entry corresponding to root.

To understand the dynamics of user management, we need to look at the steps taken by the OS during startup. At the time of OS startup, the OS loads the disk block containing the user table into memory page 60 (see [memory organization](../os-implementation.md)). The OS startup code hand creates three processes - the idle process (PID=0), the INIT process (PID=1) and the SHELL process (PID=2). The INIT process of eXpOS is called the **login process**. The user-id of the idle process and the login process are set to 0 in their respective process table entries. Hence, both processes are treated as special “kernel processes”. The user-id of the shell process will be set to the user who has logged into the system.

### Login and Shell Processes

The login process executes a loop and asks the user to enter a _login name_ and (unencrypted) _text password_. The login process supplies these arguments to the **Login** system call. _Login_ system call checks whether there is an entry in the user table corresponding to the login name given. If so, it encrypts the text password given as argument (using the ENCRYPT instruction) and matches the result with the encrypted password stored in the user table entry of the user. If either check fails, then _Login_ system call returns an error code. In this case, the login process announces “login failure” and continues to ask for another username and password. Note that the first user to login after running FDISK must be the root user with the password “root” (without quotes).

If the username and password matches a user, the _Login_ system call sets the **shell program** ready for execution. The shell program’s code is pre-loaded into the memory. The stack pages are allocated for the shell process and page table entries for PID=2 are set to these values during boot time. Hence, the effective work of _Login_ is to just set the process ready to run. The **shell process is assigned user-id of the logged in user and its Parent PID is set to the PID of the login process. Hence, the shell process runs the shell in the context of the logged in user**. Consequently, any other program executed by the shell will also execute in the context of the same user as the _Fork_ system call copies the user-id of the parent to the child. The login process has done its work for the time being, and will go into sleep waiting for the exit of the shell process spawned for the user (essentially doing the work of _Wait_ system call as well internally). After waking up (which can happen only when the shell executes the _Logout_ system call), Login process resumes execution by asking for the username and password of the next user. Note that login runs in an infinite loop and never terminates.  
 

**The shell is always executed with PID = 2.** Once the shell process starts execution from the context of a user, system calls for process management, file management, interprocess communication and process synchronization work in the normal way. As the shell program is a special system program supplied by the OS designer, by design, it never executes the _Exit_ system call. The only way in which the shell can wake up the login process is to execute the _Logout_ system call. The shell executes the _Logout_ system call when the user enters the shell command “logout”. _Logout_ system call terminates all processes of the current user (including the shell) and wakes up the login process so that the next user may be logged in. Hence _Logout_ system call, in effect, does the work of the _Exit_ system call on all currently active processes of the currently logged in user. eXpOS specification stipulates that the _Logout_ system call can be executed only by the shell process (PID = 2).

### Multi-user system calls

eXpOS **system calls for user management** are:

1. _Newusr_ - to create a new user
2. _Remusr_ - to remove a user
3. _Setpwd_ - set the password of a user
4. _Getuid_ - to get the user-id of the currently logged in user
5. _Getuname_ - to get the username of the currently logged in user
6. _Login_ - to login a user
7. _Logout_ - logout the current user
8. _Shutdown_ - to shutdown the system after committing the memory copies of all disk data structures into the disk

Among these, **_Newusr_, _Remusr_ and _Shutdown_ can be executed from the shell of the root user only and _Setpwd_ and _Logout_ can be executed from the shell process of any user**. Only the root user is permitted to change the password of other users using the _Setpwd_ system call. (See [specification](../os-spec/multiuser.md).)
 
The _security model_ guaranteed to the user by the above scheme is the following. A user may run any eXpFS executable program using the shell, and the program will be to access any file which the user has access to. The program can also spawn more processes, all running with permissions allowed for the logged in user. The program cannot delete or write into files which the user does not have write permission. The program is also not allowed to do things that “harm the user’s account” - like changing the user’s password etc., or tamper with the accounts of other users. The only way for a user to change one’s password is to do so using the shell. One user cannot change the password of others. A normal user can log out of the system using the shell, but cannot shut down the system.

The system administrator, _root_, can run programs that access, modify or delete the files of any user. The root can also use the shell to delete a user’s account. (Note: The _Remusr_ system call requires that all files owned by a user must be deleted before the account can be deleted. This is necessary to ensure that the system is not left with “abandoned” files when a user’s account is deleted). The root is permitted to change the password of any user. Root is the only user who is authorized to run the shell command to shutdown the system.

Also see the specification of the [eXpOS shell](../os-spec/shell-spec.md).