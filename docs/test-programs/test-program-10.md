---
title: 'Test Program 10'
hide:
  - navigation
---
**Input**

\-

**Output (For each 12 proceesses)**

A file will be created containing 100 consecutive numbers (PID-3)\*100+1 to (PID-3)\*100+100

**Description :** This program can not be run individualy. The test program 9 will invoke Exec with below given program with name "pgm1.xsm". Make sure to compile and save this program as "pgm1.xsm". Below given program will create a new file according to the PID of the process and read 100 numbers from file "num.dat" from offset (PID-3)\*100 to (PID-3)\*100+99 and write to newly created file. After successful execution, there should be 12 data files each containing 100 consecutive numbers (PID-3)\*100+1 to PID-3)\*100+100.

```

int main()
{
decl
    int temp, fdread, fdwrite, permission, pid, offset, data, iter;
    string filename;
enddecl

begin
    pid=exposcall("Getpid");
    if(pid==3) then
        filename="3.dat";
    endif;
    if(pid==4) then
        filename="4.dat";
    endif;
    if(pid==5) then
        filename="5.dat";
    endif;
    if(pid==6) then
        filename="6.dat";
    endif;
    if(pid==7) then
        filename="7.dat";
    endif;
    if(pid==8) then
        filename="8.dat";
    endif;
    if(pid==9) then
        filename="9.dat";
    endif;
    if(pid==10) then
        filename="10.dat";
    endif;
    if(pid==11) then
        filename="11.dat";
    endif;
    if(pid==12) then
        filename="12.dat";
    endif;
    if(pid==13) then
        filename="13.dat";
    endif;
    if(pid==14) then
        filename="14.dat";
    endif;

    permission=1;
    temp=exposcall("Create",filename,permission);
    fdwrite=exposcall("Open",filename);
    fdread=exposcall("Open","num.dat");
          
    if(fdread>=0 AND fdwrite>=0) then
        offset=(pid-3)*100;
        temp=exposcall("Seek",fdread,offset);

        iter=0;
        while(iter<100) do
            temp=exposcall("Read", fdread, data);
            temp=exposcall("Write", fdwrite, data);
            iter=iter+1;
        endwhile;

        temp=exposcall("Close", fdread);
        temp=exposcall("Close", fdwrite);
    else
        temp=exposcall("Write", -2, "OPEN FAIL");
    endif;
          
    return 0;
end
}
```
