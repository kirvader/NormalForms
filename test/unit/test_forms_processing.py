import pytest

from expression_forms.cnf import get_cnf_from_expr
from expression_forms.dnf import get_dnf_from_expr
from expression_forms.nnf import get_nnf
from parsers.array_to_expr_parser import get_expr_tree_from_string


class TestForms:
    @pytest.mark.parametrize(
        "input_expr,output",
        [
            ("a|(b|c)&d", "a|(b|c)&d"),
            ("(a|b)&c", "(a|b)&c"),
            ("a|-(b&c)", "a|-b|-c"),
            ("a|b|c", "a|b|c"),
            ("-a&b", "-a&b"),
            ("-a", "-a"),
            ("-(a&b)|-(a|c)", "-a|-b|-a&-c"),
            ("-(a&-(b|-(c&d)))", "-a|b|-c|-d")
        ]
    )
    def test_nnf(self, input_expr, output):
        assert (str(get_nnf(get_expr_tree_from_string(input_expr))) == output)

    # CNF has static members so it can affect new tests
    @pytest.mark.parametrize(
        "input_expr,output",
        [
            ("a|(b|c)&d", "t26&(-t26|a|t25)&(t26|-a)&(t26|-t25)&(t25|-t24|-d)&(-t25|t24)&(-t25|d)&(-t24|b|c)&(t24|-b)&(t24|-c)"),
            ("(a|b)&c", "t28&(t28|-t27|-c)&(-t28|t27)&(-t28|c)&(-t27|a|b)&(t27|-a)&(t27|-b)"),
            ("a|-(b&c)", "t30&(-t30|a|t29)&(t30|-a)&(t30|-t29)&(-t29|-b|-c)&(t29|b)&(t29|c)"),
            ("a|b|c", "t32&(-t32|t31|c)&(t32|-t31)&(t32|-c)&(-t31|a|b)&(t31|-a)&(t31|-b)"),
            ("-a&b", "t33&(t33|a|-b)&(-t33|-a)&(-t33|b)"),
            ("-a", "-a"),
            ("-(a&b)|-(a|c)", "t36&(-t36|t34|t35)&(t36|-t34)&(t36|-t35)&(-t34|-a|-b)&(t34|a)&(t34|b)&(t35|a|c)&(-t35|-a)&(-t35|-c)"),
            ("-(a&-(b|-(c&d)))", "-t39&(-t39|-a|t38)&(t39|a)&(t39|-t38)&(-t38|b|t37)&(t38|-b)&(t38|-t37)&(-t37|-c|-d)&(t37|c)&(t37|d)")
        ]
    )
    def test_cnf(self, input_expr, output):
        assert (str(get_cnf_from_expr(get_expr_tree_from_string(input_expr))) == output)

    # CNF has static members so it can affect new tests
    @pytest.mark.parametrize(
        "input_expr,output",
        [
            ("a|(b|c)&d", "a|(b&d)|(c&d)"),
            ("(a|b)&c", "(a&c)|(b&c)"),
            ("a|-(b&c)", "a|-b|-c"),
            ("a|b|c", "a|b|c"),
            ("-a&b", "(-a&b)"),
            ("-a", "-a"),
            ("-(a&b)|-(a|c)", "-a|-b|(-a&-c)"),
            ("-(a&-(b|-(c&d)))", "-a|b|-c|-d")
        ]
    )
    def test_dnf(self, input_expr, output):
        assert (str(get_dnf_from_expr(get_expr_tree_from_string(input_expr))) == output)
