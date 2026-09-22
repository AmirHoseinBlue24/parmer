import gi

gi.require_version("Atspi", "2.0")

from gi.repository import Atspi


def print_object(obj):
    try:
        if not obj.get_state_set().contains(Atspi.StateType.FOCUSED):
            return

        if not obj.is_text():
            return

        text = obj.get_text()
        caret = obj.get_text_iface().get_caret_offset()

        application = obj.get_application()
        app_name = application.get_name() if application else "Unknown"

        print("\033[2J\033[H", end="")
        print(f"Application : {app_name}")
        print(f"Role        : {obj.get_role_name()}")
        print(f"Name        : {obj.get_name()}")
        print(f"Cursor      : {caret}")
        print("-" * 60)
        print(text)

    except Exception as error:
        print(f"Error: {error}")


def on_event(event):
    print_object(event.source)


Atspi.init()

desktop = Atspi.get_desktop(0)

print("AT-SPI initialized")
print("Applications:")

for i in range(desktop.get_child_count()):
    app = desktop.get_child_at_index(i)

    if app:
        print(f"- {app.get_name()}")

print()
print("Listening for focused text fields...")
print("Press Ctrl+C to exit.")

focus_listener = Atspi.EventListener.new(on_event)
caret_listener = Atspi.EventListener.new(on_event)

focus_listener.register("object:state-changed:focused")
caret_listener.register("object:text-caret-moved")

Atspi.event_main()
