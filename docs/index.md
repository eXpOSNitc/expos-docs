---
hide:
    - navigation
    - toc
---
# eXpOS NITC
<div style="float: right; border-style: solid; padding: 16px; border-radius: 16px; margin: 16px;">
    <h5>Project Infomation:</h5>
    <p>
    Source Code:
    <a href="https://github.com/exposnitc">https://github.com/exposnitc</a>
    <br/>
    Contact:
    <a href="https://groups.google.com/g/xos-users">Google Group</a>
    <br/>
    <span style="color: red;">Trial version</span>, errors are being corrected as reported.
    <br/>
    Last updated: 5th April 2021 (see <a href="/releases/">Release Notes</a>) 
    </p>
</div>

Project eXpOS (eXperimental Operating System) is an on-line educational platform which helps undergraduate students to learn the working on an operating system. A detailed project roadmap that is part of the platform provides step by step guidance to the student towards writing a small operating system from scratch. The student learns the implementation of various OS data structures and kernel routines during the course of the project. The OS written by the student will run on a machine simulator supplied along with the platform. The project assumes that the student has undergone a course in computer organization, and is comfortable with programming.

## Roadmap
If you wish to work on the project, the approach we suggest is to follow the project roadmap. The roadmap takes you through a step by step journey towards the complete implementation of the operating system. At each step, you will be asked to read concepts, specifications and interfaces that are required for that step. In fact, you will be asked to read only what is necessary for completing that step. The links to the relevant reading material will be given at appropriate places in the roadmap. Proceed to [Roadmap :material-road:](https://exposnitc.github.io/Roadmap.html){target=_blank}.

## Final System
![Final User View](img/user-view.png){ align=left } If you are curious about what the "final system" you are going to build looks like, we give a brief overview here. You are warned not to get lost in the links. The roadmap will ask you to read the appropriate parts of the documentation as and when required. 

In the figure, an architecture simulator for the eXperimental String Machine (XSM) is given to you. Your primary job is to implement the eXpOS kernel for this machine in such a way that application programs can be loaded and executed by your kernel. You will also be asked to write a few application programs,­ like the shell (for providing a user interface).