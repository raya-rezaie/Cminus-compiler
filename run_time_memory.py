from enum import Enum


class memory():
    def __init__(self):
        self.data = {}
    def write(self, address, value):
        self.data[address] = value
    def read(self , address):
        return self.data.get(address , None)


class Tree_address_codes():
        def __init__(self, operation):
            self.op = operation
        def op_to_value(self):
            instruction = []
            instruction[0] = self.op[0]
            for i,operand in enumerate(self.op):
                if operand[i].startswith("#"):
                    instruction[i] = int(operand[1:])
                elif operand[i].startswith("@"):
                    addr = int(self.op2[1:])
                    instruction[i] = memory.read(addr)     
                else:
                        
                
            
        
        def action(self):
            match self.opcode:
                case "ADD":
                    if self.op1.startswith()