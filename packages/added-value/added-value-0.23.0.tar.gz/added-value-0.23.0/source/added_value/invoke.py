def parse_call(text: str) -> tuple[str, str]:
    """Parse a string containing a reference to a Python attribute or invocation thereof.

    Args:
        text: The text to parse. e.g. "foo.bar.baz" or "foo.bar.baz(1, 2)"

    Returns:
        A tuple of the form (attribute, args) where attribute is the attribute name and args is the
        argument list, if any. e.g. ("foo.bar.baz", "") or ("foo.bar.baz", "(1, 2)")

    """
    *parts, last = text.split(".")


    identifier, paren, tail = last.partition("(")

    if paren and not tail.endswith(")"):
        raise ValueError(f"Invalid Python call: {text!r}")

    if not identifier.isidentifier():
        raise ValueError(f"Invalid Python identifier: {identifier!r}")

    args = paren + tail if paren else ""
    attribute = ".".join(parts + [identifier])

    return attribute, args


def resolve_attr(attr, args: str):
    """Resolve a Python attribute, optionally invoking it with the given arguments.

    """
    if not args:
        return attr

    if not callable(attr):
        raise TypeError(f"Cannot call non-callable attribute: {attr!r}")

    return eval(f"func{args}", {"func": attr}, {})
