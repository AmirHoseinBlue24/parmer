import gi

gi.require_version("Atspi", "2.0")

from gi.repository import Atspi


editable_roles = (
    Atspi.Role.ENTRY,
    Atspi.Role.TEXT,
    Atspi.Role.COMBO_BOX,
    Atspi.Role.DOCUMENT_FRAME,
    Atspi.Role.DOCUMENT_WEB,
)


def is_text_field(obj):
    try:
        role = obj.get_role()
    except Exception:
        return False

    return role in editable_roles
