import os
import sys
import subprocess
from main.lib.Argument import Argument
Argument=Argument(sys.argv)
class Where_locate:
    def Internal_Command():
        print("This Command Belong's To Internal Command")
    def External_command():
        print("This Command Belong's To External Command")
    def included_command():
        print("This command Belong's Included_command")
    def find_location(self):
        value=Argument.Validate_loaction(sys.argv)
        for i in value:
            if(os.path.exists(f"/usr/bin/{i}") or os.path.exists(f"/usr/sbin/{i}")):
                Where_locate.External_command()
            elif(os.system(f'which {i}')):
                Where_locate.Internal_Command()
            else:
                Where_locate.included_command()
            

        
            