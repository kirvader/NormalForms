class Segment:
    def __init__(self, left, right, priority=False):
        self.left = left
        self.right = right
        self.priority = priority

    def get_substring(self, cur_str):
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


# That function simulates pyparsing style of parsing string into expressions but with a good type and from scratch
# cur_str has to be without any whitespaces
def parse_string(cur_str):
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
        new_str = segments[0].get_substring(cur_str)
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
        for seg in segments:
            if seg == '|':
                ans.append(seg)
                continue
            ans.append(parse_string(seg.get_substring(cur_str)))
        return ans
    if not exist_or:
        ans = []
        for seg in segments:
            if seg == '&':
                ans.append(seg)
                continue
            ans.append(parse_string(seg.get_substring(cur_str)))
        return ans
    ans = []
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
            last_high_priority_block.append(parse_string(seg.get_substring(cur_str)))
            in_and_block = True
        else:
            ans.append(parse_string(seg.get_substring(cur_str)))
    if in_and_block:
        ans.append(last_high_priority_block)
    return ans


# That's the function to call on any string expression
def get_parsed_array(cur_str):
    return parse_string("".join(filter(lambda x: x != ' ', cur_str)))
