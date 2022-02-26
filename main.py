import argparse

from writers.expr_tree_writer import print_expr_tree_from_string
from writers.nf_writer import print_nnf_from_string, print_cnf_from_string, print_dnf_from_string

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input expression")
parser.add_argument("--nnf", help="when checked outputs negative normal form",
                    action="store_true")
parser.add_argument("--cnf", help="when checked outputs conjunctive normal form",
                    action="store_true")
parser.add_argument("--dnf", help="when checked outputs disjunctive normal form",
                    action="store_true")
parser.add_argument("--verbose", help="Show all info about input and all forms",
                    action="store_true")
args = parser.parse_args()

actions = [
    (args.nnf, print_nnf_from_string),
    (args.cnf, print_cnf_from_string),
    (args.dnf, print_dnf_from_string),
]

if args.verbose:
    print('I have received this expression:')
    print_expr_tree_from_string(args.input)
    print('And there are chosen normal forms:\n')

for action in actions:
    if args.verbose or action[0]:
        action[1](args.input)
