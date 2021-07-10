---
title: 'Module 3: File Manager'
original_url: http://exposnitc.github.io/os_modules/Module_3.html
---

This module contains the functions that manages files.

!!! warning "Important Note"
    All functions in this module expect that the inode is locked before they are called.

| Function Number    | FunctionName   | Arguments                                 | Return Value               |
| ------------------ | -------------- | ----------------------------------------- | -------------------------- |
| BUFFERED_WRITE = 1 | Buffered Write | Disk Block Number, Offset, Word           | NIL                        |
| BUFFERED_READ = 2  | Buffered Read  | Disk Block Number, Offset, Memory Address | NIL                        |
| OPEN = 3           | Open           | File Name                                 | File Table Index, -1 or -2 |
| CLOSE = 4          | Close          | File Table Index                          | NIL                        |

![](../assets/img/modules/FileManager.png)

###  Buffered Write
The disk page provided is loaded to the corresponding buffer. The word provided is written into the offset position of the buffer.

Buffer managemnet is handled by this function internally.

<pre><code>
Identify the buffer ; 			
/* Buffer Number = (Disk Number % 4) is a simple scheme, 
good enough for our purposes. More efficient schemes are used in real systems */

Acquire the buffer by calling the Acquire_Buffer() function	
in the <a href="../../modules/module-00/">Resource Manager module</a>;

if (the buffer contains a different disk block){  			/* check block number in <a href="../../os-design/mem-ds/#buffer-table">Buffer Table</a>. */
    
    if (the buffer contents are dirty){					/* check DIRTY BIT of buffer table */
            Write back the contents of the buffer
            to the disk by invoking disk_store() 
            function in the <a href="../../modules/module-04/">device manager module</a>;
    }
    
    Load the required disk block into the buffer by invoking
    the disk_load() function in the <a href="../../modules/module-04/">device manager module</a>;

    Set the new Disk block number in the Buffer table entry;
}

Write the contents of the word taken as input into the offset
location in the buffer; 

Mark the buffer as Dirty;

Release the buffer by calling the Release_Buffer() function
in the Resource Manager module;

return;
</code></pre>

Called by the Write system call.

### Buffered Read

The disk page provided is loaded to the corresponding buffer. The word present at the offset position of the buffer is copied to the Memory address provided as input. Buffer management is handled by this function internally.<br> <br>
NOTE: Physical memory address must be provided. 

<pre><code>
Identify the buffer ; 			
/* Buffer Number = (Disk Number % 4) is a simple scheme, 
good enough for our purposes. More efficient schemes are used in real systems */

Acquire the buffer by calling the Acquire_Buffer() function
in the <a href="../../modules/module-00/">Resource Manager module</a>;

if (the buffer contains a different disk block){  			/* check block number in <a href="../../os-design/mem-ds/#buffer-table">Buffer Table</a>. */
    
    if (the buffer contents are dirty){					/* check DIRTY BIT of buffer table */
            Write back the contents of the buffer
            to the disk by invoking disk_store() 
            function in the <a href="../../modules/module-04/">device manager module</a>;
            
            Mark the buffer as clean in the 
            corresponding buffer table entry;
    }
    
    Load the required disk block into the buffer by invoking
    the disk_load() function in the device manager module;

    Set the new Disk block number in the Buffer table entry;
}

Copy the contents in the offset location in the buffer to the
physical address given as input; 
    
Release the buffer by calling the Release_Buffer() function
in the Resource Manager module;

return;
</code></pre>

Called by the Read system call. 

### Open

Locates the file in the inode table and makes an entry in the Open File Table. Returns the Open File Table index or an error code if file does not exist or the table is full. On a successfull open, the file status table entry of the file is incremented.

!!! note
     This function must not be called unless a the calling process has a free entry available in the <a href="../../os-design/process-table/#per-process-resource-table">per-process resource table</a> to store the open file table index returned by this function.

<pre><code>

Find the index of the <a href="../../os-design/disk-ds/#inode-table">Inode Table</a> entry of the file. If the entry is not found, return -1.

Call the <b>acquire_inode()</b> function in the <a href="../../modules/module-00/">Resource Manager</a> module.&nbsp;&nbsp; /* Lock the inode */
If the locking fails, return -1. 

If the file is of type EXEC, <b>release_inode()</b> and return -1. 	/* Only data files can be opened */

Find a free entry in the <a href="../../os-design/mem-ds/#open-file-table">Open File Table</a>.
If there are no free entries, <b>release_inode()</b> and return -2.  /* Reached maximum number of open files in the system. */

<b>If</b> the file name is "root" <b>then</b> 
	Set the INODE INDEX field in the open file table entry to <a href="../../support-tools/constants/">INODE_ROOT</a>. 
<b>else</b>
	In the <a href="../../os-design/mem-ds/#file-inode-status-table">File Status Table</a>, if the File Open Count is -1, set it to 1. Otherwise, increment the File Open Count.
	Set the INODE INDEX field in the open file table entry to the inode table index of the file. 

Set the OPEN INSTANCE COUNT to 1 and LSEEK to 0 in the open file table entry.

Call the <b>release_inode()</b> function in the <a href="../../modules/module-00/">Resource Manager</a> module.&nbsp;&nbsp; /* Free the inode */

return the Open File Table Index.
</code></pre>

Called by the open system call.

!!! question
    Why don't we need to maintain file open count for the root file? We still need to maintain open instance count for the root file, why?
!!! question
    After acquiring the inode, why do we check if the input file name matches the inode table entry?



### Close
Closes the open instance of a file. Assumes a valid Open File Table index is given as input. 


<pre><code>

Find the index of the <a href="../../os-design/disk-ds/#inode-table">Inode Table</a> entry of the file from the Open File Table.

In the <a href="../../os-design/mem-ds/#open-file-table">Open File Table Entry</a>, decrement the Open Instance Count.

If the Open Instance Count becomes 0
	Invalidate the entry by setting all fields to -1.
	If the file is not the "root", decrement the File Open Count in the <a href="../../os-design/mem-ds/#file-inode-status-table">File (Inode) Status Table</a>.
	If the File Open Count in File Status Table becomes 0, set it to -1.
	/* Check the INODE_INDEX field in the Open File Table entry */

return;
</code></pre>


Called by the close, exit system call.