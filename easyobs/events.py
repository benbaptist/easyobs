class Events:
    def __init__(self, easyobs):
        self.easyobs = easyobs

        # Subscribe to events
        self.register_events()

    def register_events(self):
        # Status-related 
        self.easyobs._event_client.callback.register(self.on_stream_state_changed)

        # Scene-related events
        self.easyobs._event_client.callback.register(self.on_current_preview_scene_changed)
        self.easyobs._event_client.callback.register(self.on_current_program_scene_changed)

        # Volume-related events
        self.easyobs._event_client.callback.register(self.on_input_volume_changed)

    def on_current_preview_scene_changed(self, data):
        print(f"Current preview scene changed to: {data}")

    def on_current_program_scene_changed(self, data):
        print(f"Current program scene changed to: {data}")

    def on_input_volume_changed(self, data):
        print(f"Input volume changed: {data.attrs()}")

    def on_stream_state_changed(self, data):
        print(f"Stream state changed to: {data.attrs}")
