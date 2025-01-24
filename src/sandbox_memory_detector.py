import psutil
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def check_memory_size():
    """
    Checks the total system memory and compares it to a threshold
    to determine if the system is likely to be a sandbox.
    """
    try:
        # Get the total memory size in GB
        total_memory = psutil.virtual_memory().total / (1024 ** 3)  # Convert to GB
        
        print(Fore.CYAN + "Checking system memory size...")

        print(Fore.GREEN + f"Total memory detected: {total_memory:.2f} GB")

        # If the memory is less than a typical threshold, flag it as a possible sandbox
        if total_memory < 4:
            print(Fore.RED + "Warning: This system may be a sandbox environment due to low memory!")
            return True
        else:
            print(Fore.GREEN + "The system memory is within the expected range for a normal environment.")
            return False

    except Exception as e:
        print(Fore.YELLOW + f"An error occurred while checking memory: {e}")
        return False
def sandbox_memory_detector():
    is_sandbox = check_memory_size()

    if is_sandbox:
        print(Fore.RED + "\nSuspicious environment detected! This might be a sandbox.")
    else:
        print(Fore.GREEN + "\nSystem environment looks normal.")
if __name__ == "__main__":
    sandbox_memory_detector()
