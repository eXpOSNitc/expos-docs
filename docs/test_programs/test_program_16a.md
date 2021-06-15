---
title: 'merge.expl (Test Program 16 - Merge Sort with Files)'
---
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
