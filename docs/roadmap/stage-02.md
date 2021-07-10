---
title: "Stage 2 : Understanding the Filesystem  (2 Hours)"
original_url: https://exposnitc.github.io/Roadmap.html
---

!!! info "Learning Objectives"
    - Load/retrieve data and executable files from/to your host (Unix) system into the
    XSM disk.
    - Explain the disk data structures of the XFS file system - INODE table, disk free
    list and root file.
    - Find out the data blocks into which a data/executable file is stored in the XSM
    disk by examining the INODE table and root file.

!!! abstract "Pre-requisite Reading"
    - Quickly go through the [Filesystem
    (eXpFS) Specification](../os-spec/expfs.md) and [XFS-Interface Specification](../support-tools/xfs-interface.md) (interface between the UNIX
    System and eXpFS). Do not spent more than 30 minutes!


The eXpOS package that you had downloaded in the previous stage consists mainly of a machine
simulator. The machine is called the **eXperimental String Machine (XSM)** and consists of a
processor, memory and disk. Some support tools that help you to program the machine are also
provided.

One important point to note about the system is that the machine is a bare, and comes with no
software in it (except for a boot ROM). Hence, the only way to insert some software code into
the system is to prepare the code "outside" (that is, in your Linux/Unix system) and insert
your code into the machine. The support tools provided along with the package are precisely
designed to help you with this task.

The package comes with three major support tools - two compilers and a disk interface tool
called [XFS-Interface](../support-tools/xfs-interface.md). The
compilers allow you to write high level code and translate it into the XSM machine code. We
will look at them in later stages. The XFS-Inteface tool helps you to transfer files between
your Linux/Unix system and the XSM machines disk.

XSM machine's disk contains 512 blocks, each capable of storing
512 words. When files are stored in the disk, some format has
to be followed so that one can figure out where in the disk
are the blocks of a file located.

XSM disk is formatted to what is known as the[eXpFS file system format](../os-spec/expfs.md). 
The format specifies how data as well as
meta-data for each file stored in the disk must be organized. The XFS interface tool allows you
to load data files (and executable files as well) from your Linux/Unix system into the XSM disk
in accordance with the eXpFS format. 

The eXpFS format specifies that each data/executable file can span across at most four data
blocks, and that the index to these blocks along with the name and the size of the file must be
stored in a pre-define area of the disk called the [Inode table](../os-design/disk-ds.md).
(The inode table is stored in disk blocks 3 and 4).
There are also other pre-defined areas of the disk that stores
meta data about the disk (see description of the [root file](../os-design/disk-ds.md#root-file)
and the [disk free list](../os-design/disk-ds.md#disk-free-list)
for more details). When you use XFS interface to load a file from your Linux/Unix system to the XSM disk, the
interface tool will correctly fill all the required meta data information as stipulated by the eXpFS format.


The [eXperimental Filesystem (eXpFS)](../os-spec/expfs.md) is a simulated filesystem.
A UNIX file named "disk.xfs" simulates the [hard disk](../arch-spec/machine-organization.md)
of the XSM machine. Building eXpOS begins with understanding the underlying filesystem (eXpFS) and its interface [(xfs-interface)](../support-tools/xfs-interface.md) to the host (UNIX) environment. 
The xfs-interface is used for transferring files between your linux system and the xsm disk.

<figure>
<img src="../../assets/img/xfs-interface.png"/>
<figcaption >Schematic interface between linux system and XSM disk
</figcaption></figure>

*In this stage, you will create a text file and load it to the XFS disk using xfs-interface.*

Run the XFS Interface
```
cd $HOME/myexpos/xfs-interface
./xfs-interface
```
This will take you to the xfs-interface prompt.

Start by formatting the disk to the eXpOS file system format in the XFS interface using **fdisk**
command.

The *fdisk&lt;* command converts the raw disk into the filesystem format recognised by the
eXpOS operating system. It initialises the disk data structures such as [disk free list, inode table, user table and root file](../os-design/disk-ds.md).

Type the following commands in the xfs-interface prompt.

```
# fdisk
# exit
```

You will be back in the UNIX shell and a file named **disk.xfs** is created in the
location **$HOME/myexpos/xfs-interface/**. This UNIX file simulates the hard disk of the
XSM machine. The disk is formatted to eXperimental File System (eXpFS) (see [eXpFS Specification](../os-spec/expfs.md)). <br/>
The XSM machine's disk is a sequence of 512 blocks, each block capable of holding
512 words (see [Disk Organization](../os-implementation.md)). The
second block of the formatted disk contains a disk free list which is explained below.

The [Disk Free List](../os-design/disk-ds.md#disk-free-list)
in XFS is a data structure which keeps track of used and unused blocks in the disk. An unused
block is indicated by 0 and a used block is indicated by 1. Check the contents of the Disk
Free List after formatting the disk. Use the **df** command to view the Disk Free List
(stored in disk block number 2). The output will be as follows:

```
0    -   1
1    -   1
2    -   1
3    -   1
4    -   1
5    -   1
6    -   1
7    -   1
8    -   1
9    -   1
10   -   1
11   -   1
12   -   1
13   -   1
14   -   1
15   -   1
16   -   1
17   -   1
18   -   1
19   -   1
20   -   1
21   -   1
22   -   1
23   -   1
24   -   1
25   -   1
.
.
No of Free Blocks = 443
Total No of Blocks = 512
```

The first 69 blocks (blocks 0 to 68) are reserved for stroing various OS data structures and
routines as well as Idle code, INIT program, etc (see [Disk
Organization)](../os-implementation.md). Hence the Disk Free List entries for these are marked as 1 (used) and
the remaining entries for blocks 69 to 511 are 0 (unused).

Create a file in your UNIX machine with sample data. A sample data file is given below:

```
There is a place where the sidewalk ends
And before the street begins,
And there the grass grows soft and white,
And there the sun burns crimson bright,
And there the moon-bird rests from his flight
To cool in the peppermint wind.
```

Save the file as `$HOME/myexpos/sample.dat`

Load this data file `$HOME/myexpos/sample.dat` to the XFS disk from your UNIX
machine. This can be done by the following commands:

```
cd $HOME/myexpos/xfs-interface
./xfs-interface
```

This will take you to the xfs-interface prompt. Type the following commands.

```
# load --data $HOME/myexpos/sample.dat
```

This will load the file to the XFS disk and the following updations happen in disk data
structures :

1) A disk block will be allocated for the file (as `sample.dat` contains less than
512 words) and corresponding to this allocated block (here block 69 - this is because the
1<sup>st</sup> free block is allocated by the allocator), an entry will be marked as 1
(used) in the [Disk Free List](../os-design/disk-ds.md#disk-free-list).

2) An entry in the [InodeTable](../os-design/disk-ds.md#inode-table) will be created for this file. Inode Table contains information such as the file type, file name, file size, userid, permission and the block numbers of the data
of data files loaded through <i>xfs-interface</i> is the <i>root</i>. Userid is the index
of the user entry in the [User Table](../os-design/disk-ds.md#user-table).The userid of <i>root</i> 
is 1 and hence the userid field in the <i>inode table</i> is set to 1 for all data files loaded 
through the <i>xfs interface</i>. The [permission](../os-spec/multiuser.md) is set to open(1). 
Note that any file in eXpFS file system is permitted to have a maximum of four data blocks.

3) An entry for this file will be made in the [Root File](../os-design/disk-ds.md#root-file) also.


Before proceeding further you must be clear about [eXpFS (eXperimental File System)](../os-spec/expfs.md). In the following steps we will see the above mentioned updations.


Find out the block numbers of the Data Blocks corresponding to the loaded file. Use the **copy**
command to copy the <i>Inode Table</i>(Inode Table is stored in disk blocks 3 and 4) to a
UNIX file (say `$HOME/myexpos/inode_table.txt`).

```
# copy 3 4 $HOME/myexpos/inode_table.txt
# exit
```

!!! note 
    The Inode table occupies only the first 960 words (60 entries, each of size 16 words)
    in the disk blocks 3 and 4. [User table](../os-design/disk-ds.md#user-table)
    occupies the next 32 words (16 entries, each of size 2 words) and the last 32 words are reserved for future use.
    (You will learn about User Table later on).

Now check the Inode table entry for the file `sample.dat` in the UNIX file `inode_table.txt`
and find the block numbers of its data blocks. The contents of the file `inode_table.txt`
will be as follows: 

```
1
root
512
0
0
-1
-1
-1
5
-1
-1
-1
-1
-1
-1
-1
2
sample.dat
19
1
1
-1
-1
-1
69
-1
-1
-1
-1
-1
-1
-1
-1
.
.
.
```

!!! note 
    Instead of using the `copy` command you can use [`dump`](../support-tools/xfs-interface.md#dumping-disk-data-structures-to-a-unix-file) command provided by the XFS interface to directly copy
    the disk data structures (inode table, root file) to the UNIX machine as shown below.

```
# dump --inodeusertable
```

This will write the contents of the inodetable into the file `$HOME/myexpos/xfs-interface/inodeusertable.txt`

Now check the contents of the disk free list and verify that the entry for the 69<sup>th</sup>
    block is marked as used. This corresponds to the Data Block 1 of `sample.dat`.


Copy the data blocks from the XFS disk and display it as a UNIX file `$HOME/myexpos/data.txt`.

```
# copy 69 69 $HOME/myexpos/data.txt
```

You will get back the contents of the file `$HOME/myexpos/sample.dat` in `$HOME/myexpos/data.txt`.
However in `$HOME/myexpos/data.txt`, each word is displayed in a line because a word
in XFS is 16 characters long. Sample `data.txt` file is shown below.


```
There is a plac
e where the sid
ewalk ends

And before the
street begins,

And there the g
rass grows soft
and white,

And there the s
un burns crimso
n bright,

And there the m
oon-bird rests
from his flight


To cool in the
peppermint wind
```


xfs-interface provides the [export](../support-tools/xfs-interface.md#export) command to export files from the XSM machine to the UNIX machine
in a single step. Export the file `sample.dat` to the UNIX file `$HOME/myexpos/data.txt`
using <i>xfs-inteface</i> as shown below and verify that the contents are same as sample.dat.


```
# export sample.dat $HOME/myexpos/data.txt
```


??? question "Q1. When a file is created entries are made in the Inode table as well as the Root file. What is the need for this duplication?"
      Inode table is a data structure which is accessible only in Kernel mode, whereas Root
      file is accessible both in Kernel and User mode. This enables the user to search for a
      file from an application program itself by reading the Root file.


!!! assignment "Assignment 1"
    Copy the contents of Root File (from Block 5 of XFS disk) to a UNIX file `$HOME/myexpos/root_file.txt` and verify that an entry for `sample.dat` is made in it also.

!!! assignment "Assignment 2"
    Delete the `sample.dat` from the XSM machine using xfs-interface and note the changes for the entries for this file in *inode
    table, root file and disk free list*.