import obsws_python as obs

from .scenes import Scenes
from .scene import Scene

from .video_settings import VideoSettings

class EasyOBS:
    def __init__(self, host="localhost", port=4455, password=None):
        self.host = host
        self.port = port
        self.password = password
        self.client = None
        self._connect()

        self.scenes = Scenes(self)

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