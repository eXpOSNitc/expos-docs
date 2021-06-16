---
title: 'Test Program 13'
hide:
    - navigation
---

### `parent.expl`
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

### `child.expl`

```
type
    List
    {
        int data;
        List next;
    }
endtype

decl
    List head, p, q;
enddecl

int main()
{
decl
    int x, temp, pid, counter;
enddecl

begin
    x = initialize();
    pid = exposcall("Getpid");

    head=null;
    counter=0;
    while(counter<10) do
        p=alloc();
        p.data=pid*100 + counter;
        p.next=null;

        if(head==null) then
            head=p;
            q=p;
        else
            q.next=p;
            q=q.next;
        endif;

        counter=counter+1;
    endwhile;

    p=head;
    while(p!=null) do
        write(p.data);
        p=p.next;
    endwhile;

    return 0;
end
}
```

