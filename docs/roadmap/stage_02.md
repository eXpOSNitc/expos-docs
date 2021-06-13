---
title: "Stage 2 : Understanding the Filesystem  (2 Hours)"
---

!!! info "Learning Objectives"
    - Load/retrieve data and executable files from/to your host (Unix) system into the
    XSM disk.
    - Explain the disk data structures of the XFS file system - INODE table, disk free
    list and root file.
    - Find out the data blocks into which a data/executable file is stored in the XSM
    disk by examining the INODE table and root file.

!!! abstract "Pre-requisite Reading"
    - Quickly go through the <a href="os_spec-files/eXpFS.html" target="_blank">Filesystem
    (eXpFS) Specification</a> and <a href="./support_tools-files/xfs-interface.html"
    target="_blank">XFS-Interface Specification</a> (interface between the UNIX
    System and eXpFS). Do not spent more than 30 minutes!


The eXpOS package that you had downloaded in the previous stage consists mainly of a machine
simulator. The machine is called the <b>eXperimental String Machine (XSM)</b> and consists of a
processor, memory and disk. Some support tools that help you to program the machine are also
provided.

<p>One important point to note about the system is that the machine is a bare, and comes with no
software in it (except for a boot ROM). Hence, the only way to insert some software code into
the system is to prepare the code "outside" (that is, in your Linux/Unix system) and insert
your code into the machine. The support tools provided along with the package are precisely
designed to help you with this task.</p>

<p>The package comes with three major support tools - two compilers and a disk interface tool
called <a href="support_tools-files/xfs-interface.html" target="_blank">XFS-Interface</a>. The
compilers allow you to write high level code and translate it into the XSM machine code. We
will look at them in later stages. The XFS-Inteface tool helps you to transfer files between
your Linux/Unix system and the XSM machines disk.</p>

<p> XSM machine's disk contains 512 blocks, each capable of storing
512 words. When files are stored in the disk, some format has
to be followed so that one can figure out where in the disk
are the blocks of a file located.</p>

<p>XSM disk is formatted to what is known as the
<a href="os_spec-files/eXpFS.html" target="_blank">eXpFS file system format</a>. The format
specifies how data as well as
meta-data for each file stored in the disk must be organized. The XFS interface tool allows you
to load data files (and executable files as well) from your Linux/Unix system into the XSM disk
in accordance with the eXpFS format. </p>


<p>The eXpFS format specifies that each data/executable file can span across at most four data
blocks, and that the index to these blocks along with the name and the size of the file must be
stored in a pre-define area of the disk called the <a href="os_design-files/disk_ds.html"
    target="_blank">Inode table</a>. (The inode table is stored in disk blocks 3 and 4).
There are also other pre-defined areas of the disk that stores
meta data about the disk (see description of the <a href="os_design-files/disk_ds.html#root_file"
    target="_blank">root file</a> and
the <a href="os_design-files/disk_ds.html#disk_free_list" target="_blank">disk free list</a>
for more details). When you use XFS interface
to load a file from your Linux/Unix system to the XSM disk, the
interface tool will correctly fill all the required meta data
information as stipulated by the eXpFS format.</p>


<p>The <a href="os_spec-files/eXpFS.html" target="_blank"><b>eXperimental Filesystem (eXpFS)</b></a>
is a simulated filesystem. A UNIX file named "disk.xfs" simulates the <a href="./arch_spec-files/machine_organisation.html"
    target="_blank"><b>hard disk</b></a> of the XSM machine. Building eXpOS begins with
understanding the underlying filesystem (eXpFS) and its interface <a href="./support_tools-files/xfs-interface.html"
    target="_blank">(xfs-interface)</a> to the host (UNIX) environment. The xfs-interface is used
for transferring files between your linux system and the xsm disk.
</p>
<br>
<figure><img src="img/xfs-interface.png" style="display:block;margin-left:auto;margin-right:auto"></img>
<figcaption style="text-align:center">Schematic interface between linux system and XSM disk</figurecaption>
</figure>
<br>
<i> In this stage, you will create a text file and load it to the XFS disk using xfs-interface.</i>
<br /><br />

<ol style="list-style-type:decimal;margin-left:2px">
<li>
    Run the XFS Interface
    <div>
    <pre>cd $HOME/myexpos/xfs-interface
./xfs-interface</pre>
    </div>
    This will take you to the xfs-interface prompt.
</li>
<li>
    Start by formatting the disk to the eXpOS file system format in the XFS interface using <b>fdisk</b>
    command.<br />
    The <i>fdisk</i> command converts the raw disk into the filesystem format recognised by the
    eXpOS operating system. It initialises the disk data structures such as <a href="/os_design-files/disk_ds.html"
    target="_blank">disk free list, inode table, user table and root file </a> .<br />
    Type the following commands in the xfs-interface prompt.
    <div>
    <pre># fdisk
# exit</pre>
    </div>

    <p>You will be back in the UNIX shell and a file named <b>disk.xfs</b> is created in the
    location <b>$HOME/myexpos/xfs-interface/</b>. This UNIX file simulates the hard disk of the
    XSM machine. The disk is formatted to eXperimental File System (eXpFS) (see <a href="os_spec-files/eXpFS.html"
        target="_blank"> eXpFS Specification</a>). <br />
    The XSM machine's disk is a sequence of 512 blocks, each block capable of holding
    512 words (see <a href="os_implementation.html" target="_blank">Disk Organization</a>). The
    second block of the formatted disk contains a disk free list which is explained below.</p>
</li>
<li>
    The <a href="os_design-files/disk_ds.html#disk_free_list" target="_blank">Disk Free List</a>
    in XFS is a data structure which keeps track of used and unused blocks in the disk. An unused
    block is indicated by 0 and a used block is indicated by 1. Check the contents of the Disk
    Free List after formatting the disk. Use the <b>df</b> command to view the Disk Free List
    (stored in disk block number 2). The output will be as follows:
    <div>
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
</div>
    The first 69 blocks (blocks 0 to 68) are reserved for stroing various OS data structures and
    routines as well as Idle code, INIT program, etc (see <a href="os_implementation.html" target="_blank">Disk
    Organization)</a>. Hence the Disk Free List entries for these are marked as 1 (used) and
    the remaining entries for blocks 69 to 511 are 0 (unused).
</li>


<li>Create a file in your UNIX machine with sample data. A sample data file is given below:

    <div>
    <pre>There is a place where the sidewalk ends
And before the street begins,
And there the grass grows soft and white,
And there the sun burns crimson bright,
And there the moon-bird rests from his flight
To cool in the peppermint wind.</pre>
    </div>
    Save the file as <b>$HOME/myexpos/sample.dat</b>
</li>


<li> Load this data file <tt>($HOME/myexpos/sample.dat)</tt> to the XFS disk from your UNIX
    machine. This can be done by the following commands:
<div>
```
cd $HOME/myexpos/xfs-interface
./xfs-interface
```

    </div>
    This will take you to the xfs-interface prompt. Type the following commands.

    <div>
    <pre># load --data $HOME/myexpos/sample.dat</pre>
    </div>
    This will load the file to the XFS disk and the following updations happen in disk data
    structures :
    <ol style="list-style-type:lower-roman;margin-left:60px">
    <li>
        A disk block will be allocated for the file (as <tt>sample.dat</tt> contains less than
        512 words) and corresponding to this allocated block (here block 69 - this is because the
        1<sup>st</sup> free block is allocated by the allocator), an entry will be marked as 1
        (used) in the <a href="os_design-files/disk_ds.html#disk_free_list" target="_blank">Disk
        Free List</a>.
    </li>
    <li>
        An entry in the <a href="os_design-files/disk_ds.html#inode_table" target="_blank"> Inode
        Table</a> will be created for this file. Inode Table contains information such as the
        file type, file name, file size, userid, permission and the block numbers of the data
        blocks of the file. The <a href="os_spec-files/multiuser.html" target="_blank">owner</a>
        of data files loaded through <i>xfs-interface</i> is the <i>root</i>. Userid is the index
        of the user entry in the <a href="os_design-files/disk_ds.html#user_table">User Table</a>.
        The userid of <i>root</i> is 1 and hence the userid field in the <i>inode table</i> is
        set to 1 for all data files loaded through the <i>xfs interface</i>. The <a href="os_spec-files/multiuser.html"
        target="_blank">permission</a> is set to open(1). Note that any file in eXpFS file
        system is permitted to have a maximum of four data blocks.
    </li>
    <li>
        An entry for this file will be made in the <a href="os_design-files/disk_ds.html#root_file"
        target="_blank">Root File</a> also.
    </li>
    </ol>
    <br>
    Before proceeding further you must be clear about <a href="os_spec-files/eXpFS.html" target="_blank"><b>eXpFS
        (eXperimental File System)</b></a>. In the following steps we will see the above
    mentioned updations.
</li>


<li> Find out the block numbers of the Data Blocks corresponding to the loaded file. Use the <b>copy</b>
    command to copy the <i>Inode Table</i>(Inode Table is stored in disk blocks 3 and 4) to a
    UNIX file (say <tt>$HOME/myexpos/inode_table.txt</tt>).

    <div>
    <pre># copy 3 4 $HOME/myexpos/inode_table.txt
# exit</pre>
    </div>

    <code>Note: </code> The Inode table occupies only the first 960 words (60 entries, each of
    size 16 words) in the disk blocks 3 and 4. <a href="./os_design-files/disk_ds.html#user_table"
    target="_blank">User table </a>occupies the next 32 words (16 entries, each of size 2
    words) and the last 32 words are reserved for future use. (You will learn about User Table
    later on).

    <br />

    <br>
    Now check the Inode table entry for the file <tt>sample.dat</tt> in the UNIX file <tt>inode_table.txt</tt>
    and find the block numbers of its data blocks. The contents of the file <tt>inode_table.txt</tt>
    will be as follows: <br><br>
    <div>
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


<code>Note: </code> Instead of using the <tt>copy</tt> command you can use <a href="./support_tools-files/xfs-interface.html#dump"
target="_blank"><tt>dump</tt></a> command provided by the XFS interface to directly copy
the disk data structures (inode table, root file) to the UNIX machine as shown below.

<pre># dump --inodeusertable</pre>

This will write the contents of the inodetable into the file
$HOME/myexpos/xfs-interface/inodeusertable.txt
</div>


</li>


<li> Now check the contents of the disk free list and verify that the entry for the 69<sup>th</sup>
    block is marked as used. This corresponds to the Data Block 1 of <tt>sample.dat</tt>.
</li>


<li>
    Copy the data blocks from the XFS disk and display it as a UNIX file <tt>$HOME/myexpos/data.txt</tt>.
    <br><br>
    <div>
    <pre># copy 69 69 $HOME/myexpos/data.txt</pre>
    </div>
    You will get back the contents of the file <tt>$HOME/myexpos/sample.dat</tt> in <tt>$HOME/myexpos/data.txt</tt>.
    However in <tt>$HOME/myexpos/data.txt</tt>, each word is displayed in a line because a word
    in XFS is 16 characters long. Sample <tt>data.txt</tt> file is shown below.
    <br><br>
    <div>
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

</li>
<br />
<li> xfs-interface provides the <a href="./support_tools-files/xfs-interface.html#export"
    target="_blank">export</a> command to export files from the XSM machine to the UNIX machine
    in a single step. Export the file <tt>sample.dat</tt> to the UNIX file <tt>$HOME/myexpos/data.txt</tt>
    using <i>xfs-inteface</i> as shown below and verify that the contents are same as sample.dat.
    <br><br>
    <div>
    <pre># export sample.dat $HOME/myexpos/data.txt</pre>
    </div>
</li>
</ol>


<details>
<summary>
    <b>Q1.</b> When a file is created entries
    are made in the Inode table as well as the Root file. What is the need for this
    duplication?
</summary>
<p>
Inode table is a data structure which is accessible only in Kernel mode, whereas Root
file is accessible both in Kernel and User mode. This enables the user to search for a
file from an application program itself by reading the Root file.
</p>
</details>


!!! question "Assignment 1"
    Copy the contents of Root File (from Block 5 of XFS disk) to a UNIX file `$HOME/myexpos/root_file.txt` and verify that an entry for `sample.dat` is made in it also.

!!! question "Assignment 2"
    Delete the `sample.dat` from the XSM machine using xfs-interface and note the changes for the entries for this file in *inode
    table, root file and disk free list*.
