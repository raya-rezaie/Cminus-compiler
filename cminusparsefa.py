from parserfa import *

def cminusParseFA(apply_fa):
    #TODO: build fa based on rules, firsts, and follows, return nonterminal "Program"
    # TERMINALS
    ID = Terminal(Token.ID, False)
    NUM = Terminal(Token.NUM, False)
    EOF = Terminal(Token.EOF, False)

    SEMICOLON = Terminal(";")
    COLON = Terminal(":")
    COMMA = Terminal(",")
    OPENBRACKET = Terminal("[")
    CLOSEBRACKET = Terminal("]")
    OPENPAR = Terminal("(")
    CLOSEPAR = Terminal(")")
    OPENCURLY = Terminal("{")
    CLOSECURLY = Terminal("}")
    LESS = Terminal("<")
    DOUBLEEQUAL = Terminal("==")
    PLUS = Terminal("+")
    MINUS = Terminal("-")
    MULT = Terminal("*")
    EQUAL = Terminal("=")
    IF = Terminal("if")
    ELSE = Terminal("else")
    VOID = Terminal("void")
    INT = Terminal("int")
    WHILE = Terminal("while")
    BREAK = Terminal("break")
    RETURN = Terminal("return")

    # NONTERMINALS
    program = NonTerminal([INT, VOID, EOF], 
                          [], apply_fa, "Program")
    declaration_list = NonTerminal([INT, VOID, ID, SEMICOLON, NUM, OPENPAR, OPENCURLY, CLOSECURLY, BREAK, IF, WHILE, RETURN, PLUS, MINUS, EOF],
                                   [ID, SEMICOLON, NUM, OPENPAR, OPENCURLY, CLOSECURLY, BREAK, IF, WHILE, RETURN, PLUS, MINUS, EOF], apply_fa, "DeclarationList")
    declaration = NonTerminal([INT, VOID], 
                              [ID, SEMICOLON, NUM, OPENPAR, INT, VOID, OPENCURLY, CLOSECURLY, BREAK, IF, WHILE, RETURN, PLUS, MINUS, EOF], apply_fa, "Declaration")
    declaration_initial = NonTerminal([INT, VOID], 
                                      [SEMICOLON, OPENBRACKET, OPENPAR, CLOSEPAR, COMMA], apply_fa, "DeclarationInitial")
    declaration_prime = NonTerminal([SEMICOLON, OPENBRACKET, OPENPAR], 
                                    [ID, SEMICOLON, NUM, OPENPAR, INT, VOID, OPENCURLY, CLOSECURLY, BREAK, IF, WHILE, RETURN, PLUS, MINUS, EOF], apply_fa, "DeclarationPrime")
    var_declaration_prime = NonTerminal([SEMICOLON, OPENBRACKET],
                                        [ID, SEMICOLON, NUM, OPENPAR, INT, VOID, OPENCURLY, CLOSECURLY, BREAK, IF, WHILE, RETURN, PLUS, MINUS, EOF], apply_fa, "VarDeclarationPrime")
    fun_declaration_prime = NonTerminal([OPENPAR],
                                        [ID, SEMICOLON, NUM, OPENPAR, INT, VOID, OPENCURLY, CLOSECURLY, BREAK, IF, WHILE, RETURN, PLUS, MINUS, EOF], apply_fa, "FunDeclarationPrime")
    type_specifier = NonTerminal([INT, VOID],
                                 [ID], apply_fa, "TypeSpecifier")
    params = NonTerminal([INT, VOID],
                         [CLOSEPAR], apply_fa, "Params")
    param_list = NonTerminal([COMMA,CLOSEPAR],
                             [CLOSEPAR], apply_fa, "ParamList")
    param = NonTerminal([INT, VOID],
                        [CLOSEPAR, COMMA],apply_fa, "Param")
    param_prime = NonTerminal([OPENBRACKET, CLOSEPAR, COMMA],
                              [CLOSEPAR, COMMA], apply_fa, "ParamPrime")
    compound_stmt = NonTerminal([OPENCURLY],
                                [ID, SEMICOLON, NUM, OPENPAR, INT, VOID, OPENCURLY, CLOSECURLY, BREAK, IF, ELSE, WHILE, RETURN, PLUS, MINUS, EOF], apply_fa, "CompoundStmt")
    statement_list = NonTerminal([ID, SEMICOLON, NUM, OPENPAR, OPENCURLY, BREAK, IF, WHILE, RETURN, PLUS, MINUS, CLOSECURLY],
                                 [CLOSECURLY], apply_fa, "StatementList")
    statement = NonTerminal([ID, SEMICOLON, NUM, OPENPAR, OPENCURLY, BREAK, IF, WHILE, RETURN, PLUS, MINUS],
                            [ID, SEMICOLON, NUM, OPENPAR, OPENCURLY, CLOSECURLY, BREAK, IF, ELSE, WHILE, RETURN, PLUS, MINUS, EOF], apply_fa, "Statement")
    expression_stmt = NonTerminal([ID, SEMICOLON, NUM, OPENPAR, BREAK, PLUS, MINUS],
                                  [ID, SEMICOLON, NUM, OPENPAR, OPENCURLY, CLOSECURLY, BREAK, IF, ELSE, WHILE, RETURN, PLUS, MINUS, EOF], apply_fa, "ExpressionStmt")
    selection_stmt = NonTerminal([IF],
                                 [ID, SEMICOLON, NUM, OPENPAR, OPENCURLY, CLOSECURLY, BREAK, IF, ELSE, WHILE, RETURN, PLUS, MINUS, EOF], apply_fa, "SelectionStmt")
    iteration_stmt = NonTerminal([WHILE],
                                 [ID, SEMICOLON, NUM, OPENPAR, OPENCURLY, CLOSECURLY, BREAK, IF, ELSE, WHILE, RETURN, PLUS, MINUS, EOF], apply_fa, "IterationStmt")
    return_stmt = NonTerminal([RETURN],
                              [ID, SEMICOLON, NUM, OPENPAR, OPENCURLY, CLOSECURLY, BREAK, IF, ELSE, WHILE, RETURN, PLUS, MINUS, EOF], apply_fa, "ReturnStmt")
    return_stmt_prime = NonTerminal([ID, SEMICOLON, NUM, OPENPAR, PLUS, MINUS],
                                    [ID, SEMICOLON, NUM, OPENPAR, OPENCURLY, CLOSECURLY, BREAK, IF, ELSE, WHILE, RETURN, PLUS, MINUS, EOF], apply_fa, "ReturnStmtPrime")
    expression = NonTerminal([ID, NUM, OPENPAR, PLUS, MINUS],
                             [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA], apply_fa, "Expression")
    b = NonTerminal([OPENBRACKET, OPENPAR, EQUAL, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA],
                    [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA], apply_fa, "B")
    h = NonTerminal([EQUAL, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA],
                    [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA], apply_fa, "H")
    simple_expression_zegond = NonTerminal([NUM, OPENPAR, PLUS, MINUS],
                                           [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA], apply_fa, "SimpleExpressionZegond")
    simple_expression_prime = NonTerminal([OPENPAR, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA],
                                          [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA], apply_fa, "SimpleExpressionPrime")
    c = NonTerminal([LESS, DOUBLEEQUAL, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA],
                    [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA], apply_fa, "C")
    relop = NonTerminal([LESS, DOUBLEEQUAL],
                        [ID, NUM, OPENPAR, PLUS, MINUS], apply_fa, "Relop")
    additive_expression = NonTerminal([ID, NUM, OPENPAR, PLUS, MINUS],
                                      [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA], apply_fa, "AdditiveExpression")
    additive_expression_prime = NonTerminal([OPENPAR, PLUS, MINUS, MULT, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL],
                                            [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL], apply_fa, "AdditiveExpressionPrime")
    additive_expression_zegond = NonTerminal([NUM, OPENPAR, PLUS, MINUS],
                                             [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL], apply_fa, "AdditiveExpressionZegond")
    d = NonTerminal([PLUS, MINUS, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL],
                    [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL], apply_fa, "D")
    addop = NonTerminal([PLUS, MINUS],
                        [ID, NUM, OPENPAR, PLUS, MINUS], apply_fa, "Addop")
    term = NonTerminal([ID, NUM, OPENPAR, PLUS, MINUS],
                       [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS], apply_fa, "Term")
    term_prime = NonTerminal([OPENPAR, MULT, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS],
                             [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS], apply_fa, "TermPrime")
    term_zegond = NonTerminal([NUM, OPENPAR, PLUS, MINUS],
                              [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS], apply_fa, "TermZegond")
    g = NonTerminal([MULT, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS],
                    [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS], apply_fa, "G")
    signed_factor = NonTerminal([ID,NUM, OPENPAR, PLUS, MINUS],
                                [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT], apply_fa, "SignedFactor")
    signed_factor_prime = NonTerminal([OPENPAR, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT],
                                      [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT], apply_fa, "SignedFactorPrime")
    signed_factor_zegond = NonTerminal([NUM, OPENPAR, PLUS, MINUS],
                                       [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT], apply_fa, "SignedFactorZegond")
    factor = NonTerminal([ID, NUM, OPENPAR],
                         [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT], apply_fa, "Factor")
    var_call_prime = NonTerminal([OPENBRACKET, OPENPAR, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT],
                                 [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT], apply_fa, "VarCallPrime")
    var_prime = NonTerminal([OPENBRACKET, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT],
                            [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT], apply_fa, "VarPrime")
    factor_prime = NonTerminal([OPENPAR, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT],
                               [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT], apply_fa, "FactorPrime")
    factor_zegond = NonTerminal([NUM, OPENPAR],
                                [SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT], apply_fa, "FactorZegond")
    args = NonTerminal([ID, NUM, OPENPAR, PLUS, MINUS, CLOSEPAR],
                       [CLOSEPAR], apply_fa, "Args")
    arg_list = NonTerminal([ID, NUM,OPENPAR, PLUS, MINUS],
                           [CLOSEPAR], apply_fa, "ArgList")
    arg_list_prime = NonTerminal([COMMA, CLOSEPAR],
                                 [CLOSEPAR], apply_fa, "ArgListPrime")

    # 1. PROGRAM
    create_fa([[declaration_list, EOF]], program)

    # 2. DECLARATION LIST
    create_fa([[declaration, declaration_list], [None]], declaration_list)

    # 3. DECLARATION
    create_fa([[declaration_initial, declaration_prime]], declaration)

    # 4. DECLARATION INITIAL
    create_fa([[type_specifier, ID]], declaration_initial)

    # 5. DECLARATION PRIME
    create_fa([[fun_declaration_prime], [var_declaration_prime]], declaration_prime)

    # 6. VAR DECLARATION PRIME
    create_fa([[SEMICOLON], [OPENBRACKET, NUM, CLOSEBRACKET, SEMICOLON]], var_declaration_prime)

    # 7. FUN DECLARATION PRIME
    create_fa([[OPENPAR, params, CLOSEPAR, compound_stmt]], fun_declaration_prime)

    # 8. TYPE SPECIFIER
    create_fa([[INT], [VOID]], type_specifier)

    # 9. PARAMS
    create_fa([[INT, ID, param_prime, param_list], [VOID]], params)

    # 10. PARAM LIST
    create_fa([[COMMA, param, param_list], [None]], param_list)

    # 11. PARAM
    create_fa([[declaration_initial, param_prime]], param)

    # 12. PARAM PRIME
    create_fa([[OPENBRACKET, CLOSEBRACKET], [None]], param_prime)

    # 13. COMPOUND STMT
    create_fa([[OPENCURLY, declaration_list, statement_list, CLOSECURLY]], compound_stmt)

    # 14. STATEMENT LIST
    create_fa([[statement, statement_list], [None]], statement_list)

    # 15. STATEMENT
    create_fa([[expression_stmt], [compound_stmt], [selection_stmt], [iteration_stmt], [return_stmt]], statement)

    # 16. EXPRESSION STMT
    create_fa([[expression, SEMICOLON], [BREAK, SEMICOLON], [SEMICOLON]], expression_stmt)

    # 17. SELECTION STMT
    create_fa([[IF, OPENPAR, expression, CLOSEPAR, statement, ELSE, statement]], selection_stmt)

    # 18. ITERATION STMT
    create_fa([[WHILE, OPENPAR, expression, CLOSEPAR, statement]], iteration_stmt)

    # 19. RETURN STMT
    create_fa([[RETURN, return_stmt_prime]], return_stmt)

    # 20. RETURN STMT PRIME
    create_fa([[SEMICOLON], [expression, SEMICOLON]], return_stmt_prime)

    # 21. EXPRESSION
    create_fa([[simple_expression_zegond], [ID, b]], expression)

    # 22. B
    create_fa([[EQUAL, expression], [OPENBRACKET, expression, CLOSEBRACKET, h], [simple_expression_prime]], b)

    # 23. H
    create_fa([[EQUAL, expression], [g, d, c]], h)

    # 24. SIMPLE EXPRESSION ZEGOND
    create_fa([[additive_expression_zegond, c]], simple_expression_zegond)

    # 25. SIMPLE EXPRESSION PRIME
    create_fa([[additive_expression_prime, c]], simple_expression_prime)

    # 26. C
    create_fa([[relop, additive_expression], [None]], c)

    # 27. RELOP
    create_fa([[LESS], [DOUBLEEQUAL]], relop)

    # 28. ADDITIVE EXPRESSION
    create_fa([[term, d]], additive_expression)

    # 29. ADDITIVE EXPRESSION PRIME
    create_fa([[term_prime, d]], additive_expression_prime)

    # 30. ADDITIVE EXPRESSION ZEGOND
    create_fa([[term_zegond, d]], additive_expression_zegond)

    # 31. D
    create_fa([[addop, term, d], [None]], d)

    # 32. ADDOP
    create_fa([[PLUS], [MINUS]], addop)

    # 33. TERM
    create_fa([[signed_factor, g]], term)

    # 34. TERM PRIME
    create_fa([[signed_factor_prime, g]], term_prime)

    # 35. TERM ZEGOND
    create_fa([[signed_factor_zegond, g]], term_zegond)

    # 36. G
    create_fa([[MULT, signed_factor, g], [None]], g)

    # 37. SIGNED FACTOR
    create_fa([[PLUS, factor], [MINUS, factor], [factor]], signed_factor)

    # 38. SIGNED FACTOR PRIME
    create_fa([[factor_prime]], signed_factor_prime)

    # 39. SIGNED FACTOR ZEGOND
    create_fa([[PLUS, factor], [MINUS, factor], [factor_zegond]], signed_factor_zegond)

    # 40. FACTOR
    create_fa([[OPENPAR, expression, CLOSEPAR], [ID, var_call_prime], [NUM]], factor)

    # 41. VAR CALL PRIME
    create_fa([[OPENPAR, args, CLOSEPAR], [var_prime]], var_call_prime)

    # 42. VAR PRIME
    create_fa([[OPENBRACKET, expression, CLOSEBRACKET], [None]], var_prime)

    # 43. FACTOR PRIME
    create_fa([[OPENPAR, args, CLOSEPAR], [None]], factor_prime)

    # 44. FACTOR ZEGOND
    create_fa([([OPENPAR, expression, CLOSEPAR], [None, None, None], [None, None, None]), 
               ([NUM], ["push_num_ss"], [None])], factor_zegond)

    # 45. ARGS
    create_fa([[arg_list], [None]], args)

    # 46. ARG LIST
    create_fa([[expression, arg_list_prime]], arg_list)

    # 47. ARG LIST PRIME
    create_fa([([COMMA, expression, arg_list_prime], [], []), [None]], arg_list_prime)

    return program

def create_fa(rules, nt):
    init_state = State()
    final_state = State((StateType.ACCEPT,))
    fa = ParserFA(init_state, nt)
    fa.addState(final_state)
    for rule in rules:
        i = 0
        curstate = init_state
        while i < len(rule[0]) - 1:
            newState = State()
            fa.addState(newState)
            fa.addTransition(curstate, newState, rule[0][i], rule[1][i], rule[2][i])
            curstate = newState
            i+=1 
        fa.addTransition(curstate, final_state, rule[0][-1], rule[1][-1], rule[2][-1])
    return fa
