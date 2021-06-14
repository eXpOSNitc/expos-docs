---
title: 'Stage 5 :
                        XSM Debugging (2 Hours)'
---
<div class="panel-collapse collapse" id="collapse5">
 <div class="panel-body">
  <!-- Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo5">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo5">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Getting familiarised with the XSM Debugger.
        </li>
       </ul>
      </div>
     </li>
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo5a">
       Pre-requisite
                                Reading
      </a>
      <div class="panel-collapse expand" id="lo5a">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Read and understand
                                    the
         <a href="support_tools-files/xsm-simulator.html" target="_blank">
          Debugger
                                      Specification
         </a>
         .
        </li>
       </ul>
      </div>
     </li>
    </ul>
   </div>
  </div>
  <!-- End Learning Objectives-->
  <p>
   In this stage you will write an SPL program with a
   <b>
    breakpoint
   </b>
   statement. The
                        breakpoint statement translates to the
   <a href="arch_spec-files/instruction_set.html" target="_blank">
    BRKP
   </a>
   machine instruction and is used for debugging.

                        If the XSM machine is run in the
   <a href="support_tools-files/xsm-simulator.html" target="_blank">
    Debug
                          mode
   </a>
   ,
                        on encountering the BRKP instruction, the machine simulator will suspend the program execution
                        and allow you to inspect
                        the values of the registers, memory, os data structures etc. Execution resumes only after you
                        instruct the simulator to proceed.
  </p>
  <ol style="list-style-type:decimal;margin-left:2px">
   <li>
    Write an SPL code to generate odd numbers from 1 to 10. Add a debug instruction in between
                          :
    <div>
     <pre>
alias counter R0;
counter = 0;
while(counter &lt;= 10) do
  if(counter%2 != 0) then
    <b>breakpoint;</b>
  endif;
  counter = counter + 1;
endwhile; </pre>
    </div>
   </li>
   <br/>
   <li>
    Compile the program using the SPL compiler.
   </li>
   <li>
    Load the compiled xsm code as OS startup code into the XSM disk using the XFS interface.
   </li>
   <li>
    Run the machine in debug mode.
    <pre>cd $HOME/myexpos/xsm
./xsm --debug</pre>
   </li>
   <li>
    The Machine pauses after the execution of the first BRKP instruction.
    <br/>
    <br/>
    View the contents of registers using the command
    <pre>reg</pre>
    Enter the following command
    <pre>mem 1</pre>
    This will write the contents of memory page 1 to the file mem inside the xsm folder (if xsm
                          is run from any other directory then the file mem will be created in that directory).
                          Open this file and view the contents.
    <br/>
    <br/>
    Use the following command step to the next instruction.
    <pre>s</pre>
   </li>
   <li>
    Press c to continue execution till the BRKP instruction is executed again.
                          You can see that the content of R0 register changes during each iteration.
    <pre>c</pre>
   </li>
  </ol>
  <a data-toggle="collapse" href="#collapse5">
   <span class="fa fa-times">
   </span>
   Close
  </a>
 </div>
</div>
