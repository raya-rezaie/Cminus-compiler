from auxFuncts import *
from enum import Enum
class actionNames(Enum):
    pid = 0 ,
    add_or_sub = 1 , 
    push_ss = 2,
    dclr_var = 3 ,
    dclr_arr = 4 ,
    update_func_params = 5,
    end_func = 6 ,
    save_param_list = 7 ,
    save_param_norm = 8,
    save_scope = 9,
    fill_break = 10 ,
    save_jmp_out_scope = 11,
    save_if_cond_jpf = 12,
    fill_if_cond_jpf = 13,
    fill_if_cond_jpt = 14,
    loc_while_cond_before = 15,
    save_while_cond_jpf = 16,
    fill_while = 17,
    return_jp = 18,
    save_return_value = 19,
    print = 20,
    assign = 21,
    calc_arr_addr = 22,
    relation = 23,
    push_num_ss =  24,
    start_args = 25,
    check_args = 26,
    calc_arr_addr = 27,
    mult = 28
    
class SemanticAction:
    def __init__(self, token , stack , pb , tb , db , number):
        self.token = token
        self.pb = pb
        self.tb = tb
        self.stack = stack
        self.number = number

        
    def get_func_by_name(self):
        match self.type:
            case "pid":
                self.pid(self)
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
                
    def pid(self):
        p = findaddr(self.token)
        self.stack.pop()
    def add_sub(self ,action):
        t = self.tb.get_temp()
        self.pb.add_instruction([action , self.stack.top() , self.stack.pop(1) , t])
        self.pb.index += 1
        self.stack.pop(2).x
        self.stack.push(t)
    def assign(self):
        self.pb.add_instruction(["ASSIGN" , self.stack.top() , self.stack.pop(1)])
        self.pb.index += 1
        self.stack.pop(2)
    def declare_var():
        pass
    def declare_arr():
        pass
    def print():
        pass
    
            

        
        
        