<div class="panel-heading" id="list_stage3">
<h4 class="panel-title">
<a data-toggle="collapse" href="#collapse3"><span class="fa fa-check-square-o"></span>Stage 3 :
Bootstrap Loader (2 Hours)</a>
</h4>
</div>
<div id="collapse3" class="panel-collapse collapse">
<div class="panel-body">
<!-- Begin Learning Objectives-->
<div class="container col-md-12">
<div class="section_area">
<ul class="list-group">
<li class="list-group-item" style="background:#dff0d8">
<span class="fa fa-book"></span> &nbsp; <a data-toggle="collapse" href="#lo3">Learning
Objectives</a>
<div id="lo3" class="panel-collapse expand">
<ul>
<li style="margin-bottom: -2px"><span class="fa fa-hand-o-right"></span>&nbsp;&nbsp;
Use the XSM Instruction set to write a small <i>OS startup</i> code.</li>
<li style="margin-bottom: -2px"><span class="fa fa-hand-o-right"></span>&nbsp;&nbsp;
Load your <i>OS startup code</i> into the <i>boot block</i> of the disk and get
this code executed on bootstrap.</li>
</ul>

</div>
</li>
<li class="list-group-item" style="background:#dff0d8">
<span class="fa fa-book"></span> &nbsp; <a data-toggle="collapse" href="#lo3a">Pre-requisite
Reading</a>
<div id="lo3a" class="panel-collapse expand">
<ul>
<li style="margin-bottom: -2px"><span class="fa fa-hand-o-right"></span>&nbsp;&nbsp;
Have a quick look at <a href="arch_spec-files/machine_organisation.html" target="_blank">
XSM Machine Organisation </a> . (Do not spend more than 15 minutes).</li>
<li style="margin-bottom: -2px"><span class="fa fa-hand-o-right"></span>&nbsp;&nbsp;
Have a quick look at <a href="arch_spec-files/instruction_set.html" target="_blank">XSM
Instruction set</a>. (Do not spend more than 15 minutes).</li>
<li style="margin-bottom: -2px"><span class="fa fa-hand-o-right"></span>&nbsp;&nbsp;
It is absolutely necessary to read the <a href="Tutorials/xsm-instruction-cycle.html"
target="_blank"><b>XSM privileged mode execution tutorial</b></a>
before proceeding further.</li>
</ul>

</div>
</li>
</ul>
</div>
</div>
<!-- End Learning Objectives-->

<p>
When the XSM machine is started up, the <a href="arch_spec-files/machine_organisation.html#Boot ROM"
target="_blank"> ROM Code</a>, which resides in page 0 of the memory, is executed. It is
hard-coded into the machine. That is, the ROM code at physical address 0 (to 511) is "already
there" when machine starts up. The ROM code is called the "Boot ROM" in OS literature. Boot ROM
code does the following operations :
<ol style="list-style-type:decimal;margin-left:10vw">
<li>Loads block 0 of the disk to page 1 of the memory (physical address 512).</li>
<li>After loading the block to memory, it sets the value of the register <a href="arch_spec-files/machine_organisation.html"
target="_blank">IP</a> (Instruction Pointer) to 512 so that the next instruction is
fetched from location 512 (page 1 in memory starts from location 512).</li>
</ol>
</p>
<p>In this stage, you will write a small assembly program to print "HELLO_WORLD" using XSM
Instruction set and load it into block 0 of the disk using XFS-Interface as the <b>OS Startup
Code</b>. As described above, this OS Startup Code is loaded from disk block 0 to memory page
1 by the ROM Code on machine startup and is then executed. </p>

<i>The steps to do this are explained in detail below. </i>
<br /><br />

<ol style="list-style-type:decimal;margin-left:2px">
<li>
Create the assembly program to print "HELLO_WORLD". <br>The assembly code to print
"HELLO_WORLD" :
<br><br>
<div>
<pre>
MOV R0, "HELLO_WORLD"
MOV R16, R0
PORT P1, R16
OUT
HALT </pre>
Save this file as <tt>$HOME/myexpos/spl/spl_progs/helloworld.xsm</tt>.
</div>
</li>


<li>
Load the file as OS Startup code to <tt>disk.xfs</tt> using XFS-Interface. Invoke the XFS
interface and use the following command to load the OS Startup Code
<br><br>
<div>
<pre>cd $HOME/myexpos/xfs-interface
./xfs-interface
# load --os $HOME/myexpos/spl/spl_progs/helloworld.xsm
# exit

</pre>
</div>
<i> Note that the <tt>--os</tt> option loads the file to Block 0 of the XFS disk. </i>
</li>

<li> Run the machine
<br><br>
<div>
<pre>cd $HOME/myexpos/xsm
./xsm</pre>
</div>
</li>
</ol>
<br>
The machine will halt after printing "HELLO_WORLD".
<br><br>
<div>
<pre>
HELLO_WORLD
Machine is halting.</pre><br>
<p style="text-indent: 0px"><code>Note :</code> The XSM simulator given to you is an assembly
language interpeter for XSM. Hence, it is possible to load and run assembly
language programs on the simulator (unlike real systems where
binary programs need to be supplied).</p>
</div>

<!--=========== BEGIN contents SECTION ================-->
<div class="container col-md-12">
<div class="section_area">
<ul class="list-group">
<li class="list-group-item">
<a data-toggle="collapse" href="#collapseq2"><b>Q1.</b> If the OS Startup Code is loaded
to some other page other than Page 1, will XSM work fine?</a>
<div id="collapseq2" class="panel-collapse collapse"> No. This is because after the
execution of the ROM Code, IP points to <b>512</b> which is the 1<sup>st</sup>
instruction of Page 1. So if the OS Startup Code is not loaded to Page 1, it results in
an <a href="./arch_spec-files/interrupts_exception_handling.html" target="_blank">exception</a>
and leads to system crash.</div>

</li>
</ul>
</div>
</div>
<p><b style="color:#26A65B">Assignment 1 : </b>Write an assembly program to print numbers from 1
to 20 and run it as the OS Startup code.</p>

<!--<p><b style="color:#26A65B">Assignment 3 : </b> Read and understand the tutorial on <a href="Tutorials/xsm-instruction-cycle.html" target="_blank">XSM Instruction Execution Cycle</a>.</p>-->

<a data-toggle="collapse" href="#collapse3">
<span class="fa fa-times"></span> Close</a>
</div>
</div>

