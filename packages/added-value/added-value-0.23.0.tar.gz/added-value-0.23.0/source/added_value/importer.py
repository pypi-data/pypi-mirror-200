from more_itertools import unique_everseen
from sphinx.ext.autosummary import import_by_name, ImportExceptionGroup


def import_object(
    obj_name: str,
    context,
):
    """Import a Python object by name.

    Args:
        obj_name (str): The dotted Python name of the object to import.
        context: The context in which the object is being imported. A directive or role.
    """
    try:
        prefixed_name, obj, parent, modname = import_by_name(obj_name)
    except ImportError as e:
        raise context.error(
            f"Could not locate Python object {obj_name} (context: {context.name}) ; {e}."
        )
    except ImportExceptionGroup as e:
        messages = " ; ".join(unique_everseen(map(str, e.exceptions)))
        raise context.error(
            f"Could not locate Python object {obj_name} (context: {context.name}) ; {messages}."
        )
    return obj, prefixed_name
