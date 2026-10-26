import os
import sys
import platform

from filesystem import FileSystem   # <-- File Management module
import users                        # <-- User management
import memorymanager as mm          # <-- Process & Memory management

fs = FileSystem()                   # <-- one shared file system for the session

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_help():
    print("\nAvailable Commands:")
    print(" help                -Show available commands")
    print(" clear               -Clear the terminal screen")
    print(" exit                -Shut down MiniOS")

    # Under File Management
    print("\n--- File Management ---")
    print(" dir [folder]        -List files and folders")
    print(" mkdir <folder>      -Create a new directory")
    print(" create <file> [text]-Create a new file")
    print(" read <file>         -Display the contents of a file")
    print(" delete <name>       -Delete a file or an empty folder")
    print(" write <file> <text> -Write text to a file")
    print(" rename <old> <new>  -Rename a file or folder")
    print(" cd <folder>         -Change directory (cd .. goes up)")
    print(" pwd                 -Show the current directory")

    # Under Process Management
    print("\n--- Process Management ---")
    print(" process             -View all processes")
    print(" run <name>          -Create a new process")
    print(" kill <id>           -Kill a process")

    # Under Memory Management
    print("\n--- Memory Management ---")
    print(" memory              -View memory status")
    print(" allocate <id> <MB>  -Allocate memory to a process")
    print(" free <id>           -Free memory from a process")
    print("")

    print("--- User & System Commands ---")
    print(" whoami              -Show current user")
    print(" systeminfo          -Show system information")
    print("")

def exit_os():
    print("\nMiniOSMTB is shutting down... \nBye, I'll miss you")
    sys.exit(0)

def show(result):
    """Print a file system/module result (skips empty strings)."""
    if result:
        print("\n" + result + "\n")

def show_systeminfo():
    print("\n========================================")
    print("           SYSTEM INFORMATION")
    print("========================================")
    print("OS Name: MiniOS MTB")
    print("Version: 1.0")
    print(f"Architecture: {platform.architecture()[0]}")
    print("CPU: Virtual CPU (simulated)")
    print("Memory: 1024 MB (simulated)")
    print(f"User: {users.get_current_user()}")
    print("========================================\n")


def main():
    clear_screen()
    print("========================================================================================================================")
    print("                                                       MINIOS MTB                                                       ")
    print("========================================================================================================================")
    print("\nWelcome to MiniOSMTB!\n")

    if users.login() is None:
        return

    while True:
        try:
            current_path = fs.pwd().strip()
            user_input = input(f"MiniOSMTB:{current_path}> ").strip()
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()
            args = parts[1:]

            if command == "exit":
                exit_os()
            elif command == "help":
                display_help()
            elif command == "clear":
                clear_screen()
                
            # ---------------- File Management ----------------
            elif command == "dir":
                show(fs.dir(args[0] if args else None))
            elif command == "mkdir":
                show(fs.mkdir(args[0] if args else ""))
            elif command == "create":
                show(fs.create(args[0] if args else "", " ".join(args[1:])))
            elif command == "read":
                show(fs.read(args[0] if args else ""))
            elif command == "delete":
                show(fs.delete(args[0] if args else ""))
            elif command == "write":
                if len(args) < 2:
                    show("Usage: write <file> <text>")
                else:
                    show(fs.write(args[0], " ".join(args[1:])))
            elif command == "rename":
                if len(args) < 2:
                    show("Usage: rename <old> <new>")
                else:
                    show(fs.rename(args[0], args[1]))
            elif command == "cd":
                show(fs.cd(args[0] if args else None))
            elif command == "pwd":
                show(fs.pwd())

            # ---------------- Process Management ----------------
            elif command == "process":
                show(mm.list_processes())
            elif command == "run":
                if len(args) < 1:
                    show("Usage: run <name>")
                else:
                    show(mm.run_process(" ".join(args)))
            elif command == "kill":
                if len(args) < 1:
                    show("Usage: kill <id>")
                else:
                    show(mm.kill_process(args[0]))
            
            # ---------------- Memory Management -----------------
            elif command == "memory":
                show(mm.show_memory())
            elif command == "allocate":
                if len(args) < 2:
                    show("Usage: allocate <id> <size>")
                else:
                    show(mm.allocate_memory(args[0], args[1]))
            elif command == "free":
                if len(args) < 1:
                    show("Usage: free <id>")
                else:
                    show(mm.free_memory(args[0]))

            # ---------------- User & System Commands ----------------
            elif command == "whoami":
                users.whoami()
            elif command == "systeminfo":
                show_systeminfo()
            else:
                print(f"\nUnknown command: '{command}'.")
                print("Type 'help' to see the available commands\n")

        except KeyboardInterrupt:
            exit_os()
        except Exception as error:
            print(f"\nError: The command could not be completed: {error}\n")

if __name__ == "__main__":
    main()
