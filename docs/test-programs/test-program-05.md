---
title: 'Test Program 5'
hide:
  - navigation
---
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
