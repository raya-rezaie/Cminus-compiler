from auxFuncts import *
from semantic_stack import * 
from semantic_analayzer import *
class SemanticAction:
    def __init__(self):
        self.type()

        
    def get_func_by_name(self ,name , input_var):
        match name:
            case "pid":
                self.pid(self ,input_var)
            case "add":
                self.add_sub("ADD")
            case "sub":
                self.add_sub("SUB")
            case "dclr_arr":
                self.declare_arr()
            case "dclr_var":
                self.declare_var()
            case "print":
                self.print()
                
                

    def pid(self,inputVar):
        p = findaddr(inputVar)
        self.stack.pop()
    def add_sub(action):
        t = temps.get_temp()
        program_block.add_instruction([action , stack.top() , stack.pop(1) , t])
        program_block.index += 1
        stack.pop(2)
        stack.push(t)
    def assign():
        program_block.add_instruction(["ASSIGN" , stack.top() , stack.pop(1)])
        program_block.index += 1
        stack.pop(2)
    def declare_var():
        pass
    def declare_arr():
        pass
    def print():
        pass
    
            

        
        
        