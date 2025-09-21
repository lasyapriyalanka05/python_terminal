
import os
import sys
import shlex
import subprocess

# --- Shell State ---
command_history = []
# Environment variables are managed here. We start by copying the system's environment.
shell_env = os.environ.copy()

# --- BUILT-IN COMMAND FUNCTIONS ---


def cd_cmd(args):
    """Changes the current working directory."""
    # Go to the HOME directory if no path is specified
    path = args[0] if args else shell_env.get("HOME", "/")
    try:
        os.chdir(path)
    except FileNotFoundError:
        print(f"cd: no such file or directory: {path}")
    except Exception as e:
        print(f"cd: an error occurred: {e}")


def history_cmd(args):
    """Prints the command history."""
    for i, cmd in enumerate(command_history, 1):
        print(f"{i: >4}  {cmd}")


def exit_cmd(args):
    """Exits the terminal."""
    print("Goodbye!")
    sys.exit(0)


def export_cmd(args):
    """Sets an environment variable. Usage: export VAR=value"""
    if not args:
        # If no args, print all shell environment variables
        for key, value in shell_env.items():
            print(f"{key}={value}")
        return

    for arg in args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            shell_env[key] = value
        else:
            print(f"export: invalid format: {arg}. Use VAR=value")


# --- Built-in Command Dispatcher ---
BUILTIN_COMMAND_MAP = {
    'cd': cd_cmd,
    'history': history_cmd,
    'exit': exit_cmd,
    'export': export_cmd,
}

# --- Core Execution Logic ---


def execute_command(parts):
    """Executes a simple, single command."""
    if not parts:
        return

    command = parts[0]
    args = parts[1:]

    # Expand environment variables ($VAR or ${VAR}) in arguments
    expanded_args = [os.path.expandvars(arg) for arg in args]

    if command in BUILTIN_COMMAND_MAP:
        BUILTIN_COMMAND_MAP[command](expanded_args)
    else:
        try:
            # Pass the shell's current environment to the subprocess
            result = subprocess.run(
                [command] + expanded_args,
                capture_output=True,
                text=True,
                check=False,
                env=shell_env
            )
            if result.stdout:
                print(result.stdout, end='')
            if result.stderr:
                print(result.stderr, end='')
        except FileNotFoundError:
            print(f"{command}: command not found")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Main Application Loop (REPL) 


def main():
    """The main Read-Evaluate-Print Loop with advanced parsing stubs."""
    while True:
        try:
            prompt = f"py-term:{os.getcwd()} $ "
            user_input = input(prompt)

            if not user_input.strip():
                continue

            command_history.append(user_input)

            # --- ADVANCED PARSING LOGIC ---
            # This is where a real shell gets complex.
            # For now, we'll just check for pipes as a demonstration.
            if "|" in user_input:
                # TODO: Implement piping logic
                print("Piping feature is not yet implemented.")
                # A real implementation would create a pipeline of subprocesses,
                # connecting the stdout of one to the stdin of the next.
                continue
            elif ">" in user_input or ">>" in user_input:
                # TODO: Implement redirection logic
                print("Redirection feature is not yet implemented.")
                # A real implementation would parse the filename and redirect
                # the command's stdout to that file.
                continue

            # If no special characters, proceed with simple execution
            parts = shlex.split(user_input)
            execute_command(parts)

        except KeyboardInterrupt:
            print("\n")
        except EOFError:
            print("exit")
            break


if _name_ == "_main_":
    main()
