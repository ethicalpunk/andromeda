from scapy.all import *
import ipaddress
from threading import Thread
import time
from sys import platform
import maxminddb
from colorama import Fore
from pyfiglet import Figlet
import tkinter as tk
from tkinter import ttk
import subprocess
import webbrowser
import os
import datetime
import urllib.request

try:
    endpoint = 'https://wtfismyip.com/text'
    data = urllib.request.urlopen(endpoint).read()
    EXT_IP = data.decode().strip()
except:
    endpoint = 'https://api.my-ip.io/ip'
    data = urllib.request.urlopen(endpoint).read()
    EXT_IP = data.decode().strip()

def banner():
    f = Figlet()
    return f.renderText('ANDROMEDA')

class variables:
    iplist = {}
    runwire = False
    wiresharkfolder = "C:/Program Files/Wireshark/Wireshark.exe" # Set this variable to your wireshark installation. Eg: C:/Program Files/Wireshark/Wireshark.exe
    DBhost = '62.195.126.36'
    DBport = 34890
    DBuser = 'ANDROMEDA_CLIENT_1'
    DBpassword = 'D7KivekOMAYOjOwi51jumesoDoJIxA'
    DBdatabase = 'ANDROMEDA_DATA'

class windowtext:
    clearterminaltext = "Clear IP-list"
    openwireshark = "Open Wireshark"
    wiresharktutorail = "Wireshark Tutorial"
    wiresharktutorailurl = "https://www.javatpoint.com/wireshark"
    QUIT = "Quit"
    runningwindowtext = None

class windowfunctions():
    def clearterminal():
        global iplist
        print(f"{Fore.RED}Clearing IP-list....{Fore.WHITE}")
        variables.iplist = {}

    def openwireshark():
        print(f"{Fore.RED}Opening wireshark.....{Fore.WHITE}")
        if variables.runwire == True:
            subprocess.call(
            [
                variables.wiresharkfolder, "-Y", 
                f"ip.dst == {host} and not ip.src == {host}/24"
                ]
            )

    def runwireshark():
        Thread(target = windowfunctions.openwireshark).start()

    def wiresharktutorail():
        webbrowser.open_new(windowtext.wiresharktutorailurl)

class GEOIP:
    ASN = maxminddb.open_database("ipdatabase/GeoLite2-ASN.mmdb")
    CITY = maxminddb.open_database("ipdatabase/GeoLite2-City.mmdb")
    COUNTRY = maxminddb.open_database("ipdatabase/GeoLite2-Country.mmdb")

class PROCESS_GEOIP:
    def getinfo(IP):
        try:
            asncode = GEOIP.ASN.get(IP)['autonomous_system_number']
        except (KeyError, IndexError, ValueError, TypeError):
            asncode = "None"
        try:
            asn = GEOIP.ASN.get(IP)['autonomous_system_organization']
        except (KeyError, IndexError, ValueError, TypeError):
            asn = "None"
        try:
            city = GEOIP.CITY.get(IP)['city']['names']['en']
        except (KeyError, IndexError, ValueError, TypeError):
            city = "None"
        try:
            country = GEOIP.COUNTRY.get(IP)['registered_country']['names']['en']
        except (KeyError, IndexError, ValueError, TypeError):
            country = "None"
        try:
            timezone = GEOIP.CITY.get(IP)['location']['time_zone']
        except (KeyError, IndexError, ValueError, TypeError):
            timezone = "None"
        try:
            iso_code = GEOIP.COUNTRY.get(IP)['registered_country']['iso_code']
        except (KeyError, IndexError, ValueError, TypeError):
            iso_code = "None"

        info = f"{Fore.CYAN}| {Fore.WHITE}[{Fore.LIGHTGREEN_EX}ASN{Fore.WHITE}]: ({asn} ({asncode})) {Fore.CYAN}| {Fore.WHITE}[{Fore.LIGHTGREEN_EX}COUNTRY {Fore.WHITE}({iso_code})]: ({country} ({city})) {Fore.CYAN}| {Fore.WHITE}[{Fore.LIGHTGREEN_EX}TIMEZONE{Fore.WHITE}]: ({timezone})"
        
        return info

class SYSTEM:
    def date():
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        return dt_string

    def systemclear():
        if platform == "linux" or platform == "linux2":
            return "clear"
        elif platform == "win32" or platform == "win64":
            return "cls"
        else:
            print("{Fore.RED}This OS is not supported\nOS'es that are supported:{Fore.WHITE}\n\n[1] Linux\n[2] Windows")
            os._exit(0)

    def getinterfaces(PLATFORM):
        interfacelist = ""
        if PLATFORM == "linux":
            interfaces = ([x.split() for x in os.popen("ip link show").readlines() if x[0].isdigit()])
            for row in interfaces:
                interfacelist += f"{Fore.WHITE}{row[1]}\n"

        elif PLATFORM == "win32" or platform == "win64":
            interfaces = ([x.split() for x in os.popen("netsh interface ip show interfaces").readlines() if len(x)>1])
            for row in interfaces:
                for x, xrow in enumerate(row):
                    if xrow in ('disconnected', 'connected'):
                        interfacestatus = row[x]
                        interface = ' '.join(row[x+1:])

                        if interfacestatus == "connected":
                            interfacelist += (f"\n[{Fore.WHITE}{interface}] -> {Fore.GREEN}{interfacestatus}{Fore.WHITE}")
                        else:
                            interfacelist += (f"\n[{Fore.WHITE}{interface}] -> {Fore.RED}{interfacestatus}{Fore.WHITE}")

                        break
    
        else:
            interfaces = None

        return interfacelist

    def getinterface():
        try:
            try:
                save = open("ipdatabase/.interface.txt", "r").read().strip()
                
                if len(save) <= 0: raise ValueError            

                x = input(f"{Fore.WHITE}A previously used network interface was detected {Fore.LIGHTRED_EX}({Fore.LIGHTGREEN_EX}{save}{Fore.LIGHTRED_EX}){Fore.WHITE}, would you like to use this interface again? {Fore.LIGHTYELLOW_EX}[{Fore.LIGHTGREEN_EX}yes{Fore.LIGHTRED_EX}/{Fore.LIGHTGREEN_EX}no{Fore.LIGHTYELLOW_EX}]{Fore.WHITE}: ")        
                
                if len(x) == 0:
                    x = "yes"

                if x.lower() == "yes" or x.lower() == "y": interface = save
                elif x.lower() == "no" or x.lower() == "n":
                    save = open("ipdatabase/.interface.txt", "w+"); save.close(); raise ValueError

            except (ValueError, FileNotFoundError):
                print(SYSTEM.getinterfaces(platform))
                interface = input(f"\n{Fore.LIGHTYELLOW_EX}Input interface{Fore.LIGHTWHITE_EX}: ")
                save = open("ipdatabase/.interface.txt", "w+"); save.write(interface); save.close()

            return interface
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Bye!....{Fore.WHITE}")
            os._exit(0)

class IP_FUNCTIONS:
    def previousIP():
        print(banner())
        try:
            save = open("ipdatabase/.ip.txt", "r").read().strip()
            host = ipaddress.ip_address(save)

            while True:
                x = input(f"{Fore.WHITE}A previously used IP Address was detected {Fore.LIGHTRED_EX}({Fore.LIGHTGREEN_EX}{host}{Fore.LIGHTRED_EX}){Fore.WHITE}, would you like to use this IP again? {Fore.LIGHTYELLOW_EX}[{Fore.LIGHTGREEN_EX}yes{Fore.LIGHTRED_EX}/{Fore.LIGHTGREEN_EX}no{Fore.LIGHTYELLOW_EX}]{Fore.WHITE}: ")
                
                if len(x) == 0:
                    x = "yes"

                if x.lower() == "yes" or x.lower() == "y": break
                elif x.lower() == "no" or x.lower() == "n":
                    save = open("ipdatabase/.ip.txt", "w+"); save.close()
                    raise ValueError
                else:
                    print(f"\n{Fore.WHITE}The answer {Fore.LIGHTRED_EX}({Fore.LIGHTGREEN_EX}{x}{Fore.LIGHTRED_EX}){Fore.LIGHTWHITE_EX} to a {Fore.LIGHTYELLOW_EX}[{Fore.LIGHTGREEN_EX}yes{Fore.LIGHTRED_EX}/{Fore.LIGHTGREEN_EX}no{Fore.LIGHTYELLOW_EX}]{Fore.WHITE} question was invalid. Try again with either {Fore.LIGHTRED_EX}yes{Fore.WHITE} or {Fore.LIGHTRED_EX}no{Fore.WHITE}\n")
                    continue

        except (ValueError, FileNotFoundError):
            try:
                
                while True:
                    try:
                        host = input(f"{Fore.LIGHTYELLOW_EX}Input IP{Fore.LIGHTWHITE_EX}: ").strip()
                        checkhost = ipaddress.ip_address(host)
                        save = open("ipdatabase/.ip.txt", "w+"); save.write(host); save.close(); break

                    except ValueError:
                        print(f"\n{Fore.WHITE}The IP Address {Fore.LIGHTGREEN_EX}({Fore.LIGHTRED_EX}{host}{Fore.LIGHTGREEN_EX}){Fore.WHITE} in not a valid IP. Try again.....\n")
                        continue

            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Bye!....{Fore.WHITE}")
                os._exit(0)

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Bye!....{Fore.WHITE}")
            os._exit(0)

        global firstoct, secondoct, thirdoct, fourthoct
        firstoct, secondoct, thirdoct, fourthoct = str(host).split(".")

        return host

    def displayips():
        while True:
            sort = sorted(variables.iplist.items(), key=lambda x: x[1], reverse=True); sort.reverse()
            sortedlist = ""
            BLACKLIST = ([x.strip() for x in open("conf/BLACKLIST.config", "r").readlines()])
            
            for value in sort:
                if f"{firstoct}.{secondoct}.{thirdoct}." in value[0].strip():
                    pass
                else:
                    if value[0].strip() not in BLACKLIST:
                        sortedlist += f"{Fore.LIGHTRED_EX}{value[0]} {Fore.LIGHTYELLOW_EX}-> {Fore.LIGHTWHITE_EX}{value[1]} {PROCESS_GEOIP.getinfo(value[0])}\n"

            sortedlist = ([x for x in sortedlist.split("\n") if len(x)>1])

            count = 1; staticcount = len(sortedlist)

            if staticcount == 0:
                print(f"{Fore.LIGHTWHITE_EX}[ ⚠️ {Fore.LIGHTYELLOW_EX} No traffic detected yet{Fore.LIGHTWHITE_EX}]")

            for row in sortedlist:
                if len(row) > 1:
                    print(f"[{Fore.LIGHTGREEN_EX}{count}-{staticcount}{Fore.LIGHTWHITE_EX}] {row}")
                    count+=1

            print(); time.sleep(3.5); os.system(SYSTEM.systemclear())
            
    def getsniff(packet):
        try:
            source = packet.getlayer(IP).src
            #dest = packet.getlayer(IP).dst
            if source == host:
                pass
            else:
                if source in variables.iplist:
                    variables.iplist[source] = variables.iplist[source] + 1
                else:
                    variables.iplist[source] = 1

        except AttributeError:
            pass

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Bye!....{Fore.WHITE}")
            os._exit(0)

    try:
        print(banner())
        save = open(variables.wiresharkfolder, "rb")

    except FileNotFoundError:
        print(f"\n{Fore.WHITE}It seems that the given folder: {Fore.RED}({Fore.LIGHTGREEN_EX}{variables.wiresharkfolder}{Fore.RED}){Fore.WHITE} was invalid and Andromeda will not be able to use the wireshark function.\nInput the folder again by restarting the script.")
        os._exit(0)

def GUI():
    root = tk.Tk()
    root.title("Andromeda")
    #root.geometry("140x100")
    root.attributes('-topmost',1)
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    
    ttk.Button(frm, text=windowtext.clearterminaltext, command=windowfunctions.clearterminal).grid(column=0, row=0)
    ttk.Button(frm, text=windowtext.openwireshark, command=windowfunctions.runwireshark).grid(column=1, row=0)
    ttk.Button(frm, text=windowtext.wiresharktutorail, command=windowfunctions.wiresharktutorail).grid(column=1, row=1)
    ttk.Button(frm, text=windowtext.QUIT, command=root.destroy).grid(column=0, row=1)

    label = ttk.Label(frm, text = f"\n{windowtext.runningwindowtext}", foreground='green')
    label.grid(columnspan=2, row = 3)
    
    variables.runwire = True

    root.mainloop()
    
    print(f"{Fore.YELLOW}Bye!....{Fore.WHITE}")
    
    os._exit(0)

try:
    os.system(SYSTEM.systemclear())
    
    host = IP_FUNCTIONS.previousIP()
    interface = SYSTEM.getinterface()
    
    windowtext.runningwindowtext = "Sniffing on {} with IP: {}".format(interface,host)

    thread1 = Thread(target = IP_FUNCTIONS.displayips); thread1.start()
    thread2 = Thread(target = GUI); thread2.start()

    sniff(iface=interface, filter=f"host {host}", prn=IP_FUNCTIONS.getsniff)

except OSError:
    print(f"{Fore.WHITE}The interface {Fore.LIGHTGREEN_EX}({Fore.LIGHTRED_EX}{interface}{Fore.LIGHTGREEN_EX}){Fore.WHITE} is invalid. Please check again if the interface was spelled correctly, or even exists.")
    os._exit(0)
