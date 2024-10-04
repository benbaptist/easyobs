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
        return f"<Scene(name={self.name}, uuid={self.uuid})>"

    @property
    def screenshot(self):
        """
        Get a screenshot of the scene.
        """

        return self.get_screenshot(
            self.root.video_settings.output_width, 
            self.root.video_settings.output_height
        )

    def get_screenshot(self, width, height, quality=92):
        """
        Get a screenshot of the scene.
        """

        resp = self.root.client.get_source_screenshot(
            self.name, 
            "jpg", 
            width, 
            height, 
            quality
        )

        parsed = datauri.parse(resp.image_data)

        return io.BytesIO(parsed.data)
