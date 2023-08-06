class Argument:
    def __init__(self,args):
        self.args=args
        self.command=[]
        self.option=[]
        self.location=[]
        self.locate=[]
        for arg in self.args:
            if '-' in arg:
                self.option.append(arg)
            elif '--' in arg[:1]:
                self.option.append(arg)
                arg.split('--')
                self.location.append(arg[1])
                print(self.location)
            else:
                self.command.append(arg)

 
    def hasOption(self,options:list): 
        user_options=set(self.option)
        required_option=set(options)
        return list(required_option & user_options)
        
        
    def hasCommands(self,commands:list):
        user_command=set(self.command)
        required_command=set(commands)
        return list(required_command & user_command)
        
    def Validate_loaction(self,option):
        for arg in option:
            if '--' in arg:
                options=arg.split('--')
                self.location.append(options[1])
            else:
                self.locate.append(option)
        
        return self.location
        



        



