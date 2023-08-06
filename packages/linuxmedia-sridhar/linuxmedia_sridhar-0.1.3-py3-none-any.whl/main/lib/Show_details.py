class Show_details:
    def tail(self):
        print("Print the last 10 lines of each FILE to standard output.With more than one FILE, precede each with a header giving the file name.")
    def uname(self):
        print("The uname command writes to standard output the name of the operating system that you are using.")
        print("The machine ID number contains 12 characters in the following digit format: xxyyyyyymmss. The xx positions indicate the system and is always 00. The yyyyyy positions contain the unique ID number for the entire system. The mm position represents the model ID. The ss position is the submodel number and is always 00. The model ID describes the ID of the CPU Planar, not the model of the System as a whole.")
        print("Most machines share a common model ID of 4C.")
        print("The machine identifier value returned by the uname command may change when new operating system software levels are installed. This change affects applications using this value to access licensed programs. To view this identifier, enter the uname -m command.")
    def pwd(self):
        print("The pwd command writes to standard output the full path name of your current directory (from the root directory). All directories are separated by a / (slash). The root directory is represented by the first /, and the last directory named is your current directory.")
    def show_ip_address(self):
        print("An IP address is a unique address that identifies a device on the internet or a local network. IP stands for Internet Protocol which is the set of rules governing the format of data sent via the internet or local network.")
        print("In essence, IP addresses are the identifier that allows information to be sent between devices on a network: they contain location information and make devices accessible for communication. The internet needs a way to differentiate between different computers, routers, and websites. IP addresses provide a way of doing so and form an essential part of how the internet works.")
    def sys_version(self):
        print("View Linux System Information. To know only the system name, you can use the uname command without any switch that will print system information or the uname -s command will print the kernel name of your system.")
    def devices(self):
        print("/proc is very special in that it is also a virtual filesystem. It's sometimes referred to as a process information pseudo-file system. It doesn't contain 'real' files but runtime system information (e.g. system memory, devices mounted, hardware configuration, etc). For this reason it can be regarded as a control and information centre for the kernel. In fact, quite a lot of system utilities are simply calls to files in this directory. For example, 'lsmod' is the same as 'cat /proc/modules' while 'lspci' is a synonym for 'cat /proc/pci'. By altering files located in this directory you can even read/change kernel parameters (sysctl) while the system is running.")
    def numcpu(self):  
        print("In this Commands Show's the Number of the CPU's That are present in our system") 
    def load(self):
        print("It will print the System's Current Load Average") 
        print("If you select the Option in -S means.It will Stream Continuously,until you Enter the Control + C COmmand")
    def cpuinfo(self):
        print("Show's The Information about of the CPU present in our System")
    def getlogin(self):
        print("Show's the name of the user logged in on the controlling terminal of the process")
    def modules(self):
        print("In this command Represent the Modules that are Present in our System's")
    def meminfo(self):
        print("Show's The Information about of the Memory in our System")
    def bus_details(self):
        print("Show's The Information about of the Bus's in our System")
    def disk_usage(self):
        print("display file system disk usage.")
    def disk_space(self):
        print("Show's the Disk space")
    def today_date(self):
        print("Show's the Current's Date")
    def date_and_time(self):
        print("Show's the Current Date and Time")
    def list_cpu(self):
        print("Show's The Information about of the list of CPU present in our System")
    def list_hardware(self):
        print("Show's The Information about of the List of Hardware present in our System")
    def interface(self):
        print("Show's The Information about of the Interface present in our System")
    def logged_user(self):
        print("To check information about users who are currently logged into the system, we use the who command in the Linux system. The who command is used to display the users logged into the system")
    def system_view(self):
        print("It's Show's the System Information")
    def htop(self):
        print("Show's the details about Linux environment to determine the cause of load by each process")
    def download_speed(self):
        print("Show's the rate that digital data is transferred from the Internet to your computer")
    def upload_speed(self):
        print("Show's the rate that online data is transferred from your computer to the Internet.")
    def getuid(self):
        print("Show's the current process’s real user id ")
    def getpid(self):
        print("Show's the process ID of the current process.")
    def logged_user_on_controlling_Terminal(self):
        print("Show's the name of the user logged in on the controlling terminal of the process.")
    def ip_address_client(self):
        print("Show's the IP Address client")
    def host_name(self):
        print("Show's the name that is provided to a device to identify it in a local network")
    def history(self):
        print("Show's the history of our Terminal's previously Entered Command")
    def ip_Version(self):
        print("Show's the Internet Protocal Version")
    def uptime(self):
        print("The current time, how long the system has been running, how many users are currently logged on, and the system load averages for the past 1, 5, and 15 minutes")
    def Desc(self):
        print("Show's the Deep Explanation About Author,History_Linux,Awards_and_achievements ,About_Linux,User_interface ,Naming,Development,Hardware_support,Video_input_infrastructure,About_Linux_Kernal ")
    def type_of_commands(self):
        print("Show's the Type's of Command's and Details")
    def bc(self):
        print("It Will open the Calculater")
    def ls(self):
        print("Show's information about the FILEs")
    def ll(self):
        print("Show's information about the FILEs and use a long listing format")
    def ping(self):
        print("If you want to check if your system is connected to router or internet then PING (Packet INternet Groper) is the command for you")
    def mkdir(self):
        print("create a new folder in any directory")
    def gzip(self):
        print("compress any file from")
    def free(self):
        print("check exactly what amount of storage is free and used in physical as well as swap memory in the system")
    def top(self):
        print("monitor all the ongoing processes on the Linux system with the user name, priority level, unique process id and shared memory by each task")
    def echo(self):
        print("Print's the given string or value's") 
    def head(self):
        print("list the first 10 lines of the file you through with head command")
    def w(self):
        print("view's the list of currently logged in users")
    def whoami(self):
        print("which user is logged into system or who you are logged in as")
    def mv(self):
        print("move one file or directory to another file or directory")
    def ps(self):
        print("list of processes that are currently running for your session or for other users on the system")
    def env(self):
        print("used to display all the environment variable in the Linux Terminal window or ")
        print("running another task or program in custom environment without need to make any modifications in current session")
    def nano(self):
        print("Linux command-line text editor just similar to Pico editor which many of you might have used for programming and other purposes")
    def vi(self):
        print("The VI editor is the most popular and classic text editor in the Linux family")
    def rm(self):
        print("remove any file from the working directory")
    def clear(self):
        print("It will clear the Screen")
    def su(self):
        print("Switch to another account right from the Linux Terminal window")
    def wget(self):
        print("Download any file from the internet and best part is download works in background so that you can continue working on your task")
    def zip(self):
        print("To compress one or more files")
    def unzip(self):
        print("To extract files from compressed zip file")
    def shutdown(self):
        print("his command will shutdown the system exactly one minute after being executed.")
    def shutdown_c(self):
        print("You can use shutdown -c command to cancel shutdown.")
    def dir(self):
        print("view the list of all directories and folders present in current working directory")
    def cd(self):
        print("To access particular directory or folder from the file system")
    def reboot(self):
        print("It Will Restart the Entire System")
    def sort(self):
        print("sort file or arrange any record in particular order generally according to their ASCII values.")
    def tac(self):
        print("display the contents of the file in reverse orders")
    def exit(self):
        print("It's used to close the Terminal shell window directly from the command-line")
    def diff(self):
        print("compare the two directories and will display difference between them")
    def dmidecode(self):
        print("retrieve hardware information but if you want information of a particular hardware component")
    def netstat(self):
        print("To monitor incoming and outgoing network connections continuously...")
    def vmstat(self):
        print("Show's the virtual Memory usage")
    def mpstat(self):
        print("display all the information about CPU utilization and performance")
    def wc(self):
        print("Show's the Count the files")
    def nproc(self):
        print("Show's the number of processing units allotted to the currently running process.")
    def sleep(self):
        print("It will delay or pause the execution of command for particular amount of time")
    def lsblk(self):
        print("Show's sysfs filesystem and displays the block device information")
    def Which_type(self):
        print("Find the Given Commend whether internel command or External command's")