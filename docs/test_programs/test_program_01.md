---
title: 'Test Program 1 (Shell version-II without multiuser)'
---

```
int main()
{
decl
    int temp, pid, a;
    string input;
enddecl
begin
    a=1;
    while(a == 1) do
        temp = exposcall("Write",-2,"---Enter---");
        temp = exposcall("Read",-1, input);
        if(input != "Shutdown") then
            pid = exposcall("Fork");
            if(pid < 0) then
                temp = exposcall("Write",-2, "Fork Failure");
                continue;
            endif;
            if(pid != 0) then
                temp = exposcall("Wait",pid);
            else
                temp = exposcall("Exec",input);
                if(temp != 0) then
                    temp = exposcall("Write",-2, "BAD COMMAND");
                    break;
                endif;
            endif;
        else
            temp = exposcall("Shutdown");
            break;
        endif;
    endwhile;
    return 0;
end
}
```