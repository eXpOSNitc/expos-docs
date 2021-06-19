---
title: "Test Programs"
original_url: https://exposnitc.github.io/test_prog.html
hide: 
    - navigation
---

## Test Program 1 (Shell version-II without multiuser) 
  

**Input**

Executable file name/string "Shutdown"

**Output**

Executes given xsm program/halt system if input is "Shutdown"

**Description :** shell version II without the multiuser

  
The code for the test program can be found [here](./test_program_01.md)

  
  

---

  
  
## Test Program 2
  

**Input**

An integer N and N integers.

**Output**

N integers entered in the input.

**Description :** The program given below implements a linked list for integers. The program reads an integer N from the console. It then creates a linked list and inserts N integers entered from console into the linked list in the same order. The program traverses the linked list and prints data to the console.

  
The code for the test program can be found [here](./test_program_02.md)

  
  

---

  
  
## Test Program 3
  

**Input**

\-

**Output**

Integers 1 to 100, not necessarily in the order.

**Description :** The program creates a linked list with numbers 1 to 100 in them. The program invokes fork to create a child process. The parent and the child process reads from the shared linked list with different pointers and prints the data read to the console. Parent process prints the even numbers 2, 4, 6, 8.. and child process prints 1, 3, 5 ..

  
The code for the test program can be found [here](./test_program_03.md)

  
  

---

  
  
## Test Program 4 (Reader-Writer Program) 
  

**Input**

\-

**Output**

Integers from 1 to 100, but not necessarily in sequential order.

**Description :** The reader-writer program provides below has two writers and one reader. The parent process will create two child processes by invoking _fork_. The parent and two child processes share a buffer of one word. At a time only one process can read/write to this buffer. To acheive this, these three processes use a shared semaphore. A writer process can write to the buffer if it is empty and the reader process can only read from the buffer if it is full. Before the word in the buffer is overwritten the reader process must read it and print the word to the console. The parent process is the reader process and its two children are writers. One child process writes even numbers from 1 to 100 and other one writes odd numbers from 1 to 100 to the buffer. The parent process reads the numbers and prints them on to the console.

  
The code for the test program can be found [here](./test_program_04.md)

  
  

---

  
  
## Test Program 5
  

**Input**

Name of a data file (String)

**Output**

Content of the given file

**Description :** The program takes names of data files as input and opens the file first. It then forks to create a child process. The content of the file with shared open instance (shared LSEEK) will be printed to the terminal concurrently by parent and child. To synchronize the use open instance between parent and child a semaphore is used.

  
The code for the test program can be found [here](./test_program_05.md)

  
  

---

  
  
## Test Program 6
  

**Input**

A file name (String) and permission (Integer)

**Output**

Integers from 1 to 100, but not necessarily in sequential order.

**Description :** The program takes a file name and permission as input and creates a new file with given inputs. It then forks to create two child processes. Similar to Reader-Writer program seen before, the two child processes act as writers and parent as reader. A file open instances is shared between two writers and there is separate open instance of the same file for reader. Two writers will write numbers from 1 to 100 to file - one writer will write even numbers other will write odd numbers and reader will read from the file and print to the console concurrently. To synchronize the use of the shared open instance between two writers a semaphore is used.

  
The code for the test program can be found [here](./test_program_06.md)

  
  

---

  
  
## Test Program 7 (Extended Shell)
  

**Input**

Built in shell command/ Name of XSM executable file (String)

**Output**

Ouput of corresponding to shell command or executable file.

**Description :** Shell program given below reads command from console. If the command is halt, then program will invoke Shutdown system call. If the command is built in shell command, then shell will read suitable number of arguments from the console and corresponding system call is invoked from shell itself. If the command is an executable file, shell will fork and exec with the given executable file.

Note that the shell program should fit in 2 blocks/pages provided in [disk/memory organization](../os_implementation.md). The program given below is optimized to fits in 2 blocks/pages. In order to optimize the code, the program violates some of the type checkings. Even with type checking errors, the program will still compile and execute correctly. Also some system calls are invoked with arguments, even though the system call does not need any arguments. This will not cause any problem as these arguments will simply be ignored in the corresponding system call.

  
The code for the test program can be found [here](./test_program_07.md)

  
  

---

  
  
## Test Program 8
  

**Input**

Delay Parameter

**Output**

8 integers - PID\*100 to PID\*100+7.

**Description :** The program given in above link will first read a delay parameter and then, call the Fork system call and create 12 processes. Each process prints numbers from PID\*100 to PID\*100 + 7. After printing each number, a delay function is called with the the delay parameter provided.

  
The code for the test program can be found [here](./test_program_08.md)

  
  

---

  
  
## Test Program 9
  

**Input**

\-

**Output**

Out of 12 processes created, if N processes complete execution, then N data files each containing 100 consecutive integers (PID-3)\*100+1 to (PID-3)\*100+100 are created.

**Description :** The program will create a file with name "num.dat" with open permission. Integers 1 to 1200 are written to this file and file is closed. The program will then invoke _Fork_ system call four times, back to back to create 12 processes and Exec system call is invoked with file "pgm1.xsm". The program for "pgm1.xsm" is provided [here](./index.md#test-program-10).

  
The code for the test program can be found [here](./test_program_09.md)

  
  

---

  
  
## Test Program 10
  

**Input**

\-

**Output (For each 12 proceesses)**

A file will be created containing 100 consecutive numbers (PID-3)\*100+1 to (PID-3)\*100+100

**Description :** This program can not be run individualy. The test program 9 will invoke Exec with below given program with name "pgm1.xsm". Make sure to compile and save this program as "pgm1.xsm". Below given program will create a new file according to the PID of the process and read 100 numbers from file "num.dat" from offset (PID-3)\*100 to (PID-3)\*100+99 and write to newly created file. After successful execution, there should be 12 data files each containing 100 consecutive numbers (PID-3)\*100+1 to PID-3)\*100+100.

  
The code for the test program can be found [here](./test_program_10.md)

  
  

---

  
  
## Test Program 11
  

**Input**

\-

**Output**

Out of 12 processes created, if N processes complete execution, then N data files each containing 100 consecutive integers from X\*1000+1 to X\*1000+100 (where X ∈ {3,4..14}) are created.

**Description :** The program will create a file with name "numbers.dat" with open permission and open the file. The program also invokes Semget to acquire a shared semaphore. The program will then invoke _Fork_ system call four times, back to back to create 12 processes. The 12 processes now share a file open instance and a semaphore. Each process will write 100 numbers consecutatively (PID\*1000+1 to PID\*1000+100) to the file "numbers.dat". Exec system call is invoked with file "pgm2.xsm". The program for "pgm2.xsm" is provided [here](./index.md#test-program-12).

  
The code for the test program can be found [here](./test_program_11.md)

  
  

---

  
  
## Test Program 12
  

**Input**

\-

**Output (For each 12 proceesses)**

A file will be created containing 100 consecutive numbers from data file "numbers.dat".

**Description :** This program can not be run individualy. Test program 11 will invoke Exec with below given program with name "pgm2.xsm". Make sure to compile and save this program as "pgm2.xsm". Below given program will create a new file according to the PID of the process and read 100 numbers from file "numbers.dat" from offset (PID-3)\*100 to (PID-3)\*100+99 and write to newly created file. After successful execution, there should be 12 data files each containing 100 numbers each X\*1000 -X\*1000+99, where X=\[3,4..14\]. The numbers written by a process in the newly created file need not be the same numbers the process has written in "numbers.dat" file.

  
The code for the test program can be found [here](./test_program_12.md)

  
  

---

  
  
## Test Program 13
  

**Input**

\-

**Output (For each 8 processes with PID = 2 to 9)**

Return values from Fork system call and integers from PID\*100 to PID\*100+9.

**Description :** This program calls fork 3 times creating 8 child processes. Each process prints the value returned from the last Fork system call and Exec system call is invoked with file "child.xsm". The "child.xsm" program stores numbers from PID\*100 to PID\*100+9 onto a linked list and prints them to the console.

  
The code for the _parent.expl_ can be found [here](./test_program_13.md#parentexpl) and the code for the _child.expl_ can be found [here](./test_program_13.md#childexpl)

  
  

---

  
  
## Test Program 14 (Merge Sort)
  

**Input**

\-

**Output**

Print numbers from 1 to 64 in ascending order.

**Description :** These two ExpL programs perform merge sort in two different ways. The first one is done in a sequential manner and the second one, in a concurrent approach. Values from 1 to 64 are stored in decreasing order in a linked list and are sorted using a recursive merge sort function. In the concurrent approach, the process is forked and the merge sort function is called recursively for the two sub-lists from the two child processes.

  
The code for the Sequential approach can be found [here](./test_program_14.md#merge-sort-sequential) and the code for the Concurrent approach can be found [here](./test_program_14.md#merge-sort-concurrent)

  
  

---

  
  
## Test Program 15 (Merge Files)
  

**Input**

\-

**Output**

Creates a file _merge.dat_ with numbers from 1 to 2048.

**Description :** The ExpL program first creates 4 files with values from s to 4\*c+s, where s=\[1..and c=\[0..511\]. The program then, merges the 4 files taking 2 at a time, and finally, creates a _merge.dat_ file containing numbers from 1 to 2048.

  
The code for the test program can be found [here](./test_program_15.md)

  
  

---

  
  
## Test Program 16 (Merge Sort with Files)
  

**Input**

\-

**Output**

Creates a file _merge.dat_ with numbers from 1 to 512 and also prints them.

**Description :** The first ExpL program, _merge.expl_, first stores numbers from 1 to 512 in a random order into a file _merge.dat_. It then forks and executes _m\_store.expl_ which creates 8 files _temp{i}.dat_, where i=1..8 and stores 64 numbers each from _merge.expl_. Then, all the temporary files are sorted by executing _m\_sort.expl_. Next, the first ExpL program forks and executes _m\_merge.expl_ which merges all the temporary files back into _merge.dat_ and finally, prints the contents from 1 to 512 in ascending order.

  
The test programs are [merge.expl](./test_program_16.md#mergeexpl), [m\_store.expl](./test_program_16.md#m_storeexpl), [m\_sort.expl](./test_program_16.md#m_sortexpl) and [m\_merge.expl](./test_program_16.md#m_mergeexpl)