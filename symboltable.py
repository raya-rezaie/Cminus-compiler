from enum import Enum
from collections import defaultdict

class SymbolType(Enum):
    TBD = ""
    INT = "int"
    VOID = "void"
    INT_FUNC = "int func"
    VOID_FUNC = "void func"


class Symbol:
    def __init__(self, name, loc=-1, type=SymbolType.TBD, len=1):
        self.name = name
        self.loc = loc
        self.type = type
        self.len = len


class SymbolTable:
    def __init__(self, keyword_list=[]):
        # a dictionary with format "scope: list of type Symbol"
        self.scope_symbols = defaultdict(list)  # each symbol is the pair (number, symbol)
        # self.types = []  # each symbol has a type (of Type SymbolType)
        # # each symbol has a location (functions: first line no., vars: location in memory)
        # self.locs = []
        # # each symbol may have a length (functions: X, normal vars: 1, arrs: N)
        # self.lens = []

        # add keywords to symbol table
        for keyword in keyword_list:
            self.add_symbol(keyword)

    def add_symbol(self, name, type=SymbolType.TBD, loc=0, len=1, scope=-1):
        # if symbol is already in table do nothing
        if self.get_symbol(name, scope):
            return
        # otherwise add symbol to table and update counter
        self.scope_symbols[scope].append(Symbol(name, type, loc, len))

    def set_symbol_loc(self, name, loc, scope):
        if scope < -1:
            return
        scope_symbol = self.scope_symbols[scope]
        for i in range(len(scope_symbol)):
            if scope_symbol[i].name == name:
                scope_symbol[i].loc = loc
                return
        self.set_symbol_loc(name, loc, scope - 1)

    def set_symbol_type(self, name, type, scope):
        if scope < -1:
            return
        scope_symbol = self.scope_symbols[scope]
        for i in range(len(scope_symbol)):
            if scope_symbol[i].name == name:
                scope_symbol[i].type = type
                return
        self.set_symbol_type(name, type, scope - 1)

    def set_symbol_len(self, name, len, scope):
        if scope < -1:
            return
        scope_symbol = self.scope_symbols[scope]
        for i in range(len(scope_symbol)):
            if scope_symbol[i].name == name:
                scope_symbol[i].len = len
                return
        self.set_symbol_len(name, len, scope - 1)

    def get_symbol(self, name, scope):  # if symbol is not in table, None is returned
        if scope < -1:
            return None
        scope_symbol = self.scope_symbols[scope]
        for ss in scope_symbol:
            if ss.name == name:
                return ss
        return self.get_symbol(name, scope - 1)

    def get_symbol_full(self, name, scope):
        if scope < -1:
            return None
        scope_symbol = self.scope_symbols[scope]
        for i in range(len(scope_symbol)):
            if scope_symbol[i].name == name:
                return scope_symbol[i]
        return None

    def find_addr(self, name, scope):
        result = self.get_symbol_full(name, scope)
        if result:
            return result.loc
        return None

    def format_to_text(self):
        text = ""
        # for symbol in self.scope_symbols:
        #     text += str(symbol[0]) + ".\t" + symbol[1] + "\n"
        return text
