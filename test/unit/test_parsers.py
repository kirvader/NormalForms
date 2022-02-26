import copy
import pytest

import conftest as config
from parsers.array_to_expr_parser import get_expr_from_parsed_array
from parsers.string_to_array_parser import is_var, Segment, get_parsed_array


@pytest.mark.parametrize("raw_string,segment,substring,moved_to_brackets_segment,negates_count",
                         [
                             ("a", Segment(0, 0), "a", Segment(0, 0), 0),
                             ("-b", Segment(0, 1), "-b", Segment(0, 1), 1),
                             ("-b", Segment(1, 1), "b", Segment(1, 1), 0),
                             ("a&b", Segment(0, 2), "a&b", Segment(0, 2), 0),
                             ("-a&b", Segment(0, 3), "-a&b", Segment(0, 3), 1),
                             ("(-a&b)", Segment(0, 5), "(-a&b)", Segment(1, 4), 0),
                         ])
class TestSegments:
    def test_substring_taking(self, raw_string, segment, substring, moved_to_brackets_segment, negates_count):
        assert (segment.get_substring(raw_string) == substring)

    def test_moving_brackets(self, raw_string, segment, substring, moved_to_brackets_segment, negates_count):
        new_seg = copy.deepcopy(segment)
        new_seg.move_edges_by_brackets(raw_string)
        print(f"there is test left: {new_seg}")
        print(f"{str(new_seg.left)} == {str(moved_to_brackets_segment.left)}")
        assert (new_seg == moved_to_brackets_segment)

    def test_count_negates(self, raw_string, segment, substring, moved_to_brackets_segment, negates_count):
        assert (segment.count_negates(raw_string) == negates_count)


class TestParsers:
    @pytest.mark.parametrize("raw_string,result",
                             [
                                 ("a", ["a"]),
                                 ("ab", ["ab"]),
                                 ("a&b", ["a", "&", "b"]),
                                 ("-a&b", [["-", "a"], "&", "b"]),
                                 ("a&-b", ["a", "&", ["-", "b"]]),
                                 ("a|c", ["a", "|", "c"]),
                                 ("a|b|c", ["a", "|", "b", "|", "c"]),
                                 ("a|b&c", ["a", "|", ["b", "&", "c"]]),
                                 ("(a|b)&c", [["a", "|", "b"], "&", "c"]),
                                 ("a|(b|c)&d", ["a", "|", [["b", "|", "c"], "&", "d"]])
                             ])
    def test_string_to_array_parser(self, raw_string, result):
        assert (get_parsed_array(raw_string) == result)

    @pytest.mark.parametrize("raw_string,result",
                             [
                                 ("a", True),
                                 ("ab", True),
                                 ("-c", False),
                                 ("a&b", False),
                                 ("-a&b", False),
                                 ("a&-b", False),
                                 ("a|c", False),
                                 ("a|b|c", False),
                                 ("a|b&c", False),
                                 ("(a|b)&c", False),
                                 ("a|(b|c)&d", False)
                             ])
    def test_is_var(self, raw_string, result):
        assert (is_var(raw_string) == result)

    @pytest.mark.parametrize("raw_array,result",
                             [
                                 (["a"], config.a),
                                 ([["-", "a"], "&", "b"], config.not_a_and_b),
                                 (["a", "|", "b"], config.a_or_b),
                                 (["a", "|", "b", "|", "c"], config.a_or_b_or_c),
                                 (["a", "|", ["b", "&", "c"]], config.a_or_b_and_c),
                                 ([["a", "|", "b"], "&", "c"], config.a_or_b_and_c_ordered),
                                 (["a", "|", [["a", "|", "b"], "&", "c"]], config.a_or_b_or_c_and_d_ordered)
                             ])
    def test_array_to_expr_parser(self, raw_array, result):
        assert (get_expr_from_parsed_array(raw_array) == result)
