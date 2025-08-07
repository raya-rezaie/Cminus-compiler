from aux import *
from semantic_stack import * 
class SemanticAction:
    def __init__(self):
        self.type()
        
    def get_func_by_name(name , stack):
        match name:
            case "pid":
                pid(self ,inputVar)
            case "add":
                add_mult()
    def pid(self,inputVar , stack):
        p = findaddr(inputVar)
        stack.pop()
    def add_mult(action):
        
        