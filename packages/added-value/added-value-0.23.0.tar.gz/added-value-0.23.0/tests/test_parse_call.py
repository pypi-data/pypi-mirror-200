from pytest import raises

from added_value.invoke import parse_call

def test_parse_call_empty_raises_value_error():
    with raises(ValueError, match="Invalid Python identifier: ''"):
        parse_call("")


def test_parse_call_invalid_identifier_raises_value_error():
    with raises(ValueError, match="Invalid Python identifier: '1foo'"):
        parse_call("1foo")


def test_parse_call_valid_identifier_returns_identifier():
    attribute, args = parse_call("foo")
    assert attribute == "foo"
    assert args == ""


def test_parse_call_valid_attribute_returns_attribute():
    attribute, args = parse_call("foo.bar")
    assert attribute == "foo.bar"
    assert args == ""


def test_parse_call_valid_attribute_with_args_returns_attribute_and_args():
    attribute, args = parse_call("foo.bar(1, 2)")
    assert attribute == "foo.bar"
    assert args == "(1, 2)"


def test_parse_call_invalid_syntax_raises_value_error():
    with raises(ValueError, match="Invalid Python identifier: ''"):
        parse_call("foo.bar(1, 2).")


def test_parse_call_with_empty_args_returns_attribute_and_empty_args():
    attribute, args = parse_call("foo.bar()")
    assert attribute == "foo.bar"
    assert args == "()"
