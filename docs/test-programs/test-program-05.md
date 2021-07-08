---
title: 'Test Program 5'
hide:
  - navigation
---
**Input**

Name of a data file (String)

**Output**

Content of the given file

**Description :** The program takes names of data files as input and opens the file first. It then forks to create a child process. The content of the file with shared open instance (shared LSEEK) will be printed to the terminal concurrently by parent and child. To synchronize the use open instance between parent and child a semaphore is used.


```

decl
    int i, semid, pid, data, temp, filedis, a;
    string filename;
enddecl

int main()
{
begin
    temp = exposcall("Read",-1,filename);
    filedis = exposcall("Open", "numbers.dat");
    semid = exposcall("Semget");

    pid = exposcall("Fork");
    a = 0;
    data = -1;
    if(pid > 0) then
        while(a != -2)  do
            temp = exposcall("SemLock", semid);
            a = exposcall("Read",filedis,data);
            temp = exposcall("Write",-2,data);
            temp = exposcall("SemUnLock", semid);
        endwhile;
        
        temp = exposcall("Semrelease", semid);
    else
        while(a != -2)  do
            temp = exposcall("SemLock", semid);
            a = exposcall("Read",filedis,data);
            temp = exposcall("Write",-2,data);
            temp = exposcall("SemUnLock", semid);
        endwhile;

        temp = exposcall("Semrelease", semid);
    endif;
    
    return 0;
end
}
```
