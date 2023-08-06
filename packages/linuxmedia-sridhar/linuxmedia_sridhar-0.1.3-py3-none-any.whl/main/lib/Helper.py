import os
import sys
from main.lib.Argument import Argument
Argument=Argument(sys.argv)
class Helper:
    def Help(self,filename):
        print(f"Usage: {sys.argv[0]} [Options]...")
        print("Options  are :")
        print("verison                                              Show's the Version of the Tool")
        print("uname                                                Show's the Information about Our Machine")
        print("pwd                                                  Show's the Current Print Working Directory")
        print("--ip         ip_address                              Show's the Device Internet Protocal Address")
        print("--sv         sys_version                             Show's  the System version and System's Version Details")
        print("--dev        devices                                 Show's the Information About Devices")
        print("--n          numcpu                                  Show's the Number of CPU's Present in our Devices")
        print("--l          load                                    Show's the Load average of cureent Devices")
        print("--c          cpuinfo                                 Show's the Information about the CPU's")
        print("--g          getlogin                                Show's the name of the user logged in on the controlling terminal of the process ")
        print("--f          modules                                 Show's the Modules are Present in our System's")
        print("--m          meminfo                                 Show's the Information about Memory")
        print("--w          bus_details                             Show's the Details about bus_details")
        print("--v          disk_usage                              Show's the Disk Usage of the Current Directory")
        print("--x          disk_space                              Show's the Disk Space of the Current Directory")
        print("--d          today_date                              Show's the Current Date")
        print("--t          date_and_time                           Show's the Current Date and Time")
        print("--j          list_cpu                                Show's the list of CPU Present in our System")
        print("--k          list_hardware                           Show's the list of Hardware's Present in our System")
        print("--q          interface                               Show's the Information about interface")
        print("--z          logged_user                             Show's the Information About users who are currently logged into the system")
        print("--B          system_view                             Show's the System Information")
        print("             htop                                    Show's the Process That are Running in the System")
        print("--C          download_speed                          Show's the data is transferred from the Internet to your computer")
        print("--E          upload_speed                            Show's the Uplaod speed our Computer to the internet")
        print("--F          getuid                                  Show's the real User Information Details")
        print("--G          getpid                                  Show's the Current Process Information Details")
        print("--M          logged_user_on_controlling_Terminal     Show's Name of the User Logged in on the controlling Terminal")
        print("--Q          ip_address_client                       Show's the IP Address Client")
        print("--R          host_name                               Show's the Host name of The System's")
        print("             history                                 Show's the Hostory of the Command line Interface")
        print("--U          ip_Version                              Show's the Type of the Internet Protocal Version")
        print("             uptime                                  Show's the Details About,how long the system has been running")
        print("             vmstat                                  Show's the Detail's about reports various bits of system information")
        print("             type_of_commands                        Show's the Description About the Type of the Command Line tools and Types")
        print("             Desc                                    Show's the Details about the Histrory,about Linux,About The Linux Kernel and Author")             
        print("             bc                                      It Will open the Calculater")
        print("             ls                                      Show's information about the FILEs")
        print("             ll                                      Show's information about the FILEs and use a long listing format")
        print("             ping                                    check if your system is connected to router or internet then PING ")
        print("                                                                 (Packet INternet Groper) is the command for you")
        print("             mkdir                                   Create the Folder")
        print("             gzip                                    compress any file from")
        print("             free                                    check exactly what amount of storage is free and used in physical as well as swap memory in the system") 
        print("             top                                     monitor all the ongoing processes on the Linux system with the user name, ")
        print("                                                                 priority level, unique process id and shared memory by each task")
        print("             echo                                    Print the Given String or Value's")
        print("             head                                    list the first 10 lines of the file you through with head command")
        print("             w                                       view's the list of currently logged in users")
        print("             mv                                      move one file or directory to another file or directory")
        print("             ps                                      list of processes that are currently running for your session or for other users on the system")
        print("             whoami                                  which user is logged into system or who you are logged in as")
        # print("             tail")            
        print("             env                                     display all the environment variable in the Linux Terminal")
        print("             vi                                      It Will open the One of the Text Editor")
        print("             nano                                    It Will open the One of the Text Editor")  
        print("             rm                                      remove any file from the working directory") 
        print("             clear                                   Clear the Screen")
        print("             su                                      switch to another account right from the Linux Terminal window")
        print("             wget                                    Download any file from the internet and best part is download works")
        print("                                                                      in background so that you can continue working on your task")
        print("             zip                                     To compress one or more files")
        print("             unzip                                   To extract files from compressed zip file")
        print("             shutdown                                Shutfown the System or Currently running process")
        print("             dir                                     view the list of all directories and folders present in current working directory")
        print("             cd                                      Change Directory")
        print("             reboot                                  It Will Restart the Entire System")
        print("             sort                                    It is used to Sort the Files ") 
        print("             tac                                     Display the contents of the file in reverse orders")
        print("             exit                                    It's used to close the Terminal shell window directly from the command-line")
        print("             diff                                    compare the two directories and will display difference between them")
        print("             dmidecode                               retrieve hardware information but if you want information of a particular hardware component")
        print("             netstat                                 To monitor incoming and outgoing network connections continuously")
        print("             mpstat                                  display all the information about CPU utilization and performance")
        print("             wc                                      Show's the Count  of the files")
        print("             nproc                                   Show's the number of processing units allotted to the currently running process.")
        print("             sleep                                   It will delay or pause the execution of command for particular amount of time")
        print("             lsblk                                   Show's sysfs filesystem and displays the block device information")
        print("             Which_type                           Find the given Command to check whether Internal command or External Command or Included COmmands")                               
        print("-h           --help                                  help Option")



    def Availale_contents(self):
        if(Argument.hasCommands(['version'])):
            return True
        if(Argument.hasCommands(['uname'])):
            return True
        if(Argument.hasOption(['--help']) or Argument.hasOption(['-h'])):
            return True
        if(Argument.hasCommands(['pwd'])):
            return True
        if(Argument.hasOption(['--ip']) or Argument.hasCommands(['ip_address'])):
            return True
        if(Argument.hasOption(['--sv']) or Argument.hasCommands(['sys_version'])):
            return True
        if(Argument.hasOption(['--dev']) or Argument.hasCommands(['devices'])):
            return True
        if(Argument.hasOption(['--n']) or Argument.hasCommands(['numcpu'])):
            return True
        if(Argument.hasOption(['--l']) or Argument.hasCommands(['load'])):
            return True
        if(Argument.hasOption(['--c']) or Argument.hasCommands(['cpuinfo'])):
            return True
        if(Argument.hasOption(['--g']) or Argument.hasCommands(['getlogin'])):
            return True
        if(Argument.hasOption(['--f']) or Argument.hasCommands(['modules'])):
            return True
        if(Argument.hasOption(['--m']) or Argument.hasCommands(['meminfo'])):
            return True
        if(Argument.hasOption(['--w']) or Argument.hasCommands(['bus_details'])):
            return True
        if(Argument.hasOption(['--v']) or Argument.hasCommands(['disk_usage'])):
            return True
        if(Argument.hasOption(['--x']) or Argument.hasCommands(['disk_space'])):
            return True
        if(Argument.hasOption(['--d']) or Argument.hasCommands(['today_date'])):
            return True
        if(Argument.hasOption(['--t']) or Argument.hasCommands(['date_and_time'])):
            return True
        if(Argument.hasOption(['--j']) or Argument.hasCommands(['list_cpu'])):
            return True
        if(Argument.hasOption(['--q']) or Argument.hasCommands(['interface'])):
            return True
        if(Argument.hasOption(['--k']) or Argument.hasCommands(['list_hardware'])):
            return True
        if(Argument.hasOption(['--z']) or Argument.hasCommands(['logged_user'])):
            return True
        if(Argument.hasOption(['--B']) or Argument.hasCommands(['system_view'])):
            return True
        if(Argument.hasOption(['--C']) or Argument.hasCommands(['download_speed'])):
            return True
        if(Argument.hasOption(['--E']) or Argument.hasCommands(['upload_speed'])):
            return True
        if(Argument.hasOption(['--F']) or Argument.hasCommands(['getuid'])):
            return True
        if(Argument.hasOption(['--G']) or Argument.hasCommands(['getpid'])):
            return True
        if(Argument.hasOption(['--M']) or Argument.hasCommands(['logged_user_on_controlling_Terminal'])):
            return True
        if(Argument.hasOption(['--Q']) or Argument.hasCommands(['ip_address_client'])):
            return True
        if(Argument.hasOption(['--G']) or Argument.hasCommands(['getpid'])):
            return True
        if(Argument.hasOption(['--R']) or Argument.hasCommands(['host_name'])):
            return True
        if(Argument.hasOption(['--U']) or Argument.hasCommands(['ip_Version'])):
            return True
        if(Argument.hasCommands(['commands'])):
            return True
        if(Argument.hasCommands(['bc'])):
            return True
        if(Argument.hasCommands(['ls'])):
            return True
        if(Argument.hasCommands(['mv'])):
            return True
        if(Argument.hasCommands(['ps'])):
            return True
        if(Argument.hasCommands(['ll'])):
            return True
        if(Argument.hasCommands(['ping'])):
            return True  
        if(Argument.hasCommands(['ps'])):
            return True 
        if(Argument.hasCommands(['mkdir'])):
            return True
        if(Argument.hasCommands(['vmstat'])):
            return True
        if(Argument.hasCommands(['exit'])):
            return True
        if(Argument.hasCommands(['uptime'])):
            return True
        if(Argument.hasCommands(['htop'])):
            return True
        if(Argument.hasCommands(['history'])):
            return True
        if(Argument.hasCommands(['free'])):
            return True
        if(Argument.hasCommands(['top'])):
            return True
        if(Argument.hasCommands(['w'])):
            return True
        if(Argument.hasCommands(['whoami'])):
            return True
        if(Argument.hasCommands(['gzip'])):
            return True
        if(Argument.hasCommands(['Desc'])):
            return True
        if(Argument.hasCommands(['echo'])):
            return True
        if(Argument.hasCommands(['head'])):
            return True
        if(Argument.hasCommands(['env'])):
            return True
        if(Argument.hasCommands(['nano'])):
            return True
        if(Argument.hasCommands(['vi'])):
            return True
        if(Argument.hasCommands(['rm'])):
            return True
        if(Argument.hasCommands(['clear'])):
            return True
        if(Argument.hasCommands(['su'])):
            return True
        if(Argument.hasCommands(['wget'])):
            return True
        if(Argument.hasCommands(['type_of_commands'])):
            return True
        if(Argument.hasCommands(['zip'])):
            return True
        if(Argument.hasCommands(['unzip'])):
            return True
        if(Argument.hasCommands(['shutdown'])):
            return True
        if(Argument.hasCommands(['dir'])):
            return True
        if(Argument.hasCommands(['cd'])):
            return True
        if(Argument.hasCommands(['reboot'])):
            return True
        if(Argument.hasCommands(['sort'])):
            return True
        if(Argument.hasCommands(['tac'])):
            return True
        if(Argument.hasCommands(['diff'])):
            return True
        if(Argument.hasCommands(['dmidecode'])):
            return True
        if(Argument.hasCommands(['netstat'])):
            return True
        if(Argument.hasCommands(['mpstat'])):
            return True
        if(Argument.hasCommands(['wc'])):
            return True
        if(Argument.hasCommands(['nproc'])):
            return True
        if(Argument.hasCommands(['sleep'])):
            return True
        if(Argument.hasCommands(['lsblk'])):
            return True
        if(Argument.hasCommands(['Which_type'])):
            return True
        if(Argument.hasCommands(['tail'])):
            return True
        if(Argument.hasCommands(['commands'])):
            return True
    def print_help(self):
        print("Usage: "+sys.argv[0]+" <command> [Options..]")
        exit(-1)



        