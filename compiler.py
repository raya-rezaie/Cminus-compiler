# Raya Rezaie 401170575
# Yasna Nooshiravani 401106674

from automata import *
from charreader import *
from symboltable import *
from lineinfo import *
from cminusautomata import *
from cminusparsefa import *

def get_next_token_aux():
    global cminusautomata
    global reader
    states = [cminusautomata.getStartState()]
    token = ""
    newlines = 0
    while states:
        char = reader.read()
        if not char:
            break
        new_states = cminusautomata.nextStates(states, char)
        if not new_states:
            reader.back()
            break
        if char == '\n':
            newlines += 1
        states = new_states
        token += char
    final_state = State.get_highest_priority_final(states)
    return final_state.type, token, newlines

def get_next_token():
    global reader
    global symbol_table
    global token_info
    global error_info
    global has_error
    global line_no
    if reader.read():
        reader.back()
        state_type, next_token, newlines = get_next_token_aux()
        if state_type[0] == StateType.ACCEPT:
            if state_type[1] == Token.ID:
                symbol_table.add_symbol(next_token)
            if not (state_type[1] == Token.WHITESPACE or state_type[1] == Token.COMMENT):
                token_info.add_info("(" + state_type[1].value + ", " + str(next_token) + ")")
        elif state_type[0] == StateType.ERROR:
            has_error = True
            if state_type[1] == Error.UNCLOSED_COMMENT:
                next_token = next_token[:7] + "..." # only print first seven characters of unclosed comment
            error_info.add_info("(" + next_token + ", " + state_type[1].value + ")")
        line_no += newlines
        token_info.add_counter(newlines)
        error_info.add_counter(newlines)
        if state_type[0] == StateType.ERROR or state_type[1] == Token.COMMENT or state_type[1] == Token.WHITESPACE:
            return get_next_token()
        return (state_type[1], next_token)
    else:
        return (Token.EOF, "$")

def parser():
    startNT = cminusParseFA(apply_fa)
    next_token = get_next_token()
    tree = startNT.call(next_token)
    return tree

def apply_fa(fa, token):
    current_state = fa.getStartState()
    subtrees = []
    while not current_state.is_terminal():
        current_state, tree = fa.nextState(current_state, token)
        subtrees.append(tree)
        token = get_next_token()
    return subtrees
        

def main():
    # SCANNER INITIALIZATION
    global cminusautomata
    global reader
    global symbol_table
    global token_info
    global error_info
    global has_error
    global line_no
    cminusautomata = buildCMinusAutomata()
    reader = CharReader('input.txt')
    symbol_table = SymbolTable(['break', 'else', 'if', 'int', 'while', 'return', 'void'])
    token_info = LineInfo()
    error_info = LineInfo()
    has_error = False
    line_no = 1

    tree = parser()
    print(tree)

    # SCANNER FILES
    error_file = open('lexical_errors.txt', 'w' ,  encoding='utf-8')
    if not has_error:
        error_file.write('There is no lexical error.')
    else:
        error_file.write(error_info.format_to_text())
    error_file.close()

    symbol_file = open('symbol_table.txt', 'w' ,  encoding='utf-8')
    symbol_file.write(symbol_table.format_to_text())
    symbol_file.close()

    token_file = open('tokens.txt', 'w' ,  encoding='utf-8')
    token_file.write(token_info.format_to_text())
    token_file.close()


if __name__=="__main__":
    main()