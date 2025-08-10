from collections import defaultdict
from automata import *
from code_gen import *
class SyntaxError(Enum):
    ILLEGAL = 0
    MISSINGNT = 1
    MISSINGT = 2

class Terminal:
    def __init__(self, type, verbatim=True):
        self.type = type # of type "Token" if verbatim=false, otherwise string
        self.verbatim = verbatim # symbol and keyword tokens need to be matched verbatim, others just need to match token type

    def __str__(self):
        if self.verbatim:
            return self.type
        return self.type.value
    
    def matches(self, token):
        if not self.verbatim:
            return token[0] == self.type
        return token[1] == self.type


class NonTerminal:
    def __init__(self, predict = [], follow = [], func = None, name = "", fa = None): #TODO: probably func something general (apply fa) since fa is passed as well
        self.predict = predict # a list of type "Terminal" (first of nonterminal + follow of nonterminal if epsilon in first)
        self.follow = follow
        self.func = func
        self.name = name
        self.fa = fa

    def __str__(self):
        return self.name

    def set_func (self, func):
        self.func = func

    def set_fa (self, fa):
        self.fa = fa
    
    def call(self, token): # returns a tree with root=nonterminal
        return Tree(str(self), self.func(self.fa, token))
    
    def matches(self, token):
        for p in self.predict:
            if p.matches(token):
                return True
        return False
    
    def handleErrorStartNT(self, token):
        for p in self.predict:
            if p.matches(token):
                return None
        for f in self.follow:
            if f.matches(token):
                return SyntaxError.MISSINGNT
        return SyntaxError.ILLEGAL


class ParserFA:
    def __init__(self, startState, nt, semantic_actions):
        self.startState = startState
        self.transitions = defaultdict(list)
        self.states = [self.startState]
        self.nt = nt
        self.semantic_actions = semantic_actions
        nt.set_fa(self)
    
    def getStartState(self):
        return self.startState

    def addState(self, state):
        self.states.append(state)

        
  #   def getAction(self, state):
  #      for i in range(len(self.states)):
  #          if state == self.states[i]:
  #              return self.actions[i]
  #      return None

    def addTransition(self, from_s, to_s, tnt):
        self.transitions[from_s].append((to_s, tnt)) # tnt == None represents epsilon

    def nextState(self, from_state, token): # returns (next state, produced parse tree)
        ep_next_state = None
        for transition in self.transitions[from_state]:
            to_s, tnt = transition
            if not tnt: # epsilon transition, last priority 
                ep_next_state = to_s
            elif isinstance(tnt, actionNames):
                if to_s.is_terminal():
                    self.semantic_actions.exec_func(tnt, token)
                else:
                    _, next_transition_tnt = self.transitions[to_s][0]
                    if next_transition_tnt.matches(token):
                        self.semantic_actions.exec_func(tnt, token)
                    else:
                        continue
                return (to_s, 23)
            elif tnt.matches(token):
                # action = SemanticAction(before_action , token)
                # action.get_func_by_name()
                if isinstance(tnt, NonTerminal):
                    return (to_s, tnt.call(token))
                    # temp = tnt.call(token) 
                # else:
                return (to_s, Tree(format_token(token)))
                # action = SemanticAction(after_action , token)
                # action.get_func_by_name()
                # return (to_s,temp)
        if ep_next_state:
            return (ep_next_state, None)
        
        # syntax error if reached here
        link = self.transitions[from_state][0]
        if isinstance(link[1], Terminal):
            return (SyntaxError.MISSINGT, link)
        for f in link[1].follow:
            if f.matches(token):
                return (SyntaxError.MISSINGNT, link) # token in follow (self.nt)
        return (SyntaxError.ILLEGAL, link) # token not in follow (self.nt)



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