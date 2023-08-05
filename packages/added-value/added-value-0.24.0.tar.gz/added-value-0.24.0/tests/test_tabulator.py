from pytest import raises

from added_value.multisort import asc, dec
from added_value.tabulator import tabulate, validate_level_indexes

a = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12],
]

b = [
    [[5, 6], [1, 9], [3, 5]],
    [[7, 2], [4], [5, 6]],
    [[7, 8], [9, 3],],
    [[1, 9], [2, 9], [3, 6]],
]

c = {
    'alpha': 5,
    'bravo': 5,
    'charlie': 6,
    'delta': 5,
    'foxtrot': 6,
    'golf': 4,
}

d = {
    'alpha': "Fox base alpha".split(),
    'bravo': "Rio bravo".split(),
    'charlie': "Charlie says".split(),
    'delta': "Concorde has a delta wing".split(),
    'foxtrot': "The foxtrot was a popular dance".split(),
    'golf': "Golf spoils a walk in the countryside".split(),
}

e = [
    {'set': 3,
     'pour': 4,
     'serve': 5
     },
    {'serve': 19,
     'set': 12,
     'volley': 9
     },
    {'set': 98,
     'pour': 1,
     'cast': 14
     },
    {'cast': 34,
     'line': 18,
     'fish':8
     }
]


def test_tabulate_list_of_dicts_with_keys_zero_and_one_on_the_vertical_axis_has_three_columns():
    table = tabulate(e, [0, 1], [])
    assert len(table[0]) == 3

def test_tabulate_list_of_dicts_with_keys_zero_and_one_on_the_vertical_axis_has_twelve_rows():
    table = tabulate(e, [0, 1], [])
    assert len(table) == 12

def test_tabulate_list_of_dicts_with_keys_zero_and_one_on_the_vertical_axis_has_expected_column_0():
    table = tabulate(e, [0, 1], [])
    assert all(row[0] in range(4) for row in table)

def test_tabulate_list_of_dicts_with_keys_zero_and_one_on_the_vertical_axis_has_expected_column_1():
    table = tabulate(e, [0, 1], [])
    assert all(row[1] in {'set', 'pour', 'serve', 'volley', 'cast', 'line', 'fish'} for row in table)

# TODO: Test hiding indexes

def test_tabulate_list_of_dicts_sorted_ascending_by_columns_1_and_ascending_by_column_2():
    actual = tabulate(e, [0, 1], [], v_level_sort_keys=(asc(), asc()))
    expected = [
        [0, 'pour', 4],
        [0, 'serve', 5],
        [0, 'set', 3],
        [1, 'serve', 19],
        [1, 'set', 12],
        [1, 'volley', 9],
        [2, 'cast', 14],
        [2, 'pour', 1],
        [2, 'set', 98],
        [3, 'cast', 34],
        [3, 'fish', 8],
        [3, 'line', 18]
    ]
    assert actual == expected


def test_tabulate_list_of_dicts_sorted_descending_by_columns_1_and_ascending_by_column_2():
    actual = tabulate(e, [0, 1], [], v_level_sort_keys=(dec(), asc()))
    expected = [
        [3, 'cast', 34],
        [3, 'fish', 8],
        [3, 'line', 18],
        [2, 'cast', 14],
        [2, 'pour', 1],
        [2, 'set', 98],
        [1, 'serve', 19],
        [1, 'set', 12],
        [1, 'volley', 9],
        [0, 'pour', 4],
        [0, 'serve', 5],
        [0, 'set', 3]
    ]
    assert actual == expected


def test_tabulate_list_of_dicts_sorted_ascending_by_columns_1_and_descending_by_column_2():
    actual = tabulate(e, [0, 1], [], v_level_sort_keys=(asc(), dec()))
    expected = [
        [0, 'set', 3],
        [0, 'serve', 5],
        [0, 'pour', 4],
        [1, 'volley', 9],
        [1, 'set', 12],
        [1, 'serve', 19],
        [2, 'set', 98],
        [2, 'pour', 1],
        [2, 'cast', 14],
        [3, 'line', 18],
        [3, 'fish', 8],
        [3, 'cast', 34]
    ]
    assert actual == expected


def test_tabulate_list_of_dicts_sorted_descending_by_columns_1_and_descending_by_column_2():
    actual = tabulate(e, [0, 1], [], v_level_sort_keys=(dec(), dec()))
    expected = [
        [3, 'line', 18],
        [3, 'fish', 8],
        [3, 'cast', 34],
        [2, 'set', 98],
        [2, 'pour', 1],
        [2, 'cast', 14],
        [1, 'volley', 9],
        [1, 'set', 12],
        [1, 'serve', 19],
        [0, 'set', 3],
        [0, 'serve', 5],
        [0, 'pour', 4]
    ]
    assert actual == expected


# TODO: str/repr/format of cells.
# TODO: Formatting of heterogeneous tuples e.g. ("Norway", 345, 12.45)  Maybe a sort of x-path syntax?

def test_validate_level_indexes_with_num_levels_less_than_zero_raises_value_error():
    with raises(ValueError):
        validate_level_indexes(-1, None, None)


def test_validate_level_indexes_with_with_num_levels_equal_to_one():
    v_level_indexes, h_level_indexes = validate_level_indexes(1, None, None)
    assert list(v_level_indexes) == [0]
    assert list(h_level_indexes) == []


def test_validate_level_indexes_with_with_num_levels_equal_to_two():
    v_level_indexes, h_level_indexes = validate_level_indexes(2, None, None)
    assert list(v_level_indexes) == [0]
    assert list(h_level_indexes) == [1]

def test_validate_level_indexes_with_with_num_levels_equal_to_three():
    v_level_indexes, h_level_indexes = validate_level_indexes(3, None, None)
    assert list(v_level_indexes) == [0, 2]
    assert list(h_level_indexes) == [1]

def test_validate_level_indexes_with_with_num_levels_equal_to_four():
    v_level_indexes, h_level_indexes = validate_level_indexes(4, None, None)
    assert list(v_level_indexes) == [0, 2]
    assert list(h_level_indexes) == [1, 3]

def test_validate_level_indexes_with_with_num_levels_equal_to_five():
    v_level_indexes, h_level_indexes = validate_level_indexes(5, None, None)
    assert list(v_level_indexes) == [0, 2, 4]
    assert list(h_level_indexes) == [1, 3]

def test_validate_level_indexes_with_only_v_level_indexes_provided():
    v_level_indexes, h_level_indexes = validate_level_indexes(5, [0, 1, 2, 3, 4], None)
    assert list(v_level_indexes) == [0, 1, 2, 3, 4]
    assert list(h_level_indexes) == []

def test_validate_level_indexes_with_only_h_level_indexes_provided():
    v_level_indexes, h_level_indexes = validate_level_indexes(5, None, [0, 1, 2, 3, 4])
    assert list(v_level_indexes) == []
    assert list(h_level_indexes) == [0, 1, 2, 3, 4]

def test_validate_level_indexes_with_mixed_indexes_provided():
    v_level_indexes, h_level_indexes = validate_level_indexes(5, [0, 1, 2], [3, 4])
    assert list(v_level_indexes) == [0, 1, 2]
    assert list(h_level_indexes) == [3, 4]

def test_validate_level_indexes_with_alternate_indexes_provided():
    v_level_indexes, h_level_indexes = validate_level_indexes(5, [0, 2, 4], [1, 3])
    assert list(v_level_indexes) == [0, 2, 4]
    assert list(h_level_indexes) == [1, 3]

def test_validate_level_indexes_with_reordered_indexes_provided():
    v_level_indexes, h_level_indexes = validate_level_indexes(5, [4, 1, 3], [0, 2])
    assert list(v_level_indexes) == [4, 1, 3]
    assert list(h_level_indexes) == [0, 2]

def test_validate_level_indexes_missing_v_level_index():
    with raises(ValueError):
        validate_level_indexes(5, [4, 3], [0, 2])

def test_validate_level_indexes_missing_h_level_index():
    with raises(ValueError):
        validate_level_indexes(5, [4, 1, 3], [0])

def test_validate_level_indexes_duplicate_v_level_index():
    with raises(ValueError):
        validate_level_indexes(5, [4, 1, 1, 3], [0, 2])

def test_validate_level_indexes_duplicate_h_level_index():
    with raises(ValueError):
        validate_level_indexes(5, [4, 1,3], [0, 0, 2])

def test_validate_level_indexes_duplicate_v_and_h_level_indexes_are_not_disjoint():
    with raises(ValueError):
        validate_level_indexes(5, [4, 1, 3], [0, 1, 2])

def test_validate_level_indexes_duplicate_v_level_index_is_out_of_lower_range():
    with raises(ValueError):
        validate_level_indexes(5, [4, 1, -1], [0, 2])

def test_validate_level_indexes_duplicate_v_level_index_is_out_of_upper_range():
    with raises(ValueError):
        validate_level_indexes(5, [4, 1, 5], [0, 2])

def test_validate_level_indexes_duplicate_h_level_index_is_out_of_lower_range():
    with raises(ValueError):
        validate_level_indexes(5, [4, 1, 3], [-1, 2])

def test_validate_level_indexes_duplicate_h_level_index_is_out_of_upper_range():
    with raises(ValueError):
        validate_level_indexes(5, [4, 1, 3], [0, 5])
