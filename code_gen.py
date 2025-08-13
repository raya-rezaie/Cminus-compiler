from run_time_memory import *
from enum import Enum


class actionNames(Enum):
    pid = 0,
    add_or_sub = 1,
    push_ss = 2,
    dclr_var = 3,
    dclr_arr = 4,
    update_func_params = 5,
    end_func = 6,
    save_param_list = 7,
    save_param_norm = 8,
    save_scope = 9,
    fill_break = 10,
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
    push_num_ss = 24,
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
    # def format_token(self, token):
        # Convert (TOKEN_TYPE, TOKEN_VALUE) or int address to  three address codes
    #    if token is None:
    #        return None
    #    if not isinstance(token, tuple) or len(token) != 2:
    #        return str(token)

    #    ttype, tval = token
    #    if ttype == "NUM":
    #        return f"#{tval}"
    #     elif ttype == "ID":
    #         addr = self.symbol_table.find_addr(tval)
    #         if addr is None:
    #             raise NameError(f"Variable '{tval}' not declared")
    #         return str(addr)
    #     elif ttype in ("SYMBOL", "KEYWORD"):
    #         return str(tval)
    #     else:
    #         raise ValueError(f"Unknown token type {ttype}")
    # def new_temp(self):
    #     #getting new temp
    #     temp_addr = self.tb.alloc_memory()
    #     if temp_addr == -1:
    #         raise MemoryError("No temp space")
    #     return temp_addr
    def emit(self, op_enum, o1=None, o2=None, r=None):
        instr = ThreeAddressCode(
            op_enum,
            self.format_token(o1),
            self.format_token(o2),
            self.format_token(r)
        )
        return instr

    def pid(self, token):
        if token[1] == 'output':
            self.stack.push('PRINT')
        entry = self.symbol_table.get_symbol_full(token[1])

        if entry is None:
            raise NameError(f"Undefined identifier {token}")
        addr = entry[2]
        self.stack.push(addr)  # push raw token called for IDs

    # def add_sub(self, action):
    #    t = self.tb.get_temp()
    #    self.pb.add_instruction([action , self.stack.top() , self.stack.pop(1) , t])
    #    self.pb.index += 1
    #    self.stack.pop(2).x
    #    self.stack.push(t)
    def assign(self):
        instr = ThreeAddressCode(ThreeAddressCodeType.assign, str(
            self.stack.pop()), str(self.stack.top()))
        self.pb.add_instruction_and_increase(instr)

    def push_ss(self, token):
        self.stack.push(token[1])

    def push_num_ss(self, token):
        self.stack.push('#' + token[1])

    def declare_var(self, token):
        # the data is supposed to be saved in db as names of the token or complete token
        name = self.stack.pop()
        type = self.stack.pop()
        memory_index = self.db.alloc_memory()
        self.db.set_value(memory_index, 0)
        self.symbol_table.set_symbol_type(name, type)
        self.symbol_table.set_symbol_len(name, 1)
        self.symbol_table.set_symbol_loc(name, memory_index)

    def declare_arr(self):
        # is the type and size ok?
        size = self.stack.pop()
        name = self.stack.pop()
        type = self.stack.pop()
        start_loc = None
        for i in range(size-1):
            loc = self.db.alloc_memory()
            if start_loc == None:
                start_loc = self.db.alloc_memory()
            self.db.set_value(loc, 0)
        self.symbol_table.set_symbol_type(name, type)
        self.symbol_table.set_symbol_len(name, size)
        self.symbol_table.set_symbol_loc(name, start_loc)

    def print(self):
        # pops the variable and prints it
        if self.stack.top(1) == 'PRINT':
            item = self.stack.pop()
            instr = ThreeAddressCode(ThreeAddressCodeType.print, item)
            self.pb.add_instruction_and_increase(instr)
        # push the type and name of current token

    def binary_op_helper(self, op_enum):
        right = self.stack.pop()
        left = self.stack.pop()
        t = self.new_temp()
        instr = ThreeAddressCode(op_enum, left, right, t)
        self.pb.add_instruction_and_increase(instr)
        self.stack.push(t)

    def add_or_sub(self):
        self.binary_op_helper(ThreeAddressCodeType.add)

    def mult(self):
        self.binary_op_helper(ThreeAddressCodeType.mult)

    def loc_while_cond_before(self):
        self.stack.push(self.pb.get_index())

    def save_while_cond_jpf(self):
        index = self.pb.get_index()
        self.stack.push(index)
        self.pb.set_index(index + 1)

    # assumes stack = pc after while cond | result of cond | pc before while cond
    def fill_while(self):
        uncond_jmp_idx = self.pb.get_index()
        # add conditional jump after checking while condition
        cond_jmp = ThreeAddressCode(
            ThreeAddressCodeType.jpf, self.stack.top(1), uncond_jmp_idx + 1)
        cond_jmp_idx = self.stack.top(0)
        if cond_jmp_idx.isdigit():
            self.pb.add_instruction_at(cond_jmp, int(cond_jmp_idx))
        else:
            pass  # bad stack, maybe report

        # add unconditional jump to before while condition, after while instructions
        uncond_jmp = ThreeAddressCode(
            ThreeAddressCodeType.jp, self.stack.top(2))
        self.pb.add_instruction_and_increase(uncond_jmp)

        self.stack.pop(3)

    def save_scope():
        # dont know where is the scope to save it
        pass

    def relation(self):
        right = self.stack.pop()
        op_sym = self.stack.pop()
        left = self.stack.pop()
        t = self.new_temp()
        if op_sym == '<':
            instr = (ThreeAddressCodeType.lt, left, right, t)
            self.pb.add_instruction_and_increase(instr)
        elif op_sym == '==':
            instr = ThreeAddressCode(ThreeAddressCodeType.eq, left, right, t)
            self.pb.add_instruction_and_increase(instr)
        else:
            raise NotImplementedError(f"relation op not supported: {op_sym}")
        self.stack.push(t)

    def calc_arr_addr(self):
        # calculating the address of an element inside an array given the base address of the array and index.
        index = self.stack.pop()
        base = self.stack.pop()
        if str(index).startswith("#"):  # index is constant
            offset_bytes = int(str(index).lstrip("#")) * BLOCKSIZE
            t = self.new_temp()
            instr = ThreeAddressCode(
                ThreeAddressCodeType.add, base, offset_bytes, t)
            self.pb.add_instruction_and_increase(instr)
            self.stack.push(t)
        else:
            t1 = self.new_temp()
            instr = ThreeAddressCode(
                ThreeAddressCodeType.mult, index, f"#{BLOCKSIZE}", t1)
            self.pb.add_instruction_and_increase(instr)
            t2 = self.new_temp()
            instr = ThreeAddressCode(ThreeAddressCodeType.add, base, t1, t2)
            self.pb.add_instruction_and_increase(instr)

            self.stack.push(t2)

    def save_jmp_out_scope(self):  # unconditional jump to fill later
        jmp_idx = self.pb.add_instruction_and_increase(
            ThreeAddressCode(ThreeAddressCodeType.jp, "", "", ""))
        self.stack.push(jmp_idx)

    def save_if_cond_jpf(self):
        # jump out if condition false
        jpf_index = self.pb.add_instruction_and_increase(
            ThreeAddressCode(ThreeAddressCodeType.jpf, "0", "", ""))
        self.stack.push(jpf_index)

    def fill_if_cond_jpf(self):
        jpf_index = self.stack.pop()
        cond = self.stack.pop()
        # current pb index to fill the jpf that was set to 0
        after_idx = self.pb.get_index()
        jpf_instr = ThreeAddressCode(
            ThreeAddressCodeType.jpf,
            cond,
            str(after_idx + 1), None)
        self.pb.add_instruction_at(jpf_instr, jpf_index)
        self.stack.push(after_idx)
        self.pb.set_index(after_idx+1)

    def fill_if_cond_jpt(self):
        # for skipping else if condition is true
        jmp_idx = self.stack.pop()
        after_idx = self.pb.get_index()
        instr = ThreeAddressCode(ThreeAddressCodeType.jp, after_idx)
        self.pb.add_instruction_at(instr, jmp_idx)
