from parserfa import *
from code_gen import *


def cminusParseFA(apply_fa, semantic_action):
    # TODO: build fa based on rules, firsts, and follows, return nonterminal "Program"
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
    param_list = NonTerminal([COMMA, CLOSEPAR],
                             [CLOSEPAR], apply_fa, "ParamList")
    param = NonTerminal([INT, VOID],
                        [CLOSEPAR, COMMA], apply_fa, "Param")
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
    signed_factor = NonTerminal([ID, NUM, OPENPAR, PLUS, MINUS],
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
    arg_list = NonTerminal([ID, NUM, OPENPAR, PLUS, MINUS],
                           [CLOSEPAR], apply_fa, "ArgList")
    arg_list_prime = NonTerminal([COMMA, CLOSEPAR],
                                 [CLOSEPAR], apply_fa, "ArgListPrime")

    # 1. PROGRAM
    create_fa([[declaration_list, EOF]], program, semantic_action)

    # 2. DECLARATION LIST
    create_fa([[declaration, declaration_list], [None]],
              declaration_list, semantic_action)

    # 3. DECLARATION
    create_fa([[declaration_initial, declaration_prime]],
              declaration, semantic_action)

    # 4. DECLARATION INITIAL
    create_fa([[actionNames.push_ss, type_specifier, ID]],
              declaration_initial, semantic_action)

    # 5. DECLARATION PRIME
    create_fa([[fun_declaration_prime], [var_declaration_prime]],
              declaration_prime, semantic_action)

    # 6. VAR DECLARATION PRIME
    create_fa([[SEMICOLON, actionNames.dclr_var], [OPENBRACKET, actionNames.push_ss, NUM,
              CLOSEBRACKET, SEMICOLON, actionNames.dclr_arr]], var_declaration_prime, semantic_action)

    # 7. FUN DECLARATION PRIME
    create_fa([[OPENPAR, params, CLOSEPAR, actionNames.update_func_params,
              compound_stmt, actionNames.end_func]], fun_declaration_prime, semantic_action)

    # 8. TYPE SPECIFIER
    create_fa([[INT], [VOID]], type_specifier, semantic_action)

    # 9. PARAMS
    create_fa([[actionNames.push_ss, INT, actionNames.push_ss, ID,
              param_prime, param_list], [VOID]], params, semantic_action)

    # 10. PARAM LIST
    create_fa([[COMMA, param, param_list], [None]],
              param_list, semantic_action)

    # 11. PARAM
    create_fa([[declaration_initial, param_prime]], param, semantic_action)

    # 12. PARAM PRIME
    create_fa([[OPENBRACKET, CLOSEBRACKET, actionNames.save_param_list], [
              None, actionNames.save_param_norm]], param_prime, semantic_action)

    # 13. COMPOUND STMT
    create_fa([[OPENCURLY, actionNames.save_scope,  declaration_list, statement_list,
              actionNames.fill_break, CLOSECURLY]], compound_stmt, semantic_action)

    # 14. STATEMENT LIST
    create_fa([[statement, statement_list], [None]],
              statement_list, semantic_action)

    # 15. STATEMENT
    create_fa([[expression_stmt], [compound_stmt], [selection_stmt], [
              iteration_stmt], [return_stmt]], statement, semantic_action)

    # 16. EXPRESSION STMT
    create_fa([[expression, SEMICOLON], [BREAK, SEMICOLON, actionNames.save_jmp_out_scope], [
              SEMICOLON]], expression_stmt, semantic_action)

    # 17. SELECTION STMT
    create_fa([[IF, OPENPAR, expression, CLOSEPAR, actionNames.save_while_cond_jpf,
              statement, ELSE, statement]], selection_stmt, semantic_action)

    # 18. ITERATION STMT
    create_fa([[WHILE, OPENPAR, expression, CLOSEPAR, statement]],
              iteration_stmt, semantic_action)

    # 19. RETURN STMT
    create_fa([[RETURN, return_stmt_prime]], return_stmt, semantic_action)

    # 20. RETURN STMT PRIME
    create_fa([[actionNames.return_jp, SEMICOLON], [
              expression, actionNames.save_return_value, SEMICOLON]], return_stmt_prime, semantic_action)

    # 21. EXPRESSION
    create_fa([[simple_expression_zegond], [actionNames.pid, ID,
              b, actionNames.print]], expression, semantic_action)

    # 22. B
    create_fa([[EQUAL, expression, actionNames.assign], [OPENBRACKET, expression, CLOSEBRACKET,
              actionNames.calc_arr_addr, h], [simple_expression_prime]], b, semantic_action)

    # 23. H
    create_fa([[EQUAL, expression, actionNames.assign],
              [g, d, c]], h, semantic_action)

    # 24. SIMPLE EXPRESSION ZEGOND
    create_fa([[additive_expression_zegond, c]],
              simple_expression_zegond, semantic_action)

    # 25. SIMPLE EXPRESSION PRIME
    create_fa([[additive_expression_prime, c]],
              simple_expression_prime, semantic_action)

    # 26. C
    create_fa([[relop, additive_expression, actionNames.relation],
              [None]], c, semantic_action)

    # 27. RELOP
    create_fa([[actionNames.push_ss, LESS], [
              actionNames.push_ss, DOUBLEEQUAL]], relop, semantic_action)

    # 28. ADDITIVE EXPRESSION
    create_fa([[term, d]], additive_expression, semantic_action)

    # 29. ADDITIVE EXPRESSION PRIME
    create_fa([[term_prime, d]], additive_expression_prime, semantic_action)

    # 30. ADDITIVE EXPRESSION ZEGOND
    create_fa([[term_zegond, d]], additive_expression_zegond, semantic_action)

    # 31. D
    create_fa([[addop, term, actionNames.add_or_sub, d], [None]],
              d, semantic_action)

    # 32. ADDOP
    create_fa([[actionNames.push_ss, PLUS], [
              actionNames.push_ss, MINUS]], addop, semantic_action)

    # 33. TERM
    create_fa([[signed_factor, g]], term, semantic_action)

    # 34. TERM PRIME
    create_fa([[signed_factor_prime, g]], term_prime, semantic_action)

    # 35. TERM ZEGOND
    create_fa([[signed_factor_zegond, g]], term_zegond, semantic_action)

    # 36. G
    create_fa([[MULT, signed_factor, actionNames.mult, g], [None]],
              g, semantic_action)

    # 37. SIGNED FACTOR
    create_fa([[PLUS, factor], [MINUS, factor], [factor]],
              signed_factor, semantic_action)

    # 38. SIGNED FACTOR PRIME
    create_fa([[factor_prime]], signed_factor_prime, semantic_action)

    # 39. SIGNED FACTOR ZEGOND
    create_fa([[PLUS, factor], [MINUS, factor], [factor_zegond]],
              signed_factor_zegond, semantic_action)

    # 40. FACTOR
    create_fa([[OPENPAR, expression, CLOSEPAR], [actionNames.pid, ID, var_call_prime], [
              actionNames.push_num_ss, NUM]], factor, semantic_action)

    # 41. VAR CALL PRIME
    create_fa([[actionNames.start_args, OPENPAR, args, CLOSEPAR, actionNames.check_args], [
              var_prime]], var_call_prime, semantic_action)

    # 42. VAR PRIME
    create_fa([[OPENBRACKET, expression, CLOSEBRACKET, actionNames.calc_arr_addr], [
              None]], var_prime, semantic_action)

    # 43. FACTOR PRIME
    create_fa([[actionNames.start_args, OPENPAR, args, CLOSEPAR,
              actionNames.check_args], [None]], factor_prime, semantic_action)

    # 44. FACTOR ZEGOND
    create_fa([[OPENPAR, expression, CLOSEPAR], [
              actionNames.push_num_ss, NUM]], factor_zegond, semantic_action)

    # 45. ARGS
    create_fa([[arg_list], [None]], args, semantic_action)

    # 46. ARG LIST
    create_fa([[expression, arg_list_prime]], arg_list, semantic_action)

    # 47. ARG LIST PRIME
    create_fa([[COMMA, expression, arg_list_prime], [None]],
              arg_list_prime, semantic_action)

    return program


def create_fa(rules, nt, semantic_action):
    init_state = State()
    final_state = State((StateType.ACCEPT,))
    fa = ParserFA(init_state, nt, semantic_action)
    fa.addState(final_state)
    for rule in rules:
        i = 0
        curstate = init_state
        while i < len(rule) - 1:
            newState = State()
            fa.addState(newState)
            fa.addTransition(curstate, newState, rule[i])
            curstate = newState
            i += 1
        fa.addTransition(curstate, final_state, rule[-1])
    return fa
