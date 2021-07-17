---
title: 'Test Program 11'
hide:
  - navigation
---
**Input**

\-

**Output**

Out of 12 processes created, if N processes complete execution, then N data files each containing 100 consecutive integers from X\*1000+1 to X\*1000+100 (where X ∈ {3,4..14}) are created.

**Description :** The program will create a file with name "numbers.dat" with open permission and open the file. The program also invokes Semget to acquire a shared semaphore. The program will then invoke _Fork_ system call four times, back to back to create 12 processes. The 12 processes now share a file open instance and a semaphore. Each process will write 100 numbers consecutatively (PID\*1000+1 to PID\*1000+100) to the file "numbers.dat". Exec system call is invoked with file "pgm2.xsm". The program for "pgm2.xsm" is provided [here](./index.md#test-program-12){ target=_blank }.

```

decl
    int fd, temp, permission, data, semid, iter, pid, endval, count;
    string filename;
enddecl

int main()
{
begin
    filename="numbers.dat";
    permission=1;
    temp = exposcall("Create",filename, permission);
    semid = exposcall("Semget");
    
    fd=exposcall("Open",filename);
    if(fd>=0) then
        pid=exposcall("Fork");
        pid=exposcall("Fork");
        pid=exposcall("Fork");
        pid=exposcall("Fork");
            
        if(pid<0) then
            temp=exposcall("Write", -2, "NO PCB");
        endif;
            
        pid=exposcall("Getpid");
        data=pid*1000+1;
        endval=data+99;
        temp=exposcall("SemLock", semid);
        
        while(data<=endval) do
            temp=exposcall("Write", fd, data);
            data=data+1;
        endwhile;
            
        temp=exposcall("SemUnLock", semid);
        temp=exposcall("Close", fd);
    else
        temp=exposcall("Write", -2, "OPEN FAIL");
    endif;
        
    temp=exposcall("Exec", "pgm2.xsm");
    return 0;
end
}
```
