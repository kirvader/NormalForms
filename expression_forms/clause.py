from expression_forms.expr_tree import Operator


def get_var_from_literal(literal):
    i = 0
    while literal[i] == '-':
        i += 1
    return Var((i % 2 == 1), literal[i:])


class Var:
    def __init__(self, negate, name):
        self.negate = negate
        self.name = name

    def __eq__(self, other):
        return self.negate == other.negate and self.name == other.name

    def __str__(self):
        if self.negate:
            return f"-{self.name}"
        return self.name

    def get_value(self, values):
        return self.negate != values[self.name]


class Clause:
    def __init__(self, operator, literals):
        self.operator = operator
        self.vars = []
        for literal in literals:
            self.vars.append(get_var_from_literal(literal))

    def __str__(self):
        if len(self.vars) == 1:
            return str(self.vars[0])
        ans = "("
        for var in self.vars:
            ans = ans + str(var) + self.operator.value
        ans = ans[:-1]
        ans += ")"
        return ans

    def __eq__(self, other):
        res = (self.operator == other.operator) and (len(self.vars) == len(other.vars))
        if not res:
            return False
        for i in range(len(self.vars)):
            res = res and (self.vars[i] == other.vars[i])
        return res

    def add_var(self, var):
        self.vars.append(var)

    def accum_func(self, a, b):
        if self.operator == Operator.OR:
            return a or b
        elif self.operator == Operator.AND:
            return a and b
        else:
            return a

    def execute(self, values):
        res = self.vars[0].get_value(values)
        for i in range(1, len(self.vars)):
            res = self.accum_func(res, self.vars[i].get_value(values))
