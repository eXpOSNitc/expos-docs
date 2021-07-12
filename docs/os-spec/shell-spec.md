---
title: 'eXpOS Shell specification'
original_url: 'http://eXpOSNitc.github.io/os_spec-files/shell_spec.html'
hide:
    - navigation
---


The eXpOS shell program is designed to repeatedly ask for user commands and execute the command specified by the user. There are two types of commands that the user can input to the shell:


### Built in Shell commands

Built in shell commands are 

1. `Newusr` (to create a new user)
2. `Remusr` (to remove a user), 3)
3. `Setpwd` (set the password of a user)
4. `Getuid` (to get the user-id of the currently logged in user)
5. `Getuname` (to get the username of the currently logged in user)
6. `Logout` (logout the current user)
7. `Shutdown` (to shutdown the system after committing back the memory copies of all disk data structures into the disk).

To execute the system call for the corresponding shell command - eg : For the system call Newusr, enter the string "Newusr" (without quotes) from the console.

Upon receipt of one of these commands, the shell directly asks the user for the input arguments for the corresponding system call (for example \- setpwd requires the username and the new password to be entered) and invokes the corresponding system call directly to execute the command. In all the above cases except logout and shutdown, the shell continues to ask the user for the next command after execution of the system call. If the executed system call for the input command is not successful, then shell simply prints "BAD COMMAND".


### Executable commands/filenames

An executable command is essentially the name of an executable file. In such case, shell first spawns a child using the Fork system call and the parent (shell) waits for the child to do an Exit upon completion of command execution. The child runs the input file using the Exec system call. If Exec fails, then child prints “BAD COMMAND” and executes the Exit system call to activate the shell again.

eXpOS specifies that some standard executable programs called (**system utilities**) are supplied to the user along with the OS implementation. These programs essentially help the user to manipulate files using the shell. They are listed below:

#### List all files
 -   _Command_ : **ls.xsm**
 -   _Input_ : **\-**
 -   _Semantics_ : Displays the names of all the files present in the disk.
#### Remove a File
-   _Command_ : **rm.xsm**
-   _Input_ : filename
-   _Semantics_ : Removes a data file _filename_ from the disk.
#### Copy content of one file to another
-   _Command_ : **cp.xsm**
-   _Input_ : filename1, filename2
-   _Semantics_ : Copies the word to word data from a file _filename1_ to the file _filename2_. (_filename1_ can be only data or root file.)
#### Print the content of a file
-   _Command_ : **cat.xsm**
-   _Input_ : filename
-   _Semantics_ : Displays the content of the file _filename_.
#### List all users
-   _Command_ : **lu.xsm**
-   _Input_ : **\-**
-   _Semantics_ : Displays the names of all the users in the system.
#### Remove all files owned by a user
-   _Command_ : **ru.xsm**
-   _Input_ : username
-   _Semantics_ : Deletes all the data files owned by the user with name _username_. (Typically it is executed from the root user to delete all the files owned by a user before removing the user from the system.)

A sample shell implementation is given [here](../test-programs/index.md#test-program-7-extended-shell). The details of implementation of system utilities are left to the OS programmer. Since eXpOS ABI does not support command line arguments, these programs may need to ask the user for inputs (like _filename_ in the case of the _cat_ command) using the _Read_ system call.

The eXpOS specification stipulates that shell always executes from the context of the currently logged in user. The shell is spawned by the [login process](../os-design/misc.md#initlogin-process).