---
title: 'Test Program 6'
hide:
  - navigation
---
**Input**

A file name (String) and permission (Integer)

**Output**

Integers from 1 to 100, but not necessarily in sequential order.

**Description :** The program takes a file name and permission as input and creates a new file with given inputs. It then forks to create two child processes. Similar to Reader-Writer program seen before, the two child processes act as writers and parent as reader. A file open instances is shared between two writers and there is separate open instance of the same file for reader. Two writers will write numbers from 1 to 100 to file - one writer will write even numbers other will write odd numbers and reader will read from the file and print to the console concurrently. To synchronize the use of the shared open instance between two writers a semaphore is used.


```

int main()
{
decl
    int temp, x, a, pidone, pidtwo, semid, iter, data, permission, fd;
    string filename;
enddecl

begin
    temp=exposcall("Read",-1,filename);
    temp=exposcall("Read",-1,permission);
    temp=exposcall("Create",filename, permission);

    pidone = exposcall("Fork");
    if (pidone != 0 ) then
        fd=exposcall("Open",filename);
        iter=1;
        while(iter <= 100) do
            a=exposcall("Read",fd, data);
            if(a!=-2) then
                temp=exposcall("Write",-2, data);
                iter=iter+1;
            endif;
        endwhile;
    else
        semid = exposcall("Semget");
        fd=exposcall("Open",filename);

        pidtwo =  exposcall("Fork");
        if(pidtwo == 0) then
            iter = 1;
            while(iter <= 100) do
                temp = exposcall("SemLock", semid);
                temp=exposcall("Write",fd, iter);
                temp = exposcall("SemUnLock", semid);
                iter=iter+2;
            endwhile;
        else
            iter = 2;
            while(iter <= 100) do
                temp = exposcall("SemLock", semid);
                temp=exposcall("Write",fd, iter);
                temp = exposcall("SemUnLock", semid);
                iter=iter+2;
            endwhile;
        endif;
        
        temp = exposcall("Semrelease", semid);
    endif;
    
    return 0;
end
}
```
