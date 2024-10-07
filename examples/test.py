from easyobs.easyobs import EasyOBS

import random
import os
import time

if __name__ == "__main__":
    obs = EasyOBS()

    # Make sure we're connected
    # assert obs.connected, "Failed to connect to OBS"

    # Print the current frame rate
    print(f"Frame rate: {obs.video_settings.frame_rate}")

    # Print the width and height of the current output
    print(f"Output width: {obs.video_settings.output_width}")
    print(f"Output height: {obs.video_settings.output_height}")

    # Enable studio mode
    obs.studio_mode = True 

    # Print the current program and preview scenes

    print(f"Program scene: {obs.scenes.program_scene.name}")
    print(f"Preview scene: {obs.scenes.preview_scene.name}")

    # Optionally, you can loop through the scenes and grab screenshots by setting this to True
    while False:
        print(f"Program scene: {obs.scenes.program_scene.name}")
        print(f"Preview scene: {obs.scenes.preview_scene.name}")

        obs.scenes.preview_scene.get_screenshot(640, 360)
        obs.scenes.program_scene.get_screenshot(640, 360)

        time.sleep(0.01)

    # Grab a screenshot of each scene and save it to a file
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    for scene in obs.scenes:
        print(f"* {scene.name} - {scene.uuid}")

        with open(f"screenshots/{scene.name}.jpg", "wb") as f:
            f.write(scene.screenshot.read())
        
        # Randomly switch to a different scene, while we're at it
        if random.random() < 0.5:
            obs.scenes.program_scene = scene
