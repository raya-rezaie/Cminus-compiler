from collections import defaultdict
from enum import Enum

class Error(Enum):
    INVALID_NUM = "Invalid number"
    INVALID_INPUT = "Invalid input"
    UNCLOSED_COMMENT = "Unclosed comment"
    UNMATCHED_COMMENT = "Unmatched comment"


class Token(Enum):
    NUM = "NUM"
    ID = "ID"
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"
    EOF = "EOF"


class StateType(Enum):
    DEF = 0
    ACCEPT = 1
    ERROR = 2


class State:
    def __init__(self, type=(StateType.DEF,), priority=0):
        self.type = type
        self.priority = priority # lower number = higher priority
    
    def is_terminal(self):
        return self.type[0] == StateType.ACCEPT or self.type[0] == StateType.ERROR
    
    def get_highest_priority_final(states):
        hp_final_state = None
        for state in states:
            if state.is_terminal() and (hp_final_state == None or state.priority < hp_final_state.priority):
                hp_final_state = state
        return hp_final_state


class Alph:
    def __init__(self):
        self.include_ranges = []
        self.exclude_ranges = []
        self.includes_all_chars = False
    
    def __isInRanges(self, ranges, char):
        for range in ranges:
            if range[0] <= char <= range[1]:
                return True
        return False
    
    def __addToRanges(self, ranges, range):
        if (len(range) == 1):
            range = (range[0], range[0])
        ranges.append(range)
    
    def include(self, range: tuple):
        self.__addToRanges(self.include_ranges, range)
        return self
    
    def exclude(self, range: tuple):
        self.__addToRanges(self.exclude_ranges, range)
        return self
    
    def includeAllChars(self):
        self.includes_all_chars = True
        return self
    
    # char is in alphabet if it is included and not excluded
    def isInAlph(self, char):
        return (self.includes_all_chars or self.__isInRanges(self.include_ranges, char)) and (not self.__isInRanges(self.exclude_ranges, char))


class Automata:
    def __init__(self, startState, default_panic_alph=Alph()):
        self.startState = startState
        self.default_panic_alph = default_panic_alph # if we are in any state and char is in default_panic_alph, we are transfered to default_panic_state
        self.default_panic_state = State((StateType.ERROR, Error.INVALID_INPUT), -10)
        self.transitions = defaultdict(list)
        self.states = [self.startState, self.default_panic_state]
        self.add_transition_to_panic(self.startState)
        # panic does not have a default_panic_alph transition to itself since invalid input is generated for each char in default_panic_alph

    def add_transition_to_panic (self, from_s):
        self.transitions[from_s].append((self.default_panic_state, self.default_panic_alph))

    def getStartState(self):
        return self.startState
    
    def addState(self, state, add_transition_to_panic = True):
        self.states.append(state)
        if add_transition_to_panic: # this value is set to false for the state in the middle of a comment
            self.add_transition_to_panic(state)
        return

    def addTransition(self, from_s, to_s, alph):
        self.transitions[from_s].append((to_s, alph))

    def nextStates(self, from_states, char):
        to_states = []
        for from_s in from_states:
            for transition in self.transitions[from_s]:
                if transition[1].isInAlph(char):
                    if (not transition[0] in to_states):
                        to_states.append(transition[0])
        return to_states

def format_token(token):
    if token[0] == Token.EOF:
        return "$"
    return "(" + token[0].value + ", " + token[1] + ")"