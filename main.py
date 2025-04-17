from automata import *
from charreader import *
from symboltable import *
from lineinfo import *

class Token(Enum):
    NUM = "NUM"
    ID = "ID"
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"


def buildCMinusAutomata():
    # initialization and start state
    start_state = State()
    panic_alphabet = Alph().includeAllChars().exclude(('a', 'z')) \
                                                    .exclude(('A', 'Z')) \
                                                    .exclude(('0', '9')) \
                                                    .exclude((':',)).exclude((';',)).exclude(('[',']')).exclude(('(',')')).exclude(('{','}')) \
                                                    .exclude(('+',)).exclude(('-',)).exclude(('*',)).exclude(('/',)).exclude(('=',)).exclude(('<',)) \
                                                    .exclude((' ',)).exclude(('\t',)).exclude(('\n',)).exclude(('\r',)).exclude(('\f',)).exclude(('\v',))
    automata = Automata(start_state, panic_alphabet)

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

def get_next_token():
    global cminusautomata
    global reader
    states = [cminusautomata.getStartState()]
    i = 0
    token = ""
    while states:
        char = reader.read()
        if not char:
            break
        new_states = cminusautomata.nextStates(states, char)
        if not new_states:
            reader.back()
            break
        states = new_states
        token += char
        i += 1
    final_state = State.get_highest_priority_final(states)
    return final_state.type, token


def main():
    global cminusautomata
    global reader
    cminusautomata = buildCMinusAutomata()
    reader = CharReader('input.txt')
    symbol_table = SymbolTable(['break', 'else', 'if', 'int', 'while', 'return', 'void', 'main'])
    token_info = LineInfo()
    error_info = LineInfo()
    has_error = False
    line_no = 1
    while reader.read() != '':
        reader.back()
        state_type, next_token = get_next_token()
        if state_type[0] == StateType.ACCEPT:
            if next_token == '\n':
                line_no += 1
                token_info.add_counter()
                error_info.add_counter()
            if state_type[1] == Token.WHITESPACE or state_type[1] == Token.COMMENT:
                continue
            if state_type[1] == Token.ID:
                symbol_table.add_symbol(next_token)
            token_info.add_info("(" + state_type[1].value + ", " + next_token + ") ")
        elif state_type[0] == StateType.ERROR:
            has_error = True
            error_info.add_info("(" + str(next_token) + ", " + state_type[1].value + ") ")

    error_file = open('lexical_errors.txt', 'w')
    if not has_error:
        error_file.write()
    else:
        error_file.write(error_info.format_to_text())
    error_file.close()

    symbol_file = open('symbol_table.txt', 'w')
    symbol_file.write(symbol_table.format_to_text())
    symbol_file.close()

    token_file = open('tokens.txt', 'w')
    token_file.write(token_info.format_to_text())
    token_file.close()


if __name__=="__main__":
    main()