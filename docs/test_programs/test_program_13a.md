---
title: 'Test Program 13 (parent.expl)'
---
```

int main()
{
    decl
        int temp,pid;
    enddecl

    begin
        pid = exposcall("Fork");
        pid = exposcall("Fork");
        pid = exposcall("Fork");

        if(pid==-1) then
            temp=exposcall("Write", -2, "Fork Error");
        else
            temp=exposcall("Write", -2, pid);
        endif;

        temp = exposcall("Exec", "child.xsm");
        return 0;
    end
}
```
