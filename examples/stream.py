from easyobs.easyobs import EasyOBS

import random
import os
import time

import pygame
import io

def display_screenshot(screenshot):
    # Start timing
    start_time = time.time()

    # Load the screenshot into a Pygame surface
    image_stream = io.BytesIO(screenshot.getvalue())
    image = pygame.image.load(image_stream)

    # Display the image
    screen.blit(image, (0, 0))
    pygame.display.flip()

    # End timing and calculate duration
    end_time = time.time()
    duration = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"Screenshot display took {duration:.2f}ms")


if __name__ == "__main__":
    obs = EasyOBS(
        host="192.168.20.150",
        password="21006t3unROaFCfi"
    )

    while not obs.connected:
        print("Waiting for OBS to connect...")
        time.sleep(1)

    image_formats = obs.version.supported_image_formats

    # Select preferred image format
    if "ppm" in image_formats:
        format = "ppm"
    elif "bmp" in image_formats:
        format = "bmp" 
    elif "jpg" in image_formats:
        format = "jpg"
    else:
        format = image_formats[0]

    print(f"Using image format: {format}")

     # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((640, 360))
    pygame.display.set_caption("OBS Screenshot")

    # Make sure we're connected
    # assert obs.connected, "Failed to connect to OBS"

    while True:
        # Start timing
        start_time = time.time()
        
        # Get screenshot
        screenshot = obs.scenes.program_scene.get_screenshot(640, 360, 15, format=format)
        
        # End timing and calculate duration
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"Screenshot capture took {duration:.2f}ms")

        display_screenshot(screenshot)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        time.sleep(0.01)