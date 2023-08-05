from hypothesis import given
from hypothesis.strategies import sets, integers
from pytest import raises

from added_value.toposet import TopoSet
from added_value.util import pairwise


def test_default_constructed_toposet_is_empty():
    t = TopoSet()
    assert len(t) == 0


def test_default_constructed_toposet_contains_no_items():
    t = TopoSet()
    assert list(t) == []


@given(sets(integers()).map(list))
def test_toposet_constructed_from_iterable_without_duplicates_has_same_length(items):
    t = TopoSet(items)
    assert list(t) == items

@given(sets(integers()).map(list))
def test_toposet_updated_from_iterable_without_duplicates_has_same_length(items):
    t = TopoSet()
    t.update(items)
    assert list(t) == items

@given(sets(integers()).map(list))
def test_toposet_updated_from_iterable_without_duplicates_has_same_length(items):
    t = TopoSet()
    for item in items:
        t.add(item)
    assert list(t) == items

@given(sets(integers()).map(list))
def test_toposet_eliminates_duplicates(items):
    t = TopoSet(items)
    t.update(items)
    assert list(t) == items

@given(item=integers(), size=integers(min_value=1, max_value=10))
def test_toposet_construction_eliminates_duplicates(item, size):
    t = TopoSet([item] * size)
    assert list(t) == [item]

@given(sets(integers()))
def test_toposet_with_items_added_from_a_set_is_equal_to_the_set(items):
    t = TopoSet()
    for item in items:
        t.add(item)
    assert t == items

@given(a=sets(integers()), b=sets(integers()))
def test_containment_positive(a, b):
    included = a - b
    t = TopoSet(included)
    assert all(item in t for item in included)

@given(a=sets(integers()), b=sets(integers()))
def test_containment_negative(a, b):
    included = a - b
    excluded = b - a
    t = TopoSet(included)
    assert all(not (item in t) for item in excluded)

@given(a=sets(integers()), b=sets(integers()))
def test_non_containment_positive(a, b):
    included = a - b
    excluded = b - a
    t = TopoSet(included)
    assert all(item not in t for item in excluded)

@given(a=sets(integers()), b=sets(integers()))
def test_non_containment_negative(a, b):
    included = a - b
    t = TopoSet(included)
    assert all(not (item not in t) for item in included)

@given(a=sets(integers()))
def test_discarding_all_elements_results_in_an_empty_set(a):
    t = TopoSet(a)
    for item in a:
        t.discard(item)
    assert len(t) == 0

@given(a=sets(integers()))
def test_discard_only_removes_one_element(a):
    t = TopoSet(a)
    sizes = [len(t)]
    for item in a:
        t.discard(item)
        sizes.append(len(t))
    assert all(a == b+1 for a, b in pairwise(sizes))

@given(a=sets(integers(), min_size=1))
def test_discarding_an_item_not_present_silently_succeeds(a):
    b = max(a) + 1
    t = TopoSet(a)
    t.discard(b)

@given(a=sets(integers(), min_size=1))
def test_removing_an_item_not_present_silently_succeeds(a):
    b = max(a) + 1
    t = TopoSet(a)
    with raises(KeyError):
        t.remove(b)

