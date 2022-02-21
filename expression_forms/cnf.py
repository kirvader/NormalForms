from expression_forms.clause import Clause, get_var_from_literal
from expression_forms.expr_tree import Operator
from expression_forms.nnf import get_nnf


class CNF:
    class CNF_Clause(Clause):
        def __init__(self, variables):
            super().__init__(Operator.OR, variables)

    def __init__(self):
        self.clauses = []
        self.local_vars = set()

    def __str__(self):
        ans = ""
        for clause in self.clauses:
            ans = ans + str(clause) + '&'
        ans = ans[:-1]
        return ans

    def execute(self, values):
        res = True
        for clause in self.clauses:
            res = res and clause.execute(values)
        return res

    def add_clause(self, clause):
        self.clauses.append(clause)

    def add_local_var(self, literal):
        self.local_vars.add(get_var_from_literal(literal))


def get_cnf_equations(expr):
    if expr.is_literal:
        return []
    cur_tuple = (expr.as_literal(), expr.left_part.as_literal(), expr.right_part.as_literal(), expr.operator)
    return [cur_tuple, *get_cnf_equations(expr.left_part), *get_cnf_equations(expr.right_part)]


def negate_literal(literal):
    # literal is string type
    if literal[0] == '-':
        return literal[1:]
    return '-' + literal


def get_cnf_from_expr(expr):
    equations = get_cnf_equations(get_nnf(expr))
    ans = CNF()
    ans.add_clause(CNF.CNF_Clause([expr.as_literal()]))
    for eq in equations:
        if eq[3] == Operator.AND:
            ans.add_clause(CNF.CNF_Clause([eq[0], negate_literal(eq[1]), negate_literal(eq[2])]))
            ans.add_clause(CNF.CNF_Clause([negate_literal(eq[0]), eq[1]]))
            ans.add_clause(CNF.CNF_Clause([negate_literal(eq[0]), eq[2]]))
        else:
            ans.add_clause(CNF.CNF_Clause([negate_literal(eq[0]), eq[1], eq[2]]))
            ans.add_clause(CNF.CNF_Clause([eq[0], negate_literal(eq[1])]))
            ans.add_clause(CNF.CNF_Clause([eq[0], negate_literal(eq[2])]))
    return ans
