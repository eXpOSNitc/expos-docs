---
title: 'Test Program 13'
hide:
    - navigation
---

**Input**

\-

**Output (For each 8 processes with PID = 2 to 9)**

Return values from Fork system call and integers from PID\*100 to PID\*100+9.

**Description :** This program calls fork 3 times creating 8 child processes. Each process prints the value returned from the last Fork system call and Exec system call is invoked with file "child.xsm". The "child.xsm" program stores numbers from PID\*100 to PID\*100+9 onto a linked list and prints them to the console.


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

