# Shelly Devices Checker V1.1
This script will call preconfigured IP addresses that re in the current network and fetch some of the returned informations.

Note: Works only with GEN-1 devices

## How to install 
1. Install python (version > 3.10) (https://www.python.org/downloads/)
2. Open command promt
3. To check if the python is installed successfully, execute the following command in the terminal: python --version
4. Download the project from the green button called "code" and then "Download ZIP"
5. Double-click on file called "SETUP"

## How to setup config file
Open the file called 'config' in your text editor.

Explanation of each variable:
 - delay - time in seconds after every check
 - attempts - number of attempts to get the data per device
 - attemptDelay - time in seconds after every attempt
 - devices - list of devices IPs
 
## How to run
Double-click file called "RUN"

## What the script does
The script will run until the user closes the terminal. It will fetch device's information and stores it in the file. 
It will make several attempts to get the data (configurable from the config file) with a custom delay between each try.

## Chanage log
 - v1.1 - Added SETUP file
 - v1.0 - Project init