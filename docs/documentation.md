---
original_url: https://exposnitc.github.io/documentation.html
---
Add contents of [Documentation](https://exposnitc.github.io/documentation.html){target=_blank}.


### ARCHITECTURE
eXpOS is basically built upon the XSM architecture. Architecture includes the specifications for the machine organisation, paging and interrupt handling and also provides the machine level instruction set.

#### [Specification](./arch-spec/index.md)
#### [Virtual Machine Model](./virtual-machine-spec.md)
#### [XSM Tutorial](./tutorials/index.md)


### OPERATING SYSTEM
eXpOS is a tiny multiprogramming operating system. It has a very simple specification that allows a junior undergraduate computer science student to implement it in a few months.

#### [Specification](./os-os-spec/index.md)
#### [Design](./os-design/index.md)
#### [Implementation](./os-implementation.md)

### Support Tools
To implement the eXpOS certain tools are provided along with the package. This includes SPL and ExpL compilers, XSM simulator and a UNIX-XFS Interface called XFS interface.

#### [Setting Up](./support-tools/setting-up.md)
#### [XFS Interface](./support-tools/xfs-interface.md)
#### [Constants](./support-tools/constants.md)
#### [SPL](./support-tools/spl.md)
#### [ExpL](./support-tools/expl.md)
#### [XSM Simulator](./support-tools/xsm-simulator.md)


### APPLICATION INTERFACE
The inteface between the application programs and the OS requires the specification of system call intefaces, format of executables, the virtual instruction set, the virtual memory layout and configuration.


#### [Application Binary Interface (ABI)](./abi.md)
#### [Low Level System Call Interface](./os-design/sw-interface.md)
#### [High Level Library Interface (API)](./os-spec/dynamicmemoryroutines.md)
#### [Low Level Library Interface](./abi.md)

### ROADMAP
The roadmap guides you step by step towards the complete implementation of the operating system. Concepts needed for completing each step will be introduced at the appropriate point.

[Proceed to Roadmap :material-road:](./roadmap/index.md){ .md-button .md-button--primary  target=_blank}