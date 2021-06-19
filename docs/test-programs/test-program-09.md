---
title: 'Test Program 9'
---
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
