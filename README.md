Apache Genie

Apache Genie is a Python-based utility that simplifies managing, configuring, and deploying an Apache server. With its interactive, step-by-step approach and cyberpunk-inspired theme, this script is perfect for users who want to manage or set up their Apache server while learning about its configurations.
Features

    Server Management:
        Restart, enable, and check the status of the Apache server.
    Diagnostics and Configuration:
        Check Apache error logs, view processes using specific ports, and test server configurations.
    Setup and Creation:
        Walk through creating an Apache server configuration from scratch, with clear prompts and explanations.
        Configure WebDAV for easy file hosting.
    Customizable Theme:
        Includes a green and purple cyberpunk-inspired terminal interface for a modern look.
    Educational:
        Displays the full configuration process step by step to help users understand and learn Apache configurations.

Installation
Prerequisites

Ensure you have the following installed:

    Python: Version 3.12 or later.
    Sublime Text (Optional): The script will use nano if Sublime Text is not installed.
    Apache: Ensure Apache is installed and running on your system.

Steps to Install

    Clone the repository to your preferred directory:

git clone https://github.com/m5trevino/apache-genie.git /path/to/your/directory

Replace /path/to/your/directory with the desired directory path.

Navigate to the directory:

cd /path/to/your/directory

Install dependencies using pip:

pip install -r requirements.txt

Add Apache Genie to your system's PATH for system-wide access:

sudo ln -s /path/to/your/directory/apache-genie.py /usr/local/bin/apache-genie

After this, you can run the script using:

    apache-genie

Usage
Running the Script

To start the script, simply type:

apache-genie

Interactive Menus

    Server Management:
        Restart the Apache server.
        Enable the Apache service to start on boot.
        Check the current status of the Apache server.

    Diagnostics and Configuration:
        View real-time Apache error logs.
        Check which process is using a specific port.
        Test the Apache server configuration for errors.

    Setup and Creation:
        Step-by-step walkthrough for creating a new Apache server configuration.
        Prompts for required information (e.g., private IP, document root, admin email).
        Explains configuration details as you go to help you understand the process.

Notes

    The script will automatically detect whether Sublime Text is installed. If not, it will use nano for editing configuration files.
    It displays your private IP during the configuration process to make it easier to set up your server.

Contribution

Feel free to fork the repository and submit pull requests for improvements or additional features.
License

Apache Genie is open-source and distributed under the MIT License. Contributions are welcome!