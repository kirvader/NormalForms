from expression_forms.expr_tree import ExprTree, Operator

a = ExprTree(label="a", is_literal=True)
not_a = ExprTree(label="a", is_literal=True, negate=True)
b = ExprTree(label="b", is_literal=True)
c = ExprTree(label="c", is_literal=True)
not_a_and_b = ExprTree(left_part=not_a, right_part=b, operator=Operator.AND)
a_or_b = ExprTree(left_part=a, right_part=b, operator=Operator.OR)
a_or_b_or_c = ExprTree(left_part=a_or_b, right_part=c, operator=Operator.OR)
b_and_c = ExprTree(left_part=b, right_part=c, operator=Operator.AND)
b_or_c = ExprTree(left_part=b, right_part=c, operator=Operator.OR)
a_or_b_and_c = ExprTree(left_part=a, right_part=b_and_c, operator=Operator.OR)
a_or_b_and_c_ordered = ExprTree(left_part=a_or_b, right_part=c, operator=Operator.AND)
a_or_b_or_c_and_d_ordered = ExprTree(left_part=a, right_part=a_or_b_and_c_ordered, operator=Operator.OR)
