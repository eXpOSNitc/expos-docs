---
title: 'Test Program 7 (Extended Shell)'
hide:
  - navigation
---
**Input**

Built in shell command/ Name of XSM executable file (String)

**Output**

Ouput of corresponding to shell command or executable file.

**Description :** Shell program given below reads command from console. If the command is halt, then program will invoke Shutdown system call. If the command is built in shell command, then shell will read suitable number of arguments from the console and corresponding system call is invoked from shell itself. If the command is an executable file, shell will fork and exec with the given executable file.

Note that the shell program should fit in 2 blocks/pages provided in [disk/memory organization](../os-implementation.md). The program given below is optimized to fits in 2 blocks/pages. In order to optimize the code, the program violates some of the type checkings. Even with type checking errors, the program will still compile and execute correctly. Also some system calls are invoked with arguments, even though the system call does not need any arguments. This will not cause any problem as these arguments will simply be ignored in the corresponding system call.


```

int main()
{
decl
    int temp, pid, a, flag, retcom;
    string input, username, password;
enddecl

begin
    a=1;
    while(a == 1) do
        temp = exposcall("Write",-2, "---Enter---");
        temp = exposcall("Read",-1, input);

        flag=0;
        if(input == "Logout" OR input == "Shutdown") then
            flag=1;
        endif;
              
        if(input == "Remusr" OR input == "Getuid" OR input == "Getuname") then
            flag=1;
            temp = exposcall("Read",-1, username);
        endif;
              
        if(input == "Newusr" OR input == "Setpwd") then
            flag=1;
            temp = exposcall("Read",-1, username);
            temp = exposcall("Read",-1, password);
        endif;
              
        if(flag==1) then
            retcom = exposcall(input, username, password);
            if(retcom < 0) then
                temp = exposcall("Write",-2, "BAD COMMAND");
            else
                if(input == "Getuid" OR input == "Getuname") then
                    temp = exposcall("Write",-2, retcom);
                endif;
            endif;
        else
            pid = exposcall("Fork");
            if(pid < 0) then
                temp = exposcall("Write",-2, "Fork Fail");
                continue;
            endif;
            
            if(pid != 0) then
                temp = exposcall("Wait",pid);
            else
                temp = exposcall("Exec",input);
                if(temp != 0) then
                    temp = exposcall("Write",-2, "BAD COMMAND");
                    break;
                endif;
            endif;
        endif;
    endwhile;
          
    return 0;
end
}
```
