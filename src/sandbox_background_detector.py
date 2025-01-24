import pyautogui
from PIL import ImageColor
from colorama import init, Fore, Style
import time
import screeninfo

# Initialize colorama
init(autoreset=True)

# List of suspicious background colors (in RGB format)
suspicious_colors = [
    (0, 0, 0),  # Black
    (255, 255, 255),  # White
    (169, 169, 169),  # Dark Gray
    (211, 211, 211)   # Light Gray
]

# List of pixel positions to check (e.g., corners and center)
def get_check_positions():
    screen = screeninfo.get_monitors()[0]
    width, height = screen.width, screen.height
    
    return [
        (0, 0),  # Top-left corner
        (0, 1),  # Near top-left
        (1, 0),  # Near top-left
        (width-1, 0),  # Top-right corner
        (0, height-1),  # Bottom-left corner
        (width-1, height-1),  # Bottom-right corner
        (width//2, height//2)  # Center
    ]

# Function to check the color of background pixels
def check_background_pixels():
    try:
        # Take a screenshot of the whole screen
        screenshot = pyautogui.screenshot()

        # Get screen dimensions dynamically
        check_positions = get_check_positions()

        suspicious_found = False

        # Iterate over the positions and check the pixel color
        for pos in check_positions:
            pixel_color = screenshot.getpixel(pos)
            print(f"Checking pixel at {pos}: {pixel_color}")

            # Check if the color matches any suspicious color
            if pixel_color in suspicious_colors:
                suspicious_found = True
                print(f"{Fore.RED}Suspicious: Background color at {pos} is {pixel_color}, which may indicate a sandbox environment.{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}Normal: Background color at {pos} is {pixel_color}.")

        if suspicious_found:
            print(f"{Fore.YELLOW}Warning: Potential sandbox environment detected based on background pixel color(s).{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}No suspicious background colors detected. The system seems normal.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def sandbox_background_detector():
    time.sleep(2)  # Adding a small delay before execution
    check_background_pixels()
    
if __name__ == "__main__":
    time.sleep(2)  # Adding a small delay before execution
    check_background_pixels()
