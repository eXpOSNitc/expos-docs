---
title: XFS Interface Usage Specification
original_url: https://exposnitc.github.io/support_tools-files/xfs-interface.html
---

**XFS Interface** (eXperimental File System Interface) is an external interface to access the [eXpFS filesystem](../os-spec/expfs.md) of the eXpOS "from the host (UNIX) system". The filesystem is simulated on a binary file called **disk.xfs**. The interface can format the disk, dump the disk data structures, load/remove files, list files, transfer data and executable files between eXpFS filesystem and the host (UNIX) file system and copy specified blocks of the XFS disk to a UNIX file.

Within your xfs-interface directory, use the following command to run the interface
```
./xfs-interface
```

!!! note
    XFS interface must not be run while the XSM simulator is run concurrently as it might leave the file system in inconsistent state.

You can also run a single command in the xfs-interface by
```
./xfs-interface < command >
```

The various commands available in XFS Interface are discussed below.

### **Help**  
*   _Syntax_ : `help`
*   _Semantics_ : It displays the general syntax and function of all the commands.

### **Disk Formatting**     
*   _Syntax_ : `fdisk`
*   _Semantics_ : It is used to create the disk (”disk.xfs”) or to format the disk if already created. On a newly created/formatted disk default entries for the [Disk Free List](../os-design/disk-ds.md#disk_free_list), [Inode Table](../os-design/disk-ds.md#inode_table), [Root File](../os-design/disk-ds.md#root_file) and [User Table](../os-design/disk-ds.md#user_table) are initialized according to the XFS [implementation](../os-implementation.md) for the XSM machine. These include entries for the root file in the Inode table, entry for the root file itself in the root file, entry for the special users "root" and "system" in the user table etc.

### **Loading Files**  

The command **load** is used to load files from the UNIX filesystem to the XFS disk. The type of the file that is loaded is specified by the first argument. The second argument `<pathname>` is the path to the UNIX file which is to be loaded to the filesystem.

The command checks the size of the [executable/data file](../os-spec/expfs.md), allocates the required number of blocks for the file, updates the [disk free list](../os-design/disk-ds.md#disk_free_list) and creates the corresponding [inode table](../os-design/disk-ds.md#inode_table) and [root file](../os-design/disk-ds.md#root_file) entries for the file. xfs-interface recognizes the disk blocks designated for the timer, console and disk interrupt handlers, the exception handler, idle process, the shell code, OS modules and the OS startup code by the [eXpOS implementation](../os-implementation.md) on the XSM machine and loads these modules to the appropriate places.

The various **load** commands are listed below :  

*   _Syntax_ : `load --exec <pathname>`  
    _Semantics_ : Loads an executable file to XFS disk after allocating sufficient disk blocks and creating [inode table](../os-design/disk-ds.md#inode_table) and root file entries.
*   _Syntax_ : `load --data <pathname>`  
    _Semantics_ : Loads a data file to XFS disk after allocating sufficient disk blocks and creating [inode table](../os-design/disk-ds.md#inode_table) and root file entries.
*   _Syntax_ : `load --init <pathname>`  
    _Semantics_ : Loads INIT/Login code to the recognised XFS [disk blocks](../os-implementation.md).  

!!! note
    Login code will be the INIT code in Multi User mode implementation of eXpOS.

*   _Syntax_ : `load --os <pathname>`  
    _Semantics_ : Loads OS startup code to the recognised XFS [disk blocks](../os-implementation.md).
*   _Syntax_ : `load --idle <pathname>`  
    _Semantics_ : Loads Idle code to the recognised XFS [disk blocks](../os-implementation.md).
*   _Syntax_ : `load --shell <pathname>`  
    _Semantics_ : Loads Shell code to the recognised XFS [disk blocks](../os-implementation.md).
*   _Syntax_ : `load --library <pathname>`  
    _Semantics_ : Loads Library to the recognised XFS [disk blocks](../os-implementation.md) .
*   _Syntax_ : `load --int=timer <pathname>`  
    _Semantics_ : Loads Timer Interrupt routine to the recognised XFS [disk blocks](../os-implementation.md).
*   _Syntax_ : `load --int=disk <pathname>`  
    _Semantics_ : Loads Disk Interrupt routine to the recognised XFS [disk blocks](../os-implementation.md).
*   _Syntax_ : `load --int=console <pathname>`  
    _Semantics_ : Loads Console Interrupt routine to the recognised XFS [disk blocks](../os-implementation.md).
*   _Syntax_ : `load --int=[4-18] <pathname>`  
    _Semantics_ : Loads the specified Interrupt routine to the recognised XFS [disk blocks](../os-implementation.md).
*   _Syntax_ : `load --exhandler <pathname>`  
    _Semantics_ : Loads exception handler routine to the recognised XFS [disk blocks](../os-implementation.md).
*   _Syntax_ : `load --module [0-7] <pathname>`  
    _Semantics_ : Loads a module to the the recognised XFS [disk blocks](../os-implementation.md).
    
### **Exporting Files**  
    
The command **export** is used to export _data files_ from the XFS disk to the UNIX filesystem. The argument `<xfs_filename>` specifies the file which is to be exported and the argument `<pathname>` specifies the UNIX file to which it is to be exported.

The command searches the [inode table](../os-design/disk-ds.md#inode_table) entries for the data file and copies all the blocks corresponding to the file to the UNIX file specified. Note that if the argument `   ` is not given the file will be stored at **$HOME/myexpos/xfs-interface/** and named as `<xfs_filename>`.

-   _Syntax_ : `export <xfs_filename> <pathname>`  
    _Semantics_ : Exports a data file from XFS disk to UNIX file system.
    
### **Removing Files**  
    
The command **rm** is used to remove files from the XFS disk. The argument `<xfs_filename>` specifies the file which is to be removed.

The command searches the [inode table](../os-design/disk-ds.md#inode_table) entries for the file (executable/data file) and clears the blocks corresponding to the file, updates the [disk free list](../os-design/disk-ds.md#disk_free_list) and removes root file and inode table entries. Only data and executable files can be removed.

-   _Syntax_ : `rm <xfs_filename>`  
    _Semantics_ : Removes an executable/data file from XFS disk.
    
### **Listing Files**   
*   _Syntax_ : `ls`
*   _Semantics_ : It lists all the files which are loaded into the filesystem. The size of the file is also displayed in number of words. This is done by traversing through the [inode table](../os-design/disk-ds.md#inode_table) entries.

###  **Display Disk Free List**  
*   _Syntax_ : `df`
*   _Semantics_ : It displays the [Disk Free List](../os-design/disk-ds.md#disk_free_list). It also displays the total number of blocks and the number of free blocks.

### **Display File Contents**  
*   _Syntax_ : `cat <xfs_filename>`
*   _Semantics_ : It displays the contents of a file in the filesystem. The [inode table](../os-design/disk-ds.md#inode_table) entries are searched to get the blocks corresponding to the file and then the blocks are displayed.
  
### **Copying Disk Blocks to a UNIX File**  
      
*   _Syntax_ : `copy <start_block> <end_block> <unix_filename>`  
    _Semantics_ : It copies the contents of specified block(s) in the filesystem to an external UNIX file and the file will be stored at **$HOME/myexpos/xfs-interface/** directory. The arguments `<start_block>` and `<end_block>` denotes the range of blocks to be copied (including both). `<unix_filename>` specifies the destination UNIX file to which the contents are copied.

### **Dumping Disk Data Structures to a UNIX File**  
The command **dump** is used to dump/export the [disk data structures](../os-design/disk-ds.md) (inode table and root file) to the predefined UNIX files as follows. The files are dumped to **$HOME/myexpos/xfs-interface/** directory.

*   _Syntax_ : `dump --inodeusertable`  
    _Semantics_ : It copies the contents of inode table and user table to an external UNIX file named inodeusertable.txt.
*   _Syntax_ : `dump --rootfile`  
    _Semantics_ : It copies the contents of root file to an external UNIX file named rootfile.txt.


### **Batch Mode Execution of Instructions**  
      
*   _Syntax_ : `run <pathname>`  
    _Semantics_ : It executes the set of xfs-interface commands specified in the `<pathname>`, sequentially. Note that, the set of commands in the file should be separated by a new line. For example, a batch file that loads timer, disk and console interrupt handlers might appear appear as below:  
      
    <pre><code>
    load --int=timer $HOME/myexpos/spl/spl_programs/timer.xsm
    load --int=disk $HOME/myexpos/spl/spl_programs/disk.xsm
    load --int=console $HOME/myexpos/spl/spl_programs/console.xsm
    </code></pre>
        
### **Exit Interface**  
*   _Syntax_ : `exit`  
    _Semantics_ : It quits the interface.

### <span style="color:red">XFS-Interface Instructions for NEXSM</span>
    
The following are the modifications to the XFS-interface for NEXSM:

-   _Syntax_ : `load --os=primary <pathname>`  
    _Semantics_ : Loads OS startup code for the primary core to the recognised XFS [disk blocks](../os-implementation.md).
-   _Syntax_ : `load --os=secondary <pathname>`  
    _Semantics_ : Loads OS startup code for the secondary core to the recognised XFS [disk blocks](../os-implementation.md).
-   _Syntax_ : `load --int=\[4-19\] <pathname>`  
    _Semantics_ : Loads the specified Interrupt routine to the recognised XFS [disk blocks](../os-implementation.md).
-   _Syntax_ : `load --module \[0-11\] <pathname>`  
    _Semantics_ : Loads the specified Module to the recognised XFS [disk blocks](../os-implementation.md).