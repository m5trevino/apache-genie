#!/bin/bash

# Set the directory where the script is located
SCRIPT_DIR="/home/flintx/apache-genie"

# Function to print ASCII art
print_ascii_art() {
    # Path to the ASCII art file
    ASCII_FILE="${SCRIPT_DIR}/apachegenieascii.txt"
    
    if [[ -f "$ASCII_FILE" ]]; then
        # Read the file into an array, splitting on blank lines
        IFS=$'\n' read -r -d '' -a ascii_blocks < <(awk -v RS= '{print}' "$ASCII_FILE" && printf '\0')
        
        # Check if we have any blocks
        if [[ ${#ascii_blocks[@]} -gt 0 ]]; then
            # Randomly pick one block of ASCII art
            random_art="${ascii_blocks[RANDOM % ${#ascii_blocks[@]}]}"
            echo -e "\e[32m$random_art\e[0m"  # Print it in green color
        else
            echo -e "\e[31m[INFO] No ASCII art found in the file.\e[0m"
        fi
    else
        echo -e "\e[31m[INFO] ASCII file not found. Skipping banner.\e[0m"
    fi
}

# Function to run and print a command
run_command() {
    echo -e "\e[34mRunning: $1\e[0m"
    eval "$1"
    if [ $? -ne 0 ]; then
        echo -e "\e[31m[ERROR] Command failed: $1\e[0m"
    else
        echo -e "\e[32m[SUCCESS] Command executed: $1\e[0m"
    fi
    echo -e "\e[34m------------------------------------\e[0m"
}

# Function to create Apache configurations from a template
create_apache_from_template() {
    echo -e "\e[35m[INFO] Creating Apache server from scratch using current configuration as a template...\e[0m"
    CONFIG_TEMPLATE=$(cat /etc/apache2/apache2.conf)
    VHOST_TEMPLATE=$(cat /etc/apache2/sites-available/000-default.conf)

    CONFIG_TEMPLATE=$(echo "$CONFIG_TEMPLATE" | sed 's/192\.168\.[0-9]*\.[0-9]*/<YOUR_PRIVATE_IP>/g')
    VHOST_TEMPLATE=$(echo "$VHOST_TEMPLATE" | sed 's/\/var\/www\/html/<YOUR_DOCUMENT_ROOT>/g')

    echo -e "\e[33mGenerated template:\e[0m"
    echo "$CONFIG_TEMPLATE"
    echo "$VHOST_TEMPLATE"

    echo -e "\n\e[36mPrompting for configuration details...\e[0m"

    read -p "Enter your private IP (e.g., 192.168.1.100): " private_ip
    read -p "Enter the document root path (e.g., /var/www/html): " document_root
    read -p "Enter the server admin email (e.g., admin@example.com): " server_admin
    read -p "Enter the port number for the server (default: 80): " server_port
    server_port=${server_port:-80}

    CONFIG_FINAL=$(echo "$CONFIG_TEMPLATE" | sed "s/<YOUR_PRIVATE_IP>/$private_ip/g")
    VHOST_FINAL=$(echo "$VHOST_TEMPLATE" | sed "s/<YOUR_DOCUMENT_ROOT>/$document_root/g" | sed "s/<YOUR_SERVER_ADMIN>/$server_admin/g" | sed "s/<YOUR_SERVER_PORT>/$server_port/g")

    echo "$CONFIG_FINAL" > /etc/apache2/apache2.conf
    echo "$VHOST_FINAL" > /etc/apache2/sites-available/000-default.conf

    echo -e "\e[32mConfiguration files updated. Restarting Apache...\e[0m"
    run_command "sudo systemctl restart apache2"
}

# Menu header
print_ascii_art
echo -e "\e[35m====================================\e[0m"
echo -e "\e[35m        Apache Genie Script         \e[0m"
echo -e "\e[35m====================================\e[0m"

# Menu loop
while true; do
    echo -e "\e[34m\nMenu Categories:\e[0m"
    echo -e "1. \e[32mServer Management\e[0m (Restart, Enable, Check Status)"
    echo -e "2. \e[36mDiagnostics and Configuration\e[0m (Check Logs, Ports, Config)"
    echo -e "3. \e[35mSetup and Creation\e[0m (Create Server from Scratch)"
    echo -e "4. \e[31mExit\e[0m\n"

    read -p "Select a category (1-4): " category
    echo ""

    case $category in
        1)
            # Server Management
            PS3=$'\n\e[32mSelect a server management option: \e[0m'
            options=(
                "Restart Apache service"
                "Enable Apache service"
                "Check Apache status"
                "Back to Main Menu"
            )
            select opt in "${options[@]}"; do
                case $opt in
                    "Restart Apache service")
                        run_command "sudo systemctl restart apache2"
                        ;;
                    "Enable Apache service")
                        run_command "sudo systemctl enable apache2"
                        ;;
                    "Check Apache status")
                        run_command "sudo systemctl status apache2"
                        ;;
                    "Back to Main Menu")
                        break
                        ;;
                    *)
                        echo -e "\e[31m[ERROR] Invalid option. Try again.\e[0m"
                        ;;
                esac
            done
            ;;

        2)
            # Diagnostics and Configuration
            PS3=$'\n\e[36mSelect a diagnostic option: \e[0m'
            options=(
                "Check Apache error logs"
                "Check which process is using a port"
                "Test Apache configuration"
                "Edit Apache configuration file"
                "Edit a site configuration file"
                "Back to Main Menu"
            )
            select opt in "${options[@]}"; do
                case $opt in
                    "Check Apache error logs")
                        run_command "sudo tail -f /var/log/apache2/error.log"
                        ;;
                    "Check which process is using a port")
                        read -p "Enter the port number to check (e.g., 80): " port_number
                        run_command "sudo netstat -tuln | grep :$port_number"
                        ;;
                    "Test Apache configuration")
                        run_command "sudo apache2ctl configtest"
                        ;;
                    "Edit Apache configuration file")
                        run_command "sudo subl /etc/apache2/apache2.conf"
                        ;;
                    "Edit a site configuration file")
                        read -p "Enter the site config filename (e.g., 000-default.conf): " site_config
                        run_command "sudo subl /etc/apache2/sites-available/$site_config"
                        ;;
                    "Back to Main Menu")
                        break
                        ;;
                    *)
                        echo -e "\e[31m[ERROR] Invalid option. Try again.\e[0m"
                        ;;
                esac
            done
            ;;

        3)
            # Setup and Creation
            PS3=$'\n\e[35mSelect a setup option: \e[0m'
            options=(
                "Create Apache server from scratch"
                "Enable WebDAV modules"
                "Back to Main Menu"
            )
            select opt in "${options[@]}"; do
                case $opt in
                    "Create Apache server from scratch")
                        create_apache_from_template
                        ;;
                    "Enable WebDAV modules")
                        run_command "sudo a2enmod dav && sudo a2enmod dav_fs"
                        ;;
                    "Back to Main Menu")
                        break
                        ;;
                    *)
                        echo -e "\e[31m[ERROR] Invalid option. Try again.\e[0m"
                        ;;
                esac
            done
            ;;

        4)
            echo -e "\e[32mExiting Apache Genie. Goodbye!\e[0m"
            exit 0
            ;;

        *)
            echo -e "\e[31m[ERROR] Invalid category. Try again.\e[0m"
            ;;
    esac
done
