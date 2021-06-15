---
title: XFS Interface Usage Specification
original_url: https://exposnitc.github.io/support_tools-files/xfs-interface.html
---

**XFS Interface** (eXperimental File System Interface) is an external interface to access the [eXpFS filesystem](../os_spec-files/eXpFS.html) of the eXpOS "from the host (UNIX) system". The filesystem is simulated on a binary file called **disk.xfs**. The interface can format the disk, dump the disk data structures, load/remove files, list files, transfer data and executable files between eXpFS filesystem and the host (UNIX) file system and copy specified blocks of the XFS disk to a UNIX file.

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