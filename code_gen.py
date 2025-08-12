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
    
class code_generator:
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
            case actionNames.dclr_arr:
                self.declare_arr()
            case actionNames.dclr_var:
                self.declare_var()
            case actionNames.print:
                self.print()
            case actionNames.loc_while_cond_before:
                self.loc_while_cond_before()
            case actionNames.save_while_cond_jpf:
                self.save_while_cond_jpf()
    def _format_token(self, token):
        # Convert (TOKEN_TYPE, TOKEN_VALUE) or int address to TAC string
        if token is None:
            return None
        if not isinstance(token, tuple) or len(token) != 2:
            return str(token)

        ttype, tval = token
        if ttype == "NUM":
            return f"#{tval}"
        elif ttype == "ID":
            addr = self.symbol_table.find_addr(tval)
            if addr is None:
                raise NameError(f"Variable '{tval}' not declared")
            return str(addr)
        elif ttype in ("SYMBOL", "KEYWORD"):
            return str(tval)
        else:
            raise ValueError(f"Unknown token type {ttype}")
    def new_temp(self):
        #getting new temp
        temp_addr = self.tb.alloc_memory()
        if temp_addr == -1:
            raise MemoryError("No temp space")
        return temp_addr
    def _emit(self, op_enum, o1=None, o2=None, r=None):
        instr = ThreeAddressCode(
            op_enum,
            self._format_token(o1),
            self._format_token(o2),
            self._format_token(r)
        )
        return self.pb.add_instruction(instr)

    def pid(self, token):
        entry = self.symbol_table.get_symbol_full(token)
        if entry is None:
            raise NameError(f"Undefined identifier {token}")
        addr = entry[2]
        self.stack.push(("ID", token))  # push raw token called for IDs
    def add_sub(self, action):
        t = self.tb.get_temp()
        self.pb.add_instruction([action , self.stack.top() , self.stack.pop(1) , t])
        self.pb.index += 1
        self.stack.pop(2).x
        self.stack.push(t)
    def assign(self):
        self.pb.add_instruction(["ASSIGN" , self.stack.top() , self.stack.pop(1)])   #shouldnt it be 1 and 2?
        self.pb.index += 1
        self.stack.pop(2)
    def push_ss(self, token):
        self.stack.push(token)
    def declare_var(self , token):
        #the data is supposed to be saved in db as names of the token or complete token
        name = self.stack.pop()
        type = self.stack.pop()
        memory_index = self.db.alloc_memory()
        self.db.set_value(memory_index , 0)
        self.symbol_table.set_symbol_type(name , type)
        self.symbol_table.set_symbol_len(name , 1)
        self.symbol_table.set_symbol_loc(name,memory_index)
     
    def declare_arr(self):
        #is the type and size ok?
        size = self.stack.pop()
        name = self.stack.pop()
        type = self.stack.pop()
        start_loc = None
        for i in range(size-1):
            loc = self.db.alloc_memory()
            if start_loc ==None:
                start_loc = self.db.alloc_memory()
            self.db.set_value(loc,0)
        self.symbol_table.set_symbol_type(name , type)
        self.symbol_table.set_symbol_len(name , size)
        self.symbol_table.set_symbol_loc(name,start_loc)
        
    def do_print(self):
        #pops the variable and prints it
        item = self.stack.pop()
        self._emit(ThreeAddressCodeType.print, item, None, None)
    def push_ss(self, token): 
        self.stack.push(token[0])
        self.stack.push(token[1])
        #push the type and name of current token

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
    def save_scope():
        #dont know where is the scope to save it
        pass
    
