from added_value.multisort import multisorted, asc, dec, as_is


def test_multisort_with_default_key():
    items = [4, 7, 1, 3, 9, 4, 5, 2]
    assert multisorted(items) == sorted(items)


def test_multisort_with_specified_ascending_key():
    items = [4, 7, 1, 3, 9, 4, 5, 2]
    assert multisorted(items, asc()) == sorted(items)


def test_multisort_with_specified_descending_key():
    items = [4, 7, 1, 3, 9, 4, 5, 2]
    assert multisorted(items, dec()) == sorted(items, reverse=True)


def test_multisort_with_specified_multiple_keys():
    items = ["Hello",
             "Hotel",
             "Hippopotamus",
             "Hero",
             "Hook",
             "Abacus",
             "Angel",
             "Angle",
             "Archway",
             "Arcuate",
             "Amazed"]
    s = sorted(sorted(items, reverse=True), key=len)
    m = multisorted(items, asc(len), dec())
    assert m == s


def test_multisort_with_as_is_preserves_order():
    items = ["Hello",
             "Hotel",
             "Hippopotamus",
             "Hero",
             "Hook",
             "Abacus",
             "Angel",
             "Angle",
             "Archway",
             "Arcuate",
             "Amazed"]
    m = multisorted(items, as_is())
    assert m == items