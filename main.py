###############################################################################
#
# (c) 2023 Schneider Electric SE. All rights reserved.
# All trademarks are owned or licensed by Schneider Electric SAS,
# its subsidiaries or affiliated companies.
#
###############################################################################

#Developed by: Gonzalo P
#Schneider Electric Project

import getpass
from hmac import new
from math import e
from turtle import clearscreen
import paramiko
import time
from dotenv import load_dotenv
import getpass
import threading
import sys
import select
import re
from datetime import datetime
import statistics

import os
import csv

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
import tkinter as tk
from tkinter import filedialog, messagebox


# --- SSH Key Selector UI ---
class SSHKeySelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SSH Key Selector")
        self.geometry("600x300")
        self.ssh_key_path = None

        self.label = tk.Label(self, text="Select your SSH key file:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self, width=40)
        self.entry.pack(pady=5)
        
        # Load last path if available
        try:
            with open("last_ssh_key.txt", "r") as f:
                last_path = f.read().strip()
                if last_path:
                    self.entry.insert(0, last_path)
                    self.ssh_key_path = last_path
                else:
                    print("No last SSH key path found.")
                    
        except FileNotFoundError:
            pass

        self.browse_button = tk.Button(self, text="Browse...", command=self.browse_file)
        self.browse_button.pack(pady=5)

        self.run_button = tk.Button(self, text="RUN", command=self.on_run)
        self.run_button.pack(pady=10)

    def browse_file(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select SSH Key File",
                filetypes=[("Private Key Files", "*.ppk *.pem *.key"), ("All Files", "*.*")]
            )
            if file_path:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, file_path)
                self.ssh_key_path = file_path
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while selecting the file: {e}")

    def on_run(self):
        try:
            self.ssh_key_path = self.entry.get()
            if not self.ssh_key_path or not os.path.isfile(self.ssh_key_path):
                messagebox.showerror("Error", "Please select a valid SSH key file.")
                return
            # Save the path
            with open("last_ssh_key.txt", "w") as f:
                f.write(self.ssh_key_path)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def get_ssh_key_path():
    try:
        app = SSHKeySelector()
        app.mainloop()
        return app.ssh_key_path
    except Exception as e:
        print(f"An error occurred while getting the SSH key path: {e}")
        return None


#Additional independent classes
class FileHandler:
    def __init__(self, filename):
        """
        Initialize the FileHandler with a filename.
        Parameters:
        filename (str): The name of the file to save data to.
        """
        self.filename = filename

    def save_data_to_csv(self, data):
        """
        Save data to a CSV file.

        Parameters:
        data (dict): The dictionary containing timestamps and signal strengths.
        """
        print("Saving plot data to CSV...")  # Debugging print statement
        timestamps = list(data.keys())
        signal_strengths = list(data.values())

        try:
            # Check if the file already exists
            file_exists = os.path.exists(self.filename)
            #print(f"File exists: {file_exists}\n")  # Debugging print statement

            # Open the file in append mode
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                
                # Write header if the file does not exist
                if not file_exists:
                    writer.writerow(["Timestamp", "Signal Strength (dBm)"])
                
                # Write data rows
                for ts, ss in zip(timestamps, signal_strengths):
                    writer.writerow([ts, ss])

            print(f"Plot data saved to {self.filename}")  # Debugging print statement

        except Exception as e:
            # Print error message if an exception occurs
            print(f"Error {e} when trying to save .csv")


class Model:
    
    #FIXME: Change to switch-case statement
    def __init__(self, ssh_client):
        self.ssh_client = ssh_client

    #model functioanity logic
    def modelApp(self):

        #Attempt to connect
        self.ssh_client.connect()
        print("""\n
        ###############################################################################
        #
        # (c) 2023 Schneider Electric SE. All rights reserved.
        # All trademarks are owned or licensed by Schneider Electric SAS,
        # its subsidiaries or affiliated companies.
        #
        ###############################################################################\n\n""")
        print("""\n
        ###################CCC Troubleshooting App MVC Model Prototype#####################
        
        Purpose: To fetch data for Controller in MVC Archicture that will be eventually used by CCC Support Team for diagnostic purposes.

        Version 1.0.0
        ################################################################################
        \n\n\n""")
        print("\n Designed and Developed by: Gonzalo Patino\n\n")
        #Open the shell
        initial_output = self.ssh_client.open_shell()
        #print("Initial shell output:")
        #print(initial_output)
        time.sleep(5)

        #Obtain serial number
        serial_number = input("\n\nPlease insert serial number:*")
        self.ssh_client.clean_serial_number(serial_number) #Setter: Make sure serial number is upper case and delete any unwanted spaces 
        #print(f"Debugging: Serial number inserted was:{self.ssh_client.serial_number}")

        

                
        #Prep command
        self.ssh_client.command = str(self.ssh_client.ssh_host) + ssh_client.serial_number

        #Authenticate serial number, if it is found, continue, otherwise, ..
        serial_status = self.ssh_client.validate_serial_number()

        #Verify connection
        self.ssh_client.try_connection(serial_status)

        
        

        #Fixme: Change for switch-case State machine with multiple threading
        while True:
            #If everything is good, the model is ready to accept requests from the controller
            print("\nValidation successful. Entering the model main menu...\n")
            

            print("""
            Available options: Please type the word to execute: 
            1. 'bye' - Close the SSH client and exit.
            2. 'redis' - Go into the Redis container and obtain Power Parameters from Scc Card
            3. 'signal strength' - Get the WiFi signal strength.
            4. 'network interface' - Get the network interface information.
            5. 'frequency band' - Get the frequency band information.
            6. 'wifi network driver' - Get the WiFi network driver information.
            7. 'process signal strength' - Process the signal strength dataset.
            8. 'plot signal strength' - Plot the signal strength data. Still Under Development- 
            9. 'hardware info' - Get hardware information including bootloader, firmware versions, and all hardware info.
            10. Any other command - Execute the command on the SSH client.
            """)



            print("\n*******************Main Menu- Model-Waiting for controller input******************************\n\n")
            command = input("Enter ssh: *")

            if command.lower() == 'bye':
                self.ssh_client.close()
                break
            elif command.startswith("redis"): #Go into redis container
                print("Redis case\n\n")             
                redisCommand = self.ssh_client.docker_redis_command_selector()
                value = self.ssh_client.docker_redis_session(redisCommand) #Go to docker redit container session 
                print(f"\nValue is: {value}")
            elif command == "signal strength":
                wifiAnalysisService = WifiAnalysis(self.ssh_client)
                wifiAnalysisService.getSignalStrength()
                
            elif command == "network interface":
                wifiAnalysisService = WifiAnalysis(self.ssh_client)
                wifiAnalysisService.getNetworkInterface()

            elif command == "frequency band":
                wifiAnalysisService = WifiAnalysis(self.ssh_client)
                wifiAnalysisService.getFreqBand()

            elif command == "wifi network driver":
                wifiAnalysisService = WifiAnalysis(self.ssh_client)
                wifiAnalysisService.getNetworkAdapterDriverInfo()

            elif command == "process signal strength":
                wifiAnalysisService = WifiAnalysis(self.ssh_client)
                wifiAnalysisService.processSignalStrengthDataSet()

            elif command == "plot signal strength":
                wifiAnalysisService = WifiAnalysis(self.ssh_client)
                wifiAnalysisService.plotSignalStrength()

            elif command == "hardware info":
                hardwareAnalysisService = HardwareInfo(self.ssh_client)
                #Testing bootloader version:
                bootLoaderVersion = hardwareAnalysisService.getBootLoaderVer()            
                print(f"Bootloader version is: *{bootLoaderVersion}*\n\n")

                #Testing firmware version:
                sccFirmwareVersion = hardwareAnalysisService.getSccFirmware()
                print(f"Firmware version is: *{sccFirmwareVersion}*\n\n")

                #Testing AFD firmware version:
                afdFirmwareVersion = hardwareAnalysisService.getAfdFirmware()
                print(f"AFD Firmware version is: *{afdFirmwareVersion}*\n\n")

                #Testing 
                allHardwareInfo = hardwareAnalysisService.getAllHardwareInfo()
                print(f"All hardware info is:\n\n {allHardwareInfo}\n")

            

                

            #only for SEIP testing

                
            else:
                print("else branch of state machine")
                output = self.ssh_client.execute_command(command)

#Children of Model Class
#class V1ProsumerService:


#Children of V1 Prosumer Service Class
class CloudClientConnection:
    print("")


#Children of V1 Prosumer Service Class
class SSHClientConnection:
    def __init__(self):
        self.ssh_host = "ssh fio@HY8K1NA1"+"-" 
        self.hostname = '52.172.50.136'
        self.port = 22
        self.username = 'azureuser'
        load_dotenv()
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.key_filename = os.getenv("SSH_KEY_FILENAME")
        self.key_file = os.path.join(self.project_root, self.key_filename)
        self.client = None
        self.shell = None
        self.output = ""
        self.serial_number=""
        self.password =""
        self.command = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            private_key = paramiko.RSAKey.from_private_key_file(self.key_file)
            self.client.connect(self.hostname, port=self.port, username=self.username, pkey=private_key)
            print(f"Connected to {self.hostname}")
        except Exception as e:
            print(f"An error occurred while connecting: {e}")

    def try_connection(self, serial_status):
        print("\n\nVerifying connection....\n")

        while "No route to host" in serial_status:
            print("\n SCC is not connected to the internet. Please try another serial number:")
            self.serial_number= input("\nPlease insert new serial number:*")
            self.serial_status = self.validate_serial_number()
            self.try_connection(self.serial_status)

            self.command = self.ssh_host + self.serial_number
            
            if self.shell:
                print("Debbuging: self.shell true")
                try:
                    self.shell.send(self.command + '\n')
                    output = ""
                    while True:
                        if self.shell.recv_ready():
                            chunk = self.shell.recv(1024).decode()
                            output += chunk
                            print(chunk, end='')  # Print the chunk to show real-time output
                            if "password:" in chunk.lower():
                                #password = getpass.getpass("Enter password: ")
                                password = input("Please insert password:*")
                                self.shell.send(password + '\n')
                            elif output.strip().endswith("$"):
                                if "not found" in chunk or "failure" in chunk:
                                    print("Serial number not found")
                                    new_serial_number = input("\nPlease insert new serial number:*")
                                    self.clean_serial_number(new_serial_number)
                                    self.command = "ssh fio@HY8K1NA1"+"-"+self.serial_number
                                    self.shell.send(self.command + '\n')


                                else:
                                    #Get out of the loop and continue with the login process
                                    break
                        
                        time.sleep(0.1)  # Small delay to allow more data to be received

                    #Got out of while loop; serial numbe was validated
                    break
                except Exception as e:
                    print(f"An error has occured: {e}")
            
        print("Scc connected to Wifi")


    def open_shell(self):
        if self.client:
            try:
                self.shell = self.client.invoke_shell()
                print("Interactive shell opened.")
                return self.read_shell_output()
            except Exception as e:
                print(f"An error occurred while opening the shell: {e}")
        else:
            print("Client is not connected.")

    def password_decoder(self, password):
        print("FIXME: I want to be able to decode the password in case it fails automatically. I return the correct password")
        #switch case
        #case 1: standard password
        #case 2: second standard password
        #case 3: MAC address algorithm

        #This method returns correct password after decoding

    def read_shell_output(self):
        output = ""
        while not output.strip().endswith("$"):
            if self.shell.recv_ready():
                output += self.shell.recv(1024).decode()
                time.sleep(0.1)  # Small delay to allow more data to be received
        print(output)
        return output

    def validate_serial_number(self):
        if self.shell:
            try:
                self.shell.send(self.command + '\n')
                output = ""
                while True:
                    if self.shell.recv_ready():
                        chunk = self.shell.recv(1024).decode()
                        output += chunk
                        print(chunk, end='')  # Print the chunk to show real-time output
                        if "password:" in chunk.lower():
                            #password = getpass.getpass("Enter password: ")
                            password = input("Please insert password:*")
                            self.shell.send(password + '\n')
                        elif output.strip().endswith("$"):
                            if "not found" in chunk or "failure" in chunk:
                                print("Serial number not found")
                                new_serial_number = input("\nPlease insert new serial number:*")
                                self.clean_serial_number(new_serial_number)
                                self.command = "ssh fio@HY8K1NA1"+"-"+self.serial_number
                                self.shell.send(self.command + '\n')


                            else:
                                #Get out of the loop and continue with the login process
                                break
                        
                    time.sleep(0.1)  # Small delay to allow more data to be received

                #Got out of while loop; serial numbe was validated
                return output


                

            except Exception as e:
                print(f"An error occurred while executing the command: {e}")
        else:
            print("Shell is not open.")
            return None

    def docker_redis_command_selector(self):
        try:
            print("SCC Sysvars. Please select an option from the list below:\n")
            print("1. Total Grid Power\n")
            print("2. Total Power Consumed By The Load\n")
            print("3. Total Battery Power\n")
            print("4. Total AC Power Inverter\n")
            print("5. Total PV DC Power Inverter\n")
            print("6. Total PV AC Power Inverter\n")
            selection = int(input("Please select an option:*\n"))

            if selection == 1:
                print("You selected Total Grid Power:\n")
                command = "svget /SYS/MEAS/STAT/GRID/P_TOTAL"
                return command
            elif selection == 2:
                print("You selected Total Power Consumed By The Load:\n")
                command = "svget /SYS/MEAS/STAT/LOAD/P_TOTAL"
                return command
            elif selection == 3:
                print("You selected Total Battery Power:\n")
                command = "svget [0]/INV/RTD/STAT/BATT/P"
                return command
            elif selection == 4:
                print("You selected Total AC Power Inverter:\n")
                command = "svget [0]/INV/RTD/STAT/AC/P_TOTAL"
                return command
            elif selection == 5:
                print("You selected Total PV DC power Inverter:\n")
                command = "svget [0]/INV/RTD/STAT/PV/P"
                return command
            elif selection == 6:
                print("You selected Total PV AC power Inverter:\n")
                command = "svget /SYS/MEAS/STAT/ACPV/P_TOTAL"
                return command
            else:
                print("You chose a wrong option")
                return None
            

        except Exception as e:
            print(f"Error during choosing a selection for redis container: {e}")




    def docker_redis_session(self, redisCommand):
        #Accesses the redis container and returns the physical value requested
        docker_redis_command = redisCommand
        command = "docker exec -it apps-redis-1 sh"
        def find_and_convert_floats(s):
            # Regular expression to match float numbers
            float_pattern = r'\b\d+\.\d+\b'
            float_strings = re.findall(float_pattern, s)
            # Convert matched strings to float
            float_numbers = [float(num) for num in float_strings]
            #print(f"Debugging: Float number detected is {float_numbers}[unit: watts, etc]\n")
            return float_numbers

        #print("Debugging: Redis Container Session...procesing...please wait...")
        output = str(self.execute_command(command))
        #print(f"Debugging: Output from docker redis is: {output}\n")
        #FIXMEWait until asking for command
        #FIXMEwhile not output.strip().endswith("#"):
        #FIXME    print("Loading docker...")
        #FIXME    time.sleep(0.1)
        time.sleep(0.5) #Wait for command
        #print("Debugging:Docker processing...please wait...:\n")
        docker_redis_command = docker_redis_command
        redis_container_ouput = self.execute_command(docker_redis_command) #Send docker redis command, get the output
        print(f"redis_container_output is: {redis_container_ouput}\n")
        #Process and obtain value
        value = statistics.mean(find_and_convert_floats(str(redis_container_ouput)))
        

        time.sleep(0.5)
        self.execute_command("exit") #close the session
        print("Left the docker redis session\n")
        return value

    def info_docker_redis_session(self, redisCommand):
        #Accesses the redis container and returns information requested
        docker_redis_command = redisCommand
        command = "docker exec -it apps-redis-1 sh"
        

        print("Info Redis Container Session...procesing...please wait...")
        output = str(self.execute_command(command))
        #print(f"Debugging: Output from docker redis is: {output}\n")
        #FIXMEWait until asking for command
        #FIXMEwhile not output.strip().endswith("#"):
        #FIXME    print("Loading docker...")
        #FIXME    time.sleep(0.1)
        time.sleep(0.5) #Wait for command
        #print("Debugging: Docker processing...please wait...:\n")
        docker_redis_command = docker_redis_command
        redis_container_ouput = self.execute_command(docker_redis_command) #Send docker redis command for info, get the output
        #print(f"Debugging: redis_container_output info is: {redis_container_ouput}\n")
        #Process and obtain value
        
    

        time.sleep(0.5)
        self.execute_command("exit") #close the session
        #print("Debugging: Exited the docker redis session\n")
        return redis_container_ouput






    def clean_serial_number(self, serial_number):
        self.serial_number = serial_number.upper().replace(" ", "")
        
        
    
    def execute_command_login(self, command):
        if self.shell:
            try:
                self.shell.send(command + '\n')
                output = ""
                while True:
                    if self.shell.recv_ready():
                        chunk = self.shell.recv(1024).decode()
                        output += chunk
                        print(chunk, end='')  # Print the chunk to show real-time output
                        if "password:" in chunk.lower():
                            #password = getpass.getpass("Enter password: ")
                            password = input("Please insert password:*")
                            self.shell.send(password + '\n')
                        elif output.strip().endswith("$"):
                            break
                    time.sleep(0.1)  # Small delay to allow more data to be received
                return output
            except Exception as e:
                print(f"An error occurred while executing the command: {e}")
        else:
            print("Shell is not open.")
            return None

    def shell_data_available(self):
        while True:
            if self.shell.recv_ready():
                print("Data is ready")          
                break;
            else:
                print("Data not available yet")
        return True     
    
    def clear_screen(self):
        if self.shell:
            try:
                self.shell.send('clear\n')
                time.sleep(0.1)  # Small delay to allow the command to execute
                self.read_shell_output()  # Read the output to clear the buffer
                print("Screen cleared.")
            except Exception as e:
                print(f"An error occurred while clearing the screen: {e}")
        else:
            print("Shell is not open.")
        
        
        
        



    def execute_command(self, command):
            if self.shell:
                try:
                    self.shell.send(command + '\n')
                    time.sleep(5)  # Small delay to add time to receive data
                    output = self.get_output_from_console()
                    
                    return output

                except Exception as e:
                    print(f"An error occurred while executing the command: {e}")
        
        
        
            else:
                print("Shell is not open.")
                return None



    def close(self):
        if self.client:
            try:
                self.client.close()
                print("Connection closed.")
            except Exception as e:
                print(f"An error occurred while closing the connection: {e}")
        else:
            print("No active connection to close.")


    def get_output_from_console(self):
        
        
        #print("Debugging: get_output_from_console method\n")
        
        
        try:
            #Check if there is any data available to be read from the shell. It returns True if there is data ready to be received.
            if self.shell.recv_ready():
                self.output = ""  # Clear previous output
                #Read 1024 bytes of data from the shell and decode it from bytes to a string
                chunk = self.shell.recv(1024).decode()
                # Filter out escape sequences
                chunk = re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', chunk)
            
                #Append to output string
            
                self.output += chunk
                #print(f"Debugging- get_output_from_console self.output: ****{self.output}****\n")
                
            
                return self.output
            else:
                print("No data available to read from the shell")
                return None
        except Exception as e:
            print(f"Not able to get output from console: {e}")



#children of SSHClientConnection Class:
class WifiAnalysis:
    def __init__(self, sshClientConnection):
        self.sshClientConnection = sshClientConnection
        self.SignalStrengthCSVlocation = r"C:\Users\sesa800227\source\repos\WebTool\plot_data_signal_strength.csv"
        self.fileHandler = FileHandler(self.SignalStrengthCSVlocation)   
        self.wifiParams = {
        "networkInterface": "",
        "frequencyBand": "",
        "wifiChan": "",
        "wifiSSID": "",
        "networkDriver": "",
        "meshNetwork": None,
        "wifiSignalStrength": {}  # "timestamp", "float value"
        }
    def getSignalStrength(self):
        print("Getting Signal strength...Please wait....")
        
        # Example command to get WiFi signal strength
        command = "iw dev wlan0 station dump | grep 'signal:'"  # Replace with the actual command you need
        signal_strength_output = self.sshClientConnection.execute_command(command)

        # Debugging: Print the raw output from the command
        #print(f"Debugging: Raw command output: {signal_strength_output}")

        # Wait for the command to execute
        time.sleep(1)

        # Extract the signal strength value using regular expressions
        match = re.search(r"signal:\s*(-?\d+)", signal_strength_output)

        if match:
            signal_strength_value = float(match.group(1))
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.wifiParams["wifiSignalStrength"][timestamp] = signal_strength_value
            # Debug print statement to confirm storage in dictionary
            print(f"\nExtracted signal strength: {signal_strength_value} dBm at {timestamp}")
            print(f"Stored in dictionary: {self.wifiParams['wifiSignalStrength'][timestamp]} dBm at {timestamp}")
            return self.wifiParams['wifiSignalStrength'][timestamp]
        else:
            print("Signal strength not found in the output.")
            return None

    def getNetworkInterface(self):
        #Provides information about the current SSID using wLan0
        print("Getting Wifi Network Adapter Data")
        
        command = "sudo iw dev wlan0 link"  # Replace with the actual command you need

        networkInterface = self.sshClientConnection.execute_command_login(command) #Because password will be required
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.wifiParams["networkInterface"] = str(networkInterface) #add to dictionary
        networkInterface = self.wifiParams["networkInterface"] #get from dictionary

        print(f"\n Extracted Wifi Network Adapter Data: {networkInterface} at {timestamp}")
        return networkInterface

    def getFreqBand(self):
        #Provides information on different frequency bands 
        #(like 2.4 GHz and 5 GHz) that inverter's Wi-Fi adapter use.
        # It will also provide additional details about each frequency band, such as supported channels and power limits.
        print("Getting Available Wifi Network Adapter Frequency Bands Info... \n")
        command = "iw list | grep -A 10 Frequencies"
        freqBand= self.sshClientConnection.execute_command(command)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.wifiParams["frequencyBand"] = str(freqBand) #add to dictionary
        freqBand = self.wifiParams["frequencyBand"]

        print(f"\n Extracted Frequency Band Data: {freqBand} at {timestamp}")
        return freqBand

    def getNetworkAdapterDriverInfo(self):
        """
        Retrieves detailed information about network interfaces,
        with a focus on extracting and emphasizing Wi-Fi driver information.

        Returns:
        String: A string containing Wi-Fi interface names as keys
            and their corresponding driver information (driver name and version) as values.
        """

        print("\nGetting Network Adapter Driver Info... \n")
        command = "sudo lshw -C network"
        networkDriver= self.sshClientConnection.execute_command_login(command)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.wifiParams["networkDriver"] = str(networkDriver) #add to dictionary
        networkDriver = self.wifiParams["networkDriver"]

        print(f"\n Extracted Network Driver Data: {networkDriver} \n at {timestamp}")
        return networkDriver


    def processSignalStrengthDataSet(self): # Step 7: Return None if not enough samples are collected
        """
        Process the signal strength data set to calculate the average signal strength.
    
        Returns:
        dict: The dictionary containing the average signal strength with timestamp, or None if not enough samples are collected.
        """
        print("Processing Signal Strength Data Set...\n")  # Step 1: Print start message
        temp_signal_strengths = []  # Step 2: Initialize temporary list for signal strength samples

        for _ in range(2):  # Step 3: Collect 5 signal strength samples
            signal_strength = self.getSignalStrength()  # Collect signal strength sample
            if signal_strength is not None:
                temp_signal_strengths.append(signal_strength)  # Add sample to temporary list
            #time.sleep(0.1)  # Adjust the sleep time as needed

        #print(f"\nDebugging: Collected signal strengths: {temp_signal_strengths}\n")  # Debugging print statement

        if len(temp_signal_strengths) >= 2:  # Step 4: Check if enough samples are collected
            avg_signal_strength = sum(temp_signal_strengths) / len(temp_signal_strengths)  # Calculate average signal strength
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
            self.wifiParams["wifiSignalStrength"][timestamp] = avg_signal_strength  # Step 5: Store average signal strength with timestamp
            print(f"\nProcessed average signal strength: {avg_signal_strength} dBm at {timestamp}\n")  # Step 6: Print processed average signal strength
            print(f"\nProcessed average signal strength dataset in dictionary temporarily is: {self.wifiParams['wifiSignalStrength']}\n")  # Debugging print statement
            return self.wifiParams["wifiSignalStrength"]  # Step 6: Return the dictionary
        else:
            print("Not enough data points collected.\n")  # Step 7: Print error message if not enough samples
            return None  # Step 7: Return None if not enough samples are collected


    def plotSignalStrength(self):
        """
        Plot the signal strength data and update the chart every 5 seconds with new dataset values.

        Steps:
        1. Initialize the plot with labels and titles.
        2. Continuously update the plot with new data in a while loop.
        3. Exit the loop gracefully using Ctrl+C.
        """
        print("Initializing plot...")  # Debugging print statement
        plt.ion()  # Enable interactive mode
        fig, ax = plt.subplots()
        ax.set_title('WiFi Signal Strength Over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Signal Strength (dBm)')
        line, = ax.plot([], [], 'r-')  # Initialize an empty plot

        start_time = datetime.now()
        timestamps = []
        signal_strengths = []

        try:
            while True:
                try:
                    print("\nAttempting to get dataset..Please wait 10 seconds or press control+C to exit...")  # Debugging print statement
                    dataset = self.processSignalStrengthDataSet()  # Update the dataset
                    if dataset:
                        print("Updating plot with new data...\n")  # Debugging print statement
                        timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in self.wifiParams["wifiSignalStrength"].keys()]
                        signal_strengths = list(self.wifiParams["wifiSignalStrength"].values())
                        #print(f"Debugging: Timestamps - {timestamps}\n")  # Debugging print statement
                        #print(f"Debugging: Signal Strengths - {signal_strengths}\n")  # Debugging print statement
                        line.set_data(timestamps, signal_strengths)
                        locator = mdates.AutoDateLocator()
                        formatter = mdates.ConciseDateFormatter(locator)
                        ax.xaxis.set_major_locator(locator)
                        ax.xaxis.set_major_formatter(formatter)
                        ax.relim()
                        ax.autoscale_view()
                        plt.draw()
                        print(f"Plot updated with data: {dataset}")  # Debugging print statement
                        # Save plot data to CSV
                        self.fileHandler.save_data_to_csv(self.wifiParams["wifiSignalStrength"])
                        print("Saved data to .csv...\n")
                    else:
                        print("Waiting for dataset...Press keyboard to exit")  # Inform that waiting on dataset

                    plt.pause(0.5)  # Pause for 0.5 seconds before updating again
                except Exception as e:
                    print(f"An error occurred: {e}")
                    time.sleep(5)  # Wait before retrying
        except KeyboardInterrupt:
            print("Exiting plot update loop...")
            
            return "Plotting completed successfully."


#children of SSHClientConnection Class:
class HardwareInfo:
    def __init__(self, sshClientConnection):
        self.sshClientConnection = sshClientConnection
        self.bootLoaderVer = ""
        self.sccFirmware = ""
        self.afdFirmware =""
        self.inverterFirmware = ""
        self.bcsFirmware = ""

    def _extract_version(self, output):
        """
        Extracts the version number from the given output string.
        
        Args:
            output (str): The output string containing the version information.
        
        Returns:
            str: The extracted version number.
        """
        try:
            # Split the output by newline and strip any leading/trailing whitespace
            version = output.split("\n")[1].strip()
            return version
        except IndexError:
            print("Error: Output format is incorrect.")
            return None


    def getBootLoaderVer(self):
        print("\nGetting BootLoader Version")
        bootloaderCommand = "svget [0]/INV/ID/STAT/DSP1_BOOTLOADER_VERSION"
        
        try:                     
            bootLoaderVer = self.sshClientConnection.info_docker_redis_session(bootloaderCommand)
            #print(f"Debugging: bootLoaderVer after obtaining from info.docker_redis_session is:\n{bootLoaderVer}")
            
            self.bootLoaderVer = self._extract_version(bootLoaderVer)#Extract bootloader from output
            #print(f"Debugging:self.bootloader after splitting in method is: {self.bootLoaderVer}\n\n")
            
            return self.bootLoaderVer


        except Exception as e:
            print(f"Error getting bootloader version: {e}")
            return None
        
    def getSccFirmware(self):
        #print("\nDebugging: Getting Firmware Version:\n\n")
        firmwareCommand = "svget [0]/INV/FWUP/STAT/CURRENT_VERSION"

        try:         
            firmwareVer = self.sshClientConnection.info_docker_redis_session(firmwareCommand)
            #print(f"Debugging: firmware version after obtaining from info.docker_redis_session is:\n{firmwareVer}")
            
            self.firmwareVer = self._extract_version(firmwareVer)#Extract firmware version from output
            #print(f"Debugging:self.firmwareVer after splitting in method is: {self.firmwareVer}\n\n")
            
            return self.firmwareVer
        except Exception as e:
            print(f"Error getting firmware version: {e}")
            return None


    def getAfdFirmware(self):
        #print("\nDebugging: Getting AFD Firmware Version:\n\n")
        #svget [0]/INV/ID/STAT/AFD_FW_VERSION
        
        afdFirmwareCommand = "svget [0]/INV/ID/STAT/AFD_FW_VERSION"

        try:         
            afdFirmwareVer = self.sshClientConnection.info_docker_redis_session(afdFirmwareCommand)
            #print(f"AFD firmware version after obtaining from info.docker_redis_session is:\n{afdFirmwareVer}")
            
            self.afdFirmwareVer = self._extract_version(afdFirmwareVer)#Extract AFD firmware version from output
            #print(f"Debugging:self.elf.afdFirmwareVer after splitting in method is: {self.afdFirmwareVer}\n\n")
            
            return self.afdFirmwareVer
        except Exception as e:
            print(f"Error getting AFD firmware version: {e}")
            return None


    def invFirmware(self):
        print("Fixme")
        #need to ask whta the command is
    def getBcsFirmware(self):
        print("Fixme")
        #need to ask whta the command is
    def getAllHardwareInfo(self):
        print("\n Print all hardware info:\n")
        bootLoaderInfo = str(self.getBootLoaderVer())
        sccFirmwareInfo = str(self.getSccFirmware())
        afdFirmwareInfo = str(self.getAfdFirmware())

        return (bootLoaderInfo +"\n"+ sccFirmwareInfo +"\n"+ afdFirmwareInfo +"\n")
        


#Cloud Module

#This should go in an independent file in the project as static params
if __name__ == "__main__":
    # Get SSH key path from user
    key_path = get_ssh_key_path()
    if not key_path:
        print("SSH key path is required to proceed. Exiting the application.")
        exit(1)
    # Create SSH client and set the key file
    ssh_client = SSHClientConnection()
    
    
    ssh_session = Model(ssh_client)


    print("*****************V1 SSH TOOL- V1*****************\n")
    
    try:
        
        ssh_session.modelApp()
        
        
    except Exception as e:
        print(f"An error occured while logging in: {e}")
        



                
            