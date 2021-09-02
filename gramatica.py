# ============== ANALIZADOR LÉXICO ===================
tokens = (
    'PARIZQ',
    'PARDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'ID'
)

#Patrones para los Tokens
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_MAS       = r'\+'
t_MENOS     = r'\-'
t_POR       = r'\*'
t_DIVIDIDO  = r'\/'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t


# Caracteres a ignorar
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("No se acepta: '%s'" % t.value[0])
    t.lexer.skip(1)


# Contrucción del analizador léxico
from io import TextIOWrapper
import ply.lex as lex
lexer = lex.lex()


# ============== ANALIZADOR SINTÁCTICO ===================

# GRAMÁTICA
# S : E
# E : E + T
# E : E - T
# E : T
# T : T * F
# T : T / F
# T : F
# F : ( E )
# F : ID

# La precedencia no es necesaria por que la gramática no es ambigua

# VARIABLES GLOBALES PARA C3D
c3d = ""
count = 0

# Producciones (Las acciones semanticas de nuestras producciones se hacen en forma de funciones)

def p_s_inicio(t):
    's_inicio : exp'
    global c3d
    print(c3d)

# E

def p_exp_mas(t):
    'exp : exp MAS texp'
    t[0] = newTemp()
    global c3d
    c3d += t[0] + "=" + t[1] + "+" + t[3] + "\n"

def p_exp_menos(t):
    'exp : exp MENOS texp'
    t[0] = newTemp()
    global c3d
    c3d += t[0] + "=" + t[1] + "-" + t[3] + "\n"

def p_exp(t):
    'exp : texp'
    t[0] = t[1]

# T

def p_texp_por(t):
    'texp : texp POR fexp'
    t[0] = newTemp()
    global c3d
    c3d += t[0] + "=" + t[1] + "*" + t[3] + "\n"

def p_texp_div(t):
    'texp : texp DIVIDIDO fexp'
    t[0] = newTemp()
    global c3d
    c3d += t[0] + "=" + t[1] + "/" + t[3] + "\n"
    

def p_texp(t):
    'texp : fexp'
    t[0] = t[1]

# F

def p_fexp_par(t):
    'fexp : PARIZQ exp PARDER'
    t[0] = t[2]

def p_fexp_ID(t):
    'fexp : ID'
    t[0] = t[1]

def newTemp():
    global count
    nt = "t"+str(count)
    count += 1
    return nt


# Errores sintacticos
def p_error(t):
    print("Error sintactico en '%s'" % t.value)


# Construyendo el analizador sintactico
import ply.yacc as yacc
parser = yacc.yacc()


# ========================= TESTEANDO ========================
f = open("./test_inputs/entrada3.txt", "r")
input = f.read()
print("\nCADENA DE ENTRADA:")
print(input)
print("\nC3D GENERADO:")
parser.parse(input)
print("Listo!")