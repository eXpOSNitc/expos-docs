---
title: 'Multi-user Extension to eXpOS'
original_url: 'http://eXpOSNitc.github.io/os_spec-files/multiuser.html'
hide: 
    - navigation
---

### Multi-user Extension to eXpOS  

This document specifies the extended features provided by eXpOS to support multiple users.

The extended eXpOS allows a maximum of MAX\_USER\_NUM users. Each user is alloted a unique **userid**. Every process is assigned the userid, corresponding to the user executing the process. Two special processes hand created by the kernel at boot-­time are given the special userid ­0. These processes are the [idle process](../os-design/misc.md#idle) and the [login process](../os-design/misc.md#login) and are called the **kernel processes**. At the end of system bootstrap, the login process is scheduled for execution. The present version of eXpOS sets MAX\_USER\_NUM to 16.

The login process waits invoking the (terminal) read system call for a username and password to be input from the console. Both username and password are strings. The login process executes the [Login system call](systemcallinterface.md#multiuser-system-calls) with the username and the password as the arguments. The login system call verifies the user and creates a new [shell process](../os-design/misc.md#shell). (In practice, the shell is preloaded into memory during OS startup and the login process sets the shell ready to run.) The shell is assigned the userid of the logged in user (by the Login system call). The login process thereafter goes to sleep and will wake up only upon execution of the logout system call. All descendent processes of the shell inherit the userid of the shell. Note that Login is the only system call that can set the userid of a process. eXpOS requires one user to logout before another user can login. Hence user processes with multiple userid values will not execute simultaneously. When the shell process executes the [logout system call](systemcallinterface.md#multiuser-system-calls), all processes of the user are terminated and the login process is woken up. The login process then proceeds to login the next user. **eXpOS specification allows only the login process to execute the login system call. Other multiuser system calls except _getuid_ and _getuname_ can be executed only from the shell.** The high level interface of the login system call is given [here](systemcallinterface.md#multiuser-system-calls).

Two special users, the **kernel** and the **root**, defined by eXpOS, are assigned **userid 0** and **userid 1** respectively. Root is the user with administrative privileges. The shutdown system call can be executed only from the shell of the root user.

The system calls for adding a user or removing an existing user from the system can be executed only by the root. A new user is created using [newusr](systemcallinterface.md) system call. An existing user can be deleted by the [remusr](systemcallinterface.md) system calls. The special users­, root and kernel, cannot be removed. A user can change his/her password using [setpwd](systemcallinterface.md) system call which takes username and password as arguments. A user, other than the root is allowed to change only his/her own password. Root can change the password of any user, including itself. The [getuid](systemcallinterface.md) system call returns the user id of the current user. The [getuname](systemcallinterface.md) system call returns the username corresponding to a userid.

The API specification of all the multi­user system calls can be seen [here](systemcallinterface.md).

### File Access Permissions
 

When a file is created by a process using the [Create](systemcallinterface.md) system call, the process can set its permission to **exclusive(value = 0)/open-access(value = 1)**, to restrict access permissions. When a file is created with it's permission set to exclusive, **write and delete system calls** to that file will fail if executed by any user other than the owner of the file or the root. Open-access data files have no such restrictions. **The root can modify/delete any data file (but not the root file or executable files) irrespective of the permissions**. Kernel processes (Idle and Init/Login) have unrestricted access to all [system calls](systemcallinterface.md). The root file has default userid 0 (kernel) and permission exclusive (value = 0).

:red_circle: By default, the owner of all executable files is set to kernel (value = 0). File access permissions are not used for executable files. They can only be created externally and loaded using the external interface (see [XFS Interface](../support-tools/xfs-interface.md) for XSM architecture.)

:blue_circle: The owner of any data file preloaded into the system through xfs-interface is set to root and permission to open-access. Hence there is no access restriction to these files.