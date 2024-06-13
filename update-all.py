import os
from aliases_config import aliases

def add_or_update_alias_in_shell_config(shell_config_path, alias_name, command):
    alias_line = f"alias {alias_name}='{command}'\n"
    # Read the current shell config content
    if os.path.exists(shell_config_path):
        with open(shell_config_path, 'r') as file:
            lines = file.readlines()
    else:
        lines = []
    # Remove any existing lines that define the alias
    lines = [line for line in lines if not line.startswith(f"alias {alias_name}=")]
    # Add the new alias line
    lines.append(alias_line)
    print(f"Alias '{alias_name}' added or updated in {shell_config_path}.")
    # Write the updated lines back to the shell config file
    with open(shell_config_path, 'w') as file:
        file.writelines(lines)

def add_current_dir_to_shell_config(shell_config_path):
    current_dir = os.getcwd()
    env_var_line = f"export EasyModularScriptsDir='{current_dir}'\n"
    # Read the current shell config content
    if os.path.exists(shell_config_path):
        with open(shell_config_path, 'r') as file:
            lines = file.readlines()
    else:
        lines = []
    # Remove any existing lines that define the environment variable
    lines = [line for line in lines if not line.startswith("export EasyModularScriptsDir=")]
    # Add the new environment variable line
    lines.append(env_var_line)
    print(f"Environment variable 'EasyModularScriptsDir' added or updated in {shell_config_path}.")
    # Write the updated lines back to the shell config file
    with open(shell_config_path, 'w') as file:
        file.writelines(lines)

def update_env_files_with_current_dir():
    current_dir = os.getcwd()
    env_var_line = f"EasyModularScriptsDir='{current_dir}'\n"
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file == ".env":
                env_path = os.path.join(root, file)
                # Read the current .env content
                if os.path.exists(env_path):
                    with open(env_path, 'r') as file:
                        lines = file.readlines()
                else:
                    lines = []
                # Remove any existing lines that define the environment variable
                lines = [line for line in lines if not line.startswith("EasyModularScriptsDir=")]
                # Add the new environment variable line
                lines.append(env_var_line)
                print(f"Environment variable 'EasyModularScriptsDir' added or updated in {env_path}.")
                # Write the updated lines back to the .env file
                with open(env_path, 'w') as file:
                    file.writelines(lines)

def main():
    bashrc_path = os.path.expanduser("~/.bashrc")
    zshrc_path = os.path.expanduser("~/.zshrc")

    for alias_name, command in aliases.items():
        add_or_update_alias_in_shell_config(bashrc_path, alias_name, command)
        add_or_update_alias_in_shell_config(zshrc_path, alias_name, command)

    add_current_dir_to_shell_config(bashrc_path)
    add_current_dir_to_shell_config(zshrc_path)

    update_env_files_with_current_dir()

    # Reload the shell config files to apply changes
    # print("Create a new window to update changes") # exec bash fixes this

if __name__ == "__main__":
    main()
