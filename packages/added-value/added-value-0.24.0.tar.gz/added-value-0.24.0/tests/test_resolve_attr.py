from pytest import raises

from added_value.invoke import resolve_attr


def test_resolve_attr_not_callable_raises_type_error():
    with raises(TypeError, match=r"Cannot call non-callable attribute: 1"):
        resolve_attr(1, "()")


def test_resolve_attr_callable_without_args_returns_callable():
    def func():
        pass
    assert resolve_attr(func, "") is func


def test_resolve_attr_callable_with_args_returns_result_of_call():
    def func():
        return 33
    assert resolve_attr(func, "()") == 33


def test_resolve_attr_callable_with_args_returns_result_of_call_with_args():
    def func(a, b):
        return a + b
    assert resolve_attr(func, "(1, 2)") == 3
