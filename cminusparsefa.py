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
    program = NonTerminal([INT, VOID, EOF], apply_fa, "Program")
    declaration_list = NonTerminal([INT, VOID, ID, SEMICOLON, NUM, OPENPAR, OPENCURLY, CLOSECURLY, BREAK, IF, WHILE, RETURN, PLUS, MINUS, EOF], apply_fa, "DeclarationList")
    declaration = NonTerminal([INT, VOID], apply_fa, "Declaration")
    declaration_initial = NonTerminal([INT, VOID], apply_fa, "Declaration Initial")
    declaration_prime = NonTerminal([SEMICOLON, OPENBRACKET, OPENPAR], apply_fa, "DeclarationPrime")
    var_declaration_prime = NonTerminal([SEMICOLON, OPENBRACKET], apply_fa, "VarDeclarationPrime")
    fun_declaration_prime = NonTerminal([OPENPAR], apply_fa, "FunDeclarationPrime")
    type_specifier = NonTerminal([INT, VOID], apply_fa, "TypeSpecifier")
    params = NonTerminal([INT, VOID], apply_fa, "Params")
    param_list = NonTerminal([COMMA,CLOSEPAR], apply_fa, "ParamList")
    param = NonTerminal([INT, VOID],apply_fa, "Param")
    param_prime = NonTerminal([OPENBRACKET, CLOSEPAR, COMMA], apply_fa, "ParamPrime")
    compound_stmt = NonTerminal([OPENCURLY], apply_fa, "CompoundStmt")
    statement_list = NonTerminal([ID, SEMICOLON, NUM, OPENPAR, OPENCURLY, BREAK, IF, WHILE, RETURN, PLUS, MINUS, CLOSECURLY], apply_fa, "StatementList")
    statement = NonTerminal([ID, SEMICOLON, NUM, OPENPAR, OPENCURLY, BREAK, IF, WHILE, RETURN, PLUS, MINUS], apply_fa, "Statement")
    expression_stmt = NonTerminal([ID, SEMICOLON, NUM, OPENPAR, BREAK, PLUS, MINUS], apply_fa, "ExpressionStmt")
    selection_stmt = NonTerminal([IF], apply_fa, "SelectionStmt")
    iteration_stmt = NonTerminal([WHILE], apply_fa, "IterationStmt")
    return_stmt = NonTerminal([RETURN], apply_fa, "ReturnStmt")
    return_stmt_prime = NonTerminal([ID, SEMICOLON, NUM, OPENPAR, PLUS, MINUS], apply_fa, "ReturnStmtPrime")
    expression = NonTerminal([ID, NUM, OPENPAR, PLUS, MINUS], apply_fa, "Expression")
    b = NonTerminal([OPENBRACKET, OPENPAR, EQUAL, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA], apply_fa, "B")
    h = NonTerminal([EQUAL, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA], apply_fa, "H")
    simple_expression_zegond = NonTerminal([NUM, OPENPAR, PLUS, MINUS], apply_fa, "SimpleExpressionZegond")
    simple_expression_prime = NonTerminal([OPENPAR, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA], apply_fa, "SimpleExpressionPrime")
    c = NonTerminal([LESS, DOUBLEEQUAL, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA], apply_fa, "C")
    relop = NonTerminal([LESS, DOUBLEEQUAL], apply_fa, "Relop")
    additive_expression = NonTerminal([ID, NUM, OPENPAR, PLUS, MINUS], apply_fa, "AdditiveExpression")
    additive_expression_prime = NonTerminal([OPENPAR, PLUS, MINUS, MULT, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL], apply_fa, "AdditiveExpressionPrime")
    additive_expression_zegond = NonTerminal([NUM, OPENPAR, PLUS, MINUS], apply_fa, "AdditiveExpressionZegond")
    d = NonTerminal([PLUS, MINUS, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL], apply_fa, "D")
    addop = NonTerminal([PLUS, MINUS], apply_fa, "Addop")
    term = NonTerminal([ID, NUM, OPENPAR, PLUS, MINUS], apply_fa, "Term")
    term_prime = NonTerminal([OPENPAR, MULT, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS], apply_fa, "TermPrime")
    term_zegond = NonTerminal([NUM, OPENPAR, PLUS, MINUS], apply_fa, "TermZegond")
    g = NonTerminal([MULT, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS], apply_fa, "G")
    signed_factor = NonTerminal([ID,NUM, OPENPAR, PLUS, MINUS], apply_fa, "SignedFactor")
    signed_factor_prime = NonTerminal([OPENPAR, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT], apply_fa, "SignedFactorPrime")
    signed_factor_zegond = NonTerminal([NUM, OPENPAR, PLUS, MINUS], apply_fa, "SignedFactorZegond")
    factor = NonTerminal([ID, NUM, OPENPAR], apply_fa, "Factor")
    var_call_prime = NonTerminal([OPENBRACKET, OPENPAR, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT], apply_fa, "VarCallPrime")
    var_prime = NonTerminal([OPENBRACKET, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT], apply_fa, "VarPrime")
    factor_prime = NonTerminal([OPENPAR, SEMICOLON, CLOSEBRACKET, CLOSEPAR, COMMA, LESS, DOUBLEEQUAL, PLUS, MINUS, MULT], apply_fa, "FactorPrime")
    factor_zegond = NonTerminal([NUM, OPENPAR], apply_fa, "FactorZegond")
    args = NonTerminal([ID, NUM, OPENPAR, PLUS, MINUS, CLOSEPAR], apply_fa, "Args")
    arg_list = NonTerminal([ID, NUM,OPENPAR, PLUS, MINUS], apply_fa, "ArgList")
    arg_list_prime = NonTerminal([COMMA, CLOSEPAR], apply_fa, "ArgListPrime")


    b.set_fa(create_fa([[expression], [OPENBRACKET, expression, CLOSEBRACKET, h], [simple_expression_prime]]))

    # 1. PROGRAM
    program.set_fa(create_fa([[declaration_list]]))

    # 2. DECLARATION LIST
    declaration_list.set_fa(create_fa([[declaration, declaration_list], [None]]))

    # 3. DECLARATION
    declaration.set_fa(create_fa([[declaration_initial, declaration_prime]]))

    # 4. DECLARATION INITIAL
    declaration_initial.set_fa(create_fa([[type_specifier, ID]]))

    # 5. DECLARATION PRIME
    declaration_prime.set_fa(create_fa([[fun_declaration_prime], [var_declaration_prime]]))

    # 6. VAR DECLARATION PRIME
    var_declaration_prime.set_fa(create_fa([[SEMICOLON], [OPENBRACKET, NUM, CLOSEBRACKET, SEMICOLON]]))

    # 7. FUN DECLARATION PRIME
    fun_declaration_prime.set_fa(create_fa([[OPENPAR, params, CLOSEPAR, compound_stmt]]))

    # 8. TYPE SPECIFIER
    type_specifier.set_fa(create_fa([[INT], [VOID]]))

    # 9. PARAMS
    params.set_fa(create_fa([[INT, ID, param_prime, param_list], [VOID]]))

    # 10. PARAM LIST
    param_list.set_fa(create_fa([[COMMA, param, param_list], [None]]))

    # 11. PARAM
    param.set_fa(create_fa([[declaration_initial, param_prime]]))

    # 12. PARAM PRIME
    param_prime.set_fa(create_fa([[OPENBRACKET, CLOSEBRACKET], [None]]))

    # 13. COMPOUND STMT
    compound_stmt.set_fa(create_fa([[OPENCURLY, declaration_list, statement_list, CLOSECURLY]]))

    # 14. STATEMENT LIST
    statement_list.set_fa(create_fa([[statement, statement_list], [None]]))

    # 15. STATEMENT
    statement.set_fa(create_fa([[expression_stmt], [compound_stmt], [selection_stmt], [iteration_stmt], [return_stmt]]))

    # 16. EXPRESSION STMT
    expression_stmt.set_fa(create_fa([[expression, SEMICOLON], [BREAK, SEMICOLON], [SEMICOLON]]))

    # 17. SELECTION STMT
    selection_stmt.set_fa(create_fa([[IF, OPENPAR, expression, CLOSEPAR, statement, ELSE, statement]]))

    # 18. ITERATION STMT
    iteration_stmt.set_fa(create_fa([[WHILE, OPENPAR, expression, CLOSEPAR, statement]]))

    # 19. RETURN STMT
    return_stmt.set_fa(create_fa([[RETURN, return_stmt_prime]]))

    # 20. RETURN STMT PRIME
    return_stmt_prime.set_fa(create_fa([[SEMICOLON], [expression, SEMICOLON]]))

    # 21. EXPRESSION
    expression.set_fa(create_fa([[simple_expression_zegond], [ID, b]]))

    # 22. B
    b.set_fa(create_fa([[EQUAL, expression], [OPENBRACKET, expression, CLOSEBRACKET, h], [simple_expression_prime]]))

    # 23. H
    h.set_fa(create_fa([[EQUAL, expression], [g, d, c]]))

    # 24. SIMPLE EXPRESSION ZEGOND
    simple_expression_zegond.set_fa(create_fa([[additive_expression_zegond, c]]))

    # 25. SIMPLE EXPRESSION PRIME
    simple_expression_prime.set_fa(create_fa([[additive_expression_prime, c]]))

    # 26. C
    c.set_fa(create_fa([[relop, additive_expression], [None]]))

    # 27. RELOP
    relop.set_fa(create_fa([[LESS], [DOUBLEEQUAL]]))

    # 28. ADDITIVE EXPRESSION
    additive_expression.set_fa(create_fa([[term, d]]))

    # 29. ADDITIVE EXPRESSION PRIME
    additive_expression_prime.set_fa(create_fa([[term_prime, d]]))

    # 30. ADDITIVE EXPRESSION ZEGOND
    additive_expression_zegond.set_fa(create_fa([[term_zegond, d]]))

    # 31. D
    d.set_fa(create_fa([[addop, term, d], [None]]))

    # 32. ADDOP
    addop.set_fa(create_fa([[PLUS], [MINUS]]))

    # 33. TERM
    term.set_fa(create_fa([[signed_factor, g]]))

    # 34. TERM PRIME
    term_prime.set_fa(create_fa([[signed_factor_prime, g]]))

    # 35. TERM ZEGOND
    term_zegond.set_fa(create_fa([[signed_factor_zegond, g]]))

    # 36. G
    g.set_fa(create_fa([[MULT, signed_factor, g], [None]]))

    # 37. SIGNED FACTOR
    signed_factor.set_fa(create_fa([[PLUS, factor], [MINUS, factor], [factor]]))

    # 38. SIGNED FACTOR PRIME
    signed_factor_prime.set_fa(create_fa([[factor_prime]]))

    # 39. SIGNED FACTOR ZEGOND
    signed_factor_zegond.set_fa(create_fa([[PLUS, factor], [MINUS, factor], [factor_zegond]]))

    # 40. FACTOR
    factor.set_fa(create_fa([[OPENPAR, expression, CLOSEPAR], [ID, var_call_prime], [NUM]]))

    # 41. VAR CALL PRIME
    var_call_prime.set_fa(create_fa([[OPENPAR, args, CLOSEPAR], [var_prime]]))

    # 42. VAR PRIME
    var_prime.set_fa(create_fa([[OPENBRACKET, expression, CLOSEBRACKET], [None]]))

    # 43. FACTOR PRIME
    factor_prime.set_fa(create_fa([[OPENPAR, args, CLOSEPAR], [None]]))

    # 44. FACTOR ZEGOND
    factor_zegond.set_fa(create_fa([[OPENPAR, expression, CLOSEPAR], [NUM]]))

    # 45. ARGS
    args.set_fa(create_fa([[arg_list], [None]]))

    # 46. ARG LIST
    arg_list.set_fa(create_fa([[expression, arg_list_prime]]))

    # 47. ARG LIST PRIME
    arg_list_prime.set_fa(create_fa([[COMMA, expression, arg_list_prime], [None]]))

    return program

def create_fa(rules):
    init_state = State()
    final_state = State((StateType.ACCEPT,))
    fa = ParserFA(init_state)
    fa.addState(final_state)
    for rule in rules:
        i = 0
        curstate = init_state
        while i < len(rule) - 1:
            newState = State()
            fa.addState(newState)
            fa.addTransition(curstate, newState, rule[i])
            curstate = newState
            i+=1 
        fa.addTransition(curstate, final_state, rule[-1])
    return fa
