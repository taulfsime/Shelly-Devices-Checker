# Shelly Devices Checker
This script will call preconfigured IP addresses in the current network and save some of the information about devices.

## How to use 
1. Install python and make sure that "Add Python to path" option is enabled (https://www.python.org/downloads/)
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
 - actions - list of actions

Actions:
 - CanNotReach
   - Desc: Execute the action if the target can't be reached after all attemps
   - Target: IP of device
 - CheckVar
   - Desc: Execute the action comparion of specific value to target value is successfull
   - Target: IP of device
   - Var: Key for specific value from device
   - Check: Comparison type, allowed values are higher, lower or equal(should be used only with bool values)
   - Value: Target value

## How to run
Double-click file called "RUN"

## What the script does
The script will run until the user closes the terminal. It will fetch device's information and stores it in the file. 
It will make several attempts to get the data (configurable from the config file) with a custom delay between each try.

## Chanage log
 - v1.3 - Add Device Base class, fetch device's temperature value, added version check
 - v1.2 - Added support for second gen devices and the data is saved in .csv file
 - v1.1 - Added SETUP file
 - v1.0 - Project init