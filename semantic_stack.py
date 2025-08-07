from collections import defaultdict
class SemantciStack:
    def __init__(self):
        self.stack = []
        self.sp = 0
    def push(self,addr):
        self.stack.append(addr)
        self.sp += 1
    def pop(self , count):
        outputs = []
        while count > 1:
            self.sp -= 1
            self.stack.pop()
            count -= 1
        self.sp -= 1
        return self.stack.pop()
    def is_empty(self):
        if self.stack:
            return 0
        else:
            return 1
    def top(self):
        
    
            