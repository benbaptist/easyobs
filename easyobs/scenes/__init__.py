from typing import Dict, Type
from .scene import Scene

class Scenes:
    def __init__(self, main):
        self._cache: Dict[str, Type[Scene]] = {}
        self.main = main

    @property
    def client(self):
        return self.main.client

    def __iter__(self):
        return iter(self._cache.values())
    
    def __getitem__(self, scene_name):
        for scene in self.scenes:
            if scene.name == scene_name:
                return scene
            
        return None
    
    @property
    def program_scene(self):
        if not hasattr(self, '_program_scene') or (time.time() - self._program_scene_time) > 1:
            resp = self.client.get_current_program_scene()
            self._program_scene = self.get(resp.scene_name)
            self._program_scene_time = time.time()
        return self._program_scene
    
    @program_scene.setter
    def program_scene(self, scene_name):
        self.client.set_current_program_scene(scene_name)

    @property
    def preview_scene(self):
        if not hasattr(self, '_preview_scene') or (time.time() - self._preview_scene_time) > 1:
            try:
                resp = self.client.get_current_preview_scene()
            except obs.error.OBSSDKRequestError as e:
                return None
            
            self._preview_scene = self.get(resp.scene_name)
            self._preview_scene_time = time.time()
        return self._preview_scene
    
    @preview_scene.setter
    def preview_scene(self, scene_name):
        self.client.set_current_preview_scene(scene_name)

    def get(self, scene_name: str) -> Type[Scene]:
        if scene_name not in self._cache:
            try:
                scene_module = __import__(f"easyobs.scenes.{scene_name}", fromlist=["Scene"])
                scene_class = getattr(scene_module, "Scene")
                self._cache[scene_name] = scene_class
            except (ImportError, AttributeError):
                raise ValueError(f"Scene '{scene_name}' not found")
        return self._cache[scene_name]