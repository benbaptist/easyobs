import datauri
import io

class Scene:
    def __init__(self, root, name, uuid):
        self.root = root
        self.name = name
        self.uuid = uuid

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Scene(name={self.name}, uuid={self.uuid})"

    @property
    def screenshot(self):
        resp = self.root.client.get_source_screenshot(
            self.name, 
            "jpg", 
            self.root.video_settings.output_width, 
            self.root.video_settings.output_height, 
            95
        )

        parsed = datauri.parse(resp.image_data)

        return io.BytesIO(parsed.data)
