import expressions, logic

cur_str = input()
expr = expressions.read_expr(cur_str)
expressions.print_left_to_right(expr)
print()
expr.make_nnf()

print("nnf")
expressions.print_left_to_right(expr)


print("\ndnf")
logic.print_dnf_str_appearance(expr)
print("\ncnf")
logic.print_cnf_str_appearance(expr)
