---
title: "ExpL Specification"
original_url: https://exposnitc.github.io/support_tools-files/expl.html
---

ExpL is a simple programming language designed specifically for instructional purposes. Application programs for eXpOS may be written in ExpL.


### [:link: Specification Of ExpL](https://silcnitc.github.io/expl.html){ target=_blank }

### The `exposcall()` interface 
The ExpL compiler supplied along with the eXpOS pakage  extents the language with an additional eXpOS library
interface function exposcall().  ExpL programs can invoke eXpOS system calls and dynamic memory
allocation routines supported by the library by passing appropriate arguments to the exposcall() function.
The exposcall() interface is given in detail [here](../os-spec/dynamicmemoryroutines.md)