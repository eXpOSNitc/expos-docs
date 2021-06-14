---
title: 'Stage 8 :
                        Handling Timer Interrupt (2 Hours)'
---
<div class="panel-collapse collapse" id="collapse8">
 <div class="panel-body">
  <!-- Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo8">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo8">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Run the XSM machine with Timer enabled.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Familiarise with timer interrupt handling.
        </li>
       </ul>
      </div>
     </li>
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo8a">
       Pre-requisite
                                Reading
      </a>
      <div class="panel-collapse expand" id="lo8a">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Read and understand the
         <a href="Tutorials/xsm_interrupts_tutorial.html" target="_blank">
          XSM
                                      tutorial on Interrupts and Exception handling
         </a>
         before proceeding further.
                                    (Read only the Timer Interrupt part).
        </li>
       </ul>
      </div>
     </li>
    </ul>
   </div>
  </div>
  <!-- End Learning Objectives-->
  <p>
   <b>
    Try to solve the following question that tests your understanding.
   </b>
  </p>
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item">
      <b>
       Q1.
      </b>
      Suppose the XSM machine was executing in unprivileged mode and just after
                              instruction at logical address 3000 was fetched and executed, the machine found that
                              the timer interrupt was pending. Suppose that at this time, the values of the
                              some of the machine registers were as the following :
      <br/>
      IP: 3000.
      <br/>
      PTBR: 29696
      <br/>
      SP 5000
     </li>
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq26">
       <b>
        a)
       </b>
       Which physical memory location will contain the physical page number to which
                                return address will be stored by the machine before transferring control to the timer
                                interrupt handler?
      </a>
      <div class="panel-collapse collapse" id="collapseq26">
       29714 (Why?) It is absolutely necessary that you read the
       <a href="http://exposnitc.github.io/Tutorials/xsm_unprivileged_tutorial.html" target="_blank">
        XSM unpreveleged mode execution tutorial
       </a>
       if you are not able to
                                solve this question yourself.
      </div>
     </li>
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq27">
       <b>
        b)
       </b>
       Suppose further that the memory location 29714 contains value 35. What will
                                be the physical memory address to which the XSM machine will copy the value of the next
                                instruction to be executed?
      </a>
      <div class="panel-collapse collapse" id="collapseq27">
       18313. (Again if you are not able to solve the problem yourself, you must read the
       <a href="http://exposnitc.github.io/Tutorials/xsm_unprivileged_tutorial.html" target="_blank">
        XSM
                                  unpreveleged mode execution tutorial
       </a>
       )
      </div>
     </li>
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq28">
       <b>
        c)
       </b>
       What will be the value stored into the location 18313 by the machine?
      </a>
      <div class="panel-collapse collapse" id="collapseq28">
       3002. This is the (logical) address of the next instruction to be executed after return
                                from the interrupt handler. Note the each XSM instruction occupies two words in memory
                                and hence the next instruction's address is at 3002 (and not 3001).
      </div>
     </li>
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq29">
       <b>
        d)
       </b>
       What value will the SP and IP registers contain after the execution of the
                                INT instruction?
      </a>
      <div class="panel-collapse collapse" id="collapseq29">
       SP=5001 and IP=2048
      </div>
     </li>
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq30">
       <b>
        e)
       </b>
       What will be the physical address from which the machine will fetch the next
                                instruction?
      </a>
      <div class="panel-collapse collapse" id="collapseq30">
       2048. Since the machine switches to privileged mode once the interrupt handler
                                is entered, the next instruction will be fetched from the address pointed to by IP
                                register
                                without performing address translation.
      </div>
     </li>
    </ul>
   </div>
  </div>
  <p>
   If the XSM simulator is run with the the timer set to some value - say 20, then every time the
                        machine completes execution of 20 instructions in user mode, the timer device will send a
                        hardware signal that interrupts machine execution. The machine will push the IP value of the
                        next user mode instruction to the stack and pass control to the the timer interrupt handler at
                        physical address 2048.
  </p>
  <p>
   eXpOS design given
   <a href="os_implementation.html" target="_blank">
    here
   </a>
   requires you to
                        load a timer interrupt routine into two pages of memory starting at memory address 2048 (pages
                        4 and 5). The routine must be written by you and loaded into disk blocks 17 and 18 so that the
                        OS startup code can load this code into memory pages 4 and 5.
  </p>
  <p>
   In this stage, we will run the machine with timer on and write a simple timer interrupt
                        handler.
  </p>
  <b>
   Modifications to OS Startup Code
  </b>
  <br/>
  <br/>
  <p>
   OS Startup code used in the previous stage has to be modified to
                        load the timer interrupt routine from disk blocks 17 and 18 to memory pages 4 and 5.
  </p>
  <div>
   <pre>loadi(4, 17);
loadi(5, 18);</pre>
  </div>
  <br/>
  <b>
   Timer Interrupt
  </b>
  <br/>
  <br/>
  <p>
   We will write the timer interupt routine such that it just prints "TIMER" and returns to the
                        user program.
  </p>
  <ol>
   <pre>
print "TIMER";
ireturn;
</pre>
   <li>
    Save this file in your UNIX machine as $HOME/myexpos/spl/spl_progs/sample_timer.spl
   </li>
   <li>
    Compile this program using the SPL compiler.
   </li>
   <li>
    Load the compiled XSM code as the timer interrupt into the XSM disk using XFS Interface.
    <div>
     <pre>cd $HOME/myexpos/xfs-interface
./xfs-interface
# load --int=timer $HOME/spl/spl_progs/sample_timer.xsm
# exit</pre>
    </div>
   </li>
   <li>
    Recompile and reload the OS Startup code.
   </li>
   <li>
    Run the XSM machine with timer enabled.
   </li>
   <pre>cd $HOME/myexpos/xsm
./xsm --timer 2</pre>
  </ol>
  <!--========= Stage descrptions ends here ===========-->
  <a data-toggle="collapse" href="#collapse8">
   <span class="fa fa-times">
   </span>
   Close
  </a>
 </div>
</div>
