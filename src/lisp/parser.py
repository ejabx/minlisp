def tokenize(s: str):
    """Add spaces around parentheses, backquote, and comma; split into tokens."""
    for char in '()`,':
        s = s.replace(char, f' {char} ')
    return s.split()

def parse(program: str):
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError("Unexpected EOF")
    token = tokens.pop(0)
    if token == "(":
        L = []
        while tokens[0] != ")":
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif token == ")":
        raise SyntaxError("Unexpected )")
    elif token == "`":
        return ["`", read_from_tokens(tokens)]
    elif token == ",":
        return [",", read_from_tokens(tokens)]
    else:
        return atom(token)

def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return str(token)
