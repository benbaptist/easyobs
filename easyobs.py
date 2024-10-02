import obsws_python as obs
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
    
class VideoSettings:
    def __init__(self, client):
        self.client = client

    @property
    def video_settings(self):
        return self.client.get_video_settings()

    @property
    def fps_numerator(self):
        return self.video_settings.fps_numerator
    
    @property
    def fps_denominator(self):
        return self.video_settings.fps_denominator
    
    @property
    def frame_rate(self):
        return self.fps_numerator / self.fps_denominator
    
    @property
    def base_height(self):
        return self.video_settings.base_height
    
    @property
    def base_width(self):
        return self.video_settings.base_width
    
    @property
    def base_resolution(self):
        return self.base_width, self.base_height
    
    @property
    def output_width(self):
        return self.video_settings.output_width
    
    @property
    def output_height(self):
        return self.video_settings.output_height
    
    @property
    def output_resolution(self):
        return self.video_settings.output_width, self.video_settings.output_height

class EasyOBS:
    def __init__(self, host="localhost", port=4455, password=None):
        self.host = host
        self.port = port
        self.password = password
        self.client = None
        self._connect()

    def _connect(self):
        try:
            self.client = obs.ReqClient(host=self.host, port=self.port, password=self.password)
        except Exception as e:
            print(f"Failed to connect to OBS: {e}")
            self.client = None
    
    @property
    def connected(self):
        return self.client is not None
    
    @property
    def video_settings(self):
        return VideoSettings(self.client)
    
    @property
    def studio_mode(self):
        return self.client.get_studio_mode_enabled()
    
    @studio_mode.setter
    def studio_mode(self, enabled):
        self.client.set_studio_mode_enabled(enabled)
    
    @property
    def program_scene(self):
        resp = self.client.get_current_program_scene()
        return Scene(root=self, name=resp.scene_name, uuid=resp.scene_uuid)
    
    @program_scene.setter
    def program_scene(self, scene_name):
        self.client.set_current_program_scene(scene_name)
    
    @property
    def preview_scene(self):
        try:
            resp = self.client.get_current_preview_scene()
            return Scene(root=self, name=resp.scene_name, uuid=resp.scene_uuid)
        except obs.error.OBSSDKRequestError as e:
            return None
    
    @preview_scene.setter
    def preview_scene(self, scene_name):
        self.client.set_current_preview_scene(scene_name)

    @property
    def scenes(self):
        resp = self.client.get_scene_list()
        return [Scene(root=self, name=scene["sceneName"], uuid=scene["sceneUuid"]) for scene in resp.scenes]
    
    def __getitem__(self, scene_name):
        for scene in self.scenes:
            if scene.name == scene_name:
                return scene
            
        return None
