from collections import defaultdict
from automata import *

class Terminal:
    def __init__(self, type, verbatim=True):
        self.type = type # of type "Token" if verbatim=false, otherwise string
        self.verbatim = verbatim # symbol and keyword tokens need to be matched verbatim, others just need to match token type
    
    def matches(self, token):
        if self.verbatim:
            return token[0] == self.type
        return token[1] == self.type


class NonTerminal:
    def __init__(self, predict = [], func = None, fa = None): #TODO: probably func something general (apply fa) since fa is passed as well
        self.predict = predict # a list of type "Terminal" (first of nonterminal + follow of nonterminal if epsilon in first)
        self.func = func
        self.fa = fa

    def set_func (self, func):
        self.func = func

    def set_fa (self, fa):
        self.fa = fa
    
    def call(self, token): #TODO: add matches check here?
        self.func(self.fa, token)
    
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

    def nextState(self, from_state, token):
        ep_next_state = None
        for transition in self.transitions[from_state]:
            to_s, tnt = transition
            if not tnt: # epsilon transition, last priority 
                ep_next_state = to_s
            elif tnt.matches(token):
                if tnt is NonTerminal:
                    tnt.call(token)
                return to_s
        return ep_next_state