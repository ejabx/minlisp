from lisp.parser import parse
from lisp.evaluator import evaluate
from lisp.environment import standard_env

def repl():
    env = standard_env()
    while True:
        try:
            code = input("lisp> ")
            if code.strip() == "exit":
                break
            ast = parse(code)
            result = evaluate(ast, env)
            if result is not None:
                print(result)
        except Exception as e:
            print("Error:", e)
