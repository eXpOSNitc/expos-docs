---
title: 'Multiuser System Call'
original_url: 'http://eXpOSNitc.github.io/os_design-files/multiusersyscalls.html'
hide:
    - navigation
---



### Newusr
#### Arguments
User name, Password

#### Return Value:

|     |                                               |
| --- | --------------------------------------------- |
| 0   | Success                                       |
| -1  | User already exists                           |
| -2  | Permission denied                             |
| -3  | Number of users has reached the system limit. |


#### Description
This system call is used to create a new user. It checks whether the user already exists. If not, it creates a new user with the username and password specified. This system call can be executed only by the shell process of root user.

#### Algorithm:
<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 22, 
indicating that the process is in the newusr system call.

If the current user is not root, or if the current process is not the shell, return -2.

Loop through the <a href="../../os-design/disk-ds/#user-table">User Table</a> and exit returning -1 if an entry for the user already exists.

Find a free entry in the User Table. If no free entry is found, return -3.

Find the encrypted password by applying the <a href="../../arch-spec/instruction-set/">ENCRYPT</a> instruction on the input password.
Set the USERNAME and ENCRYPTED PASSWORD fields of the User Table entry.

Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry of the parent process to 0.

Return 0

</code></pre>

!!! note
	At each point of return from the system call, remember to reset the MODE FLAG.


### Remusr

#### Arguments
User name

#### Return Value

|     |                                    |
| --- | ---------------------------------- |
| 0   | Success                            |
| -1  | User does not exist                |
| -2  | Permission denied                  |
| -3  | Undeleted files exist for the user |


#### Description
This system call is used to remove an existing user. This system call can be executed from the shell proces of the root user. The root user and kernel cannot be removed. 

#### Algorithm

<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 23, 
indicating that the process is in the remuser system call.

If the current user is not root, or if the current process is not the shell, return -2.

If the user to be removed is the "root" or "kernel" return -2.

Loop through the <a href="../../os-design/disk-ds/#user-table">User Table</a> and find the entry curresponding to the user.
If the entry is not found, return -1.

Loop through the <a href="../../os-design/disk-ds/#root-file">Root File</a> and exit returning -3 if there are files of the user present on disk.

Invalidate the entry by setting the USERNAME and ENCRYPTED PASSWORD fields to -1.

Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry of the parent process to 0.

Return 0.

</code></pre>

!!! note
	At each point of return from the system call, remember to reset the MODE FLAG.

  
  
### Setpwd

#### Arguments
User name, Password

#### Return Value:

|     |                                         |
| --- | --------------------------------------- |
| 0   | Success                                 |
| -1  | Unauthorised attempt to change password |
| -2  | The user does not exist                 |


#### Description
This system call is used to change the password of an existing user. This system call can be exected only from the shell process. A user can set only his/her password. Root user can set any user's password. 

#### Algorithm:

<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 24, 
indicating that the process is in the setpwd system call.

If the current process is not the shell, return -1.

Loop through the <a href="../../os-design/disk-ds/#user-table">User Table</a> and finds the entry curresponding to the user name.
If entry is not found, return -2.

If (userid of the process is not equal to the userid of the user) {
	If (the current user is not root)) { 
		Return -1 
	}
}

Find the encrypted password by applying the <a href="../../arch-spec/instruction-set/">ENCRYPT</a> instruction on the input password.
Set the ENCRYPTED PASSWORD field in the user table entry.

Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry of the parent process to 0.

Return 0.
</code></pre>

!!! note
	At each point of return from the system call, remember to reset the MODE FLAG.



### Getuid

#### Arguments
User name

#### Return Value:

|                 |                  |
| --------------- | ---------------- |
| -1              | Invalid Username |
| User Identifier | Success          |


#### Description
If the username is valid, this system call returns the userid corresponding to the username. Otherwise, it returns -1.
The userid of a user is the index of the user table entry of the user.
  

#### Algorithm

<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 26, 
indicating that the process is in the getuid system call.

Loop through the <a href="../../os-design/disk-ds/#user-table">User Table</a>:
	If username is equal to USERNAME field of the entry
		return index of the entry

Return -1
</code></pre>

!!! note
	 At each point of return from the system call, remember to reset the MODE FLAG.

### Getuname

#### Arguments
User ID


#### Return Value

|           |                |
| --------- | -------------- |
| -1        | Invalid UserID |
| User Name | Success        |


#### Description
If the userid is valid, this system call returns the username corresponding to the userid. Otherwise, it returns -1.


#### Algorithm:


<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 25, 
indicating that the process is in the getuname system call.

If (UserID < 0 or UserID > 15)
	Return -1

If the user table entry curresponding to the userid is invalid, return -1.

Fetch the user name from the <a href="../../os-design/disk-ds/#user-table">User Table</a>.

Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry of the parent process to 0.
Return the username.
 
</code></pre>

!!! note
	At each point of return from the system call, remember to reset the MODE FLAG.

  
### Login

#### Arguments
User name, Password

#### Return Value 

|     |                              |
| --- | ---------------------------- |
| 0   | Success                      |
| -1  | Invalid username or password |
| -2  | Permission denied            |


#### Description
This system call is used to login a new user. It can be executed only from the login process. It verifies the user. Upon successful login, a new user process (shell) with the userid of the user specified is created. The calling process goes to sleep till the exit of the newly created shell process.
 

#### Algorithm:

<pre><code>
	Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 27, 
	indicating that the process is in the login system call.

	//Switch to the Kernel Stack. see <a href="../../os-design/stack-smcall/">kernel stack management during system calls</a>
	Save the value of SP to the USER SP field in the <a href="../../os-design/process-table/">Process Table</a> entry of the process.
	Set the value of SP to the beginning of User Area Page.

	If PID of the current process is not 1, return -2. 	/* Login process has PID = 1 */

	Get the <a href="../../os-design/disk-ds/#user-table">User Table</a> entry curresponding to the username.
	If an entry does not exist, return -1.

	Use the <a href="../../support-tools/spl/">ecrypt statement</a> to encrypt the password supplied as input.

	If the encypted input password does not match the ENCRYPTED PASSWORD field in the user table entry, return -1.

	In the process table entry for the shell process, set STATE as CREATED and USERID as that of the user who is logging in.

	Set the state of the current process in it's process table entry as (WAIT_PROCESS, 2) /* Login waits for shell to exit */

        In <a href="../../os-design/mem-ds/#system-status-table" target="_blank">system status table</a>, set the CURRENT_USER_ID as that of the user who is logging in.

	Invoke the <b>context_switch()</b> function in the <a href="../../modules/module-05/">Scheduler Module</a>.

	Reset the MODE_FLAG and restore SP to user stack.
	ireturn;

</code></pre>

!!! note
	At each point of return from the system call, remember to reset the MODE FLAG.


!!! question
	Login process does not load the shell process, but sets it's state to CREATED. Can it happen that the shell is not present in memory?



### Logout

#### Arguments
None

#### Return Value
-1 on error, otherwise does not return


#### Description
This system call is used to logout the current user. It can be invoked only from the shell process (PID = 2). When the logout system call is invoked, all running processes of the current user are terminated and all resources released. Idle and init/Login will be the only processes running after the execution of Logout. Login process is woken up at the end of logout.


![](../assets/img/roadmap/logout.png)
  

Control flow diagram for *Logout* system call

  
  

#### Algorithm
<pre><code>
Set the MODE_FLAG in the <a href="../../os-design/process-table/">process table</a> entry to 28, 
indicating that the process is in the logout system call.
	
//Switch to the Kernel Stack. see <a href="../../os-design/stack-smcall/">kernel stack management during system calls</a>
Save the value of SP to the USER SP field in the <a href="../../os-design/process-table/">Process Table</a> entry of the process.
Set the value of SP to the beginning of User Area Page.

If the current process is not the shell, return -1.	/* <a href="../../os-design/misc/#shell">Shell process</a> has the PID 2 */

Kill all user processes except the shell by calling the <b>kill_all()</b> function in the <a href="../../modules/module-01/">Process Manager</a> module.

Set the STATE of the current process(shell) in the process table to TERMINATED.

/* Shell should be set ready to run when the next user logs in. */
Obtain the entry point IP value from the header of the shell program. Place it in the beginning (logical addesss 4096) 
of the stack of the shell(current process). Reset the USERSP field of the shell to 4096.

Wake up the Login process by changing STATE in it's process table entry to READY.

In <a href="../../os-design/mem-ds/#system-status-table" target="_blank">system status table</a>, reset the CURRENT_USER_ID field back to 0 (kernel).

Invoke the <b>context_switch()</b> function in the <a href="../../modules/module-05/">Scheduler Module</a>.

</code></pre>

!!! note
	At each point of return from the system call, remember to reset the MODE FLAG and switch back to the user stack.


  

!!! question
	Why don't we kill the current process (shell) by using the exit\_process() module function?












































