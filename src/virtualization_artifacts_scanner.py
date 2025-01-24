import os
import sys
from rich.console import Console
from rich.table import Table

# Console for beautiful output
console = Console()

# List of VirtualBox and VMware artifacts
artifacts = {
    "VirtualBox": [
        r"system32\drivers\VBoxMouse.sys",
        r"system32\drivers\VBoxGuest.sys",
        r"system32\drivers\VBoxSF.sys",
        r"system32\drivers\VBoxVideo.sys",
        r"system32\vboxdisp.dll",
        r"system32\vboxhook.dll",
        r"system32\vboxmrxnp.dll",
        r"system32\vboxogl.dll",
        r"system32\vboxoglarrayspu.dll",
        r"system32\vboxoglcrutil.dll",
        r"system32\vboxoglerrorspu.dll",
        r"system32\vboxoglfeedbackspu.dll",
        r"system32\vboxoglpackspu.dll",
        r"system32\vboxoglpassthroughspu.dll",
        r"system32\vboxservice.exe",
        r"system32\vboxtray.exe",
        r"system32\VBoxControl.exe"
    ],
    "VMware": [
        r"system32\drivers\vmmouse.sys",
        r"system32\drivers\vmhgfs.sys",
        r"system32\drivers\vm3dmp.sys",
        r"system32\drivers\vmci.sys",
        r"system32\drivers\vmmemctl.sys",
        r"system32\drivers\vmrawdsk.sys",
        r"system32\drivers\vmusbmouse.sys"
    ]
}

def check_artifacts():
    """
    Check the presence of VirtualBox and VMware artifacts on the file system.
    """
    detected = []
    for platform, files in artifacts.items():
        for file in files:
            file_path = os.path.join(os.getenv("SystemRoot", "C:\\Windows"), file)
            if os.path.exists(file_path):
                detected.append((platform, file_path))
    return detected

def display_results(detected_artifacts):
    """
    Display the results in a professional table format.
    """
    console.print("[bold green]File System Artifact Scanner[/bold green]\n")
    table = Table(title="Detection Results", style="blue")
    table.add_column("Platform", style="cyan", justify="center")
    table.add_column("File Path", style="magenta", justify="left")
    
    if detected_artifacts:
        for platform, path in detected_artifacts:
            table.add_row(platform, path)
        console.print(table)
        console.print(f"\n[bold yellow]Artifacts detected: {len(detected_artifacts)}[/bold yellow]")
    else:
        console.print("[bold green]No virtual environment artifacts were detected.[/bold green]")

def main():
    detected_artifacts = check_artifacts()
    display_results(detected_artifacts)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Scan interrupted by user.[/bold red]")
        sys.exit(1)
