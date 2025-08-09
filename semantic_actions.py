from run_time_memory import *
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
    mult = 27
    
class SemanticAction:
    def __init__(self, runtime_memory, semantic_stack, symbol_table):
        # self.token = token
        self.pb = runtime_memory.get_pb()
        self.tb = runtime_memory.get_temp()
        self.db = runtime_memory.get_db()
        self.stack = semantic_stack
        self.symbol_table = symbol_table
        # self.number = number

        
    def exec_func(self, type, token):
        match type:
            case actionNames.pid:
                self.pid(token)
            # case "add":
            #     self.add_sub("ADD")
            # case "sub":
            #     self.add_sub("SUB")
            case "dclr_arr":
                self.declare_arr()
            case "dclr_var":
                self.declare_var()
            case "print":
                self.print()
            case actionNames.loc_while_cond_before:
                self.loc_while_cond_before()
            case actionNames.save_while_cond_jpf:
                self.save_while_cond_jpf()
                
    def pid(self, token):
        p = self.symbol_table.findaddr(token)
        self.stack.pop()
    def add_sub(self, action):
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

    def loc_while_cond_before(self):
        self.stack.push(self.pb.get_index())

    def save_while_cond_jpf(self):
        index = self.pb.get_index()
        self.stack.push(index)
        self.pb.set_index(index + 1)

    def fill_while(self): # assumes stack = pc after while cond | result of cond | pc before while cond
        uncond_jmp_idx = self.pb.get_index()
        # add conditional jump after checking while condition
        cond_jmp = ThreeAddressCode(ThreeAddressCodeType.jpf, self.stack.top(1), uncond_jmp_idx + 1)
        cond_jmp_idx = self.stack.top(0)
        if cond_jmp_idx.isdigit():
            self.pb.add_instruction_at(cond_jmp, int(cond_jmp_idx))
        else:
            pass # bad stack, maybe report
        
        # add unconditional jump to before while condition, after while instructions
        uncond_jmp = ThreeAddressCode(ThreeAddressCodeType.jp, self.stack.top(2))
        self.pb.add_instruction_at(uncond_jmp, uncond_jmp_idx)
        
        self.pd.set_index(uncond_jmp_idx +  1)
        self.stack.pop(3)
