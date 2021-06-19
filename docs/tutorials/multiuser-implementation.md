---
title: Multi-user Implementation Tutorial
original_url: http://exposnitc.github.io/Tutorials/multiuser_implementation.html
---

!!! note "Prerequisites"
    It is necessary to read the following documentations before starting with this tutorial.
    
    1. User level specification of <a href="../os_spec-files/multiuser.html" target="_blank">eXpOS multi-user model</a>.<br>
    2. <a href="../os_spec-files/systemcallinterface.html#multiusersystemcalls" target="_blank">Multi-user system call specification</a>.<br>
    3. Specification of <a href="../os_spec-files/shell_spec.html" target="_blank">Shell commands and system utilities</a>.<br>

eXpOS implements a very primitive support for multiple users to login into the system. eXpOS supports only one terminal. Hence, only one user is permitted to login into the system at one time and another user can login only after the current user logs out. The OS permits only a maximum of 16 users to be created. Of these 16, two are default users - the <b>kernel</b> and the <b>root</b>.

The OS maintains a single disk data structure, the <a href="../os_design-files/disk_ds.html#user_table" target="_blank">user table</a> - for storing information pertaining to the users in the system. The user table contains 16 entries. Each entry contains just two fields - a <b>username</b> and an <b>encrypted password</b>. The OS maintains one entry per user. The OS also assigns a <b>user-id</b> to each user. The user-id of a user is the index of the user’s entry in the user table. (Hence there is no field for storing the user-id of a user in the user table.) Thus, the first entry in the user table corresponds to user-id = 0, the next user has userid = 1 and so on. The user table is stored in 32 words of disk block 4 in the disk. Note that the user table appears at the end of the Inode table in the disk. (See <a href="../os_implementation.html" target="_blank">disk organization</a>). 

eXpOS assumes that the machine provides some kind of password encryption mechanism. The XSM machine provides the <a href="../arch_spec-files/instruction_set.html" target="_blank">ENCRYPT</a> to convert a text password to encrypted form. (The SPL instruction <a href="../support_tools-files/spl/html" target="_blank">encrypt</a> gets translated to the above machine instruction).

When the xfs-disk is formatted using the <a href="../support_tools-files/xfs-interface.html" target="_blank">FDISK command</a> of the XFS-interface, the user table is initialized with valid entries for the two default users - kernel and the root. The first two entries of the user table are assigned to kernel and root. Consequently, the user-id of kernel is 0 and the user-id of root is 1. All other entries are initialized to -1 (invalid entry).

Among the two default users, <b>kernel is a non-loggable user</b>. Hence, kernel has no password set initially by FDISK. The root user is assigned a default password “root” (without quotes) by FDISK. This means that the <b>encrypted form of the string “root”</b> (without quotes) is stored in the user table entry corresponding to root.


To understand the dynamics of user management, we need to look at the steps taken by the OS during startup. At the time of OS startup, the OS loads the disk block containing the user table into memory page 60 (see <a href="../os_implementation.html" target="_blank">memory organization</a>). The OS startup code hand creates three processes - the idle process (PID=0), the INIT process (PID=1) and the SHELL process (PID=2). The INIT process of eXpOS is called the <b>login process</b>. The user-id of the idle process and the login process are set to 0 in their respective process table entries. Hence, both processes are treated as special “kernel processes”. The user-id of the shell process will be set to the user who has logged into the system. 

### Login and Shell Processes

The login process executes a loop and asks the user to enter a <i>login name</i> and (unencrypted) <i>text password</i>. The login process supplies these arguments to the <b>Login</b> system call. <i>Login</i> system call checks whether there is an entry in the user table corresponding to the login name given. If so, it encrypts the text password given as argument (using the ENCRYPT instruction) and matches the result with the encrypted password stored in the user table entry of the user. If either check fails, then <i>Login</i> system call returns an error code. In this case, the login process announces “login failure” and continues to ask for another username and password. Note that the first user to login after running FDISK must be the root user with the password “root” (without quotes).

If the username and password matches a user, the <i>Login</i> system call sets the <b>shell program</b> ready for execution. The shell program’s code is pre-loaded into the memory. The stack pages are allocated for the shell process and page table entries for PID=2 are set to these values during boot time. Hence, the effective work of <i>Login</i> is to just set the process ready to run.   The <b>shell process is assigned user-id of the logged in user and its Parent PID is set to the PID of the login process.  Hence, the shell process runs the shell in the context of the logged in user</b>.  Consequently, any other program executed by the shell will also execute in the context of the same user as the <i>Fork</i> system call copies the user-id of the parent to the child. The login process has done its work for the time being, and will go into sleep waiting for the exit of the shell process spawned for the user (essentially doing the work of <i>Wait</i> system call as well internally). After waking up (which can happen only when the shell executes the <i>Logout</i> system call), Login process resumes execution by asking for the username and password of the next user. Note that login runs in an infinite loop and never terminates.   
 

<b>The shell is always executed with PID = 2.</b> Once the shell process starts execution from the context of a user, system calls for process management, file management, interprocess communication and process synchronization work in the normal way. As the shell program is a special system program supplied by the OS designer, by design, it never executes the <i>Exit</i> system call. The only way in which the shell can wake up the login process is to execute the <i>Logout</i> system call. The shell executes the <i>Logout</i> system call when the user enters the shell command “logout”. <i>Logout</i> system call terminates all processes of the current user (including the shell) and wakes up the login process so that the next user may be logged in. Hence <i>Logout</i> system call, in effect, does the work of the <i>Exit</i> system call on all currently active processes of the currently logged in user. eXpOS specification stipulates that the <i>Logout</i> system call can be executed only by the shell process (PID = 2).

### Multi-user system calls

eXpOS **system calls for user management** are:

1. <i>Newusr</i> - to create a new user
2. <i>Remusr</i> - to remove a user
3. <i>Setpwd</i> - set the password of a user
4. <i>Getuid</i> - to get the user-id of the currently logged in user
5. <i>Getuname</i> - to get the username of the currently logged in user
6. <i>Login</i> - to login a user
7. <i>Logout</i> - logout the current user
8. <i>Shutdown</i> - to shutdown the system after committing the memory copies of all disk data structures into the disk

Among these, <b><i>Newusr</i>, <i>Remusr</i> and <i>Shutdown</i> can be executed from the shell of the root user only and <i>Setpwd</i> and <i>Logout</i> can be executed from the shell process of any user</b>. Only the root user is permitted to change the password of other users using the <i>Setpwd</i> system call. (See <a href="../os_spec-files/multiuser.html" target="_blank">specification</a>.)
 
The <i>security model</i> guaranteed to the user by the above scheme is the following.  A user may run any eXpFS executable program using the shell, and the program will be to access any file which the user has access to. The program can also spawn more processes, all running with permissions allowed for the logged in user. The program cannot delete or write into files which the user does not have write permission. The program is also not allowed to do things that “harm the user’s account” - like changing the user’s password etc., or tamper with the accounts of other users. The only way for a user to change one’s password is to do so using the shell. One user cannot change the password of others. A normal user can log out of the system using the shell, but cannot shut down the system.

The system administrator, <i>root</i>, can run programs that access, modify or delete the files of any user. The root can also use the shell to delete a user’s account. (Note: The <i>Remusr</i> system call requires that all files owned by a user must be deleted before the account can be deleted. This is necessary to ensure that the system is not left with “abandoned” files when a user’s account is deleted). The root is permitted to change the password of any user. Root is the only user who is authorized to run the shell command to shutdown the system.

<p style="text-indent: 0px">Also see the specification of the <a href="../os_spec-files/shell_spec.html" target="_blank">eXpOS shell</a>.
