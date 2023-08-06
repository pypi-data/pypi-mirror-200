from starlark_go import Starlark


def parse(expression: str):
    s = Starlark()
    ret = {
        "result": None,
    }
    try:
        starlark_exec = s.exec(expression)
        starlark_eval = s.eval("___return")
        ret["result"] = starlark_eval
    except Exception as e:
        column = e.errors[0].column
        line = e.errors[0].line
        ret["error"] = {"line": line, "column": column, "message": str(e)}

    return ret
