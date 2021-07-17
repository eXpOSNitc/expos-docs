---
title: 'Test Program 12'
hide:
  - navigation
---

**Input**

\-

**Output (For each 12 proceesses)**

A file will be created containing 100 consecutive numbers from data file "numbers.dat".

**Description :** This program can not be run individualy. Test program 11 will invoke Exec with below given program with name "pgm2.xsm". Make sure to compile and save this program as "pgm2.xsm". Below given program will create a new file according to the PID of the process and read 100 numbers from file "numbers.dat" from offset (PID-3)\*100 to (PID-3)\*100+99 and write to newly created file. After successful execution, there should be 12 data files each containing 100 numbers each X\*1000 -X\*1000+99, where X=\[3,4..14\]. The numbers written by a process in the newly created file need not be the same numbers the process has written in "numbers.dat" file.

```

decl
    int data;
    int fdread, fdwrite, temp, permission, offset, pid, iter;
    string filename, newfile;
enddecl

int main()
{
begin
    fdread=exposcall("Open", "numbers.dat");
          
    pid=exposcall("Getpid");
    if(pid==3) then
        newfile="three.dat";
    endif;
    if(pid==4) then
        newfile="four.dat";
    endif;
    if(pid==5) then
        newfile="five.dat";
    endif;
    if(pid==6) then
        newfile="six.dat";
    endif;
    if(pid==7) then
        newfile="seven.dat";
    endif;
    if(pid==8) then
        newfile="eight.dat";
    endif;
    if(pid==9) then
        newfile="nine.dat";
    endif;
    if(pid==10) then
        newfile="ten.dat";
    endif;
    if(pid==11) then
        newfile="eleven.dat";
    endif;
    if(pid==12) then
        newfile="twelve.dat";
    endif;
    if(pid==13) then
        newfile="thirteen.dat";
    endif;
    if(pid==14) then
        newfile="fourteen.dat";
    endif;
          
    temp=exposcall("Create", newfile, 1);
    fdwrite=exposcall("Open", newfile);
    if(fdread>=0 AND fdwrite>=0) then
        offset=(pid-3)*100;
        temp=exposcall("Seek",fdread, offset);
              
        iter=0;
        while(iter<=99) do
            temp=exposcall("Read",fdread, data);
            temp=exposcall("Write",fdwrite, data);
            iter=iter+1;
        endwhile;
              
        temp=exposcall("Close",fdread);
        temp=exposcall("Close",fdwrite);
    else
        temp=exposcall("Write",-2, "OPEN FAIL");
    endif;

    return 0;
end
}
```
