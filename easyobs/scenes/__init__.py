from typing import Dict, Type
from .scene import Scene

import obsws_python as obs

# TODO: Implement a retry mechanism for the scenes property
# TODO: Cache Scene objects for consistency

class Scenes:
    def __init__(self, root):
        self.root = root

    @property
    def client(self):
        return self.root.client

    def __iter__(self):
       return iter(self.list)

    def __getitem__(self, scene_name):
        for scene in self.list:
            if scene.name == scene_name:
                return scene
            
        raise KeyError(f"Scene {scene_name} not found")

    @property
    def program_scene(self):
        # Due to the intermittent nature of OBS's current program scene property,
        # we need to implement a retry mechanism before giving up and raising an exception.
        i = 0

        while i < 3:
            try:
                resp = self.client.get_current_program_scene()
                return Scene(root=self.root, name=resp.scene_name, uuid=resp.scene_uuid)
            except AttributeError:
                print("Failed to get program scene, retrying...")
            except obs.error.OBSSDKRequestError as e:
                raise ConnectionError(f"Network error while getting program scene: {e}")
            i += 1
        
        raise Exception("Failed to get program scene")
    
    @program_scene.setter
    def program_scene(self, scene):
        # If the scene is already in the desired state, do nothing
        if scene.name == self.program_scene.name:
            return
        
        self.client.set_current_program_scene(scene.name)
    
    @property
    def preview_scene(self):
        # Due to the intermittent nature of OBS's current preview scene property,
        # we need to implement a retry mechanism before giving up and raising an exception.
        i = 0

        while i < 3:

            try:
                resp = self.client.get_current_preview_scene()
                return Scene(root=self.root, name=resp.scene_name, uuid=resp.scene_uuid)
            except AttributeError:
                print("Failed to get preview scene, retrying...")
            except obs.error.OBSSDKRequestError as e:
                raise ConnectionError(f"Network error while getting preview scene: {e}")
            i += 1

        raise Exception("Failed to get preview scene")
    
    @preview_scene.setter
    def preview_scene(self, scene):
        # If the scene is already in the desired state, do nothing
        if scene.name == self.preview_scene.name:
            return

        self.client.set_current_preview_scene(scene.name)

    @property
    def list(self):
        resp = self.client.get_scene_list()

        return [
            Scene(
                root=self.root, 
                name=scene["sceneName"], 
                uuid=scene["sceneUuid"]
            ) for scene in resp.scenes
        ]
