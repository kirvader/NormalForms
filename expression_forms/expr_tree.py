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

    def __eq__(self, other):
        if self.is_literal and other.is_literal:
            return self.as_literal() == other.as_literal()

        return (self.is_literal == other.is_literal) and \
               (self.negate == other.negate) and \
               (self.operator == other.operator) and \
               (self.left_part == other.left_part) and \
               (self.right_part == other.right_part)

    def _left_part_need_brackets(self):
        if self.left_part.is_literal:
            return False
        if self.left_part.negate:
            return False
        if self.left_part.operator == Operator.AND:
            return False
        if self.operator == Operator.OR:
            return False
        return True

    def _right_part_need_brackets(self):
        if self.right_part.is_literal:
            return False
        if self.right_part.negate:
            return False
        if self.right_part.operator == Operator.AND:
            return False
        if self.operator == Operator.OR:
            return False
        return True

    def __str__(self):
        if self.is_literal:
            return self.as_literal()
        ans = ''
        if self.negate:
            ans += '-('
        if self._left_part_need_brackets():
            ans += '(' + str(self.left_part) + ')'
        else:
            ans += str(self.left_part)
        ans += str(self.operator.value)
        if self._right_part_need_brackets():
            ans += '(' + str(self.right_part) + ')'
        else:
            ans += str(self.right_part)
        if self.negate:
            ans += ')'
        return ans

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
