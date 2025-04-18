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
                                                .exclude((':',)).exclude((';',)).exclude(('[',']')).exclude(('(',')')).exclude(('{','}')).exclude(',',) \
                                                .exclude(('+',)).exclude(('-',)).exclude(('*',)).exclude(('/',)).exclude(('=',)).exclude(('<',)) \
                                                .exclude((' ',)).exclude(('\t',)).exclude(('\n',)).exclude(('\r',)).exclude(('\f',)).exclude(('\v',))
    alph_invalid_num = Alph().includeAllChars().exclude(('0', '9')) \
                                                .exclude((':',)).exclude((';',)).exclude(('[',']')).exclude(('(',')')).exclude(('{','}')).exclude((',',)) \
                                                .exclude(('+',)).exclude(('-',)).exclude(('*',)).exclude(('/',)).exclude(('=',)).exclude(('<',)) \
                                                .exclude((' ',)).exclude(('\t',)).exclude(('\n',)).exclude(('\r',)).exclude(('\f',)).exclude(('\v',))
    automata = Automata(start_state, panic_alphabet)

    alph_v = Alph().include(('v' , 'v'))
    alph_o = Alph().include(('o' , 'o'))
    alph_d = Alph().include(('d' , 'd'))
    alph_i = Alph().include(('i', 'i'))
    alph_f = Alph().include(('f' , 'f'))
    alph_e = Alph().include(('e' , 'e'))
    alph_l = Alph().include(('l' , 'l'))
    alph_s = Alph().include(('s' , 's'))
    alph_n = Alph().include(('n' , 'n'))
    alph_t = Alph().include(('t' , 't'))
    alph_h = Alph().include(('h' , 'h'))
    alph_w = Alph().include(('w' , 'w'))
    alph_b = Alph().include(('b' , 'b'))
    alph_r = Alph().include(('r' , 'r'))
    alph_a = Alph().include(('a' , 'a'))
    alph_k = Alph().include(('k' , 'k'))
    alph_u = Alph().include(('u' , 'u'))
    alph_white = Alph().include((' ',)).include(('\n',)).include(('\t',)).include(('\r',)).include(('\v',)).include(('\f',))
    # alph_white = Alph().include((' ' , ' ')).include(('\t' , '\r'))
    alph_semicolon = Alph().include((';' , ';'))
    alph_colon = Alph().include((':' , ':'))
    alph_equal = Alph().include(('=' , '='))
    alph_bracket1 = Alph().include(('[' , '['))
    alph_bracket2 = Alph().include((']' , ']'))
    alph_paranth1 = Alph().include(('(' , '('))
    alph_paranth2= Alph().include((')' , ')'))
    alph_aqulad1 = Alph().include(('{' , '{'))
    alph_aqulad2 = Alph().include(('}' , '}'))
    alph_plus = Alph().include(('+' , '+'))
    alph_minus = Alph().include(('-' , '-'))
    alph_star = Alph().include(('*' , '*'))    
    alph_less = Alph().include(('<' , '<'))
    alph_comma = Alph().include((',' , ','))
    alph_eng = Alph().include(('a', 'z')).include(('A', 'Z'))
    alph09 = Alph().include(('0', '9'))
    alph_slash = Alph().include(( '/' , '/' ))
    comment_alphabet = Alph().includeAllChars().exclude(('*' , '*'))
    comment_alphabet2 = Alph().includeAllChars().exclude(('/', '/'))

    # numbers
    num_state = State((StateType.ACCEPT, Token.NUM))
    automata.addState(num_state)
    err_invalid_num_state = State((StateType.ERROR, Error.INVALID_NUM))
    automata.addState(err_invalid_num_state, False) #TODO: change if 234d! is not (234d, invalid number) (!, invalid input)

    automata.addTransition(start_state, num_state, alph09)
    automata.addTransition(num_state, num_state, alph09)
    automata.addTransition(num_state, err_invalid_num_state, alph_invalid_num)

    #if
    if0_state = State((StateType.DEF,))
    automata.addState(if0_state)  
    if1_state = State((StateType.ACCEPT , Token.KEYWORD) , -1)
    automata.addState(if1_state)
    
    automata.addTransition(start_state,if0_state , alph_i)
    automata.addTransition(if0_state ,if1_state , alph_f)

    #else
    else0_state = State((StateType.DEF,))
    else1_state = State((StateType.DEF,))
    else2_state = State((StateType.DEF,))
    else3_state = State((StateType.ACCEPT , Token.KEYWORD) , -1)
    automata.addState(else0_state)
    automata.addState(else1_state)
    automata.addState(else2_state)
    automata.addState(else3_state)

    automata.addTransition(start_state , else0_state , alph_e)
    automata.addTransition(else0_state , else1_state , alph_l)
    automata.addTransition(else1_state , else2_state , alph_s)
    automata.addTransition(else2_state , else3_state , alph_e)

    #int
    int0_state = State((StateType.DEF,))
    int1_state = State((StateType.DEF,))
    int2_state = State((StateType.ACCEPT , Token.KEYWORD) , -1)

    automata.addTransition(start_state , int0_state , alph_i)
    automata.addTransition(int0_state , int1_state , alph_n)
    automata.addTransition(int1_state , int2_state , alph_t)

    #void
    void0_state = State((StateType.DEF,))
    void1_state = State((StateType.DEF,))
    void2_state = State((StateType.DEF,))
    void3_state = State((StateType.ACCEPT , Token.KEYWORD) , -1)
    automata.addState(void0_state)
    automata.addState(void1_state)
    automata.addState(void2_state)
    automata.addState(void3_state)
    automata.addTransition(start_state , void0_state , alph_v)
    automata.addTransition(void0_state , void1_state , alph_o)
    automata.addTransition(void1_state , void2_state , alph_i)
    automata.addTransition(void2_state , void3_state , alph_d)

    #while
    while0_state = State((StateType.DEF,))
    while1_state = State((StateType.DEF,))
    while2_state = State((StateType.DEF,))
    while3_state = State((StateType.DEF,))
    while4_state = State((StateType.ACCEPT , Token.KEYWORD) , -1)
    automata.addState(while0_state)
    automata.addState(while1_state)
    automata.addState(while2_state)
    automata.addState(while3_state)
    automata.addState(while4_state)
    automata.addTransition(start_state , while0_state , alph_w)
    automata.addTransition(while0_state , while1_state , alph_h)
    automata.addTransition(while1_state , while2_state , alph_i)
    automata.addTransition(while2_state , while3_state , alph_l)
    automata.addTransition(while3_state , while4_state , alph_e)

    #break
    break0_state = State((StateType.DEF,))
    break1_state = State((StateType.DEF,))
    break2_state = State((StateType.DEF,))
    break3_state = State((StateType.DEF,))
    break4_state = State((StateType.ACCEPT , Token.KEYWORD) , -1)
    automata.addState(break0_state)
    automata.addState(break1_state)
    automata.addState(break2_state)
    automata.addState(break3_state)
    automata.addState(break4_state)
    automata.addTransition(start_state , break0_state , alph_b)
    automata.addTransition(break0_state , break1_state , alph_r)
    automata.addTransition(break1_state , break2_state , alph_e)
    automata.addTransition(break2_state , break3_state , alph_a)
    automata.addTransition(break3_state , break4_state ,  alph_k)

    #return 
    return0_state = State((StateType.DEF,))
    return1_state = State((StateType.DEF,))
    return2_state = State((StateType.DEF,))
    return3_state = State((StateType.DEF,))
    return4_state = State((StateType.DEF,))
    return5_state = State((StateType.ACCEPT , Token.KEYWORD) ,-1)
    automata.addState(return0_state)
    automata.addState(return1_state)
    automata.addState(return2_state)
    automata.addState(return3_state)
    automata.addState(return4_state)
    automata.addState(return5_state)
    automata.addTransition(start_state , return0_state , alph_r)
    automata.addTransition(return0_state , return1_state , alph_e)
    automata.addTransition(return1_state , return2_state , alph_t)
    automata.addTransition(return2_state , return3_state , alph_u)
    automata.addTransition(return3_state , return4_state , alph_r)
    automata.addTransition(return4_state , return5_state , alph_n)

    #whitespace
    whiteSpace0_state = State((StateType.ACCEPT , Token.WHITESPACE))
    automata.addState(whiteSpace0_state, False)
    automata.addTransition(start_state , whiteSpace0_state , alph_white)

    #automata.addTransition(whiteSpace0_state , start_state , new_token_alphabet)
    #= & ==
    equal0_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(equal0_state)
    equal1_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(equal1_state, False)
    automata.addTransition(start_state , equal0_state , alph_equal)
    automata.addTransition(equal0_state , equal1_state , alph_equal)

    #semicolon
    semicolon_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(semicolon_state, False)
    automata.addTransition(start_state , semicolon_state , alph_semicolon)

    #colon
    colon_state =  State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(colon_state, False)
    automata.addTransition(start_state , colon_state , alph_colon)

    #comma 
    comma_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(comma_state, False)
    automata.addTransition(start_state , comma_state , alph_comma)

    #[
    bracket1_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(bracket1_state, False)
    automata.addTransition(start_state , bracket1_state  , alph_bracket1)

    #]
    bracket2_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(bracket2_state, False)
    automata.addTransition(start_state , bracket2_state , alph_bracket2)

    #{
    aqulad1_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(aqulad1_state, False)
    automata.addTransition(start_state , aqulad1_state, alph_aqulad1)

    #}
    aqulad2_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(aqulad2_state, False)
    automata.addTransition(start_state , aqulad2_state, alph_aqulad2)

    # +
    plus_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(plus_state, False)
    automata.addTransition(start_state , plus_state , alph_plus)

    # -
    minus_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(minus_state, False)
    automata.addTransition(start_state , minus_state , alph_minus)

    # <
    less_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(less_state, False)
    automata.addTransition(start_state , less_state , alph_less)

    # *
    star_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(star_state)
    automata.addTransition(start_state , star_state , alph_star)

    # ( 
    paranth_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(paranth_state, False)
    automata.addTransition(start_state , paranth_state , alph_paranth1)

    # )
    paranth2_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(paranth2_state, False)
    automata.addTransition(start_state , paranth2_state , alph_paranth2)

    # / and comment
    slash_state = State((StateType.ACCEPT , Token.SYMBOL))
    automata.addState(slash_state)
    comment0_state = State((StateType.ERROR , Error.UNCLOSED_COMMENT), -1)
    automata.addState(comment0_state, False)
    comment1_state = State((StateType.ERROR , Error.UNCLOSED_COMMENT), -1)
    automata.addState(comment1_state, False)
    comment2_state = State((StateType.ACCEPT , Token.COMMENT) , -2)
    automata.addState(comment2_state, False)
    automata.addTransition(start_state , slash_state , alph_slash)
    automata.addTransition(slash_state , comment0_state ,  alph_star)
    automata.addTransition(comment0_state , comment1_state , alph_star)
    automata.addTransition(comment0_state , comment0_state , comment_alphabet)
    automata.addTransition(comment1_state , comment0_state , comment_alphabet2)
    automata.addTransition(comment1_state , comment2_state , alph_slash)
    # unmatched 
    unmatched_comment_state = State((StateType.ERROR , Error.UNMATCHED_COMMENT))
    automata.addState(unmatched_comment_state)
    automata.addTransition(star_state , unmatched_comment_state , alph_slash)

    # ID
    ID_state = State((StateType.ACCEPT , Token.ID))
    automata.addState(ID_state)
    automata.addTransition(start_state , ID_state , alph_eng)
    automata.addTransition(ID_state , ID_state , alph09)
    automata.addTransition(ID_state , ID_state , alph_eng)

    return automata


def get_next_token():
    global cminusautomata
    global reader
    states = [cminusautomata.getStartState()]
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
    final_state = State.get_highest_priority_final(states)
    return final_state.type, token


def main():
    global cminusautomata
    global reader
    cminusautomata = buildCMinusAutomata()
    reader = CharReader('input.txt')
    symbol_table = SymbolTable(['break', 'else', 'if', 'int', 'while', 'return', 'void'])
    token_info = LineInfo()
    error_info = LineInfo()
    has_error = False
    line_no = 1
    while reader.read():
        reader.back()
        state_type, next_token = get_next_token()
        if state_type[0] == StateType.ACCEPT:
            if next_token == '\n':
                line_no += 1
                token_info.add_counter(1)
                error_info.add_counter(1)
            if state_type[1] == Token.WHITESPACE or state_type[1] == Token.COMMENT:
                continue
            if state_type[1] == Token.ID:
                symbol_table.add_symbol(next_token)
            token_info.add_info("(" + state_type[1].value + ", " + next_token + ")")
        elif state_type[0] == StateType.ERROR:
            has_error = True
            error_info.add_info("(" + str(next_token) + ", " + state_type[1].value + ")")

    error_file = open('lexical_errors.txt', 'w')
    if not has_error:
        error_file.write('There is no lexical error.')
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