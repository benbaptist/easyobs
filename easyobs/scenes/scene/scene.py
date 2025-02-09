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
    
    @property
    def available_formats(self):
        return self.root.version.supported_image_formats

    def get_screenshot(self, width, height, quality=92, format="jpg"):
        """
        Get a screenshot of the scene, with the specified width and height.

        :param width: The width of the screenshot.
        :param height: The height of the screenshot.
        :param quality: The quality of the screenshot, from 0 to 100, when using jpg.
        """

        resp = self.root.client.get_source_screenshot(
            self.name, 
            format, 
            width, 
            height, 
            quality
        )

        parsed = datauri.parse(resp.image_data)

        return io.BytesIO(parsed.data)
