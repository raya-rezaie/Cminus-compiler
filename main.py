from automata import *

class Error(Enum):
    INVALID_NUM = 0

class Token(Enum):
    NUM = 0

def buildCMinusAutomata():
    # initialization and start state
    start_state = State()
    automata = Automata(start_state)

    # numbers
    num_state = State((StateType.ACCEPT, Token.NUM))
    automata.addState(num_state)
    err_invalid_num_state = State((StateType.ERROR, Error.INVALID_NUM))
    automata.addState(err_invalid_num_state)
    alph09 = Alph().include(('0', '9'))
    automata.addTransition(start_state, num_state, alph09)
    automata.addTransition(num_state, num_state, alph09)
    alph_eng = Alph().include(('a', 'z')).include(('A', 'Z'))
    automata.addTransition(num_state, err_invalid_num_state, alph_eng)
    return automata

# test
automata = buildCMinusAutomata()
print(automata.nextStates(automata.nextStates([automata.getStartState()], 'a'), '4'))