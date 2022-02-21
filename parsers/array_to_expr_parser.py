from expression_forms.expr_tree import ExprTree, Operator
from parsers.string_to_array_parser import get_parsed_array


def get_expr_from_parsed_array(mb_arr):
    if not isinstance(mb_arr, list):
        return ExprTree(label=mb_arr, is_literal=True)
    if len(mb_arr) == 2 and mb_arr[0] == '-':
        cur_expr = get_expr_from_parsed_array(mb_arr[1])
        cur_expr.invert_negate()
        return cur_expr

    left_part = None
    operator = Operator.NONE
    for part in mb_arr:
        if part == '&':
            operator = Operator.AND
        elif part == '|':
            operator = Operator.OR
        else:
            if left_part is None:
                left_part = get_expr_from_parsed_array(part)
            else:
                left_part = ExprTree(left_part=left_part, right_part=get_expr_from_parsed_array(part),
                                     operator=operator)
            operator = Operator.NONE
    return left_part


def get_expr_tree_from_string(string):
    return get_expr_from_parsed_array(get_parsed_array(string))