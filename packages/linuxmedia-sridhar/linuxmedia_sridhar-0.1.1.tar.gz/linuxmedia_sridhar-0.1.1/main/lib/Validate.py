import os
import sys
import platform
import json
from optparse import OptionParser
import psutil
import shutil
from datetime import datetime,date
import readline
from pyspeedtest import * 
import speedtest 
import socket
import ipaddress
import time
from urllib.request import urlopen
import uuid
from main.lib.Description import Description
Description=Description()
from main.lib.Argument import Argument
from main.lib.Command_help import Command_help
from main.lib.Description import Description
Description=Description()
from main.lib.Where_locate import Where_locate
from main.lib.Show_details import Show_details
from main.lib.Helper import Helper
Where_locate=Where_locate()
Helper=Helper()
Argument=Argument(sys.argv)
Show_details=Show_details()
Command_help=Command_help()
url='http://ipinfo.io/json'
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
class Validate:
    def __init__(self,args):
        self.args=args

    def uname(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['uname'])):
                if(Argument.hasOption(['--all']) or (Argument.hasOption(['-a']))):
                    return os.system("uname -a")
                if(Argument.hasOption(['-s']) or Argument.hasCommands(['kernel-name'])):
                    return os.system("uname -s")
                if(Argument.hasOption(['-n']) or Argument.hasCommands(['nodename'])):
                    return os.system("uname -n")
                if(Argument.hasOption(['-r']) or Argument.hasCommands(['kernel-release'])):
                    return os.system("uname -r")
                if(Argument.hasOption(['-v']) or Argument.hasCommands(['kernel-version'])):
                    return os.system("uname -v")
                if(Argument.hasOption(['-m']) or Argument.hasCommands(['machine'])):
                    return os.system("uname -m")
                if(Argument.hasOption(['-p']) or Argument.hasCommands(['processor'])):
                    return os.system("uname -p")
                if(Argument.hasOption(['-i']) or Argument.hasCommands(['hardware-platform'])):
                    return os.system("uname -i")
                if(Argument.hasOption(['-o']) or Argument.hasCommands(['operating-system'])):
                    return os.system("uname -o")
                elif(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.uname_help(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.uname()
                
        else:
            return Command_help.uname_help(sys.argv[1])
            
    def pwd(self):
            if(Argument.hasCommands(['pwd'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.pwd_help(sys.argv[1])
                if(Argument.hasOption(['-L'])):
                    return os.system("pwd -L")
                if(Argument.hasOption(['-P'])):
                    return os.system("pwd -P")
                if(Argument.hasCommands(["show"])):
                    return Show_details.pwd()
                print(os.getcwd())
    def ip_address(self):
        if(Argument.hasOption(['--ip']) or Argument.hasCommands(['ip_address'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.ip_address_help(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.show_ip_address()
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            print(ipaddress.ip_address(ip_address))
            # ipaddress.ip_address(ip_address) --> Show's the Internet Protocal Version with Ip Address
            # ipaddress.ip_address('192.0.2.1')
            # Output :: IPv4Address('192.0.2.1')
    def sys_version(self):
        if(Argument.hasOption(['--sv']) or Argument.hasCommands(['sys_version'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.sys_version(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.sys_version()
            return os.system("cat /proc/version")
    def devices(self):
        if(Argument.hasOption(['--dev']) or Argument.hasCommands(['devices'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.devices_help(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.devices()
            return os.system("cat /proc/devices")
    def commands(self):
        if(Argument.hasCommands(['commands'])):
            if(Argument.hasOption(['-in_c']) or Argument.hasOption(['--In_c_details'])):
                return Description.Desc_Internal_Command()
            if(Argument.hasOption(['-inc_c']) or Argument.hasOption(['--Incl_c_details'])):
                return Description.Desc_Included_Command()
            if(Argument.hasOption(['-ex_c']) or Argument.hasOption(['--EX_c_details'])):
                return Description.Desc_External_Command()
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.type_of_commands(sys.argv[1])
    def numcpu(self):
        if(Argument.hasOption(['--n']) or Argument.hasCommands(['numcpu'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.numcpu(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.numcpu()
        print("Number of CPU : ",psutil.cpu_count())
    def load(self):
        if(Argument.hasOption(['--l']) or Argument.hasCommands(['load'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.load(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.load()
            print("Load Average: ", psutil.getloadavg())
    def cpuinfo(self):
        if(Argument.hasOption(['--c']) or Argument.hasCommands(['cpuinfo'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.cpuinfo(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.cpuinfo()
            return os.system("cat /proc/cpuinfo")
    def getlogin(self):
        if(Argument.hasOption(['--g']) or Argument.hasCommands(['getlogin'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.getlogin(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.getlogin()
            return print(os.getlogin())
    def modules(self):
        if(Argument.hasOption(['--f']) or Argument.hasCommands(['modules'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.modules(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.modules()
            return print(os.system("cat /proc/modules"))
    def meminfo(self):
        if(Argument.hasOption(['--m']) or Argument.hasCommands(['meminfo'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.meminfo(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.meminfo()
            return print(os.system("cat /proc/modules"))
    def bus_details(self):
        if(Argument.hasOption(['--w']) or Argument.hasCommands(['bus_details'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.bus_details(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.bus_details()
            return print(os.system("cat /proc/bus"))
    def disk_usage(self):
        if(Argument.hasOption(['--v']) or Argument.hasCommands(['disk_usage'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.disk_usage(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.disk_usage()
            return print(shutil.disk_usage(os.getcwd()))
    def disk_space(self):
        if(Argument.hasOption(['--x']) or Argument.hasCommands(['disk_space'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.disk_space(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.disk_space()
            return os.system("df")
    def today_date(self):
        if(Argument.hasOption(['--d']) or Argument.hasCommands(['today_date'])):
            today = date.today()
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.today_date(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.today_date()
            return print("Today's Date:",date.today())

    def date_and_time(self):
        if(Argument.hasOption(['--t']) or Argument.hasCommands(['date_and_time'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.date_and_time(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.date_and_time()
            today = datetime.now()
            return print("Current date and time is", today)
             
    def list_cpu(self):
        if(Argument.hasOption(['--j']) or Argument.hasCommands(['list_cpu'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.list_cpu(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.list_cpu()
            return print(os.system("lscpu"))
    def list_hardware(self):
        if(Argument.hasOption(['--k']) or Argument.hasCommands(['list_hardware'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.list_hardware(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.list_hardware()
            return (os.system("cat /sys/devices/system/cpu"))
    def interface(self):
        if(Argument.hasOption(['--q']) or Argument.hasCommands(['interface'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.interface(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.interface()
            return os.system("ifconfig -a")
    def logged_user(self):
        if(Argument.hasOption(['--z']) or Argument.hasCommands(['logged_user'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.logged_user(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.logged_user()
            return os.system("last")
    def system_view(self):
        if(Argument.hasOption(['--B']) or Argument.hasCommands(['system_view'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.system_view(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.system_view()
            return os.system("last")
    def htop(self):
        if(Argument.hasCommands(['htop'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.htop(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.htop()
            return os.system("htop")
    def download_speed(self):
        if(Argument.hasOption(['--C']) or Argument.hasCommands(['download_speed'])):
            st = speedtest.Speedtest()
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.download_speed(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.download_speed()
            return print(f"Download speed :: {st.download()}")
    def upload_speed(self):
        if(Argument.hasOption(['--E']) or Argument.hasCommands(['upload_speed'])):
            st = speedtest.Speedtest()
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.upload_speed(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.upload_speed()
            return print(f"Upload Speed :: {st.upload()}")
    def getuid(self):
        if(Argument.hasOption(['--F']) or Argument.hasCommands(['getuid'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.getuid(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.getuid()
            return print("real user ID :: ",os.getuid())
    def getpid(self):
        if(Argument.hasOption(['--G']) or Argument.hasCommands(['getpid'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.getpid(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.getpid()
            return print("current process id :: ",os.getpid())
    def logged_user_on_controlling_Terminal(self):
        if(Argument.hasOption(['--M']) or Argument.hasCommands(['logged_user_on_controlling_Terminal'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.logged_user_on_controlling_Terminal(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.logged_user_on_controlling_Terminal()
            return print("Name of the User Logged in on the controlling Terminal :: ",os.getlogin())
    def ip_address_client(self):
        if(Argument.hasOption(['--Q']) or Argument.hasCommands(['ip_address_client'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.ip_address_client(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.ip_address_client()
            return print(f"IP Address: {ip_address}")
    def host_name(self):
        if(Argument.hasOption(['--R']) or Argument.hasCommands(['host_name'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.host_name(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.host_name()
            return print(f"Hostname: {hostname}")
    def history(self):
        if(Argument.hasCommands(['history'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.history(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.history()
            return os.system("cat /home/sridhard.21cse/.bash_history")
    def ip_Version(self):
        if(Argument.hasOption(['--U']) or Argument.hasCommands(['ip_Version'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.ip_Version(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.ip_Version()
            print("IP Address Version ::")
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            str(ip_address)
            version=(ipaddress.ip_address(ip_address))  
            # ipaddress.ip_address(ip_address) --> Show's the Internet Protocal Version with Ip Address
            # ipaddress.ip_address('192.0.2.1')
            # Output :: IPv4Address('192.0.2.1')
            return print(version)
    def uptime(self):
        if(Argument.hasCommands(['uptime'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.uptime(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.uptime()
            print("shows system memory, processes, interrupts, paging, block I/O, and CPU info :")
            return print(os.system("vmstat"))
    def vmstat(self):
        if(Argument.hasCommands(['vmstat'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.vmstat(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.vmstat()
            return print(os.system("vmstat"))
    def type_of_commands(self):
        if(Argument.hasCommands(['type_of_commands'])):
            if(Argument.hasCommands(['Internal_Command'])):
                Description.Desc_Internal_Command()
            if(Argument.hasCommands(['External_Command'])):
                Description.Desc_External_Command()
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.type_of_commands(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.type_of_commands()
            return Command_help.type_of_commands(sys.argv[1])

            
    def Desc(self):
        if(Argument.hasCommands(['Desc'])):
            if(Argument.hasCommands(["Author"])):
                return Description.Author()
            if(Argument.hasCommands(["History_Linux"])):
                return Description.History_Linux()
            if(Argument.hasCommands(["Awards_and_achievements"])):
                return Description.Awards_and_achievements()
            if(Argument.hasCommands(["About_Linux"])):
                return Description.About_Linux()
            if(Argument.hasCommands(["Design"])):
                return Description.Design()
            if(Argument.hasCommands(["User_interface"])):
                return Description.User_interface()
            if(Argument.hasCommands(["Naming"])):
                return Description.Naming()
            if(Argument.hasCommands(["Development"])):
                return Description.Development()
            if(Argument.hasCommands(["Hardware_support"])):
                return Description.Hardware_support()
            if(Argument.hasCommands(["Video_input_infrastructure"])):
                return Description.Video_input_infrastructure()
            if(Argument.hasCommands(["About_Linux_Kernal"])):
                return Description.About_Linux_Kernal()
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.Desc(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.Desc()
    def bc(self):
        if(Argument.hasCommands(['bc'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.bc(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.bc()
            return os.system("bc")
    def ls(self):
        if(Argument.hasCommands(['ls'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.ls(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.ls()
            return os.system("ls")
    def ll(self):
        if(Argument.hasCommands(['ll'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.ll(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.ll()
            return os.system("ls -l")
    def ping(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['ping'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.ping(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.ping()
                return os.system(f"ping {sys.argv[2]}")
        else:
            return Command_help.ping(sys.argv[1])
    def mkdir(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['mkdir'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.mkdir(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.mkdir()
                return os.system(f"mkdir {sys.argv[2]}")
        else:
            return Command_help.mkdir(sys.argv[1])
    def gzip(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['gzip'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.gzip(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.gzip()
                return os.system(f"gzip {sys.argv[2]}")
        else:
            return Command_help.gzip(sys.argv[1])
    def free(self):
        if(Argument.hasCommands(['free'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.free(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.free()
            return os.system("free")
    def top(self):
        if(Argument.hasCommands(['top'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.top(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.top()
            return os.system("top")
    def echo(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['echo'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.echo(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.echo()
                return os.system(f"echo {sys.argv[2]}")
        else:
            return Command_help.echo(sys.argv[1])
            
    def head(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['head'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.head(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.head()
                return os.system(f"head {sys.argv[2]}")
        else:
            return Command_help.head(sys.argv[1])

    def mv(self):
        if(len(sys.argv)>3):
            if(Argument.hasCommands(['mv'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.mv(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.mv()
                return os.system(f"mv {sys.argv[2]} {sys.argv[3]}")
        else:
            return Command_help.head(sys.argv[1])

    def w(self):
        if(Argument.hasCommands(['w'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.w(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.w()
            return os.system("w") 

    def ps(self):
        if(Argument.hasCommands(['ps'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.ps(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.ps()
            return os.system("ps -u") 

    def whoami(self):
        if(Argument.hasCommands(['whoami'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.whoami(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.whoami()
            return os.system("whoami")  

    def tail(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['tail'])):
                if(Argument.hasOption(['-f'])):
                    return os.system(f"tail -f {sys.argv[3]}")
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.tail(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.tail()
                return os.system(f"tail -f {sys.argv[2]}") 
            else:
                return Command_help.tail(sys.argv[1])
    def env(self):
        if(Argument.hasCommands(['env'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.env(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.env()
            return os.system("env") 
            

    def vi(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['vi'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.vi(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.vi()
                return os.system(f"vi {sys.argv[2]}")
        else:
            return Command_help.vi(sys.argv[1])

    def nano(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['nano'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.nano(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.nano()
                return os.system(f"nano {sys.argv[2]}")
        else:
            return Command_help.nano(sys.argv[1])

    def rm(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['rm'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.rm(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.rm()
                return os.system(f"rm {sys.argv[2]}")
        else:
            return Command_help.rm(sys.argv[1])

    def clear(self):
        if(Argument.hasCommands(['clear'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.clear(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.clear()
            return os.system("clear")

    def su(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['su'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.su(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.su()
                return os.system(f"su {sys.argv[2]}")
        else:
            return Command_help.su(sys.argv[1])

    def wget(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['wget'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.wget(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.wget()
                return os.system(f"wget {sys.argv[2]}")
        else:
            return Command_help.wget(sys.argv[1])

    def zip(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['zip'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.zip(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.zip()
                return os.system(f"zip {sys.argv[2]}")
        else:
            return Command_help.zip(sys.argv[1])

    def unzip(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['unzip'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.unzip(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.unzip()
                return os.system(f"unzip {sys.argv[2]}")
        else:
            return Command_help.unzip(sys.argv[1])

    def shutdown(self):
        if(Argument.hasCommands(['shutdown'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.shutdown(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.shutdown()
            return os.system("shutdown")
            if(Argument.hasOption(['-c'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.shutdown_c(sys.argv[1])
                return os.system("shutdown -c")

    def dir(self):
        if(Argument.hasCommands(['dir'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.dir(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.dir()
            return os.system("dir")

    def cd(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['cd'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.cd(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.cd()
                return os.system(f"cd {sys.argv[2]}")
        else:
            return Command_help.cd(sys.argv[1])

    def reboot(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['reboot'])):
                if(Argument.hasOption(["-p"])):
                    return os.system("reboot -p")
                if(Argument.hasOption(["-f"])):
                    return os.system("reboot -f")
                if(Argument.hasOption(["-w"])):
                    return os.system("reboot -w")
                if(Argument.hasOption(["-d"])):
                    return os.system("reboot -d")
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.reboot(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.reboot()
        else:
            return Command_help.reboot(sys.argv[1])
            
    def sort(self):
        if((len(sys.argv)>3) or (len(sys.argv)>4)):
            if(Argument.hasCommands(['sort'])):
                if(Argument.hasOption(["-b"])):
                    return os.system("sort -b")
                if(Argument.hasOption(["-d"])):
                    return os.system("sort -d")
                if(Argument.hasOption(["-f"])):
                    return os.system("sort -f")
                if(Argument.hasOption(["-g"])):
                    return os.system("sort -g")
                if(Argument.hasOption(["-i"])):
                    return os.system("sort -i")
                if(Argument.hasOption(["-m"])):
                    return os.system("sort -m")
                if(Argument.hasOption(["-h"])):
                    return os.system("sort -h")
                if(Argument.hasOption(["-n"])):
                    return os.system("sort -n")
        elif(len(sys.argv)>1):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.sort(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.sort()
        else:
            return Command_help.sort(sys.argv[1])

    def tac(self):
        if(Argument.hasCommands(['tac'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.tac(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.tac()
            return os.system("tac")
    def exit(self):
        if(Argument.hasCommands(['exit'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.exit(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.exit()
            return exit()

    def diff(self):
        if((len(sys.argv)>3) or (len(sys.argv)>4)):
            if(Argument.hasCommands(['diff'])):
                if(Argument.hasOption(["-f"])):
                    return os.system(f"diff -F {sys.argv[2]} {sys.argv[3]}")
                return os.system(f"diff {sys.argv[2]} {sys.argv[3]}")
        elif(len(sys.argv)>2):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.diff(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.diff()
        else:
            return Command_help.diff(sys.argv[1])

    def dmidecode(self):
        if(len(sys.argv)>3):
            if(Argument.hasCommands(['dmidecode'])):
                if(Argument.hasOption(['-d']) or Argument.hasCommands(['dev-mem'])):
                    return os.system(f"dmidecode -d {sys.argv[3]}")
                if(Argument.hasOption(['-q']) or Argument.hasCommands(['quiet'])):
                    return os.system("dmidecode -q")
                if(Argument.hasOption(['-s']) or Argument.hasCommands(['string'])):
                    return os.system(f"dmidecode -s {sys.argv[3]}")
                if(Argument.hasOption(['-t']) or Argument.hasCommands(['type'])):
                    return os.system(f"dmidecode -t {sys.argv[3]}")
                if(Argument.hasOption(['-H']) or Argument.hasCommands(['handle'])):
                    return os.system(f"dmidecode -H {sys.argv[3]}")
                if(Argument.hasOption(['-u']) or Argument.hasCommands(['dump'])):
                    return os.system(f"dmidecode -u {sys.argv[3]}")
                if(Argument.hasCommands(['dump-bin'])):
                    return os.system(f"dmidecode --dump-bin {sys.argv[3]}")
                if(Argument.hasCommands(['from-dump'])):
                    return os.system(f"dmidecode --from-dump {sys.argv[3]}")
                if(Argument.hasCommands(['no-sysfs'])):
                    return os.system(f"dmidecode --no-sysfs {sys.argv[3]}")
                elif(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.dmidecode(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.dmidecode()
                
        else:
            return Command_help.dmidecode(sys.argv[1])

    def netstat(self):
        if(Argument.hasCommands(['netstat'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.netstat(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.netstat()
            return os.system("netstat")
    def mpstat(self):
        if(Argument.hasCommands(['mpstat'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.mpstat(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.mpstat()
            return os.system("mpstat")
    def wc(self):
        if(Argument.hasCommands(['wc'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.wc(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.wc()
            print("The count of files :: ")
            return os.system("ls | wc -l")
    def nproc(self):
        if(Argument.hasCommands(['nproc'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.nproc(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.nproc()
            return os.system("nproc")
    def sleep(self):
        if(Argument.hasCommands(['sleep'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.sleep(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.sleep()
            
            return time.sleep(int(sys.argv[2]))
    def lsblk(self):
        if(Argument.hasCommands(['lsblk'])):
            if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                return Command_help.lsblk(sys.argv[1])
            if(Argument.hasCommands(["show"])):
                return Show_details.lsblk()
            
            return os.system('lsblk')
    def Which_type(self):
        if(len(sys.argv)>2):
            if(Argument.hasCommands(['Which_type'])):
                if(Argument.hasOption(['-h']) or Argument.hasOption(['--help'])):
                    return Command_help.Which_type(sys.argv[1])
                if(Argument.hasCommands(["show"])):
                    return Show_details.Which_type()
            return Where_locate.find_location()
        else:
            return Command_help.Which_type(sys.argv[1])
    
            


    
                
                         
    
            

               
                