---
title: 'Test Program 3'
---
```

type
List
{
    int data;
    List next;
}
endtype
            
decl
    List head;
    int x, pid, temp, length;
enddecl
            
int main()
{
decl
    List p, q;
    int i;
enddecl
            
begin
    temp = exposcall("Heapset");
    head = null;
    q = head;

    length=1;
    while (length <= 100)  do
        p = exposcall("Alloc",2);
        p.data = length;
        p.next = null;
        
        if (head == null) then
            head = p;
            q = p;
        else
            q.next = p;
            q = q.next;
        endif;
                          
        length = length+1;
    endwhile;
                      
    pid = exposcall("Fork");
    if(pid == 0) then
        p = head;
        while(p != null)  do
            x = p.data;
            temp = exposcall("Write",-2,x);
            p = p.next;
            if(p == null) then
                break;
            endif;
            p = p.next;
        endwhile;
    else
        q = head.next;
        while(q != null)  do
            x = q.data;
            temp = exposcall("Write",-2,x);
            q = q.next;
            if(q == null) then
                break;
            endif;
            q = q.next;
        endwhile;
    endif;
                
    return 0;
end
}
```
