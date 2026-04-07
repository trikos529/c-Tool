import subprocess
from pathlib import Path
import platform
import json

operating_system = platform.system()
script_dir = Path(__file__).parent.absolute()
user_dir = Path.cwd()
config_path = script_dir / "config.json"

def config_add(tool: str):
    if config_path.exists():
        with config_path.open("r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    data[tool] = True
    with config_path.open("w") as f:
        json.dump(data, f)

def compiler_select():
    should_compiler_select_run = True  
    while should_compiler_select_run:
        print("1. Set up gcc compiler")
        print("2. Set up LLVM compiler")
        print("3. Set up emscripten web assembly (GIT REQUIRED)")
        print("4. Go back")
        
        try:
            user_input = int(input("Select an option: "))
        except ValueError:
            print("Please enter a valid number")
            continue

        downloads_dir = script_dir / "downloads"
        
        if operating_system == "Windows":
            if user_input == 1: 
                gcc_path = downloads_dir / "gcc"
                if gcc_path.exists():
                    config_add("gcc")
                else:
                    downloads_dir.mkdir(exist_ok=True)
                    # subprocess.run(["winget", "install", "BrechtSanders.WinLibs.POSIX.UCRT"], check=True)  # Uncomment when ready
                    print("Downloading GCC...")
                    config_add("gcc")                    
            elif user_input == 2:
                llvm_path = downloads_dir / "LLVM"
                if llvm_path.exists():
                    config_add("LLVM")
                else:
                    downloads_dir.mkdir(exist_ok=True)
                    subprocess.run(["winget", "install", "llvm"], check=True)
                    config_add("LLVM")
            elif user_input == 3:
                em_path = downloads_dir / "emscripten"
                if em_path.exists():
                    config_add("emscripten")
                else:
                    downloads_dir.mkdir(exist_ok=True)
                    # subprocess.run(["git", "clone", "https://github.com/emscripten-core/emsdk.git", str(em_path)], check=True)
                    print("Downloading emscripten...")
                    config_add("emscripten")
            elif user_input == 4:
                should_compiler_select_run = False
            else:
                print("Invalid Option")
        
        # Linux
        elif operating_system == "Linux":
            if user_input == 1:   
                gcc_path = downloads_dir / "gcc"
                if gcc_path.exists():
                    config_add("gcc")
                else:
                    downloads_dir.mkdir(exist_ok=True)
                    # Use apt, dnf, pacman, etc.
                    # subprocess.run(["sudo", "apt", "install", "gcc"], check=True)
                    print("Downloading GCC... (apt command placeholder)")
                    config_add("gcc")
            elif user_input == 2:
                llvm_path = downloads_dir / "LLVM"
                if llvm_path.exists():
                    config_add("LLVM")
                else:
                    downloads_dir.mkdir(exist_ok=True)
                    # subprocess.run(["sudo", "apt", "install", "llvm"], check=True)
                    print("Downloading LLVM... (apt command placeholder)")
                    config_add("LLVM")
            elif user_input == 3:
                em_path = downloads_dir / "emscripten"
                if em_path.exists():
                    config_add("emscripten")
                else:
                    downloads_dir.mkdir(exist_ok=True)
                    # subprocess.run(["git", "clone", "https://github.com/emscripten-core/emsdk.git", str(em_path)], check=True)
                    print("Downloading emscripten... (git command placeholder)")
                    config_add("emscripten")
            elif user_input == 4:
                should_compiler_select_run = False
            else:
                print("Invalid Option")
        
        # MacOS
        elif operating_system == "Darwin":  # Fixed spelling
            if user_input == 1:   
                gcc_path = downloads_dir / "gcc"
                if gcc_path.exists():
                    config_add("gcc")
                else:
                    downloads_dir.mkdir(exist_ok=True)
                    # Use homebrew
                    # subprocess.run(["brew", "install", "gcc"], check=True)
                    print("Downloading GCC... (brew command placeholder)")
                    config_add("gcc")
            elif user_input == 2:
                llvm_path = downloads_dir / "LLVM"
                if llvm_path.exists():
                    config_add("LLVM")
                else:
                    downloads_dir.mkdir(exist_ok=True)
                    # subprocess.run(["brew", "install", "llvm"], check=True)
                    print("Downloading LLVM... (brew command placeholder)")
                    config_add("LLVM")
            elif user_input == 3:
                em_path = downloads_dir / "emscripten"
                if em_path.exists():
                    config_add("emscripten")
                else:
                    downloads_dir.mkdir(exist_ok=True)
                    # subprocess.run(["git", "clone", "https://github.com/emscripten-core/emsdk.git", str(em_path)], check=True)
                    print("Downloading emscripten... (git command placeholder)")
                    config_add("emscripten")
            elif user_input == 4:
                should_compiler_select_run = False
            else:
                print("Invalid Option")

def setup():
    should_setup_run = True
    while should_setup_run:
        print("1. Set up CMake + compiler + vcpkg")
        print("2. Return to main menu")
        
        try:
            user_input = int(input("Select an option: "))
        except ValueError:
            print("Please enter a valid number")
            continue
            
        if user_input == 1:
            compiler_select()
            # cmake_check()
            # vcpkg_check()
        elif user_input == 2:
            should_setup_run = False 
        else:
            print("Invalid option")

def main():
    print(r" ██████╗    ████████╗ ██████╗  ██████╗ ██╗")
    print(r"██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║  ")
    print(r"██║            ██║   ██║   ██║██║   ██║██║ ")
    print(r"██║            ██║   ██║   ██║██║   ██║██║")
    print(r"╚██████╗       ██║   ╚██████╔╝╚██████╔╝███████╗")
    print(r" ╚═════╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝")
    
    should_run = True
    while should_run:
        print("")
        print("1. Setup profile for compilation")
        print("2. Compile")
        print("3. Help")
        print("4. Quit")
        print("")
        
        try:
            user_choice = int(input("Select an option: "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        if user_choice == 1:
            setup()
        elif user_choice == 2:
            # Compile using profile
            break
        elif user_choice == 3:
            # Help Function
            break
        elif user_choice == 4:
            should_run = False
        else:
            print("Invalid Option")

if __name__ == "__main__":
    main()