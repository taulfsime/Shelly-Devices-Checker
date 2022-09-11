# Shelly Devices Checker
This script will call preconfigured IP addresses in the current network and save some of the information about devices. Suppport wenhooks which will run based on a condition and can execute multiple actions.

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
 - webhooks - list of webhooks

Webhooks:
 - CanNotReach
   - Desc: Execute actions if the target can't be reached after all attemps
   - Target: IP of device
 - CheckVar
   - Desc: Execute actions if the comparison of specific value to target value is successful
   - Target: IP of device
   - Var: Key for specific value from device
   - Check: Comparison type, allowed values are higher, lower or equal(should be used only with bool values)
   - Value: Target value
 - EachCheck
   - Desc: Execute actions on each attemp to fetch data

## How to run
Double-click file called "RUN"

## What the script does
The script will run until the user closes the terminal. It will fetch device's information and stores it in the file. 
It will make several attempts to get the data (configurable from the config file) with a custom delay between each try.
The scipt support multiple webhooks with the following conditions: when the device can't be reached after all attempts, based on values comparison, on each attempt to fetch data. You can execute multiple actions, currectly supported are request to specific URL, add to event log, print to console.

## Change log
 - v1.4 - Added webhooks and event log
 - v1.3 - Added device base class, fetch device's temperature value and added version check at start
 - v1.2 - Added support for second gen devices and the data is saved in .csv file
 - v1.1 - Added SETUP file
 - v1.0 - Project init