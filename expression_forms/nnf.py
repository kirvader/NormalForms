import copy


def get_nnf(expr):
    new_expr = copy.deepcopy(expr)
    new_expr.make_nnf()
    return new_expr
