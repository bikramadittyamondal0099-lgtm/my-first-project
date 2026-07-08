# my-first-project
# PyChronicle – Week 1 Progress

## Overview

PyChronicle is an AST-Powered Time-Travel Debugger designed to record and visualize the historical state of Python programs. The goal is to allow developers to move backward and forward through program execution without re-running the application.

## Week 1 Objectives

* Learn and explore Python's Abstract Syntax Tree (AST) module.
* Parse Python source files and analyze their structure.
* Detect and extract variable assignments from Python code.
* Design a storage system for execution data using SQLite.
* Build the foundation for future execution tracing and time-travel debugging.

## Work Completed

* Implemented an AST parser capable of reading and analyzing Python source files.
* Developed a custom `NodeVisitor` to identify variable assignments and their corresponding line numbers.
* Created an SQLite database schema to store execution-related information, including timestamps, line numbers, variable names, and values.
* Successfully connected the AST analysis module with the SQLite storage layer.
* Tested the parser using sample Python programs and verified correct extraction of variables and line information.

## Technologies Used

* Python
* AST (Abstract Syntax Tree)
* SQLite3

## Key Learning Outcomes

* Understanding Python code representation through AST nodes.
* Working with the `ast.NodeVisitor` class for code analysis.
* Designing and managing SQLite databases programmatically.
* Building modular components for developer tooling and metaprogramming projects.

## Next Steps (Week 2)

* Implement runtime execution tracing using `sys.settrace()`.
* Capture variable state changes during program execution.
* Store execution traces in SQLite for historical inspection.
* Begin development of the Terminal User Interface (TUI) using Textual.

This week established the core static-analysis and storage infrastructure required for PyChronicle's time-travel debugging system.
