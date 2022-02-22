from expression_forms.expr_tree import Operator
from parsers.array_to_expr_parser import get_expr_from_parsed_array
from parsers.string_to_array_parser import get_parsed_array


def get_string_repr(expr):
    ans = ""
    if expr.invert_negate:
        ans += '-'
    if expr.left_part is None and expr.right_part is None:
        ans = ans + expr.label
    else:
        ans += '(' + get_string_repr(expr.left_part) + expr.operator.value + get_string_repr(expr.right_part) + ')'
    return ans


def print_left_to_right(expr):
    if expr is None:
        return
    if expr.negate:
        print('-', end='')
    print('(', end='')
    print_left_to_right(expr.left_part)
    if expr.operator != Operator.NONE:
        print(expr.operator.value, end='')
    else:
        print(expr.label, end='')
    print_left_to_right(expr.right_part)
    print(')', end='')


def print_expr_tree_from_string(string):
    print(get_expr_from_parsed_array(get_parsed_array(string)))

