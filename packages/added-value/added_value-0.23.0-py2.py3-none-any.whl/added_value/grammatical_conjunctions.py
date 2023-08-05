from les_iterables import separate_with


def list_conjunction(sequence, conjunction):
    return "".join(
        list_conjunction_parts(
            items=sequence,
            separator=", ",
            conjunction=f" {conjunction} ",
        )
    )


def list_conjunction_parts(items, separator, conjunction, item_factory=str, separator_factory=str):
    if len(items) == 0:
        parts = []
    elif len(items) == 1:
        parts = [item_factory(items[0])]
    elif len(items) == 2:
        parts = [
            item_factory(items[0]),
            separator_factory(conjunction),
            item_factory(items[1])
        ]
    else:
        parts = [
            *separate_with(
                map(item_factory, items[:-1]),
                separator_factory(separator)
            ),
            separator_factory(conjunction),
            item_factory(items[-1])
        ]
    return parts

