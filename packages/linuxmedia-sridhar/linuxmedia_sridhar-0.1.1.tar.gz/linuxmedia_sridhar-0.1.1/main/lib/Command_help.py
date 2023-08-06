class Command_help:
    def tail(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("      Print the last 10 lines of each FILE to standard output.")
        print("Options are:   ")
        print("         tail                        Print the last 10 lines of each FILE to standard output.")
        print("-f                                   output appended data as the file grows")
        print("-h       --help                      display this help and exit")
        print("         show                        print the Description about that Command")

    def uname_help(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("Print certain system information.  With no OPTION, same as -s.")
        print("Options are:   ")
        print("-a,      --all                       print all information, in the following order,")
        print("-s,      kernel-name                 print the kernel name")
        print("-n,      nodename                    print the network node hostname")
        print("-r,      kernel-release              print the kernel release")
        print("-v,      kernel-version              print the kernel version")
        print("-m,      machine                     print the machine hardware name")
        print("-p,      processor                   print the processor type (non-portable)")
        print("-i,      hardware-platform           print the hardware platform (non-portable)")
        print("-o,      operating-system            print the operating system")
        print("-h       --help                      display this help and exit")
        print("         show                        print the Description about that Command")

    def pwd_help(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Print the name of the current working directory.")
        print("Options are:   ")
        print("-L                                    print the value of $PWD if it names the current working directory")
        print("-P                                    print the physical directory, without any symbolic links")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def Desc(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Decription....")
        print("Options are:   ")
        print("        Author                            Show's the details About Linux Author")
        print("        History_Linux                     Show's the History of Linux")
        print("        Awards_and_achievements           Show's the Awards_and_achievements of Linux untill today")
        print("        About_Linux                       Show's the deep details About Linux and It's Details")
        print("        Design                            Show's the Design and Implementation of Linux")
        print("        User_interface                    Show's the User_interface in Linux Operationg System and Linux Terminal's")
        print("        Naming                            Show's the What is the purpose of Linux is  Named in Linux")
        print("        Development                       Show's the Development of Linux and Construction of Linux")
        print("        Hardware_support                  Show's the Hardware_support of Linux and Hardware propertites")
        print("        Video_input_infrastructure        Show's the Video_input_infrastructure of Linux")
        print("        About_Linux_Kernal                Show's about Linux Kernal and It's Flavour's")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")
        
    def ip_address_help(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("Show's the INTERNET PROTOCAL ADDRESS")
        print("Options are:   ")
        print("--ip         ip_address      Show's the Internal Protocal Address")
        print("-h           --help          Display this help and exit")
        print("             show            Print the Description about that Command")
    
    def sys_version(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's  the System version and System's Version Details")
        print("Options are:   ")
        print("--sv         sys_version     View Linux System Information")
        print("-h           --help          Display this help and exit")
        print("             show            Print the Description about that Command")
    
    def devices_help(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Information About Devices")
        print("Options are:   ")
        print("--dev         devices     Show's the Devices THat are included in our System's")
        print("-h            --help      Display this help and exit")
        print("              show        Print the Description about that Command")
    
    def numcpu(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Number of CPU's Present in our Devices")
        print("Options are:   ")
        print("--n          numcpu      Show's the Number of CPU's are Present in our System")
        print("-h           --help      Display this help and exit")
        print("             show        Print the Description about that Command")
    
    def load(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Load average of cureent Devices")
        print("Options are:   ")
        print("--l          load        Show's the Current Load Average of the System")
        print("-h           --help      Display this help and exit")
        print("             show        Print the Description about that Command")

    def cpuinfo(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Information about the CPU's")
        print("Options are:   ")
        print("--c          cpuinfo     Show's the Information about the CPU")
        print("-h           --help      Display this help and exit")
        print("             show        Print the Description about that Command")
    
    def getlogin(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the name of the user logged in on the controlling terminal of the process")
        print("Options are:   ")
        print("--g          getlogin        Show's the name of the user logged in on the controlling terminal of the process")
        print("-h           --help          Display this help and exit")
        print("             show            Print the Description about that Command")

    def modules(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Modules are Present in our System's")
        print("Options are:   ")
        print("--f          modules     Show's the Modules are Present in our System")
        print("-h           --help      Display this help and exit")
        print("             show        Print the Description about that Command")

    def meminfo(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Information about Memory")
        print("Options are:   ")
        print("--m          meminfo     Show's the Information About the Memory Information")
        print("-h           --help      Display this help and exit")
        print("             show        Print the Description about that Command")
    
    def bus_details(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Details about bus_details")
        print("Options are:   ")
        print("--w          bus_details     Show's the Buses are Present in our System")
        print("-h           --help          Display this help and exit")
        print("             show            Print the Description about that Command")

    def disk_usage(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Disk Usage of the Current Directory")
        print("Options are:   ")
        print("--v          disk_usage      Show's the Details About the Disk Usage")
        print("-h           --help          Display this help and exit")
        print("             show            Print the Description about that Command")

    def disk_space(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Disk Space of the Current Directory")
        print("Options are:   ")
        print("--x          disk_space      Show's the Empty Space in the Disk")
        print("-h           --help          Display this help and exit")
        print("             show            Print the Description about that Command")

    def today_date(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Current Date")
        print("Options are:   ")
        print("--d          today_date      Show's the Current's Date")
        print("-h           --help          Display this help and exit")
        print("             show            Print the Description about that Command")

    def date_and_time(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Current Date and Time")
        print("Options are:   ")
        print("--t          date_and_time       Show's the Current Date and Time")
        print("-h           --help              Display this help and exit")
        print("             show                Print the Description about that Command")

    def list_cpu(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the list of CPU Present in our System")
        print("Options are:   ")
        print("--j          list_cpu        Show's the List of the CPU")
        print("-h           --help          Display this help and exit")
        print("             show            Print the Description about that Command")

    def list_hardware(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the list of Hardware's Present in our System")
        print("Options are:   ")
        print("--k         list_hardware        Show's the List of Hardware's ")
        print("-h           --help              Display this help and exit")
        print("             show                Print the Description about that Command")

    def interface(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Information about interface")
        print("Options are:   ")
        print("--q          interface       Show's The Information about of the List of Hardware present in our System")
        print("-h           --help          Display this help and exit")
        print("             show            Print the Description about that Command")

    def logged_user(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Information About users who are currently logged into the system")
        print("Options are:   ")
        print("--z         logged_user       Information about users who are ")
        print("                                     currently logged into the system, we use the who command in the Linux system. The who command ")
        print("                                     is used to display the users logged into the system")
        print("-h           --help            Display this help and exit")
        print("             show              Print the Description about that Command")
    
    def system_view(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the System Information")
        print("Options are:   ")
        print("--B          system_view     It's Show's the System Information")
        print("-h           --help          Display this help and exit")
        print("             show            Print the Description about that Command")

    def htop(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Process That are Running in the System")
        print("Options are:   ")
        print("         htop        Show's the details about Linux environment to determine the cause of load by each process")
        print("-h       --help      Display this help and exit")
        print("         show        Print the Description about that Command")
    
    def download_speed(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the data is transferred from the Internet to your computer")
        print("Options are:   ")
        print("--C          download_speed      Show's the rate that digital data is transferred from the Internet to your computer")
        print("-h           --help              Display this help and exit")
        print("             show                Print the Description about that Command")

    def upload_speed(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Uplaod speed our Computer to the internet")
        print("Options are:   ")
        print("--E          upload_speed        Show's the rate that online data is transferred from your computer to the Internet")
        print("-h           --help               Display this help and exit")
        print("             show                 Print the Description about that Command")

    def getuid(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the real User Information Details")
        print("Options are:   ")
        print("--F          getuid      Show's the current process’s real user id")
        print("-h           --help      Display this help and exit")
        print("             show        Print the Description about that Command")

    def getpid(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Current Process Information Details")
        print("Options are:   ")
        print("--G          getpid      Show's the process ID of the current process")
        print("-h           --help      Display this help and exit")
        print("             show        Print the Description about that Command")

    def logged_user_on_controlling_Terminal(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's Name of the User Logged in on the controlling Terminal")
        print("Options are:   ")
        print("--M          logged_user_on_controlling_Terminal         Show's the name of the user logged in on the controlling terminal of the process")
        print("-h           --help                                      Display this help and exit")
        print("             show                                        Print the Description about that Command")

    def ip_address_client(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the IP Address Client")
        print("Options are:   ")
        print("--Q          ip_address_client       Show's the IP Address client")
        print("-h           --help                  Display this help and exit")
        print("             show                    Print the Description about that Command")

    def host_name(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Host name of The System's")
        print("Options are:   ")
        print("--R          host_name       Show's the name that is provided to a device to identify it in a local network")
        print("-h           --help          Display this help and exit")
        print("             show            Print the Description about that Command")

    def history(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Hostory of the Command line Interface")
        print("Options are:   ")
        print("         history         Show's the history of our Terminal's previously Entered Command ")
        print("-h       --help          Display this help and exit")
        print("         show            Print the Description about that Command")

    def ip_Version(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Type of the Internet Protocal Version")
        print("Options are:   ")
        print("--U          ip_Version      Show's the Internet Protocal Version")
        print("-h           --help          Display this help and exit")
        print("             show            Print the Description about that Command")

    def uptime(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Details About,how long the system has been running")
        print("Options are:   ")
        print("         uptime          The current time, how long the system has been running, how many users are currently logged on, and the system load averages for the past 1, 5, and 15 minutes")
        print("-h       --help          Display this help and exit")
        print("         show            Print the Description about that Command")

    def vmstat(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Detail's about reports various bits of system information")
        print("Options are:   ")
        print("             vmstat           Show's the virtual Memory usage")
        print("-h           --help           Display this help and exit")
        print("             show             Print the Description about that Command")

    def type_of_commands(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Description About the Type of the Command Line tools and Types")
        print("Options are:   ")
        print("-in_c              --In_c_details                Show's the Description About the Internal_Command")
        print("-inc_c             --EX_c_details                Show's the Description About the External_Command")
        print("-ex_c              --Incl_c_details              Show's the Descriptoin About the Included_COmmand")
        print("-h                 --help                        Display this help and exit")
        print("                   show                          Print the Description about that Command")

    def bc(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Simple Calculater")
        print("Options are:   ")
        print("             bc              It Will open the Calculater")
        print("-h           --help          Display this help and exit")
        print("             show            Print the Description about that Command")

    def ls(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("          List the Files And Directory's")
        print("Options are: ")
        print("         ls                Show's information about the FILEs")
        print("-h       --help            Display this help and exit")
        print("         show              Print the Description about that Command")
    
    def ll(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's information about the FILEs and use a long listing format")
        print("Options are:   ")
        print("         ll               Show's information about the FILEs and use a long listing format")
        print("-h       --help           Display this help and exit")
        print("         show             Print the Description about that Command")

    def ping(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         check if your system is connected to router")
        print("Options are:   ")
        print("         ping              If you want to check if your system is connected to router or internet then PING (Packet INternet Groper) is the command for you")
        print("-h       --help            Display this help and exit")
        print("         show              Print the Description about that Command")

    def mkdir(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Create the Empty Directory's")
        print("Options are:   ")
        print("         mkdir                 Create the DIrectory in Any Places")
        print("-h       --help                Display this help and exit")
        print("         show                  Print the Description about that Command")

    def gzip(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         compress any file from")
        print("Options are:   ")
        print("         gzip             compress any file from")
        print("-h       --help           Display this help and exit")
        print("         show             Print the Description about that Command")

    def free(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         check exactly what amount of storage is free and used in physical as well as swap memory in the system")
        print("Options are:   ")
        print("         free             check exactly what amount of storage is free and used in physical as well as swap memory in the system")
        print("-h       --help            Display this help and exit")
        print("         show              Print the Description about that Command")

    def top(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         monitor all the ongoing processes on the Linux system with the user name,")
        print("                     priority level, unique process id and shared memory by each task")
        print("Options are:   ")
        print("         top               monitor all the ongoing processes on the Linux system with the user name, priority level, unique process id and shared memory by each task")
        print("-h       --help            Display this help and exit")
        print("         show              Print the Description about that Command")

    def echo(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("Print the Given String or Print The Given Value ")
        print("Options are:   ")
        print("         echo         Print the Given String or Given Value")
        print("-h       --help       Display this help and exit")
        print("         show         Print the Description about that Command")

    def head(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         list the first 10 lines of the file you through with head command")
        print("Options are:   ")
        print("         head                list the first 10 lines of the file you through with head command")
        print("-h       --help              Display this help and exit")
        print("         show                Print the Description about that Command")

    def w(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         view's the list of currently logged in users")
        print("Options are:   ")
        print("         w                  view's the list of currently logged in users")
        print("-h       --help             Display this help and exit")
        print("         show               Print the Description about that Command")

    def whoami(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         which user is logged into system or who you are logged in as")
        print("Options are:   ")
        print("         whoami                      which user is logged into system or who you are logged in as")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def mv(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Move the File or Directory  one place to Another place")
        print("Options are:   ")
        print("         mv                         Move one file or directory to another file or directory")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def ps(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         list of processes that are currently running for your session or for other users on the system")
        print("Options are:   ")
        print("         ps                          list of processes that are currently running for your session or for other users on the system")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def vi(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         One of the Text Editor in Linux ")
        print("Options are:   ")
        print("         vi                          Open the One of the Text Editor in Linux")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")
    
    def nano(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         One of the Text Editor in Linux")
        print("Options are:   ")
        print("         nano                        Open the One of the Text Editor in Linux")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def env(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         display all the environment variable in the Linux Terminal")
        print("Options are:   ")
        print("         env                         Show's the Enviroment Variable Present in our System")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def rm(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Remove the File's or Directory's")
        print("Options are:   ")
        print("         rm                          Remove the File's or Directory's in the Working Directory")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def clear(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Clear the Screen ot Terminal")
        print("Options are:   ")
        print("         clear                       It will Clear the Screen")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def su(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         switch to another account right from the Linux Terminal window")
        print("Options are:   ")
        print("         su                          Switch to another account right from the Linux Terminal window")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def wget(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Download any FIle's from the Internet")
        print("Options are:   ")
        print("         wget                        Download any file from the internet and best part is")
        print("                                                     download works in background so that you can continue working on your task")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def zip(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         To compress one or more files")
        print("Options are:   ")
        print("         zip                         To Compress One or More File's")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def unzip(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         To extract files from compressed zip file")
        print("Options are:   ")
        print("         unzip                       To extract files from compressed zip file")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def shutdown(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Shutdown the System..")
        print("Options are:   ")
        print("         shutdown                   Shutdown the System or lTurn off the System")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")
        
    def shutdown_c(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         To cancel the Executed Shutdown Command")
        print("Options are:   ")
        print("         shutdown_c                  Cancel teh Shutdown Process")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def dir(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         List the Directoy")
        print("Options are:   ")
        print("         dir                         view the list of all directories and folders present in current working directory")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def cd(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Change Directory")
        print("Options are:   ")
        print("         cd                         Change the Directory in the any path")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")
        
    def reboot(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Restart the System")
        print("Options are:   ")
        print("             reboot                Restart the System")
        print("-p                                 Switch off the machine")
        print("-f                                 Force immediate halt/power-off/reboot")
        print("-w                                 Don't halt/power-off/reboot, just write wtmp record")
        print("-d                                 Don't write wtmp record")
        print("-h           --help                Display this help and exit")
        print("             show                  Print the Description about that Command")

    def sort(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         It is used to Sort the Files")
        print("Options are:   ")
        print("         sort                    sort file or arrange any record in particular order generally according to their ASCII values")
        print("-b                               ignore leading blanks")
        print("-d                               consider only blanks and alphanumeric characters")
        print("-f                               fold lower case to upper case characters")
        print("-g                               compare according to general numerical value")
        print("-i                               consider only printable characters")
        print("-m                               compare (unknown) < 'JAN' < ... < 'DEC'")
        print("-h                               compare human readable numbers (e.g., 2K 1G)")
        print("-n                               compare according to string numerical value")
        print("-h       --help                  Display this help and exit")
        print("         show                    Print the Description about that Command")

    def tac(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Display the contents of the file in reverse orders")
        print("Options are:   ")
        print("         tac                 Display the contents of the file in reverse orders")
        print("-h       --help              Display this help and exit")
        print("         show                Print the Description about that Command")

    def exit(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Exit the Terminal or Exit the Current Loggin Account")
        print("Options are:   ")
        print("         exit                        Exit the current state or to exit the Terminal")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def diff(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Difference the Two File's in Line by Line")
        print("Options are:   ")
        print("         diff            compare the two directories and will display difference between them")
        print("-F                       show the most recent line matching RE")
        print("-h       --help          Display this help and exit")
        print("         show            Print the Description about that Command")

    def dmidecode(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         retrieve hardware information but if you want information of a particular hardware component")
        print("Options are:   ")
        print("             dmidecode                  Retrieve hardware information but if you want information of a particular hardware component")
        print("-d           dev-mem FILE               Read memory from device FILE (default: /dev/mem)")
        print("-q           quiet                      Less verbose output")
        print("-s           string KEYWORD             Only display the value of the given DMI string")
        print("-t           type TYPE                  Only display the entries of given type")
        print("-H           handle HANDLE              Only display the entry of given handle")
        print("-u           dump                       Do not decode the entries")
        print("             dump-bin FILE              Dump the DMI data to a binary file")
        print("             from-dump FILE             Read the DMI data from a binary file")
        print("             no-sysfs                   Do not attempt to read DMI data from sysfs files")
        print("-h           --help                     Display this help and exit")
        print("             show                       Print the Description about that Command")

    def netstat(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         To monitor incoming and outgoing network connections continuously")
        print("Options are:   ")
        print("         netstat                     To monitor incoming and outgoing network connections continuously")
        print("-h       --help                      Display this help and exit")
        print("         show                        Print the Description about that Command")

    def mpstat(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         display all the information about CPU utilization and performance")
        print("Options are:   ")
        print("         mpstat           Display all the information about CPU utilization and performance")
        print("-h       --help           Display this help and exit")
        print("         show             Print the Description about that Command")
    
    def wc(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the Count of  the files")
        print("Options are:   ")
        print("         wc              Show's the Count of th e File's")
        print("-h       --help          Display this help and exit")
        print("         show            Print the Description about that Command")

    def nproc(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's the number of processing units allotted to the currently running process")
        print("Options are:   ")
        print("         nproc            Show's the number of processing units allotted to the currently running process")
        print("-h       --help           Display this help and exit")
        print("         show             Print the Description about that Command")

    def sleep(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         It will delay or pause the execution of command for particular amount of time")
        print("Options are:   ")
        print("         sleep            It will delay or pause the execution of command for particular amount of time")
        print("-h       --help           Display this help and exit")
        print("         show             Print the Description about that Command")

    def lsblk(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         Show's sysfs filesystem and displays the block device information")
        print("Options are:   ")
        print("         lsblk                Show's sysfs filesystem and displays the block device information")
        print("-h       --help               Display this help and exit")
        print("         show                 Print the Description about that Command")

    # def hdparm(self,filename):
        # print("Usage: "+filename+" [OPTION] ")
        # print("hdparm           ")
    def Which_type(self,filename):
        print("Usage: "+filename+" [OPTION] ")
        print("         To find the Given Command is Internal Command or External Command or Included Command")
        print("Options are:   ")
        print("         <-->[Argument(cd,ls,cat...)]           To check the Given the Argument is Internal Command's or ")
        print("                                                               External Command's or Included Command's")
        print("-h       --help                                  Display this help and exit")
        print("         show                                    Print the Description about that Command")
        
    
    
    
    
    