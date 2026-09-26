import gi

gi.require_version("Atspi", "2.0")

from gi.repository import Atspi
from core.checker import Checker
from engines.languagetool import LanguageToolEngine
from accessibility.focus import should_handle
from accessibility.text import is_text_field
from core.debouncer import Debouncer
from core.text_tracker import TextTracker


tracker = TextTracker()
debouncer = Debouncer()
checker = Checker(engine=LanguageToolEngine())

def on_text_ready():
    context = tracker.get_context()

    suggestions = checker.check(context)

    print("Suggestions:")

    for suggestion in suggestions:
        print(suggestion)


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

            if tracker.text_changed:
                debouncer.call(on_text_ready)

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
