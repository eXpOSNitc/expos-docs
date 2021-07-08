---
title: 'Test Program 16 - Merge Sort with Files'
hide:
  - navigation
---

**Input**

\-

**Output**

Creates a file _merge.dat_ with numbers from 1 to 512 and also prints them.

**Description :** The first ExpL program, _merge.expl_, first stores numbers from 1 to 512 in a random order into a file _merge.dat_. It then forks and executes _m\_store.expl_ which creates 8 files _temp{i}.dat_, where i=1..8 and stores 64 numbers each from _merge.expl_. Then, all the temporary files are sorted by executing _m\_sort.expl_. Next, the first ExpL program forks and executes _m\_merge.expl_ which merges all the temporary files back into _merge.dat_ and finally, prints the contents from 1 to 512 in ascending order.

### `merge.expl`
```
int main()
{
decl
  int x, fp, counter, word, a, pid;
enddecl

begin
  x=initialize();

  x=exposcall("Create", "merge.dat", 1);
  fp=exposcall("Open", "merge.dat");

  counter=0;
  while(counter<512) do
    word=512-counter;
    x=exposcall("Write", fp, word);
    counter=counter+1;
  endwhile;

  write("Created");

  pid=exposcall("Fork");
  if(pid!=0) then
    x=exposcall("Wait", pid);
  else
    x=exposcall("Exec", "m_store.xsm");
  endif;

  pid=exposcall("Fork");
  if(pid!=0) then
    x=exposcall("Wait", pid);
  else
    x=exposcall("Exec", "m_merge.xsm");
  endif;

  a=exposcall("Seek", fp, 0);
  a=exposcall("Read", fp, word);
  while(a!=-2) do
    write(word);
    a=exposcall("Read", fp, word);
  endwhile;

  x=exposcall("Close", fp);
  return 1;
end
}
```

### `m_store.expl`
```
decl
  int store(str file, int start);
enddecl

int store(str file, int start)
{
  decl
    int x, fp, fp1, a, word, counter;
  enddecl

  begin
    x=exposcall("Create", file, 1);
    fp=exposcall("Open", "merge.dat");
    fp1=exposcall("Open", file);

    x=exposcall("Seek", fp, start);

    counter=0;
    a=exposcall("Read", fp, word);
    while(a!=-2 AND counter<64) do
      x=exposcall("Write", fp1, word);
      a=exposcall("Read", fp, word);
      counter=counter+1;
    endwhile;

    x=exposcall("Close", fp);
    x=exposcall("Close", fp1);
    return 0;
  end
}

int main()
{
decl
  int x, pid, pid1, pid2;
  str file;
enddecl

begin
  x=initialize();

  pid=exposcall("Fork");
  if(pid!=0) then
    while(pid<13) do
      x=exposcall("Wait", pid);
      pid=pid+1;
    endwhile;
  else
    x=exposcall("Fork");
    x=exposcall("Fork");
    x=exposcall("Fork");

    pid=exposcall("Getpid");

    if(pid==5) then
      file="temp1.dat";
    endif;
    if(pid==6) then
      file="temp2.dat";
    endif;
    if(pid==7) then
      file="temp3.dat";
    endif;
    if(pid==8) then
      file="temp4.dat";
    endif;
    if(pid==9) then
      file="temp5.dat";
    endif;
    if(pid==10) then
      file="temp6.dat";
    endif;
    if(pid==11) then
      file="temp7.dat";
    endif;
    if(pid==12) then
      file="temp8.dat";
    endif;

    pid=(pid-5)*64;
    x=store(file, pid);
    x=exposcall("Exit");
  endif;

  write("Stored");

  pid=exposcall("Fork");
  if(pid!=0) then
    while(pid<13) do
      x=exposcall("Wait", pid);
      pid=pid+1;
    endwhile;
  else
    x=exposcall("Fork");
    x=exposcall("Fork");
    x=exposcall("Fork");

    x=exposcall("Exec", "m_sort.xsm");
  endif;

  write("Sorted");

  return 1;
end
}
```

### `m_sort.expl`

```
type
  List
  {
    int data;
    List next;
  }
  Share
  {
    List link;
  }
endtype

decl
  int x, semid, fp;
  List head;
  List mergeSort(List top);
  List merge(List a, List b);
enddecl

List mergeSort(List top)
{
  decl
    int pid;
    List slow, fast, a, b;
    Share s;
  enddecl

  begin
    if((top!=null) AND (top.next!=null)) then
      slow=top;
      fast=top.next;

      while(fast!=null) do
        fast=fast.next;
        if(fast!=null) then
            slow=slow.next;
            fast=fast.next;
        endif;
      endwhile;

      a=top;
      b=slow.next;
      slow.next=null;

      a=mergeSort(a);
      b=mergeSort(b);

      top=merge(a, b);
    endif;

    return top;
  end
}

List merge(List a, List b)
{
  decl
    List result;
  enddecl

  begin
    result=null;

    if(a==null) then
      result=b;
    endif;
    if(b==null) then
      result=a;
    endif;

    if(a!=null AND b!=null) then
      if(a.data<=b.data) then
        result=a;
        result.next=merge(a.next, b);
      else
        result=b;
        result.next=merge(a, b.next);
      endif;
    endif;

    return result;
  end
}

int main()
{
  decl
    int x, counter, pid, fp, a, word;
    str file;
    List p, q;
  enddecl

  begin
    x=initialize();
    semid=exposcall("Semget");
    pid=exposcall("Getpid");

    if(pid==5) then
      file="temp1.dat";
    endif;
    if(pid==6) then
      file="temp2.dat";
    endif;
    if(pid==7) then
      file="temp3.dat";
    endif;
    if(pid==8) then
      file="temp4.dat";
    endif;
    if(pid==9) then
      file="temp5.dat";
    endif;
    if(pid==10) then
      file="temp6.dat";
    endif;
    if(pid==11) then
      file="temp7.dat";
    endif;
    if(pid==12) then
      file="temp8.dat";
    endif;

    fp=exposcall("Open", file);

    head=null;
    counter=0;
    a=exposcall("Read", fp, word);
    while(counter<64) do
      p=alloc();
      p.data=word;
      p.next=null;

      if(head==null) then
        head=p;
        q=p;
      else
        q.next=p;
        q=q.next;
      endif;

      a=exposcall("Read", fp, word);
      counter=counter+1;
    endwhile;

    head=mergeSort(head);

    x=exposcall("Seek", fp, 0);
    p=head;
    while(p!=null) do
      word=p.data;
      x=exposcall("Write", fp, word);
      p=p.next;
    endwhile;

    x=exposcall("Close", fp);
    x=exposcall("Semrelease");
    pid=exposcall("Getpid");
    x=pid+1;
    while(x<13) do
    	a=exposcall("Wait",x);
    	x=x+1;
    endwhile;
    return 1;
  end
}
```

### `m_merge.expl `
```
decl
  int merge(str out, str in1, str in2);
enddecl

int merge(str out, str in1, str in2)
{
  decl
    int fp, fp1, fp2;
    int x, a, b, w1, w2;
  enddecl

  begin
    x=exposcall("Create", out, 1);
    fp=exposcall("Open", out);

    fp1=exposcall("Open", in1);
    fp2=exposcall("Open", in2);

    a=exposcall("Read", fp1, w1);
    b=exposcall("Read", fp2, w2);

    while(a!=-2 AND b!=-2) do
      if(w1<=w2) then
        x=exposcall("Write", fp, w1);
        a=exposcall("Read", fp1, w1);
      else
        x=exposcall("Write", fp, w2);
        b=exposcall("Read", fp2, w2);
      endif;
    endwhile;

    while(a!=-2) do
      x=exposcall("Write", fp, w1);
      a=exposcall("Read", fp1, w1);
    endwhile;

    while(b!=-2) do
      x=exposcall("Write", fp, w2);
      b=exposcall("Read", fp2, w2);
    endwhile;

    x=exposcall("Close", fp);
    x=exposcall("Close", fp1);
    x=exposcall("Close", fp2);

    x=exposcall("Delete", in1);
    x=exposcall("Delete", in2);

    return 0;
  end
}

int main()
{
decl
  int x, pid, pid1, pid2;
enddecl

begin
  x=initialize();

  pid1=exposcall("Fork");
  if(pid1!=0) then
    pid2=exposcall("Fork");
    if(pid2!=0) then
      x=merge("temp12.dat", "temp1.dat", "temp2.dat");
      x=exposcall("Wait", pid2);
    else
      x=merge("temp34.dat", "temp3.dat", "temp4.dat");
      x=exposcall("Exit");
    endif;
    x=merge("temp14.dat", "temp12.dat", "temp34.dat");
    x=exposcall("Wait", pid1);
  else
    pid2=exposcall("Fork");
    if(pid2!=0) then
      x=merge("temp56.dat", "temp5.dat", "temp6.dat");
      x=exposcall("Wait", pid2);
    else
      x=merge("temp78.dat", "temp7.dat", "temp8.dat");
      x=exposcall("Exit");
    endif;
    x=merge("temp58.dat", "temp56.dat", "temp78.dat");
    x=exposcall("Exit");
  endif;

  x=merge("merge.dat", "temp14.dat", "temp58.dat");

  write("Merged");

  return 1;
end
}
```
