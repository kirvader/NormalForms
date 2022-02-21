def get_nnf(expr):
    new_expr = expr
    new_expr.make_nnf()
    return new_expr
