---
title: Predefined Constants in SPL
original_url: https://exposnitc.github.io/support_tools-files/constants.html
hide:
    - navigation
---

#### SPL constants defining the call addresses for Interrupts/Exceptions/Modules

| Name                               | Default Value | Comments                                                               |
| ---------------------------------- | ------------- | ---------------------------------------------------------------------- |
| EX_HANDLER / EXCEPTION             | 1024          | Starting address of Exception Handler                                  |
| TIMER                              | 2048          | Starting address of Timer Interrupt Routine                            |
| DISK                               | 3072          | Starting address of Disk Controller Interrupt Routine                  |
| CONSOLE                            | 4096          | Starting address of Console Interrupt Routine                          |
| INT_4                              | 5120          | (Create, 1)<span style="color:red">*</span>, (Delete, 4)               |
| INT_5                              | 6144          | (Seek, 6), (Open, 2), (Close,3)                                        |
| INT_6                              | 7168          | (Read, 7)                                                              |
| INT_7                              | 8192          | (Write, 5)                                                             |
| INT_8                              | 9216          | (Fork, 8)                                                              |
| INT_9                              | 10240         | (Exec, 9)                                                              |
| INT_10                             | 11264         | (Exit, 10)                                                             |
| INT_11                             | 12288         | (Getpid, 11), (Getppid, 12), (Wait, 13), (Signal, 14)                  |
| INT_12                             | 13312         | (Logout, 28)                                                           |
| INT_13                             | 14336         | (Semget, 17), (Semrelease, 18)                                         |
| INT_14                             | 15360         | (SemLock, 19), (SemUnLock, 20)                                         |
| INT_15                             | 16384         | (Shutdown, 21)                                                         |
| INT_16                             | 17408         | (Newusr, 22), (Remusr, 23), (Setpwd, 24), (Getuname, 25), (Getuid, 26) |
| INT_17                             | 18432         | (Login, 27)                                                            |
| INT_18                             | 19456         | (Test0, 96), (Test1, 97), (Test2, 98), (Test3, 99)                     |
| MOD_0 / RESOURCE_MANAGER           | 20480         | Resource Manager                                                       |
| MOD_1 / PROCESS_MANAGER            | 21504         | Process Manager                                                        |
| MOD_2 / MEMORY_MANAGER             | 22528         | Memory Manager                                                         |
| MOD_3 / FILE_MANAGER               | 23552         | File Manager                                                           |
| MOD_4 / DEVICE_MANAGER             | 24576         | Device Manager                                                         |
| MOD_5 / CONTEXT_SWITCH / SCHEDULER | 25600         | Context Switch Module (Scheduler Module)                               |
| MOD_6 / PAGER_MODULE               | 26624         | Pager Module                                                           |
| MOD_7 / BOOT_MODULE                | 27648         | Boot Module                                                            |

<span style="color: red">*</span>(System Call Name, System Call Number)

#### SPL constants for the [System Call Numbers](../os-design/sw-interface.md)

| Name           | System Call Number | Comments               |
| -------------- | ------------------ | ---------------------- |
| INT_CREATE     | 1                  | Create System Call     |
| INT_OPEN       | 2                  | Open System Call       |
| INT_CLOSE      | 3                  | Close System Call      |
| INT_DELETE     | 4                  | Delete System Call     |
| INT_WRITE      | 5                  | Write System Call      |
| INT_SEEK       | 6                  | Seek System Call       |
| INT_READ       | 7                  | Read System Call       |
| INT_FORK       | 8                  | Fork System Call       |
| INT_EXEC       | 9                  | Exec System Call       |
| INT_EXIT       | 10                 | Exit System Call       |
| INT_GETPID     | 11                 | Getpid System Call     |
| INT_GETPPID    | 12                 | Getppid System Call    |
| INT_WAIT       | 13                 | Wait System Call       |
| INT_SIGNAL     | 14                 | Signal System Call     |
| INT_SEMGET     | 17                 | Semget System Call     |
| INT_SEMRELEASE | 18                 | Semrelease System Call |
| INT_SEMLOCK    | 19                 | SemLock System Call    |
| INT_SEMUNLOCK  | 20                 | SemUnLock System Call  |
| INT_SHUTDOWN   | 21                 | Shutdown System Call   |
| INT_NEWUSR     | 22                 | Newusr System Call     |
| INT_REMUSR     | 23                 | Remusr System Call     |
| INT_SETPWD     | 24                 | Setpwd System Call     |
| INT_GETUNAME   | 25                 | Getuname System Call   |
| INT_GETUID     | 26                 | Getuid System Call     |
| INT_LOGIN      | 27                 | Login System Call      |
| INT_LOGOUT     | 28                 | Logout System Call     |
| INT_TEST0      | 96                 | Test System Call 0     |
| INT_TEST1      | 97                 | Test System Call 1     |
| INT_TEST2      | 98                 | Test System Call 2     |
| INT_TEST3      | 99                 | Test System Call 3     |


#### SPL constants for indicating the Function Numbers in Modules

| Name                | Default Value | Comments                     |
| ------------------- | ------------- | ---------------------------- |
| ACQUIRE_BUFFER      | 1             | Resource Manager Function #1 |
| RELEASE_BUFFER      | 2             | Resource Manager Function #2 |
| ACQUIRE_DISK        | 3             | Resource Manager Function #3 |
| ACQUIRE_INODE       | 4             | Resource Manager Function #4 |
| RELEASE_INODE       | 5             | Resource Manager Function #5 |
| ACQUIRE_SEMAPHORE   | 6             | Resource Manager Function #6 |
| RELEASE_SEMAPHORE   | 7             | Resource Manager Function #7 |
| ACQUIRE_TERMINAL    | 8             | Resource Manager Function #8 |
| RELEASE TERMINAL    | 9             | Resource Manager Function #9 |
| GET_PCB_ENTRY       | 1             | Process Manager Function #1  |
| FREE_USER_AREA_PAGE | 2             | Process Manager Function #2  |
| EXIT_PROCESS        | 3             | Process Manager Function #3  |
| FREE_PAGE_TABLE     | 4             | Process Manager Function #4  |
| KILL_ALL            | 5             | Process Manager Function #5  |
| GET_FREE_PAGE       | 1             | Memory Manager Function #1   |
| RELEASE_PAGE        | 2             | Memory Manager Function #2   |
| GET_FREE_BLOCK      | 3             | Memory Manager Function #3   |
| RELEASE_BLOCK       | 4             | Memory Manager Function #4   |
| GET_CODE_PAGE       | 5             | Memory Manager Function #5   |
| GET_SWAP_BLOCK      | 6             | Memory Manager Function #6   |
| BUFFERED_WRITE      | 1             | File Manager Function #1     |
| BUFFERED_READ       | 2             | File Manager Function #2     |
| OPEN                | 3             | File Manager Function #3     |
| CLOSE               | 4             | File Manager Function #4     |
| DISK_STORE          | 1             | Device Manager Function #1   |
| DISK_LOAD           | 2             | Device Manager Function #2   |
| TERMINAL_WRITE      | 3             | Device Manager Function #3   |
| TERMINAL_READ       | 4             | Device Manager Function #4   |
| SWAP_OUT            | 1             | Pager Module Function #1     |
| SWAP_IN             | 2             | Pager Module Function #2     |

#### SPL constants for indicating the starting addresses of Kernel Data Structures in Memory (See [Memory Organisation](../os-implementation.md))

| Name                  | Default Value | Comments                                  |
| --------------------- | ------------- | ----------------------------------------- |
| PROCESS_TABLE         | 28672         | Starting address of Process Table         |
| OPEN_FILE_TABLE       | 28928         | Starting address of Open File Table       |
| SEMAPHORE_TABLE       | 29056         | Starting address of Semaphore Table       |
| MEMORY_FREE_LIST      | 29184         | Starting address of Memory Free List      |
| FILE_STATUS_TABLE     | 29312         | Starting address of File Status Table     |
| DISK_STATUS_TABLE     | 29552         | Starting address of Disk Status Table     |
| SYSTEM_STATUS_TABLE   | 29560         | Starting address of System Status Table   |
| TERMINAL_STATUS_TABLE | 29568         | Starting address of Terminal Status Table |
| PAGE_TABLE_BASE       | 29696         | Starting address of Page tables           |
| BUFFER_TABLE          | 30016         | Starting address of Buffer Table          |
| DISK_MAP_TABLE        | 30032         | Starting address of Disk Map Table        |
| INODE_TABLE           | 30208         | Starting address of Inode Table           |
| USER_TABLE            | 31168         | Starting address of User Table            |
| DISK_FREE_LIST        | 31232         | Starting address of Disk Free List        |
| ROOT_FILE             | 31744         | Starting address of Root File             |
| BUFFER                | 36352         | Starting address of Buffer Cache          |
| BUFFER_BASE           | 71            | Starting page number of Buffer Cache      |

#### SPL constants for related to User Programs loaded by the Kernel to Memory (See [Memory Organisation](../os-implementation.md))

| Name                         | Default Value | Comments                                 |
| ---------------------------- | ------------- | ---------------------------------------- |
| LIBRARY                      | 32256         | Starting address of eXpOS Library        |
| INIT / LOGIN                 | 33280         | Starting address of INIT/Login Program   |
| SHELL                        | 34304         | Starting address of Shell Program        |
| IDLE / SWAPPER               | 35328         | Starting address of Idle/Swapper Program |
| IDLE_PROCESS                 | 0             | PID of the Idle Process                  |
| INIT_PROCESS / LOGIN_PROCESS | 1             | PID of the Init/Login Proces             |
| SHELL_PROCESS                | 2             | PID of the Shell                         |
| SWAPPER_DAEMON               | 15            | PID of the Swapper Daemon                |


#### SPL constants for indicating the [Process States](../os-design/state-diag.md)

| Name           | Default Value | Comments                                                                                     |
| -------------- | ------------- | -------------------------------------------------------------------------------------------- |
| READY          | 1             | Process State READY                                                                          |
| RUNNING        | 2             | Process State RUNNING                                                                        |
| CREATED        | 3             | Process State CREATED                                                                        |
| TERMINATED     | 4             | Process State TERMINATED                                                                     |
| WAIT_DISK      | 5             | Process is waiting to acquire disk                                                           |
| WAIT_FILE      | 6             | Process is waiting for release on an Inode                                                   |
| WAIT_BUFFER    | 7             | Process is waiting for release of buffer cache                                               |
| WAIT_TERMINAL  | 8             | Process is waiting to acquire terminal                                                       |
| WAIT_PROCESS   | 9             | Process is waiting for a signal from another process                                         |
| WAIT_SEMAPHORE | 10            | Process is waiting to acquire a semaphore                                                    |
| WAIT_MEM       | 11            | Process is waiting as memory is not available                                                |
| ALLOCATED      | 12            | Process Table entry has been allocated for the process, but process creation is not complete |


#### SPL constants identifying the File Type/Permission in [Inode Table](../os-design/disk-ds.md#inode-table)
| Name        | Default Value | Comments                                      |
| ----------- | ------------- | --------------------------------------------- |
| EXCLUSIVE   | 0             | EXCLUSIVE file permission                     |
| OPEN_ACCESS | 1             | OPEN ACCESS file permission                   |
| ROOT        | 1             | Indicates that the file is the root file      |
| DATA        | 2             | Indicates that the file is a data file        |
| EXEC        | 3             | Indicates that the file is an executable file |


#### SPL constants related to [Per-process Resource Table](../os-design/process-table.md#per-process-resource-table)

| Name                  | Default Value | Comments                                                         |
| --------------------- | ------------- | ---------------------------------------------------------------- |
| FILE                  | 0             | Indicates that the resource is a file in the resource table      |
| SEMAPHORE             | 1             | Indicates that the resource is a semaphore in the resource table |
| RESOURCE_TABLE_OFFSET | 496           | Offset of the Resource Table from the start of user area page    |

#### SPL constants related to Swapping

| Name     | Default Value | Comments                                                                          |
| -------- | ------------- | --------------------------------------------------------------------------------- |
| MEM_LOW  | 4             | Memory is critically low so that swap out has to be initiated                     |
| MEM_HIGH | 12            | Memory is high enough such that a process can be swapped in                       |
| MAX_TICK | 1000          | Indicates the threshold after which a swapped out process must be swapped back in |

#### SPL constants related to eXpFS Disk (See [Disk Origanisation](../os-implementation.md))

| Name            | Default Value | Comments                                             |
| --------------- | ------------- | ---------------------------------------------------- |
| XFS_BSIZE       | 512           | Number of words in a disk block                      |
| MAX_FILE_BLOCKS | 4             | Maximum number of blocks allocatable to each file.   |
| DISK_SWAP_AREA  | 256           | Starting block number of Swap Area in the disk       |
| DISK_FREE_AREA  | 69            | Starting block number of User Block area in the disk |
| DISK_SIZE       | 512           | Number of blocks in the disk                         |


#### SPL constants defining the maximum limits

| Name             | Default Value | Comments                                        |
| ---------------- | ------------- | ----------------------------------------------- |
| PAGE_SIZE        | 512           | Size of a memory page in eXpOS                  |
| NUM_MEM_PAGES    | 128           | Number of memory pages in eXpOS                 |
| MAX_PROC_NUM     | 16            | Max. number of process allowed by eXpOS         |
| PT_ENTRY_SIZE    | 16            | Size of one page table entry                    |
| MAX_OPENFILE_NUM | 32            | Max. number of open files allowed by eXpOS      |
| MAX_MEM_PAGE     | 128           | Max. number of memory pages availble to eXpOS   |
| MAX_SEM_COUNT    | 32            | Max. number of semaphores allowed by eXpOS      |
| MAX_PROC_PAGES   | 10            | Max. number of pages allowed for each process   |
| MAX_BUFFER       | 4             | Max. number of file read/write buffers in eXpOS |
| MAX_FILE_NUM     | 60            | Max. number of files possible                   |
| MAX_FILE_SIZE    | 2048          | Max. words in a file                            |
| MAX_USER_NUM     | 16            | Max. number of users allowed                    |


#### Miscellaneous Constants

| Name       | Default Value | Comments                                                                                    |
| ---------- | ------------- | ------------------------------------------------------------------------------------------- |
| INODE_ROOT | 0             | Inode Index field of the Open File Table is set to INODE_ROOT if the file is the Root file. |
| KERNEL     | 0             | Indicates the Kernel user in the CURRENT_USER_ID field of the System Status Table           |
| ZERO       | 0             | Zero                                                                                        |
| ONE        | 1             | One                                                                                         |

#### <span style="color:red">Constants for [NEXSM](../arch-spec/nexsm.md)</span>

| Name                   | Default Value | Comments                                                |
| ---------------------- | ------------- | ------------------------------------------------------- |
| OS_SECONDARY           | 65536         | Starting address of OS Startup code for secondary core. |
| INT_19                 | 66560         | (Test4, 100), (Test5, 101), (Test6, 102), (Test7, 103)  |
| MOD_8 / ACCESS_CONTROL | 67584         | Access Control Module                                   |
| MOD_9 / TESTA          | 68608         | TestA (Reserved for Future use)                         |
| MOD_10 / TESTB         | 69632         | TestB (Reserved for Future use)                         |
| MOD_11 / TESTC         | 70656         | TestC (Reserved for Future use)                         |
| IDLE2_PROCESS          | 14            | PID of the Idle Process for secondary core              |
| INT_TEST4              | 100           | Test System Call 4                                      |
| INT_TEST5              | 101           | Test System Call 5                                      |
| INT_TEST6              | 102           | Test System Call 6                                      |
| INT_TEST7              | 103           | Test System Call 7                                      |
| ACQUIRE_KERN_LOCK      | 1             | Access Control Module Function #1                       |
| ACQUIRE_SCHED_LOCK     | 2             | Access Control Module Function #2                       |
| ACQUIRE_GLOCK          | 3             | Access Control Module Function #3                       |
| RELEASE_LOCK           | 4             | Access Control Module Function #4                       |
| PRIMARY_CORE           | 0             | Indicates that the current core is primary core         |
| SECONDARY_CORE         | 1             | Indicates that the current core is secondary core       |
| ACCESS_LOCK_TABLE      | 29576         | Starting address of Access Lock Table                   |
| KERN_LOCK              | 29576         | Kernel Lock                                             |
| SCHED_LOCK             | 29577         | Scheduler Lock                                          |
| GLOCK                  | 29578         | General Purpose Lock                                    |
| NUM_MEM_PAGES *        | 144           | Number of memory pages in eXpOS                         |
| DISK_SIZE *            | 528           | Number of blocks in the disk                            |
