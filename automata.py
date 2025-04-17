from collections import defaultdict
from enum import Enum

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
    
    def includeAllChars(self, range: tuple):
        self.include((chr(0), chr(127)))
        return self
    
    # char is in alphabet if it is included and not excluded
    def isInAlph(self, char):
        return self.__isInRanges(self.include_ranges, char) and not self.__isInRanges(self.exclude_ranges, char)


class Automata:
    def __init__(self, startState):
        self.startState = startState
        self.states = [startState]
        self.transitions = defaultdict(list)

    def getStartState(self):
        return self.startState
    
    def addState(self, state):
        self.states.append(state)
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
