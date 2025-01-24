import os
import fnmatch
from colorama import init, Fore, Style

init()

# List of suspicious filenames that may indicate a sandbox environment
known_sandbox_filenames = [
    "sample.exe", "sandbox.exe", "vmtoolsd.exe", "vboxservice.exe",
    "vmwareuser.exe", "vmmemctl.sys", "VBoxControl.exe", "vboxnetadp.sys", 
    "vmsrvc.exe", "vmmem.exe", "sandboxie.exe", "pbox.exe", "cuckoo.exe",
    "sandboxed.exe", "procmon.exe", "Wireshark.exe", "x32dbg.exe", "x64dbg.exe",
    "OllyDbg.exe", "qemu-system-x86_64.exe", "bochs.exe", "kvm.exe", "analysis.exe",
    "test.exe", "detonate.exe"
]

# Function to check for known files in system directories
def check_known_files_in_directories(directories):
    found_files = []
    
    # Loop through all provided directories
    for directory in directories:
        if os.path.exists(directory):
            print(f"{Fore.YELLOW}Searching in {directory}...{Style.RESET_ALL}")
            for root, dirs, files in os.walk(directory):
                for filename in files:
                    if any(fnmatch.fnmatch(filename.lower(), pattern.lower()) for pattern in known_sandbox_filenames):
                        file_path = os.path.join(root, filename)
                        found_files.append(file_path)
                        print(f"{Fore.RED}Suspicious file found: {file_path}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Directory {directory} does not exist.{Style.RESET_ALL}")
    
    return found_files


def check_known_sandbox_files():

    username = os.getenv("USERNAME")
    if not username:
        print(f"{Fore.RED}Username not found!{Style.RESET_ALL}")
        return
    
    common_directories = [
        "C:\\Windows\\Temp", 
        f"C:\\Users\\{username}\\AppData\\Local\\Temp",  
        "C:\\Users\\Public\\Documents", 
        "C:\\ProgramData",  
        f"C:\\Users\\{username}\\AppData\\Roaming",  
        "C:\\Windows\\System32",  
        "C:\\Windows\\SysWOW64",  
        "C:\\Program Files",  
        "C:\\Program Files (x86)",  
        f"C:\\Users\\{username}\\AppData\\Local", 
    ]
    
    # Search through the directories
    found_files = check_known_files_in_directories(common_directories)
    
    if found_files:
        print(f"{Fore.GREEN}Found {len(found_files)} suspicious files. You might be in a sandbox environment.{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}No suspicious files were found in the specified directories.{Style.RESET_ALL}")

# Execute the function
if __name__ == "__main__":
    check_known_sandbox_files()
