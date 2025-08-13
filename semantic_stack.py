from collections import defaultdict

class SemanticStack:
    def __init__(self):
        self.stack = []
        self.sp = 0

    def push(self, addr):
        self.stack.append(addr)
        self.sp += 1

    def pop(self, count=1):
        while count > 1:
            self.sp -= 1
            self.stack.pop()
            count -= 1
        self.sp -= 1
        return self.stack.pop()

    def is_empty(self):  # what does it return?
        if self.stack:
            return 0
        else:
            return 1

    def top(self, offset=0):
        if self.sp - offset - 1 >= 0:
            return self.stack[self.sp - offset - 1]
        return None
