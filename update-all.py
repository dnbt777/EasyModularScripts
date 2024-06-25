import os
from aliases_config import aliases

def add_or_update_alias_in_shell_rc(alias_name, command, shell_rc):
    rc_path = os.path.expanduser(f"~/{shell_rc}")
    alias_line = f"alias {alias_name}='{command}'\n"
    
    if os.path.exists(rc_path):
        with open(rc_path, 'r') as file:
            lines = file.readlines()
    else:
        lines = []
    
    lines = [line for line in lines if not line.startswith(f"alias {alias_name}=")]
    lines.append(alias_line)
    print(f"Alias '{alias_name}' added or updated in {shell_rc}.")
    
    with open(rc_path, 'w') as file:
        file.writelines(lines)

def add_current_dir_to_shell_rc(shell_rc):
    rc_path = os.path.expanduser(f"~/{shell_rc}")
    current_dir = os.getcwd()
    env_var_line = f"export EasyModularScriptsDir='{current_dir}'\n"
    
    if os.path.exists(rc_path):
        with open(rc_path, 'r') as file:
            lines = file.readlines()
    else:
        lines = []
    
    lines = [line for line in lines if not line.startswith("export EasyModularScriptsDir=")]
    lines.append(env_var_line)
    print(f"Environment variable 'EasyModularScriptsDir' added or updated in {shell_rc}.")
    
    with open(rc_path, 'w') as file:
        file.writelines(lines)

def update_env_files_with_current_dir():
    current_dir = os.getcwd()
    env_var_line = f"EasyModularScriptsDir='{current_dir}'\n"
    
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file == ".env":
                env_path = os.path.join(root, file)
                
                if os.path.exists(env_path):
                    with open(env_path, 'r') as file:
                        lines = file.readlines()
                else:
                    lines = []
                
                lines = [line for line in lines if not line.startswith("EasyModularScriptsDir=")]
                lines.append(env_var_line)
                print(f"Environment variable 'EasyModularScriptsDir' added or updated in {env_path}.")
                
                with open(env_path, 'w') as file:
                    file.writelines(lines)

def main():
    shell_rc_files = ['.bashrc', '.zshrc']
    
    for shell_rc in shell_rc_files:
        for alias_name, command in aliases.items():
            add_or_update_alias_in_shell_rc(alias_name, command, shell_rc)
        add_current_dir_to_shell_rc(shell_rc)
    
    update_env_files_with_current_dir()
    print("Changes applied to .bashrc and .zshrc. You may need to restart your terminal or run 'source ~/.bashrc' and 'source ~/.zshrc' to apply changes.")

if __name__ == "__main__":
    main()
