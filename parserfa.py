from collections import defaultdict
from automata import *

class Terminal:
    def __init__(self, type, verbatim=True):
        self.type = type # of type "Token" if verbatim=false, otherwise string
        self.verbatim = verbatim # symbol and keyword tokens need to be matched verbatim, others just need to match token type
    
    def matches(self, token):
        if not self.verbatim:
            return token[0] == self.type
        return token[1] == self.type


class NonTerminal:
    def __init__(self, predict = [], func = None, name = "", fa = None): #TODO: probably func something general (apply fa) since fa is passed as well
        self.predict = predict # a list of type "Terminal" (first of nonterminal + follow of nonterminal if epsilon in first)
        self.func = func
        self.name = name
        self.fa = fa

    def __str__(self):
        return self.name

    def set_func (self, func):
        self.func = func

    def set_fa (self, fa):
        self.fa = fa
    
    def call(self, token): #TODO: add matches check here?, returns a tree with root=nonterminal
        if self.matches(token):
            return Tree(str(self), self.func(self.fa, token))
        return None
    
    def matches(self, token):
        for p in self.predict:
            if p.matches(token):
                return True
        return False


class ParserFA:
    def __init__(self, startState):
        self.startState = startState
        self.transitions = defaultdict(list)
        self.states = [self.startState]
    
    def getStartState(self):
        return self.startState
    
    def addState(self, state):
        self.states.append(state)

    def addTransition(self, from_s, to_s, tnt):
        self.transitions[from_s].append((to_s, tnt)) # tnt == None represents epsilon

    def nextState(self, from_state, token): # returns (next state, produced parse tree)
        ep_next_state = None
        for transition in self.transitions[from_state]:
            to_s, tnt = transition
            if not tnt: # epsilon transition, last priority 
                ep_next_state = to_s
            elif tnt.matches(token):
                if isinstance(tnt, NonTerminal):
                    return (to_s, tnt.call(token))
                return (to_s, Tree(format_token(token)))
        return (ep_next_state, None)
    

class Tree:
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children # each child is a tree itself

    def __str__(self):
        return self.str_aux("", True, True)
        
    def str_aux(self, tab, last, first):
        res = tab + ("└── " if last else "├── ") + self.value + "\n"
        if first:
            res = self.value + "\n"
        i = 0
        while i < len(self.children):
            child = self.children[i]
            res += child.str_aux((tab if first else (tab + ("    " if last else "│   "))), i == (len(self.children) - 1), False)
            i += 1
        return res