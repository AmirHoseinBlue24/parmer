import gi

gi.require_version("Atspi", "2.0")

from gi.repository import Atspi

from accessibility.focus import should_handle

from accessibility.text import is_text_field

from core.text_tracker import TextTracker


tracker = TextTracker()


def on_event(event):
    try:
        if not should_handle(event):
            return

        obj = event.source

        if obj is None:
            return

        if not is_text_field(obj):
            return

        changed = tracker.update(obj)

        if changed:
            tracker.print(event.type)

    except Exception as error:
        print(f"AT-SPI error: {error}")


Atspi.init()

focus_listener = Atspi.EventListener.new(on_event)
caret_listener = Atspi.EventListener.new(on_event)
text_listener = Atspi.EventListener.new(on_event)

focus_listener.register(
    "object:state-changed:focused"
)

caret_listener.register(
    "object:text-caret-moved"
)

text_listener.register(
    "object:text-changed"
)

print("Parmer AT-SPI listener started.")
print("Waiting for text input...")

Atspi.event_main()
