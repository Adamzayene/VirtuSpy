import check_sandbox_files
import sandbox_memory_detector
import sandbox_background_detector
import WinGuardX
import VirtualizationRegistryScan
import virtualization_artifacts_scanner
import mac_virtual_platform_detector
import virtualization_process_detector
import banner
from colorama import init, Fore, Style

def main():
    banner.banner()
    detected_count = 0  
    total_checks = 10  
    
    print("Checking for known sandbox files...")
    found_files = check_sandbox_files.check_known_sandbox_files()
    if found_files:
        detected_count += 1
    
    print(Fore.YELLOW + "Starting sandbox detection based on memory size...\n")
    found_memory = sandbox_memory_detector.sandbox_memory_detector()
    if found_memory:
        detected_count += 1

    print(f"{Fore.BLUE}Starting the background pixel color check...{Style.RESET_ALL}")
    found_pixel = sandbox_background_detector.sandbox_background_detector()
    if found_pixel:
        detected_count += 1

    print(Style.BRIGHT + Fore.CYAN + "\nWindows Activation & Environment Check")
    print(Fore.CYAN + "Checking Windows Genuine Installation...\n")
    WinGuard = WinGuardX.main()
    if WinGuard:
        detected_count += 1

    print(Fore.CYAN + "[*] Checking registry keys for virtualization artifacts...")
    virtualizationRegistryScan = VirtualizationRegistryScan.virtualization()
    if virtualizationRegistryScan:
        detected_count += 1

    print(Fore.CYAN + "Scanning the file system for virtualization artifacts...")
    Virtualization_artifacts_scanner = virtualization_artifacts_scanner.main()
    if Virtualization_artifacts_scanner:
        detected_count += 1

    print(Fore.CYAN + "Scanning for MAC Address...")
    Mac_virtual_platform_detector = mac_virtual_platform_detector.main()
    if Mac_virtual_platform_detector:
        detected_count += 1

    print("Scanning for virtual machine processes...")
    Virtualization_process_detector = virtualization_process_detector.main()
    if Virtualization_process_detector:
        detected_count += 1

    # Calculate percentage of detections
    detection_percentage = (detected_count / total_checks) * 100
    print(f"\nDetection Percentage: {detection_percentage:.2f}%")
    
    # Interpret the result
    if detection_percentage > 50:
        print(Fore.RED + "[*] It is highly likely you are in a virtual environment.")
    else:
        print(Fore.GREEN + "[*] It is unlikely you are in a virtual environment.")

if __name__ == "__main__":
    main()

