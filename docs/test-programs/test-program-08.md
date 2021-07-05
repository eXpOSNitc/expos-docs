---
title: 'Test Program 8'
hide:
  - navigation
---
```

decl
    int temp, data, pid, count, delay;
    int delayFunc(int delay);
enddecl

int delayFunc(int delay)
{
decl
    int num;
enddecl

begin
    num = 0;
    while(num < delay) do
        num = num + 1;
    endwhile;

    return 0;
end
}

int main()
{
begin
    read(delay);

    pid = exposcall("Fork");
    pid = exposcall("Fork");
    pid = exposcall("Fork");
    pid = exposcall("Fork");

    if(pid < 0) then
        write("No PCB");
    endif;

    pid = exposcall("Getpid");
    count = 0;

    while(count < 8) do
        data = pid*100 + count;
        write(data);
        temp = delayFunc(delay);

        count = count + 1;
    endwhile;

    return 0;
end
}
```
