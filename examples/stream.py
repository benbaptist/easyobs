from easyobs.easyobs import EasyOBS

import random
import os
import time

import pygame
import io

CAPTURE_SIZE = (640, 360)
WINDOW_SIZE = (640, 360)
SCALE_FACTOR = 1  # Add this new constant for initial scaling

def display_screenshot(screenshot):
    # Start timing
    start_time = time.time()

    # Load the screenshot into a Pygame surface
    image_stream = io.BytesIO(screenshot.getvalue())
    image = pygame.image.load(image_stream)

    # Scale image to window size
    window_size = screen.get_size()
    scaled_image = pygame.transform.scale(image, window_size)
    
    # Display the scaled image
    screen.blit(scaled_image, (0, 0))
    pygame.display.flip()

    # End timing and calculate duration
    end_time = time.time()
    duration = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"Screenshot display took {duration:.2f}ms")


if __name__ == "__main__":
    obs = EasyOBS(
        host="localhost",
        password=""
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

    format = "jpg"

    print(f"Using image format: {format}")

     # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("OBS Screenshot")

    # Add scale factor variable
    scale_factor = SCALE_FACTOR

    while True:
        # Start timing
        start_time = time.time()
        
        # Get screenshot with dynamic resolution
        screenshot = obs.scenes.program_scene.get_screenshot(
            CAPTURE_SIZE[0] / scale_factor, 
            CAPTURE_SIZE[1] / scale_factor, 
            100, 
            format=format
        )
        
        # End timing and calculate duration
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"Screenshot capture took {duration:.2f}ms")

        display_screenshot(screenshot)

        # Update window title with current capture resolution
        pygame.display.set_caption(f"OBS Screenshot ({int(CAPTURE_SIZE[0]/scale_factor)}x{int(CAPTURE_SIZE[1]/scale_factor)}) (scale: {scale_factor})")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    scale_factor = min(scale_factor + 1, 8)  # Limit max scaling
                    print(f"Resolution scale factor: {scale_factor}")
                elif event.key == pygame.K_o:
                    scale_factor = max(scale_factor - 1, 1)  # Prevent scaling below 1
                    print(f"Resolution scale factor: {scale_factor}")

        time.sleep(0.01)