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

# GRAMÁTICA             # Lowercase for ply

# S : E                 s    :   e
# E : E + T             e    :   e  +   t
# E : E - T             e    :   e  -   t
# E : T                 e    :   t
# T : T * F             t    :   t  *   f
# T : T / F             t    :   t  /   f
# T : F                 t    :   f
# F : ( E )             f    :   ( E )
# F : ID                f    :   ID

# La precedencia no es necesaria por que la gramática no es ambigua

# Variable global
count = 0

# Utilizaremos la clase NTerminal para simular atributos en los no terminanes
class NTerminal:
    """Clase que representa un No Terminal de la gramatica"""
    tipo = ""
    c3d = ""
    tmp = ""

    def __init__(self, tipo, c3d, tmp):
        self.tipo = tipo
        self.c3d = c3d
        self.tmp = tmp


# Producciones (Las acciones semanticas de nuestras producciones se hacen en forma de funciones)

def p_s_inicio(t):
    's : e'
    print(t[1].c3d)

# E

def p_e_mas(t):
    'e : e MAS t'
    eTMP = newTemp()
    eC3D = t[1].c3d + t[3].c3d + eTMP + "=" + t[1].tmp + "+" + t[3].tmp + "\n"
    t[0] = NTerminal("E", eC3D, eTMP)

def p_e_menos(t):
    'e : e MENOS t'
    nTemp = newTemp()
    localc3d = t[1].c3d + t[3].c3d + nTemp + "=" + t[1].tmp + "-" + t[3].tmp + "\n"
    t[0] = NTerminal("E", localc3d, nTemp)

def p_e(t):
    'e : t'
    t[0] = NTerminal("E", t[1].c3d, t[1].tmp)

# T

def p_te_por(t):
    't : t POR f'
    nTemp = newTemp()
    localc3d = t[1].c3d + t[3].c3d + nTemp + "=" + t[1].tmp + "*" + t[3].tmp + "\n"
    t[0] = NTerminal("T", localc3d, nTemp)

def p_te_div(t):
    't : t DIVIDIDO f'
    nTemp = newTemp()
    localc3d = t[1].c3d + t[3].c3d + nTemp + "=" + t[1].tmp + "/" + t[3].tmp +"\n"
    t[0] = NTerminal("T", localc3d, nTemp)
    

def p_te(t):
    't : f'
    t[0] = NTerminal("T", t[1].c3d, t[1].tmp)

# F

def p_fe_par(t):
    'f : PARIZQ e PARDER'
    t[0] = NTerminal("F", t[2].c3d, t[2].tmp)

def p_fe_ID(t):
    'f : ID'
    t[0] = NTerminal("F", "", t[1])

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