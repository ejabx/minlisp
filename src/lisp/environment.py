import math
import operator as op

class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        super().__init__()
        self.update(zip(params, args))
        self.outer = outer

    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        elif self.outer:
            return self.outer[key]
        else:
            raise NameError(f"Undefined symbol: {key}")

class Macro:
    def __init__(self, params, body):
        self.params = params
        self.body = body

def is_macro(x):
    return isinstance(x, Macro)

def standard_env():
    env = Env()
    env.update(vars(math))
    env.update({
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'abs': abs,
        'max': max,
        'min': min,
        'print': print,
    })
    return env
