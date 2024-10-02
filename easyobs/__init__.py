import obsws_python as obs

from .scene import Scene
from .video_settings import VideoSettings

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
