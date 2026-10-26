# MiniOS MTB

## User Manual, Technical Documentation, and Contrition Reports:
### https://docs.google.com/document/d/1hAqNpA6dP0OhKlG2ADuQ4q1T0B6WRsqrisFWJa8mnnI/edit?usp=sharing

## Demonstration Video
### https://youtu.be/9xREmRYXbzE

## Group Members:

- Eliel Zicri B. Cabarles - Project Leader 
- JC Allen Abangan - CLI Developer 
- Denmark Izra Nunieza - File Management Developer
- Tom Aeron Turbanos - Process and Memory Developer
- Christian Joseph Eguilos - User/System Developer

## Project Description

MiniOS MTB is a command-line operating system simulator developed in Python. It is designed to demonstrate core operating system concepts, including a centralized command shell, file navigation, process execution tracking, and memory allocation. It runs entirely through the Windows Command Prompt (CMD) and does not require a graphical user interface.

## Features

Command-Line Interface: Dynamic shell prompt with active directory tracking and error handling.

File Management: Simulate creating, reading, editing, and navigating files and directories.

Process Simulation: Automatically generate Process IDs (PIDs) and track process states (Ready, Running, Terminated).

Memory Simulation: Allocate and free simulated RAM blocks to specific running processes.

User Management: Login system restricting access to authenticated users.

System Information: Display current user and simulated hardware specifications.

## Requirements:

Python 3.x
Windows Command Prompt (CMD)

## How to Run:

- Clone the repository to your local machine.
- Open Windows Command Prompt (CMD).
- Navigate to the project folder using the cd command.
- Run the main file by typing: ***python main.py***


Log in using your assigned credentials (e.g., admin. username:admin password:admin123).

## Available Commands

### General Commands

- help - Show available commands
- clear - Clear the terminal screen
- exit - Shut down MiniOS

### File Management

- dir [folder] - List files and folders
- mkdir <folder> - Create a new directory
- create <file> [text] - Create a new file
- read <file> - Display the contents of a file
- delete <name> - Delete a file or an empty folder
- write <file> <text> - Write text to a file
- rename <old> <new> - Rename a file or folder
- cd <folder> - Change directory (cd .. goes up)
- pwd - Show the current directory

### Process Management

- process - View all active and terminated processes
- run <name> - Start a new process (automatically assigns a PID)
- kill <id> - Terminate a process and release its memory

### Memory Management

- memory - View total, available, and allocated memory status
- allocate <id> <MB> - Allocate a specific amount of memory to a process
- free <id> - Manually free memory from a process

# User & System Commands

- whoami - Show the current logged-in user
- systeminfo - Show system architecture and specs
