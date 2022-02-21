from expression_forms.cnf import get_cnf_from_expr
from expression_forms.dnf import get_dnf_from_expr
from expression_forms.nnf import get_nnf
from parsers.array_to_expr_parser import get_expr_from_parsed_array
from parsers.string_to_array_parser import get_parsed_array
from writers.expr_tree_writer import print_expr_tree


def print_nnf_from_string(string):
    print_expr_tree(get_nnf(get_expr_from_parsed_array(get_parsed_array(string))))


def print_cnf_from_string(string):
    print(get_cnf_from_expr(get_expr_from_parsed_array(get_parsed_array(string))))


def print_dnf_from_string(string):
    print(get_dnf_from_expr((get_expr_from_parsed_array(get_parsed_array(string)))))
