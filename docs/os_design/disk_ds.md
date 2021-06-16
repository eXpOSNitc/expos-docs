---
title: 'Disk Data Structures'
original_url: 'http://eXpOSNitc.github.io/os_design-files/disk_ds.html'
---





Disk Data Structures































 



























  

  

  




Inode Table
-----------


  

  

The Inode table is stored in the disk and has an entry for each file present in the disk (A copy of the Inode table is maintained in the memory when the OS is running). It consists of MAX\_FILE\_NUM entries. Thus [eXpFS](../os_spec-files/eXpFS.html) permits a maximum of MAX\_FILE\_NUM files. This version of eXpOS sets MAX\_FILE\_NUM = 60. 


 Each Inode table entry stores the name, size, type and data block numbers of a file stored in the disk ( * In [Multiuser](http://exposnitc.github.io/os_spec-files/multiuser.html) extension of eXpOS, userid and permission are also included in the inode table entry). The current version of eXpOS limits the maximum number of blocks in an eXpFS file to MAX\_FILE\_BLOCKS = 4. Each Inode table entry consists of 16 words of which the 7 are unused in the present version of eXpOS. 


 eXpoS reserves the first entry in the Inode table for the [root file](disk_ds.html#root_file). The root file is a special file containing details about other files stored in the system. 


The entry of an Inode table has the following format:




|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FILE TYPE | FILE NAME | FILE SIZE | USER ID | PERMISSION | Unused (3 words) | DATA BLOCK 1 | DATA BLOCK 2 | DATA BLOCK 3 | DATA BLOCK 4 | Unused (4 words) |


* **FILE TYPE**  (1 word) - specifies the type of the given file ([DATA](../support_tools-files/constants.html), [EXEC](../support_tools-files/constants.html) or [ROOT](../support_tools-files/constants.html)). More information about file types is given [here](../os_spec-files/eXpFS.html).
* **FILE NAME** (1 word) - Name of the file
* **FILE SIZE** (1 word) - Size of the file. Maximum size for File = MAX\_FILE\_SIZE = 2048 words
* **USER ID** (1 word) - User Id of the owner of the file.
* **PERMISSION** (1 word) - Permission of the file; it can be [OPEN\_ACCESS](../support_tools-files/constants.html) or [EXCLUSIVE](../support_tools-files/constants.html).
* **Unused** (3 words)
* **DATA BLOCK 1 to 4** (4 words) - each DATA BLOCK column stores the block number of a data block of the file. If a file does not use a particular DATA BLOCK , it is set to -1.
* **Unused** (4 words)


An unused entry is indicated by -1 in the FILE NAME field.


**Note 1** : fdisk command of XFS Interface initilizes the inode table entry of the root file with values FILE TYPE = 1, FILE SIZE = 512, and DATA BLOCK = 5 (Root file is stored in block 5 of disk. See [Disk Organisation](../os_implementation.html)).


**Note 2** : A Free inode entry is denoted by  **-1**  in the  **FILENAME**  field.


**Note 3 :** Memory copy of the Inode Table is present in page 59 of the memory (see [Memory Organisation](../os_implementation.html)), and the SPL constant [INODE\_TABLE](../support_tools-files/constants.html) points to the starting address of the table.


 **Importanat Note:** eXpOS requires that the index of the inode table entry of a file and the 
 index of its root file entry must match. For example, suppose the 5th entry of the inode table holds
 information about a file, then the entry for the same file in the root must be the 5th entry. XFS
 interface stores files into the disk following this convention.






  

  



  

  

  




Disk Free List
--------------


  

  

The Disk Free List consists of DISK\_SIZE entries. (The value of DISK\_SIZE is fixed to 512 in the present version). Each entry is of size one word and thus, the size of the disk free list is DISK\_SIZE = 512 words. For each block in the disk there is an entry in the Disk Free List which contains either 0 (free) or 1 (used). 


When the system starts up, the OS startup code loads the Disk Free List to memory. It is stored back when the system halts or a Shutdown system call is executed.


**Note :** Memory copy of the Disk Free List is present in page 61 of the memory (see [Memory Organisation](../os_implementation.html)), and the SPL constant [DISK\_FREE\_LIST](../support_tools-files/constants.html) points to the starting address of the table.






  

  




  

  

  




Root File
---------


  

  

The Root File is stored in the disk and has an entry for each file present in the disk (A copy of the Root File is maintained in the memory when the OS is running). It consists of MAX\_FILE\_NUM entries. Thus eXpFS permits a maximum of MAX\_FILE\_NUM files. This version of eXpOS sets MAX\_FILE\_NUM = 60. 


 The root file has the name **root** and contains meta-data about the files stored in the file system. For each file stored in eXpFS, the root stores five words of information - file-name, file-size, file-type and username, permission in the case of [Multiuser](http://exposnitc.github.io/os_spec-files/multiuser.html) extension of eXpOS. This 5-tuple is called the root entry for the file. The first root entry is for the root itself. Each Root File entry consists of 8 words of which the last 3 are unused in the present version of eXpOS. 


The entry of Root file has the following format:




|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| FILE NAME | FILE SIZE | FILE TYPE | USER NAME | PERMISSION | Unused |


* **FILE NAME** (1 word) - Name of the file
* **FILE SIZE** (1 word) - Size of the file
* **FILE TYPE**  (1 word) - Specifies the type of the given file (ROOT indicated by 1 , DATA indicated by 2 or EXEC indicated by 3).
* **USER NAME** (1 word) - Name of the owner of the file
* **PERMISSION** (1 word) - Permission of the file; open-access (1) or exclusive (0)
* **Unused** (3 words)


An unused entry is indicated by -1 in the FILE NAME field.


**Note :** Memory copy of the Root File is present in page 62 of the memory (see [Memory Organisation](../os_implementation.html)), and the SPL constant [ROOT\_FILE](../support_tools-files/constants.html) points to the starting address of data structure.


 **Important Note:** eXpOS requires that the index of the inode table entry of a file and the 
 index of its root file entry must match. For example, suppose the 5th entry of the inode table holds
 information about a file, then the entry for the same file in the root must be the 5th entry. XFS
 interface stores files into the disk following this convention.








  

  

  




User Table
----------


  

  

The User table is stored in the disk and has an entry for each user. (A copy of the User table is maintained in the memory when the OS is running). It consists of MAX\_USER\_NUM entries. This version of eXpOS sets MAX\_USER\_NUM = 16 including entries for the kernel and the root. 


 Each User table entry stores the user name and encrypted password of a user. Each User table entry consists of 2 words. 


The entry of an User table has the following format:




|  |  |
| --- | --- |
| USER NAME | ENCRYPTED PASSWORD |


* **USER NAME** (1 word) - Name of the user
* **ENCRYPTED PASSWORD** (1 word) - Password of the user in an encrypted form.


   

 All unused entries are set to -1.  
  

 The User table entry for two special users - the kernel and root are set at the time of disk formatting.  







  

  








































