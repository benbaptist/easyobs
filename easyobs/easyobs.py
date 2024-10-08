import obsws_python as obs
import time
from functools import wraps

from .scenes import Scenes
from .video_settings import VideoSettings
from .output_status import OutputStatus

class EasyOBS:
    def __init__(self, host="localhost", port=4455, password=None, connect_on_init=True):
        self.host = host
        self.port = port
        self.password = password
        self._client = None
        self._connecting_thread = None

        if connect_on_init:
            self._connecting_thread = threading.Thread(target=self.ensure_connected)
            self._connecting_thread.daemon = True
            self._connecting_thread.start()

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
        if self._connecting_thread is not None:
            print("Waiting for connection thread to finish...")
            self._connecting_thread.join()
            return 

        retries = 0

        while retries < max_retries:
            if self.connected:
                return True
            else:
                print(f"Not connected. Attempting to reconnect (attempt {retries + 1}/{max_retries})...")

                try:
                    self._connect()
                    self._connecting_thread = None
                    return True
                except ConnectionError as e:
                    retries += 1
                    time.sleep(retry_delay)

        self._connecting_thread = None
        raise ConnectionRefusedError("Failed to connect to OBS after multiple attempts")
    
    @property
    def connected(self):
        if self._client is None:
            return False
        else:
            try:
                self._client.get_version()
                return True
            except Exception:
                return False
    
    @property
    def video_settings(self):
        return VideoSettings(self.client)
    
    @property
    def studio_mode(self):
        return self.client.get_studio_mode_enabled()
    
    @studio_mode.setter
    def studio_mode(self, enabled):
        # If the studio mode is already in the desired state, do nothing
        if self.studio_mode == enabled:
            return
        
        self.client.set_studio_mode_enabled(enabled)

    @property
    def stream(self):
        resp = self.client.get_stream_status()

        return OutputStatus(
            type="stream",
            active=resp.output_active,
            bytes=resp.output_bytes,
            duration=resp.output_duration,
            timecode=resp.output_timecode,
            skipped_frames=resp.output_skipped_frames,
            total_frames=resp.output_total_frames,
            congestion=resp.output_congestion,
            reconnecting=resp.output_reconnecting
        )
    
    @stream.setter
    def stream(self, enabled):
        # If the stream is already in the desired state, do nothing
        if self.stream.active == enabled:
            return
        
        if enabled:
            self.client.start_stream()
        else:
            self.client.stop_stream()

    @property
    def record(self):
        resp = self.client.get_record_status()

        return OutputStatus(
            type="record",
            active=resp.output_active,
            paused=resp.output_paused,
            bytes=resp.output_bytes,
            duration=resp.output_duration,
            timecode=resp.output_timecode
        )
    
    @record.setter
    def record(self, enabled):
        # If the recording is already in the desired state, do nothing
        if self.record.active == enabled:
            return
        
        if enabled:
            self.client.start_record()
        else:
            self.client.stop_record()

    @property
    def virtual_cam(self):
        resp = self.client.get_virtual_cam_status()
        
        return OutputStatus(
            type="virtual_cam", 
            active=resp.output_active
        )
    
    @virtual_cam.setter
    def virtual_cam(self, enabled):
        # If the virtual cam is already in the desired state, do nothing
        if self.virtual_cam.active == enabled:
            return
        
        if enabled:
            self.client.start_virtual_cam()
        else:
            self.client.stop_virtual_cam()
    
    def __getitem__(self, scene_name):
        for scene in self.scenes:
            if scene.name == scene_name:
                return scene
            
        return None
