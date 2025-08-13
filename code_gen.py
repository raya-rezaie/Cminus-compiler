from run_time_memory import *
from symboltable import *
from enum import Enum


class code_generator:
    def __init__(self, runtime_memory, semantic_stack, symbol_table):
        self.pb = runtime_memory.get_pb()
        self.tb = runtime_memory.get_temp()
        self.db = runtime_memory.get_db()
        self.stack = semantic_stack
        self.symbol_table = symbol_table
        self.token = ""

    def exec_func(self, type, token):
        self.token = token
        type.value(self, token)

    def pid(self):
        if self.token[1] == 'output':
            self.stack.push('PRINT')
            return

        entry = self.symbol_table.get_symbol_full(self.token[1])

        if entry is None:
            # TODO: catch errors to handle semantic errors
            raise NameError(f"Undefined identifier {self.token[1]}")

        addr = entry[2]
        self.stack.push(addr)

    def add_or_sub(self):
        # TODO: must do add or sub depending on stack
        self.binary_op_helper(ThreeAddressCodeType.add)

    def push_ss(self):
        self.stack.push(self.token[1])

    def declare_var(self):
        # the data is supposed to be saved in db as names of the token or complete token
        name = self.stack.pop()
        type = self.stack.pop()
        memory_index = self.db.alloc_memory()
        self.db.set_value(memory_index, 0)
        self.symbol_table.set_symbol_type(name, SymbolType(type))
        self.symbol_table.set_symbol_len(name, 1)
        self.symbol_table.set_symbol_loc(name, memory_index)

    def declare_arr(self):
        # is the type and size ok?
        size = int(self.stack.pop())
        name = self.stack.pop()
        type = SymbolType(self.stack.pop())
        start_loc = None
        for i in range(size):
            loc = self.db.alloc_memory()
            if start_loc == None:
                start_loc = self.db.alloc_memory()
            self.db.set_value(loc, 0)
        self.symbol_table.set_symbol_type(name, type)
        self.symbol_table.set_symbol_len(name, size)
        self.symbol_table.set_symbol_loc(name, start_loc)

    def update_func_params(self):
        pass

    def end_func(self):
        pass

    def save_param_list(self):
        pass

    def save_param_norm(self):
        pass

    def save_scope():
        # dont know where is the scope to save it
        pass

    def fill_break(self):
        pass

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

    def return_jmp(self):
        pass

    def save_return_value(self):
        pass

    def print(self):
        # pops the variable and prints it
        if self.stack.top(1) == 'PRINT':
            item = self.stack.pop()
            instr = ThreeAddressCode(ThreeAddressCodeType.print, item)
            self.pb.add_instruction_and_increase(instr)
        # push the type and name of current token

    def assign(self):
        instr = ThreeAddressCode(ThreeAddressCodeType.assign, str(
            self.stack.pop()), str(self.stack.top()))
        self.pb.add_instruction_and_increase(instr)

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

    def push_num_ss(self):
        self.stack.push('#' + self.token[1])

    def start_args(self):
        pass

    def check_args(self):
        pass

    def mult(self):
        self.binary_op_helper(ThreeAddressCodeType.mult)

    def binary_op_helper(self, op_enum):
        right = self.stack.pop()
        left = self.stack.pop()
        t = self.new_temp()
        instr = ThreeAddressCode(op_enum, left, right, t)
        self.pb.add_instruction_and_increase(instr)
        self.stack.push(t)

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
    # def emit(self, op_enum, o1=None, o2=None, r=None):
    #     instr = ThreeAddressCode(
    #         op_enum,
    #         self.format_token(o1),
    #         self.format_token(o2),
    #         self.format_token(r)
    #     )
    #     return instr


class actionNames(Enum):
    pid = code_generator.pid
    add_or_sub = code_generator.add_or_sub
    push_ss = code_generator.push_ss
    dclr_var = code_generator.declare_var
    dclr_arr = code_generator.declare_arr
    update_func_params = code_generator.update_func_params
    end_func = code_generator.end_func
    save_param_list = code_generator.save_param_list
    save_param_norm = code_generator.save_param_norm
    save_scope = code_generator.save_scope
    fill_break = code_generator.fill_break
    save_jmp_out_scope = code_generator.save_jmp_out_scope
    save_if_cond_jpf = code_generator.save_if_cond_jpf
    fill_if_cond_jpf = code_generator.fill_if_cond_jpf
    fill_if_cond_jpt = code_generator.fill_if_cond_jpt
    loc_while_cond_before = code_generator.loc_while_cond_before
    save_while_cond_jpf = code_generator.save_while_cond_jpf
    fill_while = code_generator.fill_while
    return_jp = code_generator.return_jp
    save_return_value = code_generator.save_return_value
    print = code_generator.print
    assign = code_generator.assign
    calc_arr_addr = code_generator.calc_arr_addr
    relation = code_generator.relation
    push_num_ss = code_generator.push_num_ss
    start_args = code_generator.start_args
    check_args = code_generator.check_args
    mult = code_generator.mult
