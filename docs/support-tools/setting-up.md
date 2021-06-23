---
title: Setting up
original_url: https://exposnitc.github.io/support_tools-files/setting-up.html
---

## Setting up

1) Install prerequisites such as gcc, make, readline, flex/lex, bison/yacc

=== "Debian-based distros"
    ```
    sudo apt-get install libreadline-dev flex bison make gcc wget curl
    ```
=== "RedHat Linux based distros"
    ```
    sudo yum install readline-devel flex flex-devel byacc make gcc wget curl
    ```
=== "Arch Linux"
    ```
    sudo pacman -S readline flex bison make gcc wget curl
    ```

2) In your terminal, copy and paste the following snippet and press enter:
```
curl -sSf https://raw.githubusercontent.com/eXpOSNitc/expos-bootstrap/main/download.sh | sh
```

When the script finishes executing, you will have a directory `myexpos` in your home drectory, with all components required for building your own eXpOS.

3) Change directory to myexpos directory.

```
cd $HOME/myexpos 
```

4) Make to build all the components.

```
make
```

If the setup worked correctly, the following executables will be created:

- **spl** in `$HOME/myexpos/spl` folder
- **expl** in `$HOME/myexpos/expl` folder
- **xfs-interface** in `$HOME/myexpos/xfs-interface` folder
- **xsm** in `$HOME/myexpos/xsm` folder

If the setting up of the system is done correctly the following directories will be created.

![](../assets/img/xsm_folders.png)

-   **$HOME/myexpos/expl**  
    This directory contains the [ExpL](./expl.md) (Experimental Language) compiler required to compile user programs to XSM machine instructions.
  
-   **$HOME/myexpos/spl**  
    This directory contains the [SPL](./spl.md) (System Programmer's Language) Compiler required to compile system programs (i.e. operating system routines) to XSM machine instructions.
  
-   **$HOME/myexpos/xfs-interface**  
    This directory contains an interface ([XFS Interface](./xfs-interface.md) or eXperimental File System Interface) through which files from your UNIX machine can be loaded into the File System of XSM. The interface can format the disk, dump the disk data structures, load/remove files, list files, transfer data and executable files between eXpFS filesystem and the host (UNIX) file system and copy specified blocks of the XFS disk to a UNIX file.
  
-   **$HOME/myexpos/xsm**  
    This directory contains the machine simulator ([XSM](./xsm-simulator.md) or eXperimental String Machine).
  
-   **$HOME/myexpos/test**  
    This directory contains the test scripts for [eXpOS](../os-spec/index.md)



## <span style="color:red">Setting Up (NEXSM)</span>

!!! warning
    This is relevant only for Stage 28 of the Roadmap.

1) Download the complete eXpOS package from [here](https://github.com/eXpOSNitc/eXpOSNitc.github.io/raw/master/package/nexpos.tar.gz).

2) Copy the tar file to your home directory.
```
cp nexpos.tar.gz $HOME/
cd $HOME
```

3) Extract the contents using the command.
```
tar -xvf nexpos.tar.gz 
```

Now you will have a directory myexpos in your home drectory, with all components required for building your own eXpOS.

4) Install `libreadline-dev` package 
```
sudo apt-get install libreadline-dev 
```

5) Make sure all the prerequisites which include `gcc`, `flex`/`lex` and `bison`/`yacc` are installed. In Ubuntu/Debian systems, use `apt` to install `flex` and `bison`
```
sudo apt-get install flex bison 
```

6) Change directory to `mynexpos` directory.
```
cd $HOME/mynexpos 
```

7) Make to build all the components.
```
./make
```

If the setup worked correctly, the following executables will be created:

- **spl** in `$HOME/mynexpos/nespl` folder
- **expl** in `$HOME/mynexpos/expl` folder
- **xfs-interface** in `$HOME/mynexpos/nexfs-interface` folder
- **xsm** in `$HOME/mynexpos/nexsm` folder

If the setting up of the system is done correctly the following directories will be created.


![](../assets/img/nexsm_folders.png)

-   **$HOME/mynexpos/expl**  
    This directory contains the [ExpL](./expl.md) (Experimental Language) compiler required to compile user programs to NEXSM machine instructions.
  
-   **$HOME/mynexpos/nespl**  
    This directory contains the [SPL](./spl.md) (System Programmer's Language) Compiler required to compile system programs (i.e. operating system routines) to NEXSM machine instructions.
  
-   **$HOME/mynexpos/nexfs-interface**  
    This directory contains an interface ([XFS Interface](./xfs-interface.md) or eXperimental File System Interface) through which files from your UNIX machine can be loaded into the File System of NEXSM. The interface can format the disk, dump the disk data structures, load/remove files, list files, transfer data and executable files between eXpFS filesystem and the host (UNIX) file system and copy specified blocks of the XFS disk to a UNIX file.
  
-   **$HOME/mynexpos/nexsm**  
    This directory contains the machine simulator ([NEXSM](./xsm-simulator.md) or NExt eXperimental String Machine).
  
-   **$HOME/mynexpos/test**  
    This directory contains the test scripts for [eXpOS](../os-spec/index.md).