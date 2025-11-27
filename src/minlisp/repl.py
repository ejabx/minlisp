import operator as op

# -----------------------
# Parsing
# -----------------------
def tokenize(s):
    return s.replace('(',' ( ').replace(')',' ) ').split()

def parse(tokens):
    if not tokens:
        raise SyntaxError("Unexpected EOF")
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(parse(tokens))
        tokens.pop(0)  # remove ')'
        return L
    elif token == ')':
        raise SyntaxError("Unexpected )")
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token  # symbol

def read(s):
    return parse(tokenize(s))


# -----------------------
# Environment
# -----------------------
class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        super().__init__(zip(params, args))
        self.outer = outer

    def find(self, key):
        if key in self:
            return self
        elif self.outer is not None:
            return self.outer.find(key)
        else:
            raise NameError(f"Undefined symbol: {key}")


# -----------------------
# Evaluation
# -----------------------
def eval(x, env):
    # atoms
    if isinstance(x, str):
        return env.find(x)[x]
    if not isinstance(x, list):
        return x

    # special forms
    if x[0] == 'define':
        _, var, expr = x
        env[var] = eval(expr, env)
        return env[var]

    if x[0] == 'if':
        _, test, conseq, alt = x
        exp = conseq if eval(test, env) else alt
        return eval(exp, env)

    if x[0] == 'lambda':
        _, params, body = x
        return lambda *args: eval(body, Env(params, args, env))

    if x[0] == 'defmacro':
        _, name, params, body = x
        def macro(*args):
            return eval(body, Env(params, args, env))
        env[name] = ('macro', macro)
        return None

    # macro expansion
    if isinstance(x[0], str) and x[0] in env:
        val = env[x[0]]
        if isinstance(val, tuple) and val[0] == 'macro':
            macro = val[1]
            return eval(macro(*x[1:]), env)

    # function application
    proc = eval(x[0], env)
    args = [eval(arg, env) for arg in x[1:]]
    return proc(*args)


# -----------------------
# REPL & Standard Environment
# -----------------------
def standard_env():
    env = Env()
    env.update(vars(op))  # math functions if needed
    env.update({
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        '>': op.gt,
        '<': op.lt,
        '=': op.eq,
        'print': lambda x: print(x) or x,
        'not': op.not_,
    })
    return env


global_env = standard_env()

# -----------------------
# REPL
# -----------------------
def repl():
    while True:
        try:
            expr = read(input("lisp> "))
            result = eval(expr, global_env)
            if result is not None:
                print(result)
        except Exception as e:
            print("Error:", e)
