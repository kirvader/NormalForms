from parsers.array_to_expr_parser import get_expr_from_parsed_array
from parsers.string_to_array_parser import get_parsed_array


def print_expr_tree_from_string(string):
    print(get_expr_from_parsed_array(get_parsed_array(string)))

