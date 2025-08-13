from enum import Enum


class SymbolType(Enum):
    TBD = "",
    INT = "int",
    VOID = "void",
    INT_FUNC = "int func",
    VOID_FUNC = "void func"


class SymbolTable:
    def __init__(self, keyword_list=[]):
        self.symbols = []  # each symbol is the pair (number, symbol)
        self.types = []  # each symbol has a type (of Type SymbolType)
        # each symbol has a location (functions: first line no., vars: location in memory)
        self.locs = []
        # each symbol may have a length (functions: X, normal vars: 1, arrs: N)
        self.lens = []

        self.counter = 1
        # add keywords to symbol table
        for keyword in keyword_list:
            self.add_symbol(keyword)

    def add_symbol(self, symbol, type=SymbolType.TBD, loc=0, len=1):
        # if symbol is already in table do nothing
        if self.get_symbol(symbol):
            return
        # otherwise add symbol to table and update counter
        self.symbols.append((self.counter, symbol))
        self.types.append(type)
        self.locs.append(loc)
        self.lens.append(len)
        self.counter += 1

    def set_symbol_loc(self, symbol, loc):
        for i in range(len(self.symbols)):
            if self.symbols[i][1] == symbol:
                self.locs[i] = loc

    def set_symbol_type(self, symbol, type):
        for i in range(len(self.symbols)):
            if self.symbols[i][1] == symbol:
                self.types[i] = type

    def set_symbol_len(self, symbol, len):
        for i in range(len(self.symbols)):
            if self.symbols[i][1] == symbol:
                self.lens[i] = len

    def get_symbol(self, symbol):  # if symbol is not in table, None is returned
        for added_sym in self.symbols:
            if symbol == added_sym[1]:
                return added_sym
        return None

    def get_symbol_full(self, symbol):
        for i in range(len(self.symbols)):
            if self.symbols[i][1] == symbol:
                return (self.symbols[i], self.types[i], self.locs[i], self.lens[i])
        return None

    def find_addr(self, symbol):
        return self.get_symbol_full(symbol)[2]

    def format_to_text(self):
        text = ""
        for symbol in self.symbols:
            text += str(symbol[0]) + ".\t" + symbol[1] + "\n"
        return text
