from NodeAS import NodeAS
import ply.yacc as yacc
from repository import  tokens
import ply.yacc as yacc

class Sintax_Analizer:
    def __init__(self):
        self.tokens = tokens 
        self.parser = yacc.yacc(module=self)

    def p_programa(self, p):
        'programa : lista_instrucciones'
        p[0] = NodeAS('PROGRAMA', p[1], lineno=p.lineno(1))

    def p_lista_instrucciones(self, p):
        '''lista_instrucciones : instruccion lista_instrucciones
                                | instruccion'''
        if len(p) == 3:
            p[0] = NodeAS('LISTA_INSTRUCCIONES', [p[1]] + p[2].hijos, lineno=p.lineno(1))
        else:
            p[0] = NodeAS('LISTA_INSTRUCCIONES', [p[1]], lineno=p.lineno(1))

    # --- ESTRUCTURAS DE CONTROL ---
    def p_instruccion_if_completo(self, p):
        'instruccion : IF LPAREN condition RPAREN LBRACE lista_instrucciones RBRACE lista_elif else_opcional'
        p[0] = NodeAS('IF_BLOQUE', [p[3], p[6], p[8], p[9]], lineno=p.lineno(1))

    def p_lista_elif(self, p):
        '''lista_elif : ELIF LPAREN condition RPAREN LBRACE lista_instrucciones RBRACE lista_elif
                      | empty'''
        if len(p) > 2:
            nodeElif = NodeAS('ELIF_BRANCH', [p[3], p[6]], lineno=p.lineno(1))
            p[0] = [nodeElif] + p[8]
        else:
            p[0] = []

    def p_else_opcional(self, p):
        '''else_opcional : ELSE LBRACE lista_instrucciones RBRACE
                         | empty'''
        if len(p) > 2:
            p[0] = NodeAS('ELSE_BRANCH', p[3], lineno=p.lineno(1))
        else:
            p[0] = []

    def p_instruccion_while(self, p):
        'instruccion : WHILE LPAREN condition RPAREN LBRACE lista_instrucciones RBRACE'
        p[0] = NodeAS('WHILE_LOOP', [p[3], p[6]], lineno=p.lineno(1))

    def p_instruccion_for(self, p):
        '''instruccion : FOR LPAREN declara_o_asigna SEMICOLON condition SEMICOLON incremento RPAREN LBRACE lista_instrucciones RBRACE
                        | FOR LPAREN condition RPAREN LBRACE lista_instrucciones RBRACE'''
        if len(p) == 12:
            p[0] = NodeAS('FOR_LOOP_COMPLETO', [p[3], p[5], p[7], p[10]], lineno=p.lineno(1))
        else:
            p[0] = NodeAS('FOR_LOOP_SIMPLE', [p[3], p[6]], lineno=p.lineno(1))

    def p_declara_o_asigna_for(self, p):
        '''declara_o_asigna : INT asignacion_base
                                | FLOAT asignacion_base
                                | STRING asignacion_base
                                | asignacion_base'''
        if len(p) == 3:
            p[0] = NodeAS('DECLARACION_FOR', [p[1], p[2]], lineno=p.lineno(1))
        else:
            p[0] = p[1]

    # --- SENTENCIAS DE CONTROL ---
    def p_instruccion_control(self, p):
        '''instruccion : BREAK SEMICOLON
                        | CONTINUE SEMICOLON
                        | RETURN expression SEMICOLON
                        | RETURN SEMICOLON'''
        token = p[1].upper()
        if token == 'RETURN':
            val = p[2] if len(p) == 4 else None
            p[0] = NodeAS('RETURN_STMT', val, lineno=p.lineno(1))
        else:
            p[0] = NodeAS(f'{token}_STMT', None, lineno=p.lineno(1))

    # --- EXPRESIONES Y ASIGNACIONES ---
    def p_asignacion_base(self, p):
        'asignacion_base : ID EQUAL expression'
        p[0] = NodeAS('ASIG_BASE', [p[1], p[3]], lineno=p.lineno(1))

    def p_instruccion_asignacion(self, p):
        'instruccion : asignacion_base SEMICOLON'
        p[0] = p[1]

    def p_instruccion_declaracion(self, p):
        '''instruccion : INT ID SEMICOLON
                        | FLOAT ID SEMICOLON
                        | STRING ID SEMICOLON''' 
        p[0] = NodeAS('DECLARACION_TIPO', [p[1], p[2]], lineno=p.lineno(1))

    def p_instruccion_declara_asigna(self, p):
        '''instruccion : INT asignacion_base SEMICOLON
                        | FLOAT asignacion_base SEMICOLON
                        | STRING asignacion_base SEMICOLON'''
        p[0] = NodeAS('DECLARACION_ASIGNACION', [p[1], p[2]], lineno=p.lineno(1))


    def p_incremento(self, p):
        '''incremento : ID INCREMENTO SEMICOLON
                      | ID PLUS PLUS SEMICOLON'''
        p[0] = NodeAS('INC_STMT', p[1], lineno=p.lineno(1))

    def p_decremento(self, p):
        '''decremento : ID MINUS MINUS SEMICOLON
                      | ID DECREMENTO SEMICOLON
        '''
        p[0] = NodeAS('DEC_STMT', p[1], lineno=p.lineno(1))

    def p_instruccion_decremento(self, p):
        'instruccion : decremento'
        p[0] = p[1]

    def p_instruccion_expresion(self, p):
        'instruccion : expression SEMICOLON'
        p[0] = NodeAS('EXPR_STMT', p[1], lineno=p.lineno(1))

    # --- CONDICIONES Y ARITMÉTICA ---
    def p_condition(self, p):
        '''condition : expression GREATER expression
                     | expression LESS expression
                     | expression ISEQUAL expression
                     | expression DISTINCT expression'''
        op_map = {'>': 'OP_MAYOR', '<': 'OP_MENOR', '==': 'OP_IGUAL', '!=': 'OP_DISTINTO'}
        p[0] = NodeAS(op_map.get(p[2], 'OP_COMP'), [p[1], p[3]], lineno=p.lineno(1))

    def p_expression_binaria(self, p):
        '''expression : expression PLUS term
                      | expression MINUS term'''
        op_node = 'OP_SUMA' if p[2] == '+' else 'OP_RESTA'
        p[0] = NodeAS(op_node, [p[1], p[3]], lineno=p.lineno(1))

    def p_expression_term(self, p):
        'expression : term'
        p[0] = NodeAS('EXPR_TERM', p[1], lineno=p.lineno(1))

    def p_term_binaria(self, p):
        '''term : term TIMES factor
                | term DIVIDE factor'''
        op_node = 'OP_MULT' if p[2] == '*' else 'OP_DIV'
        p[0] = NodeAS(op_node, [p[1], p[3]], lineno=p.lineno(1))

    def p_term_factor(self, p):
        'term : factor'
        p[0] = NodeAS('TERM_FACT', p[1], lineno=p.lineno(1))

    # --- FACTORES (HOJAS) ---
    def p_factor_id(self, p):
        'factor : ID'
        p[0] = NodeAS('FACT_ID', p[1], lineno=p.lineno(1))

    def p_factor_num(self, p):
        'factor : INT'
        p[0] = NodeAS('FACT_INT', p[1], lineno=p.lineno(1))

    def p_factor_string(self, p):
        'factor : STRING'
        p[0] = NodeAS('FACT_STR', p[1], lineno=p.lineno(1))

    def p_factor_expr(self, p):
        'factor : LPAREN expression RPAREN'
        p[0] = p[2]

    # --- FUNCIONES NATIVAS ---
    def p_comando_print(self, p):
        'instruccion : PRINT LPAREN expression RPAREN SEMICOLON'
        p[0] = NodeAS('PRINT_STMT', p[3], lineno=p.lineno(1))

    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        if p:
            print(f"Error de sintaxis en '{p.value}' (Línea {p.lineno})")
        else:
            print("Error de sintaxis: Fin de archivo inesperado")