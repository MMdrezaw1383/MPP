#!/usr/bin/env python3
import pygame
import time
import os
import sys

# Mock Tello class for testing without actual hardware
class MockTello:
    """
    Mock Tello class that simulates drone behavior for testing purposes.
    """
    def __init__(self):
        self.battery = 85
        self.connected = False
        self.flying = False
        print("Mock Tello initialized")
    
    def connect(self):
        print("Mock: Connecting to Tello...")
        time.sleep(0.5)  # Simulate connection delay
        self.connected = True
        print("Mock: Connected successfully!")
    
    def get_battery(self):
        return self.battery
    
    def streamoff(self):
        print("Mock: Stream off")
    
    def takeoff(self):
        print("Mock: Taking off...")
        self.flying = True
        return True
    
    def land(self):
        print("Mock: Landing...")
        self.flying = False
        return True
    
    def send_rc_control(self, lr, fb, ud, yaw):
        # Only print if there's actual movement to avoid spam
        if lr != 0 or fb != 0 or ud != 0 or yaw != 0:
            print(f"Mock RC: LR:{lr:3d} FB:{fb:3d} UD:{ud:3d} YAW:{yaw:3d}")
    
    def emergency(self):
        print("Mock: EMERGENCY STOP!")
        self.flying = False

# Try to import real Tello, fallback to Mock if not available
try:
    from djitellopy import Tello
    USE_REAL_TELLO = True
    print("Real Tello library found - will use actual drone if connected")
except ImportError:
    print("djitellopy not found - using mock Tello for testing")
    Tello = MockTello
    USE_REAL_TELLO = False

# Speed of the drone
S = 60
# Control intervals
FPS = 60  # Reduced for better performance

class TelloController:
    """
    A class to control the Tello drone using keyboard input.
    Enhanced for macOS compatibility and testing without hardware.
    """

    def __init__(self, use_mock=False):
        # Force Pygame to use specific video driver on macOS
        if sys.platform == "darwin":  # macOS
            os.environ['SDL_VIDEODRIVER'] = 'cocoa'
        
        # Initialize Pygame
        pygame.init()
        pygame.mixer.quit()  # Disable audio to prevent issues
        
        # Set up display with specific flags for macOS
        width, height = 800, 600
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption("Tello Controller - Press T for takeoff, L for land, ESC to quit")
        
        # Fill screen with a dark color initially
        self.screen.fill((30, 30, 50))
        pygame.display.flip()
        
        # macOS specific: Force window to front
        if sys.platform == "darwin":
            try:
                os.system('''osascript -e 'tell application "System Events" to set frontmost of first process whose name is "Python" to true' ''')
            except:
                pass  # Ignore if AppleScript fails
        
        # Initialize fonts for text display
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Initialize Tello (real or mock)
        if use_mock or not USE_REAL_TELLO:
            self.tello = MockTello()
            self.using_mock = True
        else:
            try:
                self.tello = Tello()
                self.using_mock = False
            except Exception as e:
                print(f"Failed to initialize real Tello, using mock: {e}")
                self.tello = MockTello()
                self.using_mock = True
        
        # Drone velocities
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 100

        # Flight state
        self.is_flying = False
        self.send_rc = True
        self.battery_level = 0
        
        # Connection status
        self.connected = False
        
        # Keys currently pressed (for visual feedback)
        self.pressed_keys = set()
        
        # Initialize connection
        self.initialize_connection()
        
        # Start main loop
        self.run()

    def initialize_connection(self):
        """Initialize connection to Tello."""
        try:
            self.tello.connect()
            self.connected = True
            self.battery_level = self.tello.get_battery()
            print(f"Battery: {self.battery_level}%")
            if hasattr(self.tello, 'streamoff'):
                self.tello.streamoff()  # In case stream was left on
        except Exception as e:
            print(f"Connection failed: {e}")
            self.connected = False

    def draw_ui(self):
        """Draw the user interface with current status and controls."""
        # Clear screen
        self.screen.fill((30, 30, 50))
        
        # Title
        title_text = "Tello Drone Controller"
        title_surface = self.font_large.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(400, 50))
        self.screen.blit(title_surface, title_rect)
        
        # Connection status
        status_color = (0, 255, 0) if self.connected else (255, 100, 100)
        status_text = "CONNECTED" if self.connected else "DISCONNECTED"
        if self.using_mock:
            status_text += " (MOCK MODE)"
        status_surface = self.font_medium.render(status_text, True, status_color)
        status_rect = status_surface.get_rect(center=(400, 90))
        self.screen.blit(status_surface, status_rect)
        
        # Flight status
        flight_color = (255, 255, 0) if self.is_flying else (150, 150, 150)
        flight_text = "FLYING" if self.is_flying else "LANDED"
        flight_surface = self.font_medium.render(flight_text, True, flight_color)
        flight_rect = flight_surface.get_rect(center=(400, 120))
        self.screen.blit(flight_surface, flight_rect)
        
        # Battery level
        battery_color = (255, 0, 0) if self.battery_level < 20 else (255, 255, 0) if self.battery_level < 50 else (0, 255, 0)
        battery_text = f"Battery: {self.battery_level}%"
        battery_surface = self.font_medium.render(battery_text, True, battery_color)
        battery_rect = battery_surface.get_rect(center=(400, 150))
        self.screen.blit(battery_surface, battery_rect)
        
        # Current velocities
        vel_y = 200
        vel_texts = [
            f"Forward/Back: {self.for_back_velocity:4d}",
            f"Left/Right:   {self.left_right_velocity:4d}",
            f"Up/Down:      {self.up_down_velocity:4d}",
            f"Yaw:          {self.yaw_velocity:4d}"
        ]
        
        for i, text in enumerate(vel_texts):
            color = (255, 255, 0) if any(abs(v) > 0 for v in [self.for_back_velocity, self.left_right_velocity, self.up_down_velocity, self.yaw_velocity]) else (200, 200, 200)
            if i == 0 and abs(self.for_back_velocity) > 0:
                color = (0, 255, 255)
            elif i == 1 and abs(self.left_right_velocity) > 0:
                color = (0, 255, 255)
            elif i == 2 and abs(self.up_down_velocity) > 0:
                color = (0, 255, 255)
            elif i == 3 and abs(self.yaw_velocity) > 0:
                color = (0, 255, 255)
            else:
                color = (150, 150, 150)
                
            vel_surface = self.font_medium.render(text, True, color)
            self.screen.blit(vel_surface, (250, vel_y + i * 30))
        
        # Control instructions
        instructions = [
            "CONTROLS:",
            "T - Takeoff",
            "L - Land",
            "W/S - Forward/Back",
            "A/D - Left/Right", 
            "↑/↓ - Up/Down",
            "←/→ - Rotate Left/Right",
            "ESC - Emergency Stop"
        ]
        
        start_y = 350
        for i, instruction in enumerate(instructions):
            color = (255, 255, 255) if i == 0 else (200, 200, 200)
            font = self.font_medium if i == 0 else self.font_small
            instruction_surface = font.render(instruction, True, color)
            self.screen.blit(instruction_surface, (50, start_y + i * 25))
        
        # Currently pressed keys
        if self.pressed_keys:
            pressed_text = f"Pressed: {', '.join(sorted(self.pressed_keys))}"
            pressed_surface = self.font_small.render(pressed_text, True, (255, 255, 0))
            self.screen.blit(pressed_surface, (50, 550))

    def run(self):
        """Main loop to handle events and send commands."""
        clock = pygame.time.Clock()
        
        print("Controller started. Window should be visible.")
        print("Press T for takeoff, L for land, ESC to quit.")
        
        while self.send_rc:
            # Handle Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.send_rc = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_down(event.key)
                elif event.type == pygame.KEYUP:
                    self.handle_key_up(event.key)
            
            # Send RC control commands
            if self.is_flying and self.connected:
                self.tello.send_rc_control(self.left_right_velocity,
                                           self.for_back_velocity,
                                           self.up_down_velocity,
                                           self.yaw_velocity)
            
            # Update display
            self.draw_ui()
            pygame.display.flip()

            # Limit the loop to our desired FPS
            clock.tick(FPS)
            
        # Cleanup before exit
        self.cleanup()

    def handle_key_down(self, key):
        """Handles key press events."""
        # Convert key to string for display
        key_name = pygame.key.name(key).upper()
        self.pressed_keys.add(key_name)
        
        if key == pygame.K_t and not self.is_flying and self.connected:
            print("Taking off...")
            try:
                self.tello.takeoff()
                self.is_flying = True
            except Exception as e:
                print(f"Takeoff failed: {e}")
                
        elif key == pygame.K_l and self.is_flying:
            print("Landing...")
            try:
                self.tello.land()
                self.is_flying = False
            except Exception as e:
                print(f"Landing failed: {e}")

        # Movement controls
        elif key == pygame.K_w:
            self.for_back_velocity = S
            print("Moving forward")
        elif key == pygame.K_s:
            self.for_back_velocity = -S
            print("Moving backward")
        elif key == pygame.K_a:
            self.left_right_velocity = -S
            print("Moving left")
        elif key == pygame.K_d:
            self.left_right_velocity = S
            print("Moving right")
        elif key == pygame.K_UP:
            self.up_down_velocity = S
            print("Moving up")
        elif key == pygame.K_DOWN:
            self.up_down_velocity = -S
            print("Moving down")
        elif key == pygame.K_LEFT:
            self.yaw_velocity = -S
            print("Rotating left")
        elif key == pygame.K_RIGHT:
            self.yaw_velocity = S
            print("Rotating right")
        
        # Emergency stop
        elif key == pygame.K_ESCAPE:
            print("EMERGENCY STOP - Exiting!")
            if self.is_flying:
                try:
                    self.tello.emergency()
                except Exception as e:
                    print(f"Emergency command failed: {e}")
            self.send_rc = False

    def handle_key_up(self, key):
        """Handles key release events to stop movement."""
        # Remove key from pressed keys
        key_name = pygame.key.name(key).upper()
        self.pressed_keys.discard(key_name)
        
        if key in (pygame.K_w, pygame.K_s):
            self.for_back_velocity = 0
            print("Stopped forward/back movement")
        elif key in (pygame.K_a, pygame.K_d):
            self.left_right_velocity = 0
            print("Stopped left/right movement")
        elif key in (pygame.K_UP, pygame.K_DOWN):
            self.up_down_velocity = 0
            print("Stopped up/down movement")
        elif key in (pygame.K_LEFT, pygame.K_RIGHT):
            self.yaw_velocity = 0
            print("Stopped rotation")

    def cleanup(self):
        """Clean up resources before exiting."""
        print("Cleaning up...")
        if self.is_flying and self.connected:
            print("Final landing command issued.")
            try:
                self.tello.land()
            except Exception as e:
                print(f"Final landing failed: {e}")
        
        pygame.quit()
        print("Controller stopped.")

def main():
    """Main function with argument handling."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Tello Drone Controller')
    parser.add_argument('--mock', action='store_true', 
                       help='Use mock Tello (for testing without drone)')
    args = parser.parse_args()
    
    try:
        controller = TelloController(use_mock=args.mock)
    except KeyboardInterrupt:
        print("\nController stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        # Emergency cleanup
        try:
            if 'controller' in locals() and hasattr(controller, 'tello'):
                if controller.is_flying:
                    controller.tello.land()
        except:
            pass

if __name__ == "__main__":
    main()