from run_time_memory import *
from symboltable import *
from enum import Enum


class CodeGenerator:
    def __init__(self, runtime_memory, semantic_stack, symbol_table):
        self.pb = runtime_memory.get_pb()
        self.tb = runtime_memory.get_temp()
        self.db = runtime_memory.get_db()
        self.stack = semantic_stack
        self.symbol_table = symbol_table
        self.scope = 0
        self.breaks = {}
        self.func_scopes = []
        self.returns = {}
        self.return_val_slot = self.tb.alloc_memory()
        self.token = ""
        self.arg_stack = []


    def exec_func(self, type, token):
        self.token = token
        type(self)

    def pid(self):
        if self.token[1] == 'output':
            self.stack.push('PRINT')
            return

        entry = self.symbol_table.get_symbol_full(self.token[1], self.scope)

        if entry is None:
            # TODO: catch errors to handle semantic errors
            raise NameError(f"Undefined identifier {self.token[1]}")

        self.stack.push(entry.loc)

    def add_or_sub(self):
        rand2 = self.stack.pop()
        rator = ThreeAddressCodeType.add if self.stack.pop(
        ) == '+' else ThreeAddressCodeType.sub
        rand1 = self.stack.pop()

        temp = self.tb.alloc_memory()
        self.stack.push(temp)
        instruction = ThreeAddressCode(rator, rand1, rand2, temp)
        self.pb.add_instruction_and_increase(instruction)

    def push_ss(self):
        self.stack.push(self.token[1])

    def declare_var(self):
        # the data is supposed to be saved in db as names of the token or complete token
        name = self.stack.pop()
        type = self.stack.pop()
        memory_index = self.db.alloc_memory()
        self.db.set_value(memory_index, 0)
        self.symbol_table.set_symbol_type(name, SymbolType(type), self.scope)
        self.symbol_table.set_symbol_len(name, 1, self.scope)
        self.symbol_table.set_symbol_loc(name, memory_index, self.scope)

    def declare_arr(self):
        # is the type and size ok? (fekr konam are)
        size = int(self.stack.pop())
        name = self.stack.pop()
        type = SymbolType(self.stack.pop())
        start_loc = None
        for i in range(size):
            loc = self.db.alloc_memory()
            if start_loc == None:
                start_loc = self.db.alloc_memory()
            self.db.set_value(loc, 0)
        self.symbol_table.set_symbol_type(name, type, self.scope)
        self.symbol_table.set_symbol_len(name, size, self.scope)
        self.symbol_table.set_symbol_loc(name, start_loc, self.scope)

    def update_func_params(self):
        func_name = self.stack.pop()
        func_type = SymbolType(self.stack.pop())
        if func_type == SymbolType.INT:
            func_type = SymbolType.INT_FUNC
        elif func_type == SymbolType.VOID:
            func_type = SymbolType.VOID_FUNC
        else:
            return  # maybe error

        # function's own scope is one less than its args => when accessing args, use function_scope + 1
        self.symbol_table.set_symbol_type(func_name. func_type, self.scope)
        self.func_scopes.append(self.scope + 1)
        self.returns[self.scope + 1] = []

    def end_func(self):
        return_pc = self.stack.pop()
        ins = ThreeAddressCode(ThreeAddressCodeType.jp, return_pc)
        func_scope = self.func_scopes.pop()
        for return_idx in self.returns[func_scope]:
            self.pb.add_instruction_at(ins, return_idx)
        del self.returns[func_scope]

    def save_param_list(self):
        function_scope = self.scope + 1
        name = self.stack.pop()
        type = self.stack.pop()
        if type != SymbolType.INT.value:
            return  # only int arrays => maybe print error
        type = SymbolType.INT_INDIRECT
        self.symbol_table.set_symbol_type(name, type, function_scope)
        arg_ptr_loc = self.db.alloc_memory()
        self.symbol_table.set_symbol_loc(name, arg_ptr_loc, function_scope)

    def save_param_norm(self):
        function_scope = self.scope + 1
        name = self.stack.pop()
        type = SymbolType(self.stack.pop())  # must be int
        if type != SymbolType.INT:
            return  # maybe print error
        self.symbol_table.set_symbol_type(name, type, function_scope)
        arg_ptr_loc = self.db.alloc_memory()
        self.symbol_table.set_symbol_loc(name, arg_ptr_loc, function_scope)

    def save_jmp_out_scope(self):  # unconditional jump to fill later
        jmp_idx = self.pb.add_instruction_and_increase(
            ThreeAddressCode(ThreeAddressCodeType.jp, "", "", ""))
        self.breaks[self.scope].append(jmp_idx)

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
        index = self.pb.get_index()
        self.stack.push(index)

    def save_while_cond_jpf(self):
        index = self.pb.get_index()
        self.stack.push(index)
        self.pb.set_index(index + 1)

        # save scope here: only valid break is in while
        self._enter_scope()

    # assumes stack = pc after while cond | result of cond | pc before while cond | ...
    def fill_while(self):
        uncond_jmp_idx = self.pb.get_index()
        # add conditional jump after checking while condition
        cond_jmp = ThreeAddressCode(
            ThreeAddressCodeType.jpf, self.stack.top(1), uncond_jmp_idx + 1)
        cond_jmp_idx = self.stack.top(0)
        self.pb.add_instruction_at(cond_jmp, cond_jmp_idx)

        # add unconditional jump to before while condition, after while instructions
        uncond_jmp = ThreeAddressCode(
            ThreeAddressCodeType.jp, self.stack.top(2))
        self.pb.add_instruction_and_increase(uncond_jmp)

        self.stack.pop(3)

        # fill breaks to current pc (no valid breaks except in while => #fill_break moved here and combined with #fill_while)
        break_ins = ThreeAddressCode(
            ThreeAddressCodeType.jp, self.pb.get_index())
        for b in self.breaks[self.scope]:
            self.pb.add_instruction_at(break_ins, b)
        self._exit_scope()

    def return_jp(self):
        filler_jp = ThreeAddressCode(ThreeAddressCodeType.jp, 0)
        self.returns[self.func_scopes[-1]
                     ].append(self.pb.add_instruction_and_increase(filler_jp))

    def save_return_value(self):
        return_val = self.stack.pop()
        assign_ins = ThreeAddressCode(
            ThreeAddressCodeType.assign, return_val, self.return_val_slot)
        self.pb.add_instruction_and_increase(assign_ins)
        self.return_jp()

    def print_func(self):
        # pops the variable and prints it
        if self.stack.top(1) == 'PRINT':
            item = self.stack.pop()
            self.stack.pop()  # pop 'PRINT'
            instr = ThreeAddressCode(ThreeAddressCodeType.print, item)
            self.pb.add_instruction_and_increase(instr)

    def assign(self):
        instr = ThreeAddressCode(ThreeAddressCodeType.assign,
                                 self.stack.pop(), self.stack.top())
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
            instr = ThreeAddressCode(
                ThreeAddressCodeType.add, base, t1, t2)
            self.pb.add_instruction_and_increase(instr)

            self.stack.push(t2)

    def relation(self):
        right = self.stack.pop()
        op_sym = self.stack.pop()
        left = self.stack.pop()

        t = self.new_temp()
        if op_sym == '<':
            instr = ThreeAddressCode(ThreeAddressCodeType.lt, left, right, t)
            self.pb.add_instruction_and_increase(instr)
        elif op_sym == '==':
            instr = ThreeAddressCode(
                ThreeAddressCodeType.eq, left, right, t)
            self.pb.add_instruction_and_increase(instr)
        else:
            raise NotImplementedError(
                f"relation op not supported: {op_sym}")
        self.stack.push(t)

    def push_num_ss(self):
        self.stack.push('#' + self.token[1])

    def start_args(self):
        self.arg_stack.clear()
    def push_arg(self):
        val = self.stack.pop()   
        self.arg_stack.append(val)

    def check_args(self):
        func_loc = self.stack.pop()

    # Pass each argument
        for idx, arg in enumerate(self.arg_stack):
            instr = ThreeAddressCode(ThreeAddressCodeType.assign, arg, f"ARG{idx}")
            self.pb.add_instruction_and_increase(instr)

        # Call function
        call_instr = ThreeAddressCode(ThreeAddressCodeType.call, func_loc)
        self.pb.add_instruction_and_increase(call_instr)

        # Push return value slot if not void
        self.stack.push(self.return_val_slot)

        # Reset arg stack for next call
        self.arg_stack.clear()

    def mult(self):
        right = self.stack.pop()
        left = self.stack.pop()
        t = self.new_temp()
        instr = ThreeAddressCode(ThreeAddressCodeType.mult, left, right, t)
        self.pb.add_instruction_and_increase(instr)
        self.stack.push(t)

    def _enter_scope(self):
        self.scope += 1
        self.breaks[self.scope] = []
        return self.scope

    def _exit_scope(self):
        del self.breaks[self.scope]
        self.symbol_table.scope_symbols[self.scope].clear()
        self.scope -= 1
        return self.scope

    def remove_last_exp_result(self):
        self.stack.pop()

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
    def new_temp(self):
        # getting new temp
        temp_addr = self.tb.alloc_memory()
        if temp_addr == -1:
            raise MemoryError("No temp space")
        return temp_addr
    # def emit(self, op_enum, o1=None, o2=None, r=None):
    #     instr = ThreeAddressCode(
    #         op_enum,
    #         self.format_token(o1),
    #         self.format_token(o2),
    #         self.format_token(r)
    #     )
    #     return instr


class ActionNames(Enum):
    PID = CodeGenerator.pid
    ADD_OR_SUB = CodeGenerator.add_or_sub
    PUSH_SS = CodeGenerator.push_ss
    DCLR_VAR = CodeGenerator.declare_var
    DCLR_ARR = CodeGenerator.declare_arr
    UPDATE_FUNC_PARAMS = CodeGenerator.update_func_params
    END_FUNC = CodeGenerator.end_func
    SAVE_PARAM_LIST = CodeGenerator.save_param_list
    SAVE_PARAM_NORM = CodeGenerator.save_param_norm
    ENTER_SCOPE = CodeGenerator._enter_scope
    EXIT_SCOPE = CodeGenerator._exit_scope
    REMOVE_LAST_EXP_RESULT = CodeGenerator.remove_last_exp_result
    SAVE_JMP_OUT_SCOPE = CodeGenerator.save_jmp_out_scope
    SAVE_IF_COND_JPF = CodeGenerator.save_if_cond_jpf
    FILL_IF_COND_JPF = CodeGenerator.fill_if_cond_jpf
    FILL_IF_COND_JPT = CodeGenerator.fill_if_cond_jpt
    LOC_WHILE_COND_BEFORE = CodeGenerator.loc_while_cond_before
    SAVE_WHILE_COND_JPF = CodeGenerator.save_while_cond_jpf
    FILL_WHILE = CodeGenerator.fill_while
    RETURN_JP = CodeGenerator.return_jp
    SAVE_RETURN_VALUE = CodeGenerator.save_return_value
    PRINT_FUNC = CodeGenerator.print_func
    ASSIGN = CodeGenerator.assign
    CALC_ARR_ADDR = CodeGenerator.calc_arr_addr
    RELATION = CodeGenerator.relation
    PUSH_NUM_SS = CodeGenerator.push_num_ss
    START_ARGS = CodeGenerator.start_args
    CHECK_ARGS = CodeGenerator.check_args
    MULT = CodeGenerator.mult
