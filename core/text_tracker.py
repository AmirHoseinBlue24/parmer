class TextTracker:
    def __init__(self):
        self.application = None
        self.field = None
        self.text = ""
        self.cursor = 0

    def update(self, obj):
        application = obj.get_application()

        self.application = (
            application.get_name()
            if application
            else "Unknown"
        )

        self.field = obj.get_name()

        text_iface = obj.get_text_iface()

        # Dont touch this 3 lines, baraye debug e.
        print("OBJECT TYPE:", type(obj))
        print("TEXT IFACE:", type(text_iface))
        print("TEXT IFACE IS SAME:", text_iface is obj)

        self.cursor = text_iface.get_caret_offset()

        character_count = text_iface.get_character_count()

        self.text = text_iface.get_text(
            0,
            character_count
        )

    def print(self, event_type):
        print("\033[2J\033[H", end="")

        print(f"Event       : {event_type}")
        print(f"Application : {self.application}")
        print(f"Field       : {self.field}")
        print(f"Cursor      : {self.cursor}")
        print("-" * 60)
        print(self.text)
