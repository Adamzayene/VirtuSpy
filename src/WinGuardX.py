import winreg
import base64
from colorama import init, Fore, Style
import os
import sys

init(autoreset=True)


class WindowsActivationChecker:

    def __init__(self):
        self.encoded_key_path = "U09GVFdBUkVcTWljcm9zb2Z0XFdpbmRvd3MgTlRcQ3VycmVudFZlcnNpb25cU29mdHdhcmVQcm90ZWN0aW9uUGxhdGZvcm0="
        self.encoded_value_name = "R2VudWluZVN0YXRl"

    def decode_string(self, encoded_string):
        return base64.b64decode(encoded_string).decode("utf-8")

    def get_genuine_state(self):
        """
        Retrieves the GenuineState value from the registry.

        Returns:
            int: The value of GenuineState.
        """
        key_path = self.decode_string(self.encoded_key_path)
        value_name = self.decode_string(self.encoded_value_name)

        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                genuine_state, _ = winreg.QueryValueEx(key, value_name)
                return genuine_state
        except FileNotFoundError:
            raise FileNotFoundError("Registry key or value not found. This might indicate a non-genuine installation.")
        except PermissionError:
            raise PermissionError("Insufficient permissions to access the registry. Please run the script as an administrator.")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while accessing the registry: {e}")

    def is_genuine_windows(self):
        """
        Checks if the Windows installation is genuine.

        Returns:
            bool: True if Windows is genuine, False otherwise.
        """
        try:
            genuine_state = self.get_genuine_state()
            return genuine_state == 1 
        except FileNotFoundError as e:
            print(Fore.YELLOW + f"[WARNING] {e}")
            return False
        except PermissionError as e:
            print(Fore.RED + f"[ERROR] {e}")
            return False
        except Exception as e:
            print(Fore.RED + f"[ERROR] {e}")
            return False

    def detect_virtual_environment(self):
        """
        Detects if the script is running in a virtual or sandboxed environment.

        Returns:
            bool: True if a virtual environment is detected, False otherwise.
        """
        suspicious_usernames = ["sandbox", "vmware", "virtualbox", "test"]
        suspicious_hostnames = ["sandbox", "vm", "debug"]

        username = os.getenv("USERNAME", "").lower()
        hostname = os.getenv("COMPUTERNAME", "").lower()

        if any(suspicious in username for suspicious in suspicious_usernames) or any(
            suspicious in hostname for suspicious in suspicious_hostnames
        ):
            return True

        return False

    def display_result(self):

        if self.detect_virtual_environment():
            print(Fore.RED + "[✗] Warning: Virtual or sandbox environment detected!")
            print(Fore.RED + "[INFO] The system environment is suspicious.")

        elif self.is_genuine_windows():
            print(Fore.GREEN + "[✓] This Windows installation is genuine.")
            print(Fore.GREEN + "[INFO] Your system environment is secure and verified.")
        else:
            print(Fore.RED + "[✗] Warning: This Windows installation is NOT genuine.")
            print(Fore.RED + "[INFO] This may indicate a sandbox or a pirated Windows installation.")



def main():
    try:
        checker = WindowsActivationChecker()
        checker.display_result()
    except KeyboardInterrupt :
        print(Fore.YELLOW + "\n[INFO] Script interrupted by user. Exiting...")
    except Exception as e:
        print(Fore.RED + f"[CRITICAL] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
    
