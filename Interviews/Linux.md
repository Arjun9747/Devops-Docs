**What happens when we execute a command in Linux Terminal? (including system calls) **

 1. You type a command in the terminal and press Enter. The terminal emulator captures the input and sends it to the shell (e.g., Bash, Zsh).

 2. The shell parses the command to determine what action to take. It breaks down the command into individual words (tokens) and identifies any special characters, such as pipes (|), redirects (>, <), or background execution (&).
 3. The shell searches for the command in its internal cache (hash table) or in the directories specified in the PATH environment variable. If the command is found, the shell retrieves its path and prepares to execute it.
 4. The shell uses the fork() system call to create a new process, which is a copy of the shell process. This new process is called the child process.
  the child process, the shell uses the exec() system call to replace the process's memory with the new command's code. The exec() call loads the command's executable file into memory and transfers control to it.
 5. When the command needs to interact with the operating system, it uses system calls (e.g., open(), read(), write(), close()) to request services from the kernel. The kernel provides these services and returns control to the command.
 6. The command executes and performs its intended action. If the command produces output, it writes to the standard output (stdout) or standard error (stderr) streams.
 7. When the command completes its execution, it terminates using the exit() system call. The kernel reclaims the resources allocated to the process.
 8. he parent process (the shell) receives a signal (SIGCHLD) indicating that the child process has terminated. The shell can then retrieve the child process's exit status using the wait() system call.
 9.  After the child process terminates, the shell displays a new command prompt, indicating that it's ready to accept the next command.

**System Calls Involved:**

fork(): Creates a new process by duplicating an existing one.

exec(): Replaces the current process image with a new one.

exit(): Terminates the current process and returns an exit status.

wait(): Suspends execution of the current process until one of its children terminates.

open(), read(), write(), close(): Used for file input/output operations.

kill(): Sends a signal to a process (not directly used in command execution, but relevant in process management).
