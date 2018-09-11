from CorpusToolkit.ply_parser.token import Token

import ply.lex as lex
import ply.yacc as yacc


# option to process function
option_merge_sub_token = False


tokens = (
    'SLASH',
    'OPEN_BRACE', 'CLOSE_BRACE',
    'OPEN_BRACKET', 'CLOSE_BRACKET',
    'TOKEN_OR_POS_OR_PINYIN',
)

# Tokens

t_SLASH = r'/'
t_OPEN_BRACE = r'\{'
t_CLOSE_BRACE = r'\}'
t_OPEN_BRACKET = r'\['
t_CLOSE_BRACKET = r'\]'


def t_TOKEN_OR_POS_OR_PINYIN(t):
    r'[^/\ \}\{\]\[][^/\ \]\{\}]*'
    t.value = str(t.value)
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    raise ValueError("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Precedence rules for the arithmetic operators
precedence = ()


def p_statement_expr(p):
    """statement : expression
                 | statement expression"""

    if not p[0]:
        p[0] = []

    if len(p) > 2:
        p[0].extend(p[1])
        p[0].extend(p[2])
    else:
        p[0].extend(p[1])


def p_simple_expression_expr(p):
    """simple_expression : TOKEN_OR_POS_OR_PINYIN SLASH TOKEN_OR_POS_OR_PINYIN
                         | TOKEN_OR_POS_OR_PINYIN OPEN_BRACE TOKEN_OR_POS_OR_PINYIN CLOSE_BRACE SLASH TOKEN_OR_POS_OR_PINYIN"""

    token = Token()

    # common assignment
    token.token = p[1]

    if len(p) > 4:
        token.pinyin = p[3]
        token.pos = p[6]
    else:
        token.pos = p[3]

    p[0] = token


def p_expression_binop(p):
    """expression : simple_expression
                  | OPEN_BRACKET statement CLOSE_BRACKET TOKEN_OR_POS_OR_PINYIN"""

    # second form
    if len(p) > 2:
        if option_merge_sub_token:
            token = Token()
            new_token_text = ''
            for sub_p in p[2]:
                new_token_text += sub_p.token

            token.token = new_token_text
            token.pos = p[4]

            p[0] = [token]
        else:
            p[0] = p[2]
    else:
        p[0] = [p[1]]


def p_error(p):
    print("Syntax error at '%s': %s" % (p.value, p))
    raise ValueError("Syntax error at '%s': %s" % (p.value, p))


# def make_lexer(debug=False, debuglog=None):
#     lexer = lex.lex(debug=debug, debuglog=debuglog)
#     return lexer


lexer = lex.lex()


def make_parser(debug=False, debuglog=None, merge_sub_token=False):
    global option_merge_sub_token
    option_merge_sub_token = merge_sub_token

    parser = yacc.yacc(debug=debug, debuglog=debuglog)
    return parser
