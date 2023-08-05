from docutils import nodes

from added_value.grammatical_conjunctions import list_conjunction, list_conjunction_parts
from added_value.pyobj_role import make_pyobj_role


def make_literal_any_items_node(rawtext, app, prefixed_name, obj, parent, modname, options):
    """Render a Python sequence as a comma-separated list, with an "or" for the final item.

    :param rawtext: Text being replaced with link node.
    :param app: Sphinx application context
    :param prefixed_name: The dotted Python name for obj.
    :param obj: The Python object to be rendered to text.
    :param parent: The parent Python object of obj.
    :param module: The name of the module containing obj.
    :param options: Options dictionary passed to role func.
    """
    new_nodes = list_conjunction_parts(
        list(obj),
        separator=", ",
        conjunction=" or ",
        separator_factory=lambda o: nodes.Text(str(o)),
        item_factory=lambda o: nodes.literal(text=str(o))

    )
    return new_nodes


literal_any_items_role = make_pyobj_role(make_literal_any_items_node)
