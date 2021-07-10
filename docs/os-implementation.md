---
title: eXpOS Implementation
original_url: https://exposnitc.github.io/os_implementation
hide:
    - navigation
---

### Introduction
This document discusses the mapping of various eXpOS data structures to the XSM machine's disk and memory. The implementation of eXpOS on XSM discussed in the project modularises the code of system calls into smaller module functions. An interface description of the module functions is given here. The document also outlines the useage of kernel stack of user processes.


### Disk Organization

| Block Number |                                           Contents                                           | Number of Blocks |
| :----------: | :------------------------------------------------------------------------------------------: | :--------------: |
|    0 - 1     |                                          Bootstrap                                           |        2         |
|      2       |                                        Disk Free List                                        |        1         |
|    3 - 4     |                              Inode + User Table :purple_circle:                              |        2         |
|      5       |                                   Root File :blue_circle:                                    |        1         |
|      6       |                                   Reserved for future use                                    |        1         |
|    7 - 8     |                                       Init/Login Code                                        |        2         |
|    9 - 10    |                                          Shell Code                                          |        2         |
|   11 - 12    |                                          Idle Code                                           |        2         |
|   13 - 14    |                                           Library                                            |        2         |
|   15 - 16    |                                      Exception Handler                                       |        2         |
|   17 - 18    |                                   Timer Interrupt Routine                                    |        2         |
|   19 - 20    |                              Disk Controller Interrupt Routine                               |        2         |
|   21 - 22    |                                  Console Interrupt Routine                                   |        2         |
|   23 - 24    |                             Interrupt 4 Routine: Create, Delete                              |        2         |
|   25 - 26    |                            Interrupt 5 Routine: Seek, Open, Close                            |        2         |
|   27 - 28    |                                  Interrupt 6 Routine: Read                                   |        2         |
|   29 - 30    |                                  Interrupt 7 Routine: Write                                  |        2         |
|   31 - 32    |                                  Interrupt 8 Routine: Fork                                   |        2         |
|   33 - 34    |                                  Interrupt 9 Routine: Exec                                   |        2         |
|   35 - 36    |                                  Interrupt 10 Routine: Exit                                  |        2         |
|   37 - 38    |                     Interrupt 11 Routine: Getpid, Getppid, Wait, Signal                      |        2         |
|   39 - 40    |                                 Interrupt 12 Routine: Logout                                 |        2         |
|   41 - 42    |                           Interrupt 13 Routine: Semget, Semrelease                           |        2         |
|   43 - 44    |                           Interrupt 14 Routine: SemLock, SemUnLock                           |        2         |
|   45 - 46    |                                Interrupt 15 Routine: Shutdown                                |        2         |
|   47 - 48    |                Interrupt 16 Routine: Newusr, Remusr, Setpwd, Getuname, Getuid                |        2         |
|   49 - 50    |                                 Interrupt 17 Routine: Login                                  |        2         |
|   51 - 52    |                       Interrupt 18 Routine: Test0, Test1, Test2, Test3                       |        2         |
|   53 - 54    |                                  Module 0: Resource Manager                                  |        2         |
|   55 - 56    |                                  Module 1: Process Manager                                   |        2         |
|   57 - 58    |                                   Module 2: Memory Manager                                   |        2         |
|   59 - 60    |                                    Module 3: File Manager                                    |        2         |
|   61 - 62    |                                   Module 4: Device Manager                                   |        2         |
|   63 - 64    |                      Module 5: Context Switch Module (Scheduler Module)                      |        2         |
|   65 - 66    |                                    Module 6: Pager Module                                    |        2         |
|   67 - 68    |                                    Module 7: Boot Module                                     |        2         |
|   69 - 255   |                                         User Blocks                                          |       187        |
|  256 - 511   |                                          Swap Area                                           |       256        |
|  512 - 513   |               <span style="color:red">Secondary Bootstrap</span> :red_circle:                |        2         |
|  514 - 515   | <span style="color:red">Interrupt 19 Routine: Test4, Test5, Test6, Test8</span> :red_circle: |        2         |
|  516 - 517   |         <span style="color:red">Module 8: Access Control Module</span> :red_circle:          |        2         |
|  518 - 519   |                   <span style="color:red">Module 9: TestA (Unused)</span>                    |        2         |
|  520 - 521   |            <span style="color:red">Module 10: TestB (Unused)</span> :red_circle:             |        2         |
|  522 - 523   |            <span style="color:red">Module 11: TestC (Unused)</span> :red_circle:             |        2         |
|  524 - 527   |                   <span style="color:red">Unallocated</span> :red_circle:                    |        4         |

:purple_circle: The Inode table occupies the first 960 words (60 entries each of size 16 words) in the disk blocks 3 and 4. User table occupies the next 32 words (16 entries each of size 2 words) and the last 32 words are reserved for future use.

:blue_circle: The Root File occupies the first 480 words of the 5th block and the last 32 words are unallocated.

:red_circle: These disk blocks are available only on eXpOS running on NEXSM (a two-core extension of XSM) machine.

### Memory Organization
The Memory layout of the XSM machine is as follows :

<!-- This table can't be migrated because it has colspan, rowspan -->
<div class="md-typeset__table">
<table class="table table-bordered" style="text-align: center;">
<thead>
<tr>
<th style="text-align: center;">Page Number</th>
<th style="text-align: center;">Contents</th>
<th style="text-align: center;">Word Address</th>
<th style="text-align: center;">Number of Words</th>
</tr>
</thead>
<tbody>
<tr>
<td>0</td>
<td>ROM Code</td>
<td>0 - 511</td>
<td>512</td>
</tr>

<tr>
<td>1</td>
<td>Page for loading the BOOT block (<a href="../os-design/misc/#os_startup" target="_blank">OS Startup Code</a>)</td>
<td>512 - 1023</td>
<td>512</td>
</tr>

<tr>
<td>2 - 3</td>
<td><a href="../os-design/exe-handler/" target="_blank">Exception Handler</a></td>
<td>1024 - 2047</td>
<td>1024</td>
</tr>
<tr>
<td>4 - 5</td>
<td><a href="../os-design/timer/" target="_blank">Timer Interrupt Routine</a></td>
<td>2048 - 3071</td>
<td>1024</td>
</tr>
<tr>
<td>6 - 7</td>
<td><a href="../os-design/disk-interrupt/" target="_blank">Disk Controller Interrupt
Routine</a></td>
<td>3072 - 4095</td>
<td>1024</td>
</tr>
<tr>
<td>8 - 9</td>
<td><a href="../os-design/term-handler/" target="_blank">Console Interrupt
Routine</a></td>
<td>4096 - 5119</td>
<td>1024</td>
</tr>
<tr>
<td>10 - 11</td>
<td>Interrupt 4 Routine: <a href="../os-design/create/" target="_blank">Create</a>,
<a href="../os-design/delete/" target="_blank">Delete</a></td>
<td>5120 - 6143</td>
<td>1024</td>
</tr>
<tr>
<td>12 - 13</td>
<td>Interrupt 5 Routine: <a href="../os-design/seek/" target="_blank">Seek</a>, <a href="../os-design/open/" target="_blank">Open</a>, <a href="../os-design/close/" target="_blank">Close</a></td>
<td>6144 - 7167</td>
<td>1024</td>
</tr>
<tr>
<td>14 - 15</td>
<td>Interrupt 6 Routine: <a href="../os-design/read/" target="_blank">Read</a></td>
<td>7168 - 8191</td>
<td>1024</td>
</tr>
<tr>
<td>16 - 17</td>
<td>Interrupt 7 Routine: <a href="../os-design/write/" target="_blank">Write</a></td>
<td>8192 - 9215</td>
<td>1024</td>
</tr>
<tr>
<td>18 - 19</td>
<td>Interrupt 8 Routine: <a href="../os-design/fork/" target="_blank">Fork</a></td>
<td>9216 - 10239</td>
<td>1024</td>
</tr>
<tr>
<td>20 - 21</td>
<td>Interrupt 9 Routine: <a href="../os-design/exec/" target="_blank">Exec</a></td>
<td>10240 - 11263</td>
<td>1024</td>
</tr>
<tr>
<td>22 - 23</td>
<td>Interrupt 10 Routine: <a href="../os-design/exit/" target="_blank">Exit</a></td>
<td>11264 - 12287</td>
<td>1024</td>
</tr>
<tr>
<td>24 - 25</td>
<td>Interrupt 11 Routine: <a href="../os-design/proc-misc/#getpid" target="_blank">Getpid</a>, <a href="../os-design/proc-misc/#getppid" target="_blank">Getppid</a>, <a href="../os-design/synchronization-algos/#wait" target="_blank">Wait</a>, <a href="../os-design/synchronization-algos/#signal" target="_blank">Signal</a></td>
<td>12288 - 13311</td>
<td>1024</td>
</tr>
<tr>
<td>26 - 27</td>
<td>Interrupt 12 Routine: <a href="../os-design/multiusersyscalls/#logout" target="_blank">Logout</a></td>
<td>13312 - 14335</td>
<td>1024</td>
</tr>
<tr>
<td>28 - 29</td>
<td>Interrupt 13 Routine: <a href="../os-design/semaphore-algos/#semget" target="_blank">Semget</a>, <a href="../os-design/semaphore-algos/#semrelease" target="_blank">Semrelease</a></td>
<td>14336 - 15359</td>
<td>1024</td>
</tr>
<tr>
<td>30 - 31</td>
<td>Interrupt 14 Routine: <a href="../os-design/semaphore-algos/#semlock" target="_blank">SemLock</a>, <a href="../os-design/semaphore-algos/#semunlock" target="_blank">SemUnLock</a></td>
<td>15360 - 16383</td>
<td>1024</td>
</tr>
<tr>
<td>32 - 33</td>
<td>Interrupt 15 Routine: <a href="../os-design/shutdown/" target="_blank">Shutdown</a></td>
<td>16384 - 17407</td>
<td>1024</td>
</tr>
<tr>
<td>34 - 35</td>
<td>Interrupt 16 Routine: <a href="../os-design/multiusersyscalls/#newusr" target="_blank">Newusr</a>, <a href="../os-design/multiusersyscalls/#remusr" target="_blank">Remusr</a>, <a href="../os-design/multiusersyscalls/#setpwd" target="_blank">Setpwd</a>, <a href="../os-design/multiusersyscalls/#getuname" target="_blank">Getuname</a>, <a href="../os-design/multiusersyscalls/#getuid" target="_blank">Getuid</a></td>
<td>17408 - 18431</td>
<td>1024</td>
</tr>
<tr>
<td>36 - 37</td>
<td>Interrupt 17 Routine: <a href="../os-design/multiusersyscalls/#login" target="_blank">Login</a></td>
<td>18432 - 19455</td>
<td>1024</td>
</tr>
<tr>
<td>38 - 39</td>
<td>Interrupt 18 Routine: Test0, Test1, Test2, Test3</td>
<td>19456 - 20479</td>
<td>1024</td>
</tr>
<tr>
<td>40 - 41</td>
<td>Module 0: <a href="../modules/module-00/" target="_blank">Resource Manager</a></td>
<td>20480 - 21503</td>
<td>1024</td>
</tr>
<tr>
<td>42 - 43</td>
<td>Module 1: <a href="../modules/module-01/" target="_blank">Process Manager</a></td>
<td>21504 - 22527</td>
<td>1024</td>
</tr>
<tr>
<td>44 - 45</td>
<td>Module 2: <a href="../modules/module-02/" target="_blank">Memory Manager</a></td>
<td>22528 - 23551</td>
<td>1024</td>
</tr>
<tr>
<td>46 - 47</td>
<td>Module 3: <a href="../modules/module-03/" target="_blank">File Manager</a></td>
<td>23552 - 24575</td>
<td>1024</td>
</tr>
<tr>
<td>48 - 49</td>
<td>Module 4: <a href="../modules/module-04/" target="_blank">Device Manager</a></td>
<td>24576 - 25599</td>
<td>1024</td>
</tr>
<tr>
<td>50 - 51</td>
<td>Module 5: <a href="../modules/module-05/" target="_blank">Context Switch Module
(Scheduler Module)</a></td>
<td>25600 - 26623</td>
<td>1024</td>
</tr>
<tr>
<td>52 - 53</td>
<td>Module 6: <a href="../modules/module-06/" target="_blank">Pager Module</a></td>
<td>26624 - 27647</td>
<td>1024</td>
</tr>
<tr>
<td>54 - 55</td>
<td>Module 7: <a href="../modules/module-07/" target="_blank">Boot Module</a></td>
<td>27648 - 28671</td>
<td>1024</td>
</tr>
<tr>
<td rowspan="3" style="vertical-align:middle">56</td>
<td><a href="../os-design/process-table/" target="_blank">Process Table</a></td>
<td>28672 - 28927</td>
<td>256</td>
</tr>
<tr>
<td><a href="../os-design/mem-ds/#open-file-table" target="_blank">Open File Table</a></td>
<td>28928 - 29055</td>
<td>128</td>
</tr>
<tr>
<td><a href="../os-design/mem-ds/#semaphore-table" target="_blank">Semaphore Table</a></td>
<td>29056 - 29183</td>
<td>128</td>
</tr>
<tr>
<td rowspan="7" style="vertical-align:middle">57</td>
<td><a href="../os-design/mem-ds/#memory-free-list" target="_blank">Memory Free List</a></td>
<td>29184 - 29311</td>
<td>128</td>
</tr>
<tr>
<td><a href="../os-design/mem-ds/#file-inode-status-table" target="_blank">File Status Table</a></td>
<td>29312 - 29551</td>
<td>240</td>
</tr>
<tr>
<td><a href="../os-design/mem-ds/#disk-status-table" target="_blank">Disk Status Table</a></td>
<td>29552 - 29559</td>
<td>8</td>
</tr>
<tr>
<td><a href="../os-design/mem-ds/#system-status-table" target="_blank">System Status Table</a></td>
<td>29560 - 29567</td>
<td>8</td>
</tr>
<tr>
<td><a href="../os-design/mem-ds/#terminal-status-table" target="_blank">Terminal Status Table</a></td>
<td>29568 - 29575</td>
<td>8</td>
</tr>
<tr>
<td><a href="../os-design/mem-ds/#access-lock-table" target="_blank" style="color:red">Access Lock Table <span style="color:red">*</span></a></td>
<td>29576 - 29583</td>
<td>8</td>
</tr>
<tr>
<td>Unallocated</td>
<td>29584 - 29695</td>
<td>112</td>
</tr>
<tr>
<td rowspan="4" style="vertical-align:middle">58</td>
<td><a href="../os-design/process-table/#per-process-page-table" target="_blank">Page tables</a></td>
<td>29696 - 30015</td>
<td>320</td>
</tr>
<tr>
<td><a href="../os-design/mem-ds/#buffer-table" target="_blank">Buffer Table</a></td>
<td>30016 - 30031</td>
<td>16</td>
</tr>
<tr>
<td><a href="../os-design/process-table/#per-process-disk-map-table" target="_blank">Disk Map Table</a></td>
<td>30032 - 30191</td>
<td>160</td>
</tr>
<tr>
<td>Unallocated</td>
<td>30192 - 30207</td>
<td>16</td>
</tr>
<tr>
<td rowspan="3" style="vertical-align:middle">59 - 60</td>
<td>Memory copy of <a href="../os-design/disk-ds/#inode-table" target="_blank"> Inode Table</a></td>
<td>30208 - 31167</td>
<td>960</td>
</tr>
<tr>
<td>Memory copy of<a href="../os-design/disk-ds/#user-table" target="_blank"> User Table</a></td>
<td>31168 - 31199</td>
<td>32</td>
</tr>
<tr>
<td>Unallocated</td>
<td>31200 - 31231</td>
<td>32</td>
</tr>
<tr>
<td>61</td>
<td>Memory copy of <a href="../os-design/disk-ds/#disk-free-list" target="_blank">Disk Free List</a></td>
<td>31232 - 31743</td>
<td>512</td>
</tr>
<tr>
<td rowspan="2" style="vertical-align:middle">62</td>
<td>Memory copy of<a href="../os-design/disk-ds/#root-file" target="_blank"> Root File</a></td>
<td>31744 - 32223</td>
<td>480</td>
</tr>
<tr>
<td>Unallocated</td>
<td>32224 - 32255</td>
<td>32</td>
</tr>
<tr>
<td>63 - 64</td>
<td><a href="../os-spec/misc/#expos_library" target="_blank">Expos Library</a></td>
<td>32256 - 33279</td>
<td>1024</td>
</tr>
<tr>
<td>65 - 66</td>
<td><a href="../os-design/misc/#login" target="_blank">INIT/Login Program</a></td>
<td>33280 - 34303</td>
<td>1024</td>
</tr>
<tr>
<td>67 - 68</td>
<td><a href="../os-design/misc/#shell" target="_blank">Shell Program</a></td>
<td>34304 - 35327</td>
<td>1024</td>
</tr>
<tr>
<td>69 - 70</td>
<td><a href="../os-design/misc/#idle" target="_blank">Idle
Program</a></td>
<td>35328 - 36351</td>
<td>1024</td>
</tr>
<tr>
<td>71 - 74</td>
<td>Buffer (disk cache)</td>
<td>36352 - 38399</td>
<td>2048</td>
</tr>
<tr>
<td>75</td>
<td>Reserved for future use (Exam!)</td>
<td>38400 - 38911</td>
<td>512</td>
</tr>
<tr height="200" valign="middle">
<td>76 - 127</td>
<td>User Programs</td>
<td>38912 - 65535</td>
<td>26624</td>
</tr>
<tr>
<td>128 - 129</td>
<td style="color:red">Page for loading the <a href="../os-design/misc/#os2_startup" target="_blank">Secondary BOOT Block</a> <span style="color:red">*</span></td>
<td>65536 - 66559</td>
<td>1024</td>
</tr>
<tr>
<td>130 - 131</td>
<td style="color:red">Interrupt 19 Routine: Test4, Test5, Test6, Test7 <span style="color:red">*</span></td>
<td>66560 - 67583</td>
<td>1024</td>
</tr>
<tr>
<td>132 - 133</td>
<td style="color:red">Module 8: <a href="../modules/module-08/" target="_blank">Access Control Module</a> <span style="color:red">*</span></td>
<td>67584 - 68607</td>
<td>1024</td>
</tr>
<tr>
<td>134 - 135</td>
<td style="color:red">Module 9: TestA (Unused) <span style="color:red">*</span></td>
<td>68608 - 69631</td>
<td>1024</td>
</tr>
<tr>
<td>136 - 137</td>
<td style="color:red">Module 10: TestB (Unused) <span style="color:red">*</span></td>
<td>69632 - 70655</td>
<td>1024</td>
</tr>
<tr>
<td>138 - 139</td>
<td style="color:red">Module 11: TestC (Unused) <span style="color:red">*</span></td>
<td>70656 - 71679</td>
<td>1024</td>
</tr>

<tr>
<td>140 - 143</td>
<td style="color:red">Reserved for future use <span style="color:red">*</span></td>
<td>71680 - 73727</td>
<td>2048</td>
</tr>
</tbody>
</table>
</div>

<span style="color:red">*</span> These memory pages are available only on eXpOS running on NEXSM (a two-core extension of XSM) machine.

!!! note
    Constants can be found [here](./support-tools/constants.md)

### [:link: Kernel Module Interface](./modules/index.md)

### Kernel Stack Management
#### [:link: Kernel Stack Management during System Calls](./os-design/stack-smcall.md)
#### [:link: Kernel Stack Management during Hardware interrupts or exceptions](./os-design/stack-interrupt.md)
#### [:link: Kernel Stack Management during Module calls](./os-design/stack-module.md)
#### [:link: Kernel Stack Management during Context Switch](./os-design/timer-stack-management.md)

### [:link: eXpOS Procees management implementation](./tutorials/process-management-implementation.md)

### [:link: eXpOS File-System and implementation](./tutorials/filesystem-implementation.md)

### [:link: eXpOS Multi-User implementation](./tutorials/multiuser-implementation.md)