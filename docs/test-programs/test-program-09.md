---
title: 'Test Program 9'
hide:
  - navigation
---
**Input**

\-

**Output**

Out of 12 processes created, if N processes complete execution, then N data files each containing 100 consecutive integers (PID-3)\*100+1 to (PID-3)\*100+100 are created.

**Description :** The program will create a file with name "num.dat" with open permission. Integers 1 to 1200 are written to this file and file is closed. The program will then invoke _Fork_ system call four times, back to back to create 12 processes and Exec system call is invoked with file "pgm1.xsm". The program for "pgm1.xsm" is provided [here](./index.md#test-program-10).

```

int main()
{
decl
    int temp, fd, permission, iter, pid;
    string filename;
enddecl

begin
    filename="num.dat";
    permission=1;
    temp=exposcall("Create",filename,permission);
    fd=exposcall("Open",filename);
          
    if(fd>=0) then
        iter=1;
        while(iter<=1200) do
            temp=exposcall("Write",fd, iter);
            iter=iter+1;
        endwhile;    
        temp=exposcall("Close",fd);

        pid=exposcall("Fork");
        pid=exposcall("Fork");
        pid=exposcall("Fork");
        pid=exposcall("Fork");
        temp = exposcall("Exec","pgm1.xsm");
    else
        temp=exposcall("Write",-2, "OPEN FAIL");
    endif;
          
    return 0;
end
}
```
