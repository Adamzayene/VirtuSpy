import winreg
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def check_registry_keys():
    """
    This function checks the registry keys for virtualization artifacts.
    """
    suspicious_keys = [
        # Key paths and expected suspicious values
        (r"HARDWARE\DEVICEMAP\Scsi\Scsi Port 0\Scsi Bus 0\Target Id 0\Logical Unit Id 0", "Identifier", ["VBOX", "QEMU", "VMWARE"]),
        (r"HARDWARE\Description\System", "SystemBiosVersion", ["VBOX", "QEMU", "VIRTUALBOX"]),
        (r"HARDWARE\Description\System", "VideoBiosVersion", ["VIRTUALBOX"]),
        (r"HARDWARE\Description\System", "SystemBiosDate", ["06/23/99"]),
        (r"HARDWARE\DEVICEMAP\Scsi\Scsi Port 1\Scsi Bus 0\Target Id 0\Logical Unit Id 0", "Identifier", ["VMWARE"]),
        (r"HARDWARE\DEVICEMAP\Scsi\Scsi Port 2\Scsi Bus 0\Target Id 0\Logical Unit Id 0", "Identifier", ["VMWARE"]),
        (r"SYSTEM\ControlSet001\Control\SystemInformation", "SystemManufacturer", ["VMWARE"]),
        (r"SYSTEM\ControlSet001\Control\SystemInformation", "SystemProductName", ["VMWARE"]),
    ]

    found_suspicious = False

    print(Fore.CYAN + "[*] Checking registry keys for virtualization artifacts...")

    for key_path, value_name, indicators in suspicious_keys:
        try:
            # Open the registry key
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                # Read the value
                value = winreg.QueryValueEx(key, value_name)[0]
                # Check if any suspicious indicator exists in the value
                if any(indicator in value for indicator in indicators):
                    found_suspicious = True
                    print(Fore.RED + f"[!] Suspicious value found!")
                    print(Fore.YELLOW + f"    Key: {key_path}")
                    print(Fore.YELLOW + f"    Value: {value_name} -> {value}")
        except FileNotFoundError:
            # If the key or value doesn't exist, skip it
            print(Fore.GREEN + f"[+] Key not found: {key_path}")
        except Exception as e:
            # Handle any other errors
            print(Fore.RED + f"[!] Error accessing {key_path}: {e}")

    if not found_suspicious:
        print(Fore.GREEN + "[+] No suspicious artifacts detected.")
    else:
        print(Fore.RED + "[!] Suspicious artifacts detected. This might be a virtual environment.")

if __name__ == "__main__":
    check_registry_keys()
