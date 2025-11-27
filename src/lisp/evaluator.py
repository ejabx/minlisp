from lisp.environment import Env, Macro, is_macro

def quasiquote(x):
    if not isinstance(x, list):
        return x
    elif len(x) > 0 and x[0] == ",":
        return x[1]
    else:
        return [quasiquote(e) for e in x]

def evaluate(x, env):
    if isinstance(x, str):
        return env[x]
    elif not isinstance(x, list):
        return x

    if x[0] == "define-macro":
        _, name, expr = x
        params = expr[0]
        body = expr[1]
        env[name] = Macro(params, body)
        return None

    elif x[0] == "define":
        _, var, expr = x
        env[var] = evaluate(expr, env)
        return None

    elif x[0] == "if":
        _, test, conseq, alt = x
        exp = (conseq if evaluate(test, env) else alt)
        return evaluate(exp, env)

    elif x[0] == "quote":
        _, exp = x
        return exp

    elif x[0] == "`":
        return quasiquote(x[1])

    else:
        proc = evaluate(x[0], env)
        if is_macro(proc):
            macro_env = Env(proc.params, x[1:], outer=env)
            expanded = evaluate(proc.body, macro_env)
            return evaluate(expanded, env)
        else:
            args = [evaluate(arg, env) for arg in x[1:]]
            return proc(*args)
