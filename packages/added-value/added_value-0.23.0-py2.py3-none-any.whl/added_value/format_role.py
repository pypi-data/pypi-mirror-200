from docutils import nodes
from sphinx.ext.autosummary import import_by_name

from added_value.pyobj_role import formatted_role


def format_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """Include Python object value, rendering it to text using str.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param make_node: A callable which accepts (rawtext, app, prefixed_name, obj, parent, modname, options) and which returns a node
    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    return formatted_role(
        make_node=lambda text, rawsource: nodes.Text(text, rawsource=rawsource),
        inliner=inliner,
        rawtext=rawtext,
        text=text,
        lineno=lineno
    )
