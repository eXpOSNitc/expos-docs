---
title: 'Test Program 2'
hide:
  - navigation
---
**Input**

An integer N and N integers.

**Output**

N integers entered in the input.

**Description :** The program given below implements a linked list for integers. The program reads an integer N from the console. It then creates a linked list and inserts N integers entered from console into the linked list in the same order. The program traverses the linked list and prints data to the console.

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
enddecl
            
int main()
{
decl
    int length, x, temp;
    List p, q;
enddecl
            
begin
    x = exposcall("Heapset");
    head=null;
    x = exposcall("Read",-1,length);
    q = head;
                      
    while (length!=0)  do
        temp = exposcall("Read",-1,x);
        p= exposcall("Alloc",2);
        p.data=x;
        p.next=null;
            
        if (head == null) then
            head=p;
            q=p;
        else
            q.next=p;
            q=q.next;
        endif;
                    
        length=length-1;
    endwhile;
                      
    p=head;
    while(p!=null)  do
        x=p.data;
        temp= exposcall("Write",-2,x);
        p=p.next;
    endwhile;
    
    return 0;
    end
}
```
