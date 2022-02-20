import expressions


def make_nnf(expr):
    expr.make_nnf()


def print_clause(clause, operator):
    if len(clause) == 1:
        print(clause[0], end='')
        return
    print('(', end='')
    print(operator.join(clause), end='')
    print(')', end='')


def print_dnf_str_appearance(expr):
    dnf = get_dnf_from_expr(expr)
    for clause in dnf[-1]:
        print_clause(clause, '&')
        print('|', end='')
    print_clause(dnf[-1], '&')


def get_dnf_from_expr(expr):
    expr.make_nnf()
    return get_dnf_from_nnf(expr)


def get_dnf_from_nnf(expr):
    if expr.is_literal:
        ans = set()
        if expr.negate:
            ans.add('-' + expr.label)
        else:
            ans.add(expr.label)
        print(expr.label)
        return [ans]
    left_dnf = get_dnf_from_nnf(expr.left_part)
    right_dnf = get_dnf_from_nnf(expr.right_part)
    ans = []
    if expr.operator == expressions.ExprTree.Operator.AND:
        for left_clause in left_dnf:
            for right_clause in right_dnf:
                ans.append(left_clause.union(right_clause))
    else:
        ans = [*left_dnf, *right_dnf]
    return ans


def get_cnf_equations(expr):
    if expr.is_literal:
        return []
    cur_tuple = (expr.as_literal(), expr.left_part.as_literal(), expr.right_part.as_literal(), expr.operator)
    return [cur_tuple, *get_cnf_equations(expr.left_part), *get_cnf_equations(expr.right_part)]


def negate_literal(literal):
    if literal[0] == '-':
        return literal[1:]
    return '-' + literal


def get_cnf_from_expr(expr):
    equations = get_cnf_equations(expr)
    ans = [[expr.as_literal()]]
    for eq in equations:
        if eq[3] == expressions.ExprTree.Operator.AND:
            ans.append([eq[0], negate_literal(eq[1]), negate_literal(eq[2])])
            ans.append([negate_literal(eq[0]), eq[1]])
            ans.append([negate_literal(eq[0]), eq[2]])
        else:
            ans.append([negate_literal(eq[0]), eq[1], eq[2]])
            ans.append([eq[0], negate_literal(eq[1])])
            ans.append([eq[0], negate_literal(eq[2])])
    return ans


def print_cnf_str_appearance(expr):
    cnf = get_cnf_from_expr(expr)
    for clause in cnf[:-1]:
        print_clause(clause, '|')
        print('&', end='')
    print_clause(cnf[-1], '|')
