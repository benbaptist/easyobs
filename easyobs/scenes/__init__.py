from typing import Dict, Type
from .scene import Scene

class Scenes:
    def __init__(self, root):
        self.root = root

    @property
    def client(self):
        return self.root.client

    def __iter__(self):
       return iter(self.list)

    def __getitem__(self, scene_name):
        return self.get(scene_name)

    @property
    def program_scene(self):
        i = 0
        while i < 3:
            try:
                resp = self.client.get_current_program_scene()
                return Scene(root=self.root, name=resp.scene_name, uuid=resp.scene_uuid)
            except AttributeError:
                print("Failed to get program scene, retrying...")
            except obs.error.OBSSDKRequestError as e:
                return None
            i += 1
        
        raise Exception("Failed to get program scene")
    
    @program_scene.setter
    def program_scene(self, scene_name):
        self.client.set_current_program_scene(scene_name)
    
    @property
    def preview_scene(self):
        i = 0
        while i < 3:

            try:
                resp = self.client.get_current_preview_scene()
                return Scene(root=self.root, name=resp.scene_name, uuid=resp.scene_uuid)
            except AttributeError:
                print("Failed to get preview scene, retrying...")
            except obs.error.OBSSDKRequestError as e:
                return None
            i += 1

        raise Exception("Failed to get preview scene")
    
    @preview_scene.setter
    def preview_scene(self, scene_name):
        self.client.set_current_preview_scene(scene_name)

    @property
    def list(self):
        resp = self.client.get_scene_list()
        return [Scene(root=self.root, name=scene["sceneName"], uuid=scene["sceneUuid"]) for scene in resp.scenes]
