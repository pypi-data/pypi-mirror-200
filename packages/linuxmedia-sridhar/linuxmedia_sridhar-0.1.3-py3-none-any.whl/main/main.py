#! /usr/bin/python
import os
import sys
from .lib.Helper import Helper
from .lib.Validate import Validate
from .lib.Argument import Argument
from .lib.Where_locate import Where_locate
from .lib.Description import Description
Description=Description()
Argument=Argument(sys.argv)
Validate=Validate(sys.argv)
Helper=Helper()
def main():
    if((Helper.Availale_contents())==True):
        if(len(sys.argv)>1):
            if(Argument.hasCommands(['version'])):
                print("Version :: 2.o")
            if(Argument.hasCommands(['uname'])):
                Validate.uname()
            if(Argument.hasCommands(['pwd'])):
                Validate.pwd()
            if(Argument.hasOption(['--ip']) or Argument.hasCommands(['ip_address'])):
                Validate.ip_address()
            if(Argument.hasOption(['--sv']) or Argument.hasCommands(['sys_version'])):
                Validate.sys_version()
            if(Argument.hasOption(['--dev']) or Argument.hasCommands(['devices'])):
                Validate.devices()
            if(Argument.hasOption(['--n']) or Argument.hasCommands(['numcpu'])):
                Validate.numcpu()
            if(Argument.hasOption(['--l']) or Argument.hasCommands(['load'])):
                Validate.load()
            if(Argument.hasOption(['--c']) or Argument.hasCommands(['cpuinfo'])):
                Validate.cpuinfo()
            if(Argument.hasOption(['--g']) or Argument.hasCommands(['getlogin'])):
                Validate.getlogin()
            if(Argument.hasOption(['--f']) or Argument.hasCommands(['modules'])):
                Validate.modules()
            if(Argument.hasOption(['--m']) or Argument.hasCommands(['meminfo'])):
                Validate.meminfo()
            if(Argument.hasOption(['--w']) or Argument.hasCommands(['bus_details'])):
                Validate.bus_details()
            if(Argument.hasOption(['--v']) or Argument.hasCommands(['disk_usage'])):
                Validate.disk_usage()
            if(Argument.hasOption(['--x']) or Argument.hasCommands(['disk_space'])):
                Validate.disk_space()
            if(Argument.hasOption(['--d']) or Argument.hasCommands(['today_date'])):
                Validate.today_date()
            if(Argument.hasOption(['--t']) or Argument.hasCommands(['date_and_time'])):
                Validate.date_and_time()
            if(Argument.hasOption(['--j']) or Argument.hasCommands(['list_cpu'])):
                Validate.list_cpu()
            if(Argument.hasOption(['--q']) or Argument.hasCommands(['interface'])):
                Validate.interface()
            if(Argument.hasOption(['--k']) or Argument.hasCommands(['list_hardware'])):
                Validate.list_hardware() #TODO : Check the Wheater location is folder or file
            if(Argument.hasOption(['--z']) or Argument.hasCommands(['logged_user'])):
                Validate.logged_user()
            if(Argument.hasOption(['--B']) or Argument.hasCommands(['system_view'])):
                Validate.system_view()
            if(Argument.hasOption(['--C']) or Argument.hasCommands(['download_speed'])):
                Validate.download_speed()
            if(Argument.hasOption(['--E']) or Argument.hasCommands(['upload_speed'])):
                Validate.upload_speed()
            if(Argument.hasOption(['--F']) or Argument.hasCommands(['getuid'])):
                Validate.getuid()
            if(Argument.hasOption(['--G']) or Argument.hasCommands(['getpid'])):
                Validate.getpid()
            if(Argument.hasOption(['--M']) or Argument.hasCommands(['logged_user_on_controlling_Terminal'])):
                Validate.logged_user_on_controlling_Terminal()
            if(Argument.hasOption(['--Q']) or Argument.hasCommands(['ip_address_client'])):
                Validate.ip_address_client()
            if(Argument.hasOption(['--G']) or Argument.hasCommands(['getpid'])):
                Validate.getpid()
            if(Argument.hasOption(['--R']) or Argument.hasCommands(['host_name'])):
                Validate.host_name()
            if(Argument.hasOption(['--U']) or Argument.hasCommands(['ip_Version'])):
                Validate.ip_Version()
            if(Argument.hasCommands(['vmstat'])):
                Validate.vmstat()
            if(Argument.hasCommands(['uptime'])):
                Validate.uptime()
            if(Argument.hasCommands(['htop'])):
                Validate.htop()
            if(Argument.hasCommands(['history'])):
                Validate.history()
            if(Argument.hasCommands(['Desc'])):
                Validate.Desc()
            if(Argument.hasCommands(['bc'])):
                Validate.bc()
            if(Argument.hasCommands(['ls'])):
                Validate.ls()
            if(Argument.hasCommands(['ll'])):
                Validate.ll()
            if(Argument.hasCommands(['ping'])):
                Validate.ping()
            if(Argument.hasCommands(['gzip'])):
                Validate.gzip()
            if(Argument.hasCommands(['mkdir'])):
                Validate.mkdir()
            if(Argument.hasCommands(['free'])):
                Validate.free()
            if(Argument.hasCommands(['top'])):
                Validate.top()
            if(Argument.hasCommands(['head'])):
                Validate.head()
            if(Argument.hasCommands(['w'])):
                Validate.w()
            if(Argument.hasCommands(['echo'])):
                Validate.echo()
            if(Argument.hasCommands(['whoami'])):
                Validate.whoami() 
            if(Argument.hasCommands(['mv'])):
                Validate.mv() 
            if(Argument.hasCommands(['ps'])):
                Validate.ps() 
            if(Argument.hasCommands(['tail'])):
                Validate.tail() 
            if(Argument.hasCommands(['env'])):
                Validate.env()
            if(Argument.hasCommands(['nano'])):
                Validate.nano()
            if(Argument.hasCommands(['vi'])):
                Validate.vi()
            if(Argument.hasCommands(['rm'])):
                Validate.rm()
            if(Argument.hasCommands(['clear'])):
                Validate.clear()
            if(Argument.hasCommands(['su'])):
                Validate.su()
            if(Argument.hasCommands(['wget'])):
                Validate.wget()
            if(Argument.hasCommands(['zip'])):
                Validate.zip()
            if(Argument.hasCommands(['unzip'])):
                Validate.unzip()
            if(Argument.hasCommands(['shutdown'])):
                Validate.shutdown()
            if(Argument.hasCommands(['dir'])):
                Validate.dir()
            if(Argument.hasCommands(['cd'])):
                Validate.cd()
            if(Argument.hasCommands(['reboot'])):
                Validate.reboot()
            if(Argument.hasCommands(['sort'])):
                Validate.sort()
            if(Argument.hasCommands(['tac'])):
                Validate.tac()
            if(Argument.hasCommands(['exit'])):
                Validate.exit()
            if(Argument.hasCommands(['diff'])):
                Validate.diff()
            if(Argument.hasCommands(['dmidecode'])):
                Validate.dmidecode()
            if(Argument.hasCommands(['netstat'])):
                Validate.netstat()
            if(Argument.hasCommands(['mpstat'])):
                Validate.mpstat()
            if(Argument.hasCommands(['wc'])):
                Validate.wc()
            if(Argument.hasCommands(['nproc'])):
                Validate.nproc()
            if(Argument.hasCommands(['sleep'])):
                Validate.sleep()
            if(Argument.hasCommands(['lsblk'])):
                Validate.lsblk()
            if(Argument.hasCommands(['hdparm'])):
                Validate.hdparm()
            if(Argument.hasCommands(['Which_type'])):
                Validate.Which_type()
            if(Argument.hasCommands(['commands'])):
                Validate.commands()
            if((sys.argv[1]=="--help")or(sys.argv[1]=="-h")):
                Helper.Help(sys.argv[0])
        else:
            Helper.Help(sys.argv[0])

            
    else:
        Helper.print_help()


if __name__ == "__main__":
    main()
        
