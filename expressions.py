from enum import Enum


class Segment:
    def __init__(self, left, right, priority=False):
        self.left = left
        self.right = right
        self.priority = priority

    def get_substr(self, cur_str):
        return cur_str[self.left:(self.right + 1)]

    def move_edges_by_brackets(self, cur_str):
        negate_count = self.count_negates(cur_str)
        self.left += negate_count  # only brackets or var
        if cur_str[self.left] == '(' and cur_str[self.right] == ')':
            self.left += 1
            self.right -= 1

    def count_negates(self, cur_str):
        res = 0
        while self.left + res <= self.right and cur_str[res] == '-':
            res += 1
        return res


def is_var(cur_str):
    return ('&' not in cur_str) \
           and ('|' not in cur_str) \
           and ('-' not in cur_str) \
           and ('(' not in cur_str) \
           and (')' not in cur_str)


def parse_string(cur_str):
    # no ws
    exist_and = False
    exist_or = False
    segments = []
    next_segment = Segment(0, -1)
    balance = 0
    for i in range(len(cur_str)):
        c = cur_str[i]
        if c == '(':
            balance += 1
            continue
        elif c == ')':
            balance -= 1
            next_segment.right = i
            continue

        if balance != 0:
            continue
        if c == '-':
            continue
        if c == '&':
            exist_and = True
            next_segment.priority = True
            segments.append(next_segment)
            segments.append(c)
            next_segment = Segment(i + 1, i, True)
            continue
        if c == '|':
            exist_or = True
            segments.append(next_segment)
            segments.append(c)
            next_segment = Segment(i + 1, i, False)
            continue
        next_segment.right = i
    segments.append(next_segment)
    if not exist_or and not exist_and:
        negate_count = segments[0].count_negates(cur_str)
        segments[0].move_edges_by_brackets(cur_str)
        ans = []
        if negate_count % 2 == 1:
            ans.append('-')
        print("1" + cur_str)
        new_str = segments[0].get_substr(cur_str)
        if is_var(new_str):
            if len(ans) != 0:
                ans.append(new_str)
                return ans
            return new_str
        else:
            ans.append(parse_string(new_str))
        return ans
    if not exist_and:
        ans = []
        print("2" + cur_str)
        for seg in segments:
            if seg == '|':
                ans.append(seg)
                continue
            ans.append(parse_string(seg.get_substr(cur_str)))
        return ans
    if not exist_or:
        ans = []
        print("3" + cur_str)
        for seg in segments:
            if seg == '&':
                ans.append(seg)
                continue
            ans.append(parse_string(seg.get_substr(cur_str)))
        return ans
    ans = []
    print("4" + cur_str)
    last_high_priority_block = []
    in_and_block = False
    for seg in segments:
        if seg == '&':
            last_high_priority_block.append('&')
            continue
        if seg == '|':
            if in_and_block:
                ans.append(last_high_priority_block)
                last_high_priority_block = []
            ans.append('|')
            in_and_block = False
            continue
        if seg.priority:
            last_high_priority_block.append(parse_string(seg.get_substr(cur_str)))
            in_and_block = True
        else:
            ans.append(parse_string(seg.get_substr(cur_str)))
    if in_and_block:
        ans.append(last_high_priority_block)
    return ans


class ExprTree:
    class Operator(Enum):
        NONE = ''
        OR = '|'
        AND = '&'

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

    def invertOperator(self):
        if self.operator == ExprTree.Operator.NONE:
            pass
        if self.operator == ExprTree.Operator.AND:
            self.operator = ExprTree.Operator.OR
        elif self.operator == ExprTree.Operator.OR:
            self.operator = ExprTree.Operator.AND

    def make_nnf(self):
        if self.left_part is None and self.right_part is None:
            pass
        if self.negate and self.operator != ExprTree.Operator.NONE:
            self.invertOperator()
            self.invert_negate()
            self.left_part.invert_negate()
            self.right_part.invert_negate()
        if not (self.left_part is None):
            self.left_part.make_nnf()
        if not (self.right_part is None):
            self.right_part.make_nnf()


def get_parsed_array(cur_str):
    return parse_string("".join(filter(lambda x: x != ' ', cur_str)))


def get_expr_from_parsed_array(mb_arr):
    if not isinstance(mb_arr, list):
        return ExprTree(label=mb_arr, is_literal=True)
    if len(mb_arr) == 2 and mb_arr[0] == '-':
        cur_expr = get_expr_from_parsed_array(mb_arr[1])
        cur_expr.invert_negate()
        return cur_expr

    left_part = None
    operator = ExprTree.Operator.NONE
    for part in mb_arr:
        if part == '&':
            operator = ExprTree.Operator.AND
        elif part == '|':
            operator = ExprTree.Operator.OR
        else:
            if left_part is None:
                left_part = get_expr_from_parsed_array(part)
            else:
                left_part = ExprTree(left_part=left_part, right_part=get_expr_from_parsed_array(part),
                                     operator=operator)
            operator = ExprTree.Operator.NONE
    return left_part


def read_expr(string):
    return get_expr_from_parsed_array(get_parsed_array(string))


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
    if expr.operator != ExprTree.Operator.NONE:
        print(expr.operator.value, end='')
    else:
        print(expr.label, end='')
    print_left_to_right(expr.right_part)
    print(')', end='')



