from added_value.all_items_role import all_items_role
from added_value.any_items_role import any_items_role
from added_value.format_role import format_role
from added_value.items_list_directive import ItemsListDirective
from added_value.items_table_directive import ItemsTableDirective
from added_value.items_toc_directive import ItemsTableOfContentsDirective
from added_value.literal_block_directive import LiteralBlockDirective
from added_value.literal_repr_role import literal_repr_role
from added_value.literal_str_role import literal_str_role
from added_value.literal_format_role import literal_format_role
from added_value.literal_any_items_role import literal_any_items_role
from added_value.literal_all_items_role import literal_all_items_role
from added_value.str_role import str_role
from added_value.repr_role import repr_role
from added_value.version import __version__


def setup(app):
    if not hasattr(app, "add_config_value"):
        return  # probably called by nose, better bail out

    app.add_role("repr", repr_role)
    app.add_role("str", str_role)
    app.add_role("format", format_role)
    app.add_role("all-items", all_items_role)
    app.add_role("any-items", any_items_role)
    app.add_directive("items-table", ItemsTableDirective)
    app.add_directive("items-list", ItemsListDirective)
    app.add_directive("items-toc", ItemsTableOfContentsDirective)
    app.add_directive("literal-block", LiteralBlockDirective)
    app.add_role("literal-repr", literal_repr_role)
    app.add_role("literal-str", literal_str_role)
    app.add_role("literal-format", literal_format_role)
    app.add_role("literal-any-items", literal_any_items_role)
    app.add_role("literal-all-items", literal_all_items_role)

    return {"version": __version__}
