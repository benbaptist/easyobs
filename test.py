from easyobs import EasyOBS
import random
import os

if __name__ == "__main__":
    obs = EasyOBS()

    # Make sure we're connected
    assert obs.connected, "Failed to connect to OBS"

    # Print the current frame rate
    print(f"Frame rate: {obs.video_settings.frame_rate}")

    # Enable studio mode
    obs.studio_mode = True 

    # Print the current program and preview scenes

    print(f"Program scene: {obs.program_scene.name}")
    print(f"Preview scene: {obs.preview_scene.name}")

    # Grab a screenshot of each scene and save it to a file
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    for scene in obs.scenes:
        print(f"* {scene.name} - {scene.uuid}")

        with open(f"screenshots/{scene.name}.jpg", "wb") as f:
            f.write(scene.screenshot.read())
        
        # Randomly switch to a different scene, while we're at it
        if random.random() < 0.5:
            obs.program_scene = scene.name
