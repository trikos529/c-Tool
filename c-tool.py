import subprocess #legacy dep 
from pathlib import Path
import platform
import json
import urllib.request
import zipfile
import tarfile

script_dir = Path(__file__).parent.absolute()
user_dir = Path.cwd()
downloads_dir = script_dir / "downloads"
project_dir = script_dir / "project"
config_path = script_dir / "config.json"
project_config = project_dir / "c-tool-project.json"
should_project_setup_run = False
is_vscode_used = False 


def config_add(tool: str, path: str):
    if config_path.exists():
        with config_path.open("r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
                path = None
    else:
        data = {}
    data[tool] = True
    path = str(downloads_dir / tool)
    with config_path.open("w") as f:
        json.dump(data, path, f)
        
def project_config_add( name: str, language: str,standard: str,version:str,cmake_min:str):
    if project_config.exists():
        with project_config.open("r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                standard = {}
                name = {}
                language = {}
                version = {}
                cmake_min = {}
                
    else:
        data[standard] = standard
        data[name] = name
        data[language] = language
        data[version] = version 
        data[cmake_min] = cmake_min
        
    with project_config.open("w") as f:
        json.dump(data, f)

def gcc():
   gcc_path = downloads_dir / "gcc"
   if gcc_path.exists():
        config_add("gcc")
   else:
    downloads_dir.mkdir(exist_ok=True)
    #dowload gcc new comand
    config_add("gcc")

def llvm():
    llvm_path = downloads_dir / "LLVM"
    if llvm_path.exists():
        config_add("LLVM")
    else:
        downloads_dir.mkdir(exist_ok=True)
        #dowload llvm new way 
        config_add("LLVM")

def emscripten():
    em_path = downloads_dir / "emscripten"
    if em_path.exists():
        config_add("emscripten")
    else:
        downloads_dir.mkdir(exist_ok=True)
        #dowload new way 
        config_add("emscripten")

def compiler_select():
    should_compiler_select_run = True  
    while should_compiler_select_run:
        print("1. Setup GCC compiler")
        print("2. Setup LLVM compiler")
        print("3. Setup emscripten web assembly (GIT REQUIRED)")
        print("4. Download all compilers")
        print("5. set custom compiler")#not yet
        print("5. Go back")
        
        try:
            user_input = int(input("Select an option: "))
        except ValueError:
            print("Please enter a valid number")
            continue

        if user_input == 1:
                gcc()
        elif user_input == 2:
                llvm()
        elif user_input == 3:
                emscripten()
        elif user_input == 4:
                gcc()
                llvm()
                emscripten()
        elif user_input == 5:  #not yet 
                print("instructions go here")
        elif user_input == 6:
                should_compiler_select_run = False
        else:
                print("Invalid Option")
        
       
def cmake_check():
    cmake_path = downloads_dir / "cmake"
    if cmake_path.exists():
        config_add("cmake")
    else:
        downloads_dir.mkdir(exist_ok=True)
        #new install method
        config_add("cmake")

def vcpkg_check():
    vcpkg_path = downloads_dir / "vcpkg"
    if vcpkg_path.exists():
        config_add("vcpkg")
    else:
        downloads_dir.mkdir(exist_ok=True)
        #new install method
        config_add("vcpkg")

def setup():
    should_setup_run = True
    while should_setup_run:
        print("1. Set up CMake + compiler + vcpkg (GIT REQUIRED)")
        print("2. Return to main menu")
        
        try:
            user_input = int(input("Select an option: "))
        except ValueError:
            print("Please enter a valid number")
            continue
            
        if user_input == 1:
            compiler_select()
            cmake_check()
            vcpkg_check()
            should_setup_run = False
        elif user_input == 2:
            should_setup_run = False 
        else:
            print("Invalid option")

def help():
    should_help_run = True
    while should_help_run:
        print("C Tool V1")
        print("C Tool installs all tools automatically within setup")
        print("For more info and help visit the GitHub repo")
        print("GitHub: https://github.com/trikos529/c-tool")
        temp = int(input("To go back press 1"))
        if temp == 1:
            should_help_run = False
        else:
            print("Invalid Option")

def nav_info():
    print("When pressing R, you restart the project setup")
    print("When pressing L, you can leave the project setup")
    print("")

def project_name_selector():
    project_name = ""
    nav_info()
    user_input = input("Enter project name: ")
           
    if user_input == "R":
        user_input = 0
        setup_project()
    elif user_input == "L":
        user_input = 0
        global should_project_setup_run
        should_project_setup_run = False
    elif user_input == "":
        project_name = "My C-Tool Project"
        return "My C-Tool Project"
    else:
        project_name = user_input
        user_input = 0
        print(f"Project name has been set to {project_name}")
        return project_name 

def project_language_selector():
    should_project_language_selector_run = True
    while should_project_language_selector_run:
        nav_info()
        print("C++. (Use C++)")
        print("C. (Use C)")
        user_input = input("Enter language: ")

        if user_input == "R":
            user_input = 0
            setup_project()
        elif user_input == "L":
            user_input = 0
            global should_project_setup_run
            should_project_setup_run = False
            should_project_language_selector_run = False
        elif user_input == "C++":
            should_project_language_selector_run = False
            return "c++"
        elif user_input == "C":
            should_project_language_selector_run = False
            return "c"  
        else:
           print("Invalid Option")

def standard_select(lang:str):
     standard_select = True
     while standard_select:
         if lang=="c":
             nav_info()
             print("Choose language standard for C")
             print("Standards available: 90, 99, 11, 17")
             user_input=input()  
             if user_input == "R":
                    user_input = 0
                    setup_project()
             elif user_input == "L":
                    user_input = 0
                    global should_project_setup_run
                    should_project_setup_run = False
             elif user_input == "90":
                 standard_select = False
                 return "C 90"
             elif user_input == "99":
                 standard_select = False
                 return "C 99"
             elif user_input == "11":
                 standard_select = False
                 return "C 11"
             elif user_input == "17":
                 standard_select = False
                 return "C 17"
             else:
                 print("invalid input")
         elif lang=="c++":
            nav_info()
            print("Choose language standard for C++")
            print("Standards available: 98, 11, 14, 17, 20")
            user_input=input()  
            if user_input == "R":
                    user_input = 0
                    setup_project()
            elif user_input == "B":
                    user_input = 0
                    project_language_selector()
            elif user_input == "L":
                    user_input = 0
                    global should_project_setup_run
                    should_project_setup_run = False
            elif user_input == "98":
                 standard_select = False
                 return "C++ 98"
            elif user_input == "11":
                 standard_select = False
                 return "C++ 11"
            elif user_input == "14":
                 standard_select = False
                 return "C++ 14"
            elif user_input == "17":
                 standard_select = False
                 return "C++ 17"
            elif user_input == "20":
                standard_select=False
                return "C++ 20"
            else:
                 print("Invalid Input")

def config_project_version():
    nav_info()
    user_input = input("type a vesrsion for the project you can always change it in the c-tool-project.json ")

    if user_input == "R":
        user_input = 0
        setup_project()
    elif user_input == "L":
        user_input = 0
    else:
        return user_input

def setup_project():
    global should_project_setup_run
    should_project_setup_run = True
    while should_project_setup_run:
        cmake_minimum = "VERSION 3.5...3.31"
        project_name = project_name_selector()
        project_version = config_project_version()
        language = project_language_selector()
        lang_standard = standard_select(language) 
        project_config_add(project_name,language,lang_standard,project_version,cmake_minimum,) 

def cmake_list_check():
    cmake_project_path = user_dir / "CMakeLists.txt"
    if project_config.exists():
        with open('project_config', 'r') as file:
            cbo="{"
            cbc="}"
            data = json.load(file)
            name = data.get('name')
            language = data.get('language')
            standard = data.get('standard')
            version = data.get('version')
            cmake_min = data.get('cmake_min')
            src_files = src_scan()
            dependencys = dependency_scan()
            h_files = h_scan()
            cmake_items = [
                            f"cmake_minimum_required(VERSION {cmake_min})",
                            f"project({name} VERSION {version})",
                            f"enable_language({language})",
                            f"set(CMAKE_{language}_STANDARD {standard})",
                            f"set(CMAKE_{language}_STANDARD_REQUIRED ON)",
                            f"set(CMAKE_RUNTIME_OUTPUT_DIRECTORY {user_dir})",
                            "",
                            "# Source files",
                            f"add_executable({name}",
                            f"    {src_files}",
                            f")",
                            "",
                            "# Dependencies",
                            f"target_link_libraries({name}",
                            f"    {dependencies}",
                            f")"
                            ]
            new_cmake_txt = "\n".join(cmake_items)
            if cmake_project_path.exists():
                old_cmake_txt = cmake_project_path.read_text()
                if old_cmake_txt == new_cmake_txt:
                    print("cmake file is up to date with current parameters")
                else:
                    cmake_project_path.write_text(new_cmake_txt)
                    print("cmake updated successfully it is recomended to keep backup of old cmake files if posible until the new ones are tested ")
            else:
                cmake_project_path.write_text(new_cmake_txt)
                print("cmake file created successfully with specified content")

    else:
        setup_project()
        cmake_list_check()
            
              #use dependency scan to add dependencys to the project json (CMake json)
def src_scan():
    extensions = ["*.c", "*.cpp","*.hpp", "*.h","*.hxx"]
    files = []
    for ext in extensions:
        files.extend(user_dir.rglob(ext))
    return files
    
def dependency_scan():
    # find all libs on project files 
    # find all header files 
    # add them to config json heeders or dependencies
    # call add_dependency_vscode 

def add_dependency_vscode():
    # check vscode true or false
    # if true check for the vs code folder and depending on the compiler chosen create the list for autocomplete

def cmake_run():
    # check avalable compilers and run the cmake command
  

def compile_project():
    compile_project_should_run=True
    while compile_project_should_run:
        print("1. To update or create CMakeLists.txt according to project config")
        print("2. Scan for dependencies and add to vscode intellisense ")
        print("3. Run compilation with CMake and installed compiler")
        print("4. Go back to main menu")

        user_input = input("Select an option: ")
        if user_input == 1:
            cmake_list_check()
        elif user_input == 2:
            dependency_scan()
        elif user_input == 3:
            cmake_run()
        elif user_input == 4:
            compile_project_should_run = False 
        else:
            print("Invalid Option")

def compile():
    should_compile_run = True
    while should_compile_run:
        print("1. Setup project")
        print("2. Use current setup")
        print("3. Go back")

        try:
            user_input = int(input("Select an option: "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        if user_input == 1:
            setup_project()
            compile_project()
        elif user_input == 2:
            compile_project()
        elif user_input == 3:
            should_compile_run = False
        else:
            print("Invalid Option")
      
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
        print("1. Setup")
        print("2. Compile")
        print("3. VS Code Toggle")
        print("4. Help")
        print("5. Quit")
        print("")
        
        try:
            user_choice = int(input("Select an option: "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        if user_choice == 1:
            setup()
        elif user_choice == 2:
            compile()
        elif user_choice == 3:
            if is_vscode_used == False:
                is_vscode_used = True
                print("VS Code enabled")
            else:
                is_vscode_used = False
                print("VS Code disabled")
        elif user_choice == 4:
            help()
        elif user_choice == 5:
            should_run = False
        else:
            print("Invalid Option")

if __name__ == "__main__":
    main()