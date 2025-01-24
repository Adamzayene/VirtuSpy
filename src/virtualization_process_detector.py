import psutil
from rich.console import Console
from rich.table import Table

# Console for beautiful output
console = Console()

# Dictionary to map known processes to virtual platforms
processes = {
    "VirtualBox": [
        "vboxservice.exe", "vboxtray.exe"
    ],
    "VMware": [
        "vmtoolsd.exe", "vmwaretray.exe", "vmwareuser.exe", "VGAuthService.exe", "vmacthlp.exe"
    ],
    "VirtualPC": [
        "vmsrvc.exe", "vmusrvc.exe"
    ],
    "Parallels": [
        "prl_cc.exe", "prl_tools.exe"
    ],
    "Citrix Xen": [
        "xenservice.exe"
    ],
    "QEMU": [
        "qemu-ga.exe"
    ]
}

def check_virtualization_processes():
    """
    Check for the presence of known virtual environment processes.
    """
    detected = []
    
    # Get the list of currently running processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # For each process, check if its name matches any known virtualization process
            for platform, process_list in processes.items():
                if proc.info['name'].lower() in (process.lower() for process in process_list):
                    detected.append((platform, proc.info['name'], proc.info['pid']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # Handle any process access errors gracefully

    return detected

def display_results(detected_processes):
    """
    Display the results in a professional table format.
    """
    console.print("[bold green]Virtualization Process Detector[/bold green]\n")
    table = Table(title="Detection Results", style="blue")
    table.add_column("Platform", style="cyan", justify="center")
    table.add_column("Process Name", style="magenta", justify="left")
    table.add_column("PID", style="yellow", justify="right")
    
    if detected_processes:
        for platform, process_name, pid in detected_processes:
            table.add_row(platform, process_name, str(pid))
        console.print(table)
        console.print(f"\n[bold yellow]Total virtualization processes detected: {len(detected_processes)}[/bold yellow]")
    else:
        console.print("[bold green]No virtualization processes were detected.[/bold green]")

def main():
    detected_processes = check_virtualization_processes()
    display_results(detected_processes)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Scan interrupted by user.[/bold red]")
        exit(1)
