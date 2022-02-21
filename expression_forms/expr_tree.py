from enum import Enum


class Operator(Enum):
    NONE = ''
    OR = '|'
    AND = '&'


class ExprTree:
    number_by_var = {}
    var_by_number = []

    last_auxiliary_number = -1

    def __init__(self, negate=False, left_part=None, right_part=None, operator=Operator.NONE, label="",
                 is_literal=False):
        self.negate = negate
        self.operator = operator
        self.left_part = left_part
        self.right_part = right_part
        self.label = label
        if label == "":
            ExprTree.last_auxiliary_number += 1
            self.label = 't' + str(ExprTree.last_auxiliary_number)
        self.is_literal = is_literal

    def as_literal(self):
        if self.negate:
            return '-' + self.label
        return self.label

    def invert_negate(self):
        self.negate = not self.negate

    def invert_operator(self):
        if self.operator == Operator.NONE:
            pass
        if self.operator == Operator.AND:
            self.operator = Operator.OR
        elif self.operator == Operator.OR:
            self.operator = Operator.AND

    def make_nnf(self):
        if self.left_part is None and self.right_part is None:
            pass
        if self.negate and self.operator != Operator.NONE:
            self.invert_operator()
            self.invert_negate()
            self.left_part.invert_negate()
            self.right_part.invert_negate()
        if not (self.left_part is None):
            self.left_part.make_nnf()
        if not (self.right_part is None):
            self.right_part.make_nnf()
