---
title: 'Stage 19 :
                        Exception Handler (6 Hours)'
---
<div class="panel-collapse collapse" id="collapse19">
 <div class="panel-body">
  <!-- Begin Learning Objectives-->
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo19">
       Learning
                                Objectives
      </a>
      <div class="panel-collapse expand" id="lo19">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Familiarize with page fault exception in XSM.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Implementation of Exception handler.
        </li>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         Modify the exec system call to load code pages of a process on
         <a href="https://en.wikipedia.org/wiki/Demand_paging" target="_blank">
          demand
         </a>
         .
        </li>
       </ul>
      </div>
     </li>
     <li class="list-group-item" style="background:#dff0d8">
      <span class="fa fa-book">
      </span>
      <a data-toggle="collapse" href="#lo19a">
       Pre-requisite Reading
      </a>
      <div class="panel-collapse expand" id="lo19a">
       <ul>
        <li style="margin-bottom: -2px">
         <span class="fa fa-hand-o-right">
         </span>
         It is absolutely necessary to have clear understanding about
         <a href="Tutorials/xsm_interrupts_tutorial.html#exception_handling_in_XSM" target="_blank">
          Exception handling in XSM
         </a>
         before proceeding further.
        </li>
       </ul>
      </div>
     </li>
    </ul>
   </div>
  </div>
  <!-- End Learning Objectives-->
  <br/>
  <br/>
  <p>
   This stage introduces you to exception handling in eXpOS. There are four events that result in
                        generation of an exception in XSM. These events are a) illegal memory access, b) illegal
                        instruction, c) arithmetic exception and d) page fault. When one of this events occur, the XSM
                        machine raises an exception and control is transferred to the exception handler. The exception
                        handler code used in previous stages contains only halt instruction which halts the system in
                        the case of an exception. Clearly it is inappropriate to halt the system (all the processes are
                        terminated) for exception occured in one process. In this stage, we implement the exception
                        handler which takes appropriate action for each exception. The exception handler occupies
   <b>
    page
                          2 and 3 in the memory and blocks 15 and 16 in the disk
   </b>
   . See disk and memory organization
   <a href="os_implementation.html" target="_blank">
    here
   </a>
   . There are 4 special registers in XSM
                        which are used to obtain the cause of the exception and the information related to the
                        exception. These registers are
   <b>
    EC, EIP, EPN and EMA
   </b>
   . The cause of the exception is
                        obtained from the value present in the EC register.
  </p>
  <p>
   Exception handler mechanism gives a facility to resume the execution of the process after the
                        corresponding exception has been taken care of. It is not always possible to resume the
                        execution of the process, as some events which cause the exception cannot be corrected. In this
                        case, the proper action is to halt the process gracefully. For the events 1) illegal memory
                        access (EC=2) 2) illegal instruction (EC=1) and 3) arithmetic exception (EC=3), the exception
                        handler just prints the cause of the exception. These cases occur because the last instruction
                        executed (in the currently running user process) resulted in the corresponding error condition.
                        As the OS is not reponsible for correcting these conditions (why?), the exception handler halts
                        the process gracefully and then invokes the scheduler to run other processes.
  </p>
  <br/>
  <p>
   The
   <b>
    page fault exception
   </b>
   (EC=0) occurs when the last instruction in the currently
                        running application tried to either -
   <br/>
   <b>
    a)
   </b>
   Access/modify data from a legal address within its address space, but the page
                        was set to invalid in the page table or
   <br/>
   <b>
    b)
   </b>
   fetch an instruction from a legal address
                        within its address space, whose page table entry is invalid.
  </p>
  <br/>
  <p>
   In either case, the exception occured not because of any error from the side of the
                        application, but because the OS had not loaded the page and set the page tables. In such case,
   <b>
    the exception handler resumes the execution of the process after allocating the required page(s) for the process and attaching the page(s) to the process (by setting page table entries appropriately).  If the faulted page is a code page, the OS needs to load the page from the disk to the newly allocated memory.
   </b>
  </p>
  <br/>
  <div style="background-color: #dff0d8; padding: 24px; border-radius: 24px">
   <p>
    But why should the OS not allocate all the pages required for a process when the process is
                          initialized by the Exec system call, as we were doing in the previous two stages? The reason
                          is that this method of pre-allocation allows fewer concurrent processes to run than with the
                          present strategy of "lazy allocation" to be described now. The strategy followed in this
                          stage is to start executing a process with just one page of code and two pages of stack
                          allocated initially. When the process, during execution, tries to access a page that was not
                          loaded, an exception is generated and the execption handler will allocate the required page.
                          If the required page is a code page, the page will be transferred from the disk to the
                          allocated memory. Since pages are allocated only on demand, memory utilization is better (on
                          the average) with this approach.
   </p>
  </div>
  <br/>
  <p>
   In previous stage, exec system call allocated 2 memory pages each for the heap and the stack.
                        It also allocated and loaded all the code pages of the process. We will modify exec to allocate
                        memory pages for only stack (2 pages).
   <b>
    No memory pages will be allocated to heap.
                          Consequently, the entries in the page table corresponding to heap are set to invalid. For
                          code blocks, only a single memory page is allocated and the first code block is loaded into
                          that memory page.
   </b>
   In previous stage, the job of allocating a new memory page and loading
                        a code block into that memory page is done by
   <i>
    Get Free Page
   </i>
   and
   <i>
    Disk Load
   </i>
   functions respectively. Now, we will write new module function
   <b>
    Get Code Page
   </b>
   in the
   <a href="os_modules/Module_2.html" target="_blank">
    memory manager module
   </a>
   for simultaneously
                        allocating a memory page and loading a code block. This function will be invoked from exec to
                        allocate one memory page and load the first code block into that memory page. Note that only
                        the first code page entry in the page table is set to valid, while remaining 3 entries are set
                        to invalid.
  </p>
  <p>
   Each process has a data structure called
   <a href="os_design-files/process_table.html#disk_map_table" target="_blank">
    <b>
     Per-process Disk map table
    </b>
   </a>
   . The disk map table stores the disk
                        block numbers corresponding to the memory pages used by the process.
   <b>
    Each disk map table has
                          10 words
   </b>
   of which one is for user area page, two for heap, four for code and two for
                        stack pages. Remaining one word is unused. Whenever the copy of the memory page of a process is
                        present in some disk block, that disk block number is stored in the per-process Disk Map Table
                        entry corresponding to that memory page. This is done to keep track of the disk copy of memory
                        pages. The SPL constant
   <a href="support_tools-files/constants.html" target="_blank">
    DISK_MAP_TABLE
   </a>
   gives the starting address of the Disk Map Table of process with PID as 0. The disk map table
                        for any process is obtained by adding PID*10 to DISK_MAP_TABLE.
  </p>
  <p>
   In this stage we will modify the exec system call to initialize the disk map table for the
                        newly created process. The code page entries of the process's Disk Map Table are filled with
                        the disk block numbers of the executable file being loaded from the inode table. Remaining
                        entries are set to invalid (-1). (In later stages, when we swap out the process to disk, we
                        will fill the stack and the heap entries with the disk block numbers used for swapping. More
                        about this will be discussed in later stages).
  </p>
  <br/>
  <p>
   <b>
    The
    <i>
     Get Code Page
    </i>
    function takes as input the block number of a single code block,
                          and loads that block into a memory page.
   </b>
   Code pages are shared by the processes running
                        the same program. The purpose of this function is to find out if the current code block is
                        already in use by some other process. This is done by going through the disk map table entries
                        of all the processes checking for the code block (block number provided as argument). If found,
                        then the
   <b>
    Get Code Page
   </b>
   checks if the code block is loaded into a memory page (entry in
                        the corresponding page table should be valid). If the code block is already present in some
                        memory page, then Get Code Page function just returns that memory page number. If not, a new
                        memory page is allocated by invoking the
   <b>
    Get Free Page
   </b>
   function of the
   <a href="os_modules/Module_2.html" target="_blank">
    memory manager module
   </a>
   . This is followed by loading the code block into
                        the newly allocated memory page using the
   <b>
    Disk Load
   </b>
   function of the
   <a href="os_modules/Module_4.html" target="_blank">
    device manager module
   </a>
   . The Get Code Page function finally returns the
                        memory page number.
  </p>
  <br/>
  <p>
   The exception handler first switches to the kernel stack and backs up the register context as
                        done by any other hardware interrupt routine. The exception handler then uses EC register to
                        find out the cause of the exception. If the cause of the exception is other than page fault,
                        exception handler should print the appropriate error message to notify the user about the
                        termination of the process. As these exceptions cannot be corrected, exception handler must
                        terminate the process by invoking the
   <b>
    Exit Process
   </b>
   function of
   <a href="os_modules/Module_1.html" target="_blank">
    process manager module
   </a>
   and invoke the scheduler to schedule other
                        processes.
  </p>
  <p>
   The register EIP saves the logical IP value of the instruction which has raised the
                        exception. The register EPN stores the logical page number of the address that has caused the
                        page fault.
   <b>
    Note that eXpOS is designed such that, page fault exception can only occur for
                          heap and code pages.
   </b>
   Library pages are shared by all processes so they are always present
                        in the memory. Stack pages are neccessary to run a process and are accessed more frequently. So
                        both library and stack pages for a process should be present in the memory.
                        Based on the value present in Exception Page Number (EPN) register, the exception handler finds
                        out whether page fault has caused for heap or code page. When page fault has occured for heap
                        page (EPN value 2 or 3), exception handler allocates 2 new memory pages by invoking the
   <b>
    Get
                          Free Page
   </b>
   function in
   <a href="os_modules/Module_2.html" target="_blank">
    memory manager
                          module
   </a>
   . If the page fault has occured for a code page, then the exception handler invokes
                        the
   <b>
    Get Code Page
   </b>
   function in memory manager module. The page table of the process is
                        updated to store the page number obtained from Get Code Page or Get Free Page functions. After
                        handling the page fault exception, the exception handler restores the register context,
                        switches to user stack and returns to user mode.
  </p>
  <p>
   <b>
    Note:
   </b>
   When page fault occurs for one heap page, the current eXpOS 
                        design allocates two pages for the heap.  This can be optimized further to
                        make the allocation lazier by allocating just one heap page and deferring 
                        allocation of a second page till a page fault occurs again for the second page. 
                        However, the lazier strategy causes some complications in the implementation of 
                        the Fork system call in the next stage.  Here, we have chosen to keep the design simple
                        by allocating both the heap pages when only one is demanded.
  </p>
  <br/>
  <div style="background-color: #dff0d8; padding: 24px; border-radius: 24px">
   <p>
    Upon return to user mode, the instruction in the application that caused the
                          exception must be re-executed. This indeed is the correct execution semantics as the machine
                          had
                          failed to execute the instruction that generated the
                          exception. The XSM hardware sets the address of the instruction in
                          the EIP register at the time of entering the exception.
                          After completing the actions
                          of the exception handler,
                          the OS must place this address on the top of the application program's stack
                          before returning control back to user mode.
                          An OS can implement
    <b>
     Demand Paging
    </b>
    , as we will be doing here, only if the underlying
                          machine hardware supports re-execution of the instruction that caused a page fault.
   </p>
  </div>
  <br/>
  <p>
   The
   <b>
    Free Page Table
   </b>
   function of the
   <a href="os_modules/Module_1.html">
    process manager
                          module
   </a>
   decrements the memory reference count (in the
   <a href="os_design-files/mem_ds.html#mem_free_list" target="_blank">
    memory free list
   </a>
   ) of the memory pages acquired by a process. If some
                        stack/heap page is swapped in the disk, the reference count of the corresponding disk block is
                        decremented in the
   <a href="os_design-files/disk_ds.html#disk_free_list" target="_blank">
    disk
                          free list
   </a>
   . Note that in the present stage, we allocate the stack/heap pages of a process
                        in memory and never allocate any disk block to store stack/heap pages. Thus, the disk free list
                        decrement is a vaccous step in the present stage. However this will be useful for later stages.
                        Hence we design the module function in advance to meet the future requirements. The following
                        is a brief explanation on why this step can be useful later.
  </p>
  <p>
   As already seen in
   <a href="" target="_blank">
    Stage 2
   </a>
   , eXpOS maintains the
   <a href="os_design-files/disk_ds.html#disk_free_list" target="_blank">
    disk free list
   </a>
   to keep track of disk block allocation.
   <b>
    In later
                          stages, the OS will allocate certain disk blocks to a process temporarily.
                          This is done to swap out the heap/stack pages of a process when the OS finds shortage of
                          memory space to run all the processes.
   </b>
   If a heap/stack page of a process is swapped out
                        into some disk block, the page can be released to some other process. In such cases, the page
                        table entry for the swapped out page will be set to invalid, but the entry corresponding to the
                        page in the
   <a href="os_design-files/process_table.html#disk_map_table" target="_blank">
    disk
                          map table
   </a>
   will contain the disk block number to which the page has been swapped out. The
                        disk free list entry for the block will be greater than zero as the block is no longer free.
                        (It can happen that multiple processes share the block. The disk free list entry for the block
                        will indicate the count of the number of processes sharing the disk block.)
  </p>
  <p>
   <b>
    When the page table entries of a process are invalidated using the
    <i>
     Free Page Table
    </i>
    function of the process manager module,
   </b>
   (either when a process exits or when the exec
                        system call replaces the current process with a new one)
   <b>
    it is necessary to ensure that any
                          temporary disk blocks allocated to the process are also released.
   </b>
   Hence the free page
                        table function checks whether the disk map table entry of a stack/heap page contains a valid
                        disk block number, and if so decrements its disk free list entry by invoking the
   <b>
    Release
                          Block
   </b>
   function of the memory manager module.
  </p>
  <br/>
  <figure style="text-align: center;">
   <img src="img/roadmap/exec3.png" style="display:block;margin-left:auto;margin-right:auto"/>
   <br/>
   <figcaption>
    Control flow for
    <i>
     Exec
    </i>
    system call
   </figcaption>
  </figure>
  <br/>
  <ol style="list-style-type: decimal; margin-left: 2px">
   <li>
    <b>
     Modifications of
     <a href="os_design-files/exec.html" target="_blank">
      exec system call
     </a>
    </b>
   </li>
   <p style="text-indent: 0px">
    1) Don't allocate memory pages for heap. Instead, invalidate page table entries for heap.
    <br/>
    2) Change the page allocation for code pages from previous stage. Invoke the
    <b>
     Get Code Page
    </b>
    function for the first code block and update the page table entry for this first code page.
                          Invalidate rest of the code pages entries in the page table.
    <br/>
    3) Initialize the disk map table of the process. The code page entries are set to the disk
                          block numbers from inode table of the program (program given as argument to exec). Initialize
                          rest of the entries to -1.
    <br/>
    With these modifications, You have completed the final implementation of Exec system call.
                          The full algorithm is provided
    <a href="os_design-files/exec.html" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <li>
    <b>
     Get Code Page (function number = 5,
     <a href="os_modules/Module_2.html" target="_blank">
      memory
                              manager module
     </a>
     )
    </b>
   </li>
   <p style="text-indent: 0px">
    1) Check the
    <a href="os_design-files/process_table.html#disk_map_table" target="_blank">
     disk
                            map table
    </a>
    entries of
    <b>
     all the processes
    </b>
    , if the given block number is present in
                          any entry and the corresponding page table entry is valid then return the memory page number.
                          Also increment the memory free list entry of that page. Memory Free list entry is incremented
                          as page is being shared by another process.
    <br/>
    2) If the code page is not in memory, then invoke
    <b>
     Get Free Page
    </b>
    function in the
    <a href="os_modules/Module_2.html" target="_blank">
     memory manager module
    </a>
    to allocate a new
                          page.
    <br/>
    3) Load the disk block to the newly acquired memory page by invoking the
    <b>
     Disk Load
    </b>
    function of the
    <a href="os_modules/Module_4.html" target="_blank">
     device manager module
    </a>
    .
    <br/>
    4) Return the memory page number to which the code block has been loaded.
    <br/>
   </p>
   <br/>
   <li>
    <b>
     Modification to the Free Page Table (function number = 4,
     <a href="os_modules/Module_1.html" target="_blank">
      process manager module
     </a>
     )
    </b>
   </li>
   <p style="text-indent: 0px">
    1) Go through the heap and stack entries in the
    <a>
     disk map table
    </a>
    of the process with
                          given PID. If any valid entries are found, invoke the
    <b>
     Release Block
    </b>
    function in the
    <a href="os_modules/Module_2.html" target="_blank">
     memory manager module
    </a>
    .
    <br/>
    2) Invalidate all the entries of the disk map table.
   </p>
   <br/>
   <li>
    <b>
     Release Block (function number = 4,
     <a href="os_modules/Module_2.html" target="_blank">
      Memory
                              Manager Module
     </a>
     )
    </b>
   </li>
   <p style="text-indent: 0px">
    1) Decrement the count of the disk block number in the memory copy of the Disk Free List.
    <br/>
    2) Return to the caller.
   </p>
   <p style="text-indent: 0px">
    <code>
     Note :
    </code>
    <b>
     Get Code Page
    </b>
    ,
    <b>
     Free Page Table
    </b>
    and
    <b>
     Release Block
    </b>
    functions implemented above are final versions. They will not
                          require modification in later stages.
   </p>
   <br/>
   <li>
    <b>
     Implementation of
     <a href="os_design-files/exe_handler.html" target="_blank">
      Exception
                              Handler
     </a>
    </b>
   </li>
   <br/>
   <figure style="text-align: center;">
    <img src="img/roadmap/exception.png" style="display:block;margin-left:auto;margin-right:auto"/>
    <br/>
    <figcaption>
     Control flow for Exception handler
    </figcaption>
   </figure>
   <br/>
   <p style="text-indent: 0px">
    1) Set the MODE FLAG to -1 in the
    <a href="os_design-files/process_table.html" target="_blank">
     process
                            table
    </a>
    of the current process, indicating in exception handler.
    <br/>
    2) Switch to the kernel stack and backup the register context and push EIP onto the stack.
    <br/>
    3) If the cause of the exception is other than page fault (EC is not equal to 0) or if the
                          user stack is full (when userSP is PTLR*512-1, the return address can't be pushed onto the
                          stack), then print a meaningful error message. Then invoke the
    <b>
     Exit Process
    </b>
    function
                          to halt the process and invoke the scheduler.
    <br/>
    4) If page fault is caused due to a code page, then get the code block number to be loaded
                          from the
    <a href="os_design-files/process_table.html#disk_map_table" target="_blank">
     disk map
                            table
    </a>
    . For this block, invoke the
    <b>
     Get Code Page
    </b>
    function present in the
    <a href="os_modules/Module_2.html" target="_blank">
     memory manager module
    </a>
    . Update the page table entry for this code page,
                          set the page number to memory page obtained from
    <b>
     Get Code Page
    </b>
    function and auxiliary
                          information to "1100".
    <br/>
    5) If page fault is caused due to a heap page, then invoke the Get Free Page function of the
    <a href="os_modules/Module_2.html" target="_blank">
     memory manager module
    </a>
    twice to allocate two memory pages for the heap. Update
                          the page table entry for these heap pages, set the page numbers to the memory pages obtained from
                          Get Free Page function and set auxiliary information to "1110".
    <br/>
    6) Reset the MODE FLAG to 0. Pop EIP from the stack and restore the register context.
    <br/>
    7) Change to the user stack. Increment the stack pointer, store the EIP value onto the
                          location pointed to by SP and return to the user mode. (Address translations needs to be done on the SP to find the stack address to which EIP is to be stored)
   </p>
   <p>
    The Exception handler implementation given above is final. The full algorithm is given
    <a href="os_design-files/exe_handler.html" target="_blank">
     here
    </a>
    .
   </p>
   <br/>
   <li>
    <b>
     Modification to the Boot Module
    </b>
   </li>
   <p>
    Initialize the disk map table entries for the INIT process. Load the Disk Free List from the
                          disk block 2 to the memory page 61. (See disk and memory organization
    <a href="os_implementation.html" target="_blank">
     here
    </a>
    .)
   </p>
  </ol>
  <br/>
  <b>
   Making things work
  </b>
  <br/>
  <br/>
  <p>
   Compile and load the modified and newly written files into the disk using the XFS-interface.
  </p>
  <div class="container col-md-12">
   <div class="section_area">
    <ul class="list-group">
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq15">
       <b>
        Q1.
       </b>
       Does EPN always equal to the
                                logical page number of EIP?
      </a>
      <div class="panel-collapse collapse" id="collapseq15">
       No. Page fault can occur in two situations. One possibility is during insturction fetch
                                - if the instruction pointer points to an invalid page. In this case, the missing
                                virtual page number (EPN) corresponds to the logical page number of the EIP. The second
                                possibility is during instruction execution when an operand fetch/memory write accesses
                                a page that is not loaded. In this case EPN will indicate the page number of the
                                missing page, and not the logical page number corresponding to EIP value.
      </div>
     </li>
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq15a">
       <b>
        Q2.
       </b>
       Why does the exception handler
                                terminate the process when the userSP value is PTLR*512-1 ?
      </a>
      <div class="panel-collapse collapse" id="collapseq15a">
       The XSM machine doesn't push the return address into the user stack when the exception
                                occurs, instead it stores the address in the EIP register. Hence, for the exception
                                handler to return to the instruction which caused the exception, the EIP register value
                                must be pushed onto the top of the user stack of the program. However, when the
                                application's stack is full (userSP = PTLR*512-1), there is no stack space left to
                                place the return address and the only sensible action for the OS is to terminate the
                                process.
      </div>
     </li>
     <li class="list-group-item">
      <a data-toggle="collapse" href="#collapseq15b">
       <b>
        Q2.
       </b>
       Why does the exception handler
                                save the contents of the EIP register immediately into the kernel stack upon entry into
                                the exception handler?
      </a>
      <div class="panel-collapse collapse" id="collapseq15b">
       The execption handler may block for a disk read and invoke the scheduler during it's
                                course of execution. The value of the EIP register must be stored before scheduling
                                other processes as the current value will be overwritten by the machine if an exception
                                occurs in another application that is scheduled in this way.
      </div>
     </li>
    </ul>
   </div>
  </div>
  <p>
   <b style="color:#26A65B">
    Assignment 1:
   </b>
   Write an ExpL program to implement a linked list.
                      Your program should first read an integer N, then read N intergers from console and store them in
                      the linked list and print the linked list to the console. Run this program using shell version-I
                      of stage 17.
  </p>
  <p>
   <b style="color:#26A65B">
    Assignment 2:
   </b>
   Use the
   <a href="support_tools-files/xsm-simulator.html" target="_blank">
    XSM debugger
   </a>
   to dump the contents of the Exception Flag registers upon entry into the Exception Handler. Also, print out the contents of the Disk Map Table and the Page Table after the Get Code Page function (inside the Memory Manager module).
  </p>
  <br/>
  <br/>
  <a data-toggle="collapse" href="#collapse19">
   <span class="fa fa-times">
   </span>
   Close
  </a>
 </div>
</div>
