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
args = parser.parse_args()

actions = [
    ('nnf', args.nnf, print_nnf_from_string),
    ('cnf', args.cnf, print_cnf_from_string),
    ('dnf', args.dnf, print_dnf_from_string),
]

show_all = False
if not (args.nnf or args.dnf or args.cnf):
    show_all = True

print('I have received this expression:')
print_expr_tree_from_string(args.input)
print('And there are chosen normal forms:\n')

for action in actions:
    if show_all or action[1]:
        print(f"{action[0]}: ", end='')
        action[2](args.input)
