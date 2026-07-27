# my-first-project
# PyChronicle – Week 2 Progress
## Overview
During Week 2, the focus shifted from analyzing Python source code to tracking its execution in real time. The goal was to build the core tracing engine that records how a program executes, captures variable changes, and stores execution history in an SQLite database. This forms the foundation of PyChronicle's time-travel debugging system.
## Week 2 Objectives
* Learn how Python's `sys.settrace()` function works.
* Monitor program execution line by line.
* Capture the current values of variables while the program runs.
* Store execution history in an SQLite database.
* Build the initial structure of a terminal-based interface.
## Work Completed
* I implemented a tracing system using Python's `sys.settrace()`.
* I tracked program execution line by line during runtime.
* I captured local variable values as they changed.
* I connected the tracer to the SQLite database and stored execution records.
* I tested the tracer with sample programs containing loops and variable updates.
* I created the basic structure for the terminal user interface using Textual.
## Technologies Used
* Python
* sys.settrace()
* SQLite3
* Textual
## Key Learning Outcomes
* I learned how Python tracing works internally.
* I understood how to access execution frames and local variables.
* I learned how runtime information can be captured without modifying the original source code.
* I gained experience storing execution history efficiently in a database.
* I built the foundation of a runtime execution tracer.
## Next Steps (Week 3)
* Implement delta compression to store only variable changes.
* Reduce database size by avoiding duplicate execution states.
* Connect the execution history with the Textual interface.
* Build a timeline slider to navigate through previous execution states.
* Highlight the corresponding source code line while moving through history.
This week I successfully built the runtime tracing engine of PyChronicle, allowing the project to record program execution history and preparing the foundation for the time-travel debugging interface.

# PyChronicle – Week 3 Progress (Ongoing)
## Overview
During Week 3, the primary goal is to transform PyChronicle from a runtime tracer into a true time-travel debugger. The focus is on optimizing data storage, improving performance, and creating an interactive interface that allows developers to move backward and forward through a program's execution history.
## Week 3 Objectives
* Implement delta compression for execution history.
* Store only changed variable values instead of complete program states.
* Connect the SQLite database with the Textual interface.
* Develop a timeline slider for navigating execution history.
* Highlight the executed source code line while scrubbing through time.
## Current Work
* Developing the delta compression system.
* Optimizing SQLite queries for faster retrieval.
* Connecting execution records with the terminal interface.
* Designing the timeline navigation system.
* Improving overall performance and reducing memory usage.
## Technologies Used
* Python
* SQLite3
* Textual
* sys.settrace()
## Expected Learning Outcomes
* Understand efficient state management.
* Learn delta-based storage techniques.
* Improve database optimization skills.
* Build interactive terminal applications using Textual.
* Gain deeper knowledge of Python metaprogramming.
## Next Steps (Week 4)
* Package PyChronicle as a command-line application.
* Add watch variables for tracking selected values.
* Improve the user interface and overall experience.
* Prepare the project for final testing and documentation.

Week 3 is currently focused on optimizing performance and building the interactive time-travel interface that will allow developers to inspect historical program states efficiently.
