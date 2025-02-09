import time 

from easyobs import EasyOBS

obs = EasyOBS()

scenes = obs.scenes

first_scene = scenes[0]
second_scene = scenes[1]

# Cut to a specific scene
for transition in obs.client.get_scene_transition_list().transitions:    
    print(transition)
