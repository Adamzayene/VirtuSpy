import re
import os
import sys
from rich.console import Console

# Console for beautiful output
console = Console()

# Dictionary to map MAC address prefixes to virtual platforms
mac_prefixes = {
    "VirtualBox": ["08:00:27"],
    "VMware": [
        "00:05:69", "00:0C:29", "00:1C:14", "00:50:56"
    ],
    "Parallels": ["00:1C:42"],
    "Xen": ["00:16:3E"],
    "Hybrid Analysis": ["0A:00:27"]
}

def get_mac_address():
    """
    Retrieve the MAC address of the first network interface.
    """
    try:
        # For Windows
        if sys.platform == "win32":
            import psutil
            interfaces = psutil.net_if_addrs()
            for interface in interfaces:
                for snic in interfaces[interface]:
                    if snic.family == psutil.AF_LINK:
                        return snic.address
        # For Linux/macOS
        elif sys.platform == "linux" or sys.platform == "darwin":
            stream = os.popen("ifconfig -a | grep ether")
            output = stream.read()
            match = re.search(r"ether\s([0-9a-fA-F:]{17})", output)
            if match:
                return match.group(1)
        return None
    except Exception as e:
        console.print(f"[bold red]Error retrieving MAC address: {e}[/bold red]")
        sys.exit(1)

def detect_virtualization(mac_address):
    """
    Detect the virtual machine environment based on the MAC address prefix.
    """
    if mac_address:
        mac_address = mac_address.replace(":", "").upper()
        for platform, prefixes in mac_prefixes.items():
            for prefix in prefixes:
                if mac_address.startswith(prefix.upper()):
                    return platform
        return "Unknown Environment"
    return "MAC Address not found"

def main():
    mac_address = get_mac_address()

    if mac_address:
        console.print(f"[bold green]Detected MAC Address: {mac_address}[/bold green]")

        # Check which virtual platform the MAC address belongs to
        platform = detect_virtualization(mac_address)
        console.print(f"[bold yellow]Virtualization Environment: {platform}[/bold yellow]")
    else:
        console.print("[bold red]No MAC address found[/bold red]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Scan interrupted by user.[/bold red]")
        sys.exit(1)
