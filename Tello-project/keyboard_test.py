#!/usr/bin/env python3
"""
Simple keyboard test script to verify all controls work without Tello library
"""
import pygame
import sys
import os

def test_keyboard_controls():
    # Force Pygame to use specific video driver on macOS
    if sys.platform == "darwin":  # macOS
        os.environ['SDL_VIDEODRIVER'] = 'cocoa'
    
    pygame.init()
    pygame.mixer.quit()  # Disable audio
    
    # Create window
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption("Keyboard Test - Press keys to test")
    
    # Initialize font
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 18)
    
    # Track pressed keys and velocities
    pressed_keys = set()
    velocities = {
        'forward_back': 0,
        'left_right': 0,
        'up_down': 0,
        'yaw': 0
    }
    
    clock = pygame.time.Clock()
    running = True
    
    print("Keyboard test started. Press keys to see if they register properly.")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key).upper()
                pressed_keys.add(key_name)
                print(f"Key pressed: {key_name}")
                
                # Test movement keys
                if event.key == pygame.K_w:
                    velocities['forward_back'] = 60
                elif event.key == pygame.K_s:
                    velocities['forward_back'] = -60
                elif event.key == pygame.K_a:
                    velocities['left_right'] = -60
                elif event.key == pygame.K_d:
                    velocities['left_right'] = 60
                elif event.key == pygame.K_UP:
                    velocities['up_down'] = 60
                elif event.key == pygame.K_DOWN:
                    velocities['up_down'] = -60
                elif event.key == pygame.K_LEFT:
                    velocities['yaw'] = -60
                elif event.key == pygame.K_RIGHT:
                    velocities['yaw'] = 60
                elif event.key == pygame.K_ESCAPE:
                    print("ESC pressed - exiting")
                    running = False
                    
            elif event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key).upper()
                pressed_keys.discard(key_name)
                print(f"Key released: {key_name}")
                
                # Reset velocities on key release
                if event.key in (pygame.K_w, pygame.K_s):
                    velocities['forward_back'] = 0
                elif event.key in (pygame.K_a, pygame.K_d):
                    velocities['left_right'] = 0
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    velocities['up_down'] = 0
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    velocities['yaw'] = 0
        
        # Clear screen
        screen.fill((20, 20, 40))
        
        # Draw title
        title = font.render("Keyboard Input Test", True, (255, 255, 255))
        screen.blit(title, (width//2 - title.get_width()//2, 20))
        
        # Draw instructions
        instructions = [
            "Test Keys:",
            "W/S - Forward/Back",
            "A/D - Left/Right",
            "↑/↓ - Up/Down", 
            "←/→ - Yaw Left/Right",
            "T - Takeoff test",
            "L - Land test",
            "ESC - Exit"
        ]
        
        y_pos = 60
        for instruction in instructions:
            text = small_font.render(instruction, True, (200, 200, 200))
            screen.blit(text, (20, y_pos))
            y_pos += 20
        
        # Draw current velocities
        vel_y = 220
        vel_texts = [
            f"Forward/Back: {velocities['forward_back']:4d}",
            f"Left/Right:   {velocities['left_right']:4d}",
            f"Up/Down:      {velocities['up_down']:4d}",
            f"Yaw:          {velocities['yaw']:4d}"
        ]
        
        for i, text in enumerate(vel_texts):
            color = (0, 255, 255) if list(velocities.values())[i] != 0 else (150, 150, 150)
            vel_surface = small_font.render(text, True, color)
            screen.blit(vel_surface, (20, vel_y + i * 20))
        
        # Draw currently pressed keys
        if pressed_keys:
            pressed_text = f"Currently pressed: {', '.join(sorted(pressed_keys))}"
            pressed_surface = small_font.render(pressed_text, True, (255, 255, 0))
            screen.blit(pressed_surface, (20, 340))
        else:
            no_keys_text = "No keys pressed"
            no_keys_surface = small_font.render(no_keys_text, True, (100, 100, 100))
            screen.blit(no_keys_surface, (20, 340))
        
        # Status indicator
        status_color = (0, 255, 0) if pressed_keys else (100, 100, 100)
        status_text = "ACTIVE" if pressed_keys else "WAITING"
        status_surface = font.render(status_text, True, status_color)
        screen.blit(status_surface, (width - 120, 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("Keyboard test completed.")

if __name__ == "__main__":
    test_keyboard_controls()