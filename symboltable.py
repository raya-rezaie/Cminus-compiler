class SymbolTable:
    def __init__(self, keyword_list=[]):
        self.symbols = [] # each symbol is the pair (number, symbol)
        self.counter = 1
        # add keywords to symbol table
        for keyword in keyword_list:
            self.add_symbol(keyword)

    def add_symbol(self, symbol):
        # if symbol is already in table do nothing
        if self.get_symbol(symbol):
            return
        # otherwise add symbol to table and update counter
        self.symbols.append((self.counter, symbol))
        self.counter += 1
    
    def get_symbol(self, symbol): # if symbol is not in table, None is returned
        for added_sym in self.symbols:
            if symbol == added_sym[1]:
                return added_sym
        return None
    
    def format_to_text(self):
        text = ""
        for symbol in self.symbols:
            text += symbol[0] + ".\t" + symbol[1] + "\n"
        return text