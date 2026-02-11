import ply.lex as lex

class Repository:
# Diccionario de palabras reservadas
    def __init__(self):
        self.lexer = lex.lex(module=self)

    
    reservadas = {
        'int': 'INT',
        'str': 'STRING',
        'float' : 'FLOAT',
        'if': 'IF',
        'else': 'ELSE',
        'elif': 'ELIF',
        'while': 'WHILE',
        'for': 'FOR',
        'print': 'PRINT',
        'return': 'RETURN',
        'break': 'BREAK',
        'continue': 'CONTINUE'
    }


    # List of token names.   This is always required
    tokens = (
        # Literales e Identificadores
        'ID', 
        
        # Operadores Aritméticos
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 
        
        # Operadores de Comparación
        'EQUAL',     # =
        'DISTINCT',  # !=
        'ISEQUAL',   # == 
        'GREATER',   # >
        'LESS',      # <
        'INCREMENTO', 'DECREMENTO',
        # Delimitadores
        'LPAREN', 'RPAREN',
        'LBRACE', 'RBRACE', # { }
        'COLON',
        'SEMICOLON',        # ;
        'COMMA',            # ,
        
    ) + tuple(reservadas.values()) # Une los tokens de las palabras reservadas

    t_COLON = r'\:'
    t_SEMICOLON = r'\;'
    t_COMMA   = r'\,'
    t_LBRACE  = r'\{'
    t_RBRACE = r'\}'
    t_EQUAL   = r'\='
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_GREATER = r'\>'
    t_LESS    = r"\<"
    t_ignore  = ' \t'

    def t_INCREMENTO(self, t):
        r'\+\+'
        return t

    def t_DECREMENTO(self, t):
        r"\-\-"

    # Regular expression rules for simple tokens
    def t_POWER(self,t):
        r'\*\*'
        return t

    def t_DISTINCT(self,t):
        r'!='
        return t

    def t_ISEQUAL(self,t):
        r"=="
        return t

    def t_FLOAT(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t
    
    def t_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self,t):
        r" \" [^\"]* \"| \' [^']* \' "
        return t

    def t_ID(self, t):
        r"[a-zA-Z][a-zA-Z0-9]*"
        t.type= self.reservadas.get(t.value, "ID")
        return t



    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)



    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


    


repo = Repository()
lexer = repo.lexer
tokens = repo.tokens