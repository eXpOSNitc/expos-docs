---
title: 'Test Program 4 (Reader-Writer Program)'
hide:
  - navigation
---

**Input**

\-

**Output**

Integers from 1 to 100, but not necessarily in sequential order.

**Description :** The reader-writer program provides below has two writers and one reader. The parent process will create two child processes by invoking _fork_. The parent and two child processes share a buffer of one word. At a time only one process can read/write to this buffer. To acheive this, these three processes use a shared semaphore. A writer process can write to the buffer if it is empty and the reader process can only read from the buffer if it is full. Before the word in the buffer is overwritten the reader process must read it and print the word to the console. The parent process is the reader process and its two children are writers. One child process writes even numbers from 1 to 100 and other one writes odd numbers from 1 to 100 to the buffer. The parent process reads the numbers and prints them on to the console.


```

type
Share
{
  int isempty;
  int data;
}
endtype

decl
  Share head;
enddecl

int main()
{
decl
  int temp, x, pidone, pidtwo, semid, iter, counter;
enddecl

begin
  x = exposcall("Heapset");
  semid = exposcall("Semget");
  head = exposcall("Alloc", 2);
  head.isempty = 1;
  pidone = exposcall("Fork");

  if (pidone == 0) then
    iter = 1;
    while(iter <= 100) do
      temp = exposcall("SemLock", semid);
      temp = head.isempty;

      if(temp == 1) then
        head.data = iter;
        head.isempty = 0;
        iter = iter + 2;
      endif;

      temp = exposcall("SemUnLock", semid);

      counter = 0;
      while(counter < 50) do
        counter = counter + 1;
      endwhile;
    endwhile;
  else
    pidtwo =  exposcall("Fork");

    if(pidtwo == 0) then
      iter = 2;
      while(iter <= 100) do
        temp = exposcall("SemLock", semid);
        temp = head.isempty;

        if(temp == 1) then
          head.data = iter;
          head.isempty = 0;
          iter = iter + 2;
        endif;
        
        temp = exposcall("SemUnLock", semid);
      endwhile;
    else
      iter = 1;
      while(iter <= 100) do
        temp = exposcall("SemLock", semid);
        temp = head.isempty;

        if(temp == 0) then
          x = head.data;
          head.isempty = 1;
          temp = exposcall("Write", -2, x);
          iter = iter + 1;
        endif;

        temp = exposcall("SemUnLock", semid);
      endwhile;
    endif;
  endif;

  temp = exposcall("Semrelease", semid);
  return 0;
end
}
```
