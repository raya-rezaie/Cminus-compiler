# Raya Rezaie 401170575
# Yasna Nooshiravani 401106674

from automata import *
from charreader import *
from symboltable import *
from lineinfo import *
from cminusautomata import *
from cminusparsefa import *
from semantic_analayzer import *
kept_token = None
global_EOF = True

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
    global scanner_error_info
    global parser_error_info
    global scanner_has_error
    global line_no
    global kept_token
    if kept_token:
        temp = kept_token
        kept_token = None
        return temp
    if reader.read():
        reader.back()
        state_type, next_token, newlines = get_next_token_aux()
        if state_type[0] == StateType.ACCEPT:
            if state_type[1] == Token.ID:
                symbol_table.add_symbol(next_token)
            if not (state_type[1] == Token.WHITESPACE or state_type[1] == Token.COMMENT):
                token_info.add_info("(" + state_type[1].value + ", " + str(next_token) + ")")
        elif state_type[0] == StateType.ERROR:
            scanner_has_error = True
            if state_type[1] == Error.UNCLOSED_COMMENT:
                next_token = next_token[:7] + "..." # only print first seven characters of unclosed comment
            scanner_error_info.add_info("(" + next_token + ", " + state_type[1].value + ")")
        line_no += newlines
        token_info.add_counter(newlines)
        scanner_error_info.add_counter(newlines)
        parser_error_info.add_counter(newlines)
        if state_type[0] == StateType.ERROR or state_type[1] == Token.COMMENT or state_type[1] == Token.WHITESPACE:
            return get_next_token()
        return (state_type[1], next_token)
    else:
        return (Token.EOF, "$")
    
def parser():
    global parser_has_error
    global parser_error_info
    
    startNT = cminusParseFA(apply_fa)
    next_token = get_next_token()
    err = startNT.handleErrorStartNT(next_token)
    is_EOF = True
    while err and is_EOF:
        if next_token[0] == Token.EOF:
            is_EOF = False
        if err == SyntaxError.ILLEGAL:
            parser_has_error = True
            if next_token[0] == Token.EOF:
                parser_error_info.add_info('Unexpected ' + token_type(next_token))
            else:
                parser_error_info.add_info('illegal ' + token_type(next_token))
            next_token = get_next_token()
            err = startNT.handleErrorStartNT(next_token)
    tree = startNT.call(next_token)
    if tree.children[-1].value != "$" and not parser_has_error:
        tree.children.append(Tree("$"))
    return tree

def keep_token(token):
    global kept_token
    kept_token = token

def apply_fa(fa, token):
    global parser_has_error
    global global_EOF
    current_state = fa.getStartState()
    subtrees = []
    EOF = True
    while global_EOF:
        if (token[0] == Token.EOF):
            EOF = False
        next_state, tree = fa.nextState(current_state, token)
        if isinstance(next_state, SyntaxError): # error handling
            if next_state == SyntaxError.MISSINGT or next_state == SyntaxError.MISSINGNT:
                if str(tree[1]) == "EOF":
                    EOF = False
                    subtrees.append(Tree("$"))
                else:
                    parser_has_error = True
                    parser_error_info.add_info('missing ' + str(tree[1]))
                keep_token(token)
                current_state = tree[0]
            elif next_state == SyntaxError.ILLEGAL:
                if token[0] == Token.EOF:
                    parser_has_error = True
                    parser_error_info.add_info('Unexpected ' + token_type(token))
                else:
                    parser_has_error = True
                    parser_error_info.add_info('illegal ' + token_type(token))
        else:
            if tree == 23:
                pass # executed action symbol
            elif tree:
                subtrees.append(tree)
            else:
                subtrees.append(Tree("epsilon"))

            if not tree:
                keep_token(token)
            current_state = next_state
        if current_state.is_terminal():
            break
        token = get_next_token()
        global_EOF = global_EOF and EOF
    return subtrees
        

def main():
    # SCANNER INITIALIZATION
    global cminusautomata
    global reader
    global symbol_table
    global token_info
    global scanner_error_info
    global parser_error_info
    global scanner_has_error
    global parser_has_error
    global line_no
    cminusautomata = buildCMinusAutomata()
    reader = CharReader('input.txt')
    symbol_table = SymbolTable(['break', 'else', 'if', 'int', 'while', 'return', 'void'])
    token_info = LineInfo()
    scanner_error_info = LineInfo()
    scanner_has_error = False
    parser_error_info = LineInfo()
    parser_has_error = False
    line_no = 1

    tree = parser()

    # SCANNER FILES
    scanner_error_file = open('lexical_errors.txt', 'w',  encoding='utf-8')
    if not scanner_has_error:
        scanner_error_file.write('There is no lexical error.')
    else:
        scanner_error_file.write(scanner_error_info.format_to_text())
    scanner_error_file.close()

    symbol_file = open('symbol_table.txt', 'w',  encoding='utf-8')
    symbol_file.write(symbol_table.format_to_text())
    symbol_file.close()

    token_file = open('tokens.txt', 'w',  encoding='utf-8')
    token_file.write(token_info.format_to_text())
    token_file.close()

    # PARSER FILES
    token_file = open('parse_tree.txt', 'w',  encoding='utf-8')
    token_file.write(str(tree))
    token_file.close()
    
    parser_error_file = open('syntax_errors.txt', 'w', encoding='utf-8')
    if not parser_has_error:
        parser_error_file.write('There is no syntax error.')
    else:
        parser_error_file.write(parser_error_info.format_to_text2())
    parser_error_file.close()


if __name__=="__main__":
    main()