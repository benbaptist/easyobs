import obsws_python as obs
import time
from functools import wraps

from .scenes import Scenes
from .video_settings import VideoSettings

class EasyOBS:
    def __init__(self, host="localhost", port=4455, password=None):
        self.host = host
        self.port = port
        self.password = password
        self._client = None

        self.scenes = Scenes(self)

    def _connect(self):
        self._client = None

        try:
            self._client = obs.ReqClient(host=self.host, port=self.port, password=self.password)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to OBS: {e}")
        
    @property
    def client(self):
        self.ensure_connected()
        return self._client

    def ensure_connected(self, max_retries=20, retry_delay=5):
        retries = 0

        while retries < max_retries:
            if self.connected:
                return True
            else:
                print(f"Not connected. Attempting to reconnect (attempt {retries + 1}/{max_retries})...")

                try:
                    self._connect()
                    return True
                except ConnectionError as e:
                    retries += 1
                    time.sleep(retry_delay)

        raise ConnectionRefusedError("Failed to connect to OBS after multiple attempts")
    
    @property
    def connected(self):
        return self._client is not None
    
    @property
    def video_settings(self):
        return VideoSettings(self.client)
    
    @property
    def studio_mode(self):
        return self.client.get_studio_mode_enabled()
    
    @studio_mode.setter
    def studio_mode(self, enabled):
        self.client.set_studio_mode_enabled(enabled)
    
    def __getitem__(self, scene_name):
        for scene in self.scenes:
            if scene.name == scene_name:
                return scene
            
        return None
