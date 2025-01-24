import winreg
from colorama import init, Fore
import sys
import logging

# Initialize colorama
init(autoreset=True)

# Configure logging to output only to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.StreamHandler(sys.stdout)
])

def check_virtualization_registry_keys():
    """
    This function checks the registry keys for virtualization artifacts related to VirtualBox, VMware, Hyper-V, and Wine.
    """
    suspicious_keys = [
        # VirtualBox related keys
        (r"HARDWARE\ACPI\DSDT\VBOX__", "VBOX"),
        (r"HARDWARE\ACPI\FADT\VBOX__", "VBOX"),
        (r"HARDWARE\ACPI\RSDT\VBOX__", "VBOX"),
        (r"SOFTWARE\Oracle\VirtualBox Guest Additions", "VBOX"),
        (r"SYSTEM\ControlSet001\Services\VBoxGuest", "VBOX"),
        (r"SYSTEM\ControlSet001\Services\VBoxMouse", "VBOX"),
        (r"SYSTEM\ControlSet001\Services\VBoxService", "VBOX"),
        (r"SYSTEM\ControlSet001\Services\VBoxSF", "VBOX"),
        (r"SYSTEM\ControlSet001\Services\VBoxVideo", "VBOX"),

        # VMware related keys
        (r"SOFTWARE\VMware, Inc.\VMware Tools", "VMWARE"),

        # Hyper-V related keys
        (r"SOFTWARE\Microsoft\Virtual Machine\Guest\Parameters", "HYPER-V"),

        # Wine related keys
        (r"SOFTWARE\Wine", "WINE"),

        # SCSI/IDE/Virtual Disk related keys
        (r"SYSTEM\CurrentControlSet\Services\Disk\Enum", "Virtual Disk"),
        (r"SYSTEM\CurrentControlSet\Enum\IDE", "Virtual IDE"),
        (r"SYSTEM\CurrentControlSet\Enum\SCSI", "Virtual SCSI"),
    ]

    found_suspicious = False


    for key_path, indicator in suspicious_keys:
        try:
            # Open the registry key
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                try:
                    # If there are values under the key, iterate over them
                    i = 0
                    while True:
                        value_name, value, _ = winreg.EnumValue(key, i)
                        if isinstance(value, str) and indicator in value:
                            found_suspicious = True
                            logging.warning(f"[!] Suspicious value found!")
                            logging.warning(f"    Key: {key_path}")
                            logging.warning(f"    Value: {value_name} -> {value}")
                        i += 1
                except OSError:
                    # If the key doesn't contain any values, continue
                    pass
        except FileNotFoundError:
            # If the key doesn't exist, log it
            logging.info(f"[+] Key not found: {key_path}")
        except Exception as e:
            # Handle any other errors
            logging.error(f"[!] Error accessing {key_path}: {e}")

    if not found_suspicious:
        logging.info(Fore.GREEN + "[+] No suspicious artifacts detected.")
    else:
        logging.error(Fore.RED + "[!] Suspicious artifacts detected. This might be a virtual environment.")

def virtualization():
    try:
        check_virtualization_registry_keys()
    except Exception as e:
        logging.critical(f"[!] An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    virtualization()
