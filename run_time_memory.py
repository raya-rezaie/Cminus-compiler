from enum import Enum

BLOCKSIZE = 4


class RunTimeMemory():
    def __init__(self, program_block, data_block, temporories):
        self.pb = program_block
        self.db = data_block
        self.temp = temporories

    def get_pb(self):
        return self.pb

    def get_db(self):
        return self.db

    def get_temp(self):
        return self.temp

    def alloc_data(self):
        return self.db.alloc_memory()

    def alloc_temp(self):
        return self.temp.alloc_memory()


class data():
    def __init__(self, lexeme, type, loc, is_func=False, attrs={}):
        self.lexeme = lexeme
        self.address = loc
        self.type = type
        self.is_func = is_func
        self.attrs = attrs


class programBlock():
    def __init__(self, base, bound):
        self.base = base
        self.bound = bound
        self.index = base
        self.block = {}

    def add_instruction_and_increase(self, instruction):
        # print("adding instruction", instruction, "and increase", self.index)
        idx = self.index
        self.block[idx] = instruction
        self.index += 1
        return idx

    def add_instruction_at(self, instruction, index):
        # print("adding instruction", instruction, "at", index)
        if self.base <= index <= self.bound:
            self.block[index] = instruction
        else:
            pass  # maybe print error

    def get_index(self):
        return self.index

    def set_index(self, index):
        # print("setting self.index from", self.index, "to", index)
        if self.base <= index <= self.bound:
            self.index = index
        else:
            pass  # maybe print error

    def to_string(self):
        result = ""
        # print(sorted(self.block))
        for key in sorted(self.block):
            result += str(key) + "\t" + self.block[key].to_string() + "\n"
        return result


class dataBlock():
    def __init__(self, base, bound=float('inf')):
        self.base = base
        self.bound = bound
        self.index = base
        self.block = []

    def alloc_memory(self):
        if self.index + BLOCKSIZE > self.bound:
            return -1  # no more space => maybe throw error
        self.block.append(None)
        self.index += BLOCKSIZE
        return self.index - BLOCKSIZE

    def _calc_array_idx(self, index):
        if index % BLOCKSIZE:
            return -1
        return (index - self.base) // BLOCKSIZE

    def get_value(self, index):
        array_idx = self._calc_array_idx(index)
        if 0 <= array_idx < len(self.block):
            return self.block[array_idx]
        return None  # invalid index => maybe throw error

    def set_value(self, index, value):
        # shouldnt the index be self.index?
        array_idx = self._calc_array_idx(index)
        if 0 <= array_idx < len(self.block):
            self.block[array_idx] = value


class ThreeAddressCodeType(Enum):
    add = "ADD"
    mult = "MULT"
    sub = "SUB"
    eq = "EQ"
    lt = "LT"
    assign = "ASSIGN"
    jpf = "JPF"
    jp = "JP"
    print = "PRINT"


class ThreeAddressCode:
    def __init__(self, rator, rand1=None, rand2=None, rand3=None):
        self.rator = rator
        self.rands = [rand1, rand2, rand3]

    def to_string(self):
        result = "("+self.rator.value
        for rand in self.rands:
            result += ","
            if rand:
                result += str(rand)
        result += ")"
        return result