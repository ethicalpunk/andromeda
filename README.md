# Andromeda
A script that sniffs ip packets and filters them according to your input. Originally made to make IP grabbing easier in online games.

Installation
============
    pip install -r requirements.txt
    
Documentation
============
**1.0 Before starting up the script, set the variable: wiresharkfolder to your wireshark.exe location. Eg: C:/Program Files/Wireshark/Wireshark.exe**

![Before running](https://github.com/ethicalpunk/andromeda/blob/main/docs/before_start.png "Before running")

**1.1 If the binary of Wireshark's location was invalid or does not exist, Andromeda will let you know something is wrong.**

![Before running error](https://github.com/ethicalpunk/andromeda/blob/main/docs/before_start_error.png "Before running error")


**2.0 Once the wireshark variable has been set correctly, you will be prompted to input an IP address. This IP must be the IP you wish to initiate a tap on.**

![First run](https://github.com/ethicalpunk/andromeda/blob/main/docs/first_start.png "First run")

**3.0 Once the IP you wish to initiate a tap on was given, Andromeda will now ask for a network interface.**

![First run interface](https://github.com/ethicalpunk/andromeda/blob/main/docs/first_run_interface.png "First run interface")

**4.0 Once the network interface was also given, Andromeda will now run with the given parameters. While Andromeda is running, you will see a small GUI window pop up with 4 buttons: __[Clear IP-list, Open Wireshark, Wireshark Tutorail, Quit]__. These buttons have the following definition.**

![First run main](https://github.com/ethicalpunk/andromeda/blob/main/docs/first_run_main.png "First run main")
    
    Clear IP-list: Clears the current output of IP addresses and starts over again.
    Open Wireshark: Open wireshark with the current set parameters. This allows you to futher inspect packets.
    Wireshark Tutorial: Redirects you to a link showing you a detailed instructions on how to use Wireshark.
    Quit: This button drops all threads and closes the program.
