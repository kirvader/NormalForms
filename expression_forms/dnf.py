from expression_forms import expr_tree
from expression_forms.clause import Clause, Var, get_var_from_literal
from expression_forms.expr_tree import Operator
from expression_forms.nnf import get_nnf


class DNF:
    class DNF_Clause(Clause):
        def __init__(self, literals):
            super().__init__(Operator.AND, literals)

        def union(self, other_clause):
            s1 = 0
            s2 = 0
            res = DNF.DNF_Clause([])
            while s1 < len(self.vars) and s2 < len(other_clause.vars):
                if self.vars[s1].name == self.vars[s2].name:
                    if self.vars[s1].negate != self.vars[s2].negate:
                        return None
                    res.add_var(self.vars[s1])
                    s1 += 1
                    s2 += 1
                    continue
                if self.vars[s1].name > self.vars[s2].name:
                    res.add_var(self.vars[s2])
                    s2 += 1
                elif self.vars[s1].name < self.vars[s2].name:
                    res.add_var(self.vars[s1])
                    s1 += 1
            while s1 < len(self.vars):
                res.add_var(self.vars[s1])
                s1 += 1
            while s2 < len(other_clause.vars):
                res.add_var(other_clause.vars[s2])
                s2 += 1
            return res

    def __init__(self, clauses=None):
        if clauses is None:
            clauses = []
        self.clauses = clauses

    def __str__(self):
        ans = ""
        for clause in self.clauses:
            ans = ans + str(clause) + '|'
        ans = ans[:-1]
        return ans

    def execute(self, values):
        res = False
        for clause in self.clauses:
            res = res or clause.execute(values)
        return res


def union_dnf(a, b):
    return DNF([*a.clauses, *b.clauses])


def get_dnf_from_nnf(expr):
    if expr.is_literal:
        ans = DNF([DNF.DNF_Clause([expr.as_literal()])])
        return ans
    left_dnf = get_dnf_from_nnf(expr.left_part)
    right_dnf = get_dnf_from_nnf(expr.right_part)
    ans = []
    if expr.operator == expr_tree.Operator.AND:
        for left_clause in left_dnf.clauses:
            for right_clause in right_dnf.clauses:
                ans.append(left_clause.union(right_clause))
    else:
        ans = union_dnf(left_dnf, right_dnf)
    return ans


def get_dnf_from_expr(expr):
    return get_dnf_from_nnf(get_nnf(expr))
