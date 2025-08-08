from enum import Enum
INTSIZE = 4

class run_time_memory():
    def __init__(self , program_block , data_block , temporories):
        self.pb = program_block
        self.db = data_block
        self.temp = temporories
class temporaryBlock():
    def __init__(self, base, bound, index):
        self.base = base
        self.bound = bound
        self.index = base
        self.data = {}
    def get_temp(self):
        i = self.index
        self.index +=4
        return  i
class programBlock():
    def __init__(self , base , bound):
        self.base = base
        self.bound = bound
        self.index = base
        self.block = {}
    def add_instruction(self ,instruction , ind):
        self.block[ind] = instruction
class dataBlock():
    def __init__(self, base, bound):
        self.base = base
        self.bound = bound
        self.index = base
        self.block = {}

        
        
        
        
        
# def write(self, address, value):
#        self.data[address] = value
# 
#def read(self , address):
#return self.data.get(address , None)'''



         
                        
                
            
        
