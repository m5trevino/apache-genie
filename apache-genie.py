#!/usr/bin/env python3

import os
import random
from termcolor import colored
import time
import shutil

# Function to detect private IP address
def get_private_ip():
    import socket
    hostname = socket.gethostname()
    try:
        private_ip = socket.gethostbyname(hostname)
        return private_ip
    except:
        return "Unknown"

# Function to print ASCII art banner
def display_ascii_art(file_path="apachegenieascii.txt"):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        ascii_file_path = os.path.join(script_dir, file_path)
        with open(ascii_file_path, "r") as f:
            art_blocks = f.read().split("\n\n")
            random_art = random.choice(art_blocks)
            print(colored(random_art, "magenta"))
    except FileNotFoundError:
        print(colored("[ERROR] ASCII art file not found!", "red"))

# Function to simulate typing with delays
def slow_type(text, delay=0.05, color="cyan"):
    for char in text:
        print(colored(char, color), end="", flush=True)
        time.sleep(delay)
    print()  # Newline after typing

# Function to create an Apache configuration from scratch
def create_apache_from_scratch():
    print(colored("\n[INFO] Let's set up your Apache server from scratch!", "cyan"))

    # Display detected private IP
    private_ip = get_private_ip()
    print(colored(f"\nDetected private IP address: {private_ip}\n", "green"))

    # Step-by-step configuration
    slow_type("Step 1: Setting the Server Admin Email", color="green")
    server_admin = input("\nEnter the server admin email (e.g., admin@example.com): ").strip()

    slow_type("\nStep 2: Setting the Document Root", color="green")
    document_root = input("Enter the document root path (e.g., /var/www/html): ").strip()

    slow_type("\nStep 3: Setting the Server Port", color="green")
    server_port = input("Enter the port number for the server (default: 80): ").strip() or "80"

    slow_type("\nStep 4: Setting the WebDAV Directory", color="green")
    webdav_dir = input("Enter the path to the WebDAV directory (e.g., /var/www/webdav): ").strip()

    # Typing out the configuration
    print(colored("\nTyping out your Apache configuration...\n", "cyan"))
    time.sleep(1)

    apache_config = f"""
<VirtualHost *:{server_port}>
    ServerAdmin {server_admin}
    DocumentRoot {document_root}
    <Directory {document_root}>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
    Alias /webdav {webdav_dir}
    <Directory {webdav_dir}>
        Options Indexes FollowSymLinks
        DAV On
        AuthType Basic
        AuthName "WebDAV Restricted Area"
        AuthUserFile /etc/apache2/.htpasswd
        Require valid-user
    </Directory>
</VirtualHost>
"""

    # Slowly type out the configuration
    for line in apache_config.splitlines():
        slow_type(line, color="magenta")
        if "<YOUR_PRIVATE_IP>" in line:
            slow_type(f"\nDetected private IP: {private_ip}\n", color="green")

    # Confirm and write the configuration
    confirm = input(colored("\nDo you want to save and deploy this configuration? (y/n): ", "yellow")).strip().lower()
    if confirm == "y":
        with open("/etc/apache2/sites-available/000-default.conf", "w") as f:
            f.write(apache_config)
        print(colored("[INFO] Configuration written successfully!", "green"))
        run_command("sudo systemctl restart apache2")
    else:
        print(colored("[INFO] Configuration creation canceled. No changes were made.", "red"))

# Function to run a system command
def run_command(command):
    print(colored(f"Running: {command}", "cyan"))
    result = os.system(command)
    if result != 0:
        print(colored(f"[ERROR] Command failed: {command}", "red"))
    else:
        print(colored("[SUCCESS] Command executed successfully!", "green"))

# Function to add script to system-wide commands
def add_to_systemwide():
    script_path = os.path.realpath(__file__)
    symlink_path = "/usr/local/bin/apache-genie"

    if os.path.exists(symlink_path):
        print(colored("[INFO] apache-genie is already installed as a system-wide command.", "green"))
        return

    try:
        shutil.copy(script_path, "/usr/local/bin/apache-genie")
        os.chmod("/usr/local/bin/apache-genie", 0o755)  # Make it executable
        print(colored("[INFO] apache-genie is now available as a system-wide command!", "green"))
        print(colored("You can now run it by typing: apache-genie", "cyan"))
    except PermissionError:
        print(colored("[ERROR] Permission denied. Try running this script with sudo.", "red"))

# Main Menu Function
def main_menu():
    while True:
        print(colored("\nMain Menu:", "magenta"))
        print(colored("1. Server Management", "green"))
        print(colored("2. Diagnostics and Configuration", "green"))
        print(colored("3. Setup and Creation", "green"))
        print(colored("4. Add Apache Genie to System-Wide Commands", "green"))
        print(colored("5. Exit", "magenta"))

        choice = input(colored("\nSelect an option (1-5): ", "yellow")).strip()

        if choice == "1":
            server_management_menu()
        elif choice == "2":
            diagnostics_menu()
        elif choice == "3":
            create_apache_from_scratch()
        elif choice == "4":
            add_to_systemwide()
        elif choice == "5":
            print(colored("\nExiting Apache Genie. Goodbye!\n", "cyan"))
            break
        else:
            print(colored("[ERROR] Invalid selection. Please try again.", "red"))

# Server Management Menu
def server_management_menu():
    while True:
        print(colored("\nServer Management Menu:", "magenta"))
        print(colored("1. Restart Apache", "green"))
        print(colored("2. Enable Apache", "green"))
        print(colored("3. Check Apache Status", "green"))
        print(colored("4. Back to Main Menu", "magenta"))

        choice = input(colored("\nSelect an option (1-4): ", "yellow")).strip()

        if choice == "1":
            run_command("sudo systemctl restart apache2")
        elif choice == "2":
            run_command("sudo systemctl enable apache2")
        elif choice == "3":
            run_command("sudo systemctl status apache2")
        elif choice == "4":
            break
        else:
            print(colored("[ERROR] Invalid selection. Please try again.", "red"))

# Diagnostics Menu
def diagnostics_menu():
    while True:
        print(colored("\nDiagnostics and Configuration Menu:", "magenta"))
        print(colored("1. Check Apache Error Logs", "green"))
        print(colored("2. Check Which Process is Using a Port", "green"))
        print(colored("3. Test Apache Configuration", "green"))
        print(colored("4. Edit Apache Configuration File", "green"))
        print(colored("5. Edit Site Configuration File", "green"))
        print(colored("6. Back to Main Menu", "magenta"))

        choice = input(colored("\nSelect an option (1-6): ", "yellow")).strip()

        if choice == "1":
            run_command("sudo tail -f /var/log/apache2/error.log")
        elif choice == "2":
            port = input(colored("Enter the port number to check (e.g., 80): ", "yellow")).strip()
            run_command(f"sudo netstat -tuln | grep :{port}")
        elif choice == "3":
            run_command("sudo apache2ctl configtest")
        elif choice == "4":
            editor = "sudo subl" if os.system("command -v subl > /dev/null") == 0 else "sudo nano"
            run_command(f"{editor} /etc/apache2/apache2.conf")
        elif choice == "5":
            site_config = input(colored("Enter the site config filename (e.g., 000-default.conf): ", "yellow")).strip()
            editor = "sudo subl" if os.system("command -v subl > /dev/null") == 0 else "sudo nano"
            run_command(f"{editor} /etc/apache2/sites-available/{site_config}")
        elif choice == "6":
            break
        else:
            print(colored("[ERROR] Invalid selection. Please try again.", "red"))

# Main Script Execution
if __name__ == "__main__":
    display_ascii_art()  # Show ASCII art on launch
    main_menu()
