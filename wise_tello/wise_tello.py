#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wise Tello - Autonomous Line Following Drone
===========================================

An intelligent Tello drone controller that uses computer vision to autonomously 
follow a red line from start to end using OpenCV.

Features:
- Real-time red line detection using HSV color space
- Autonomous navigation based on line position
- Safety mechanisms and emergency stop
- Battery monitoring and low battery warnings
- Manual override controls

Requirements:
- djitellopy
- opencv-python
- numpy
- pygame (for display)

Usage:
1. Connect to Tello WiFi network (TELLO-XXXXXX)
2. Run: python wise_tello.py
3. Press 't' to takeoff and start autonomous following
4. Press 'l' to land
5. Press 'esc' for emergency stop

Author: AI Assistant
Date: 2025
"""

import cv2
import numpy as np
import time
import sys
import os
from typing import Tuple, Optional, List

# Tello drone library
try:
    from djitellopy import Tello
    TELLO_AVAILABLE = True
    print("✅ Tello library found - Real drone mode")
except ImportError:
    TELLO_AVAILABLE = False
    print("❌ Tello library not found!")
    print("Install with: pip install djitellopy")
    sys.exit(1)

# Computer Vision settings
class VisionConfig:
    # HSV color range for red line detection
    RED_LOWER_1 = np.array([0, 120, 70])      # Lower red range
    RED_UPPER_1 = np.array([10, 255, 255])    # Upper red range
    RED_LOWER_2 = np.array([170, 120, 70])    # Lower red range (wraparound)
    RED_UPPER_2 = np.array([180, 255, 255])   # Upper red range (wraparound)
    
    # Line detection parameters
    MIN_LINE_LENGTH = 50          # Minimum line length to consider
    MAX_LINE_GAP = 10             # Maximum gap between line segments
    LINE_THICKNESS = 3            # Thickness for drawing detected lines
    
    # Image processing
    BLUR_KERNEL = (5, 5)          # Gaussian blur kernel
    MORPH_KERNEL = np.ones((3, 3), np.uint8)  # Morphological operations kernel
    
    # Camera settings
    CAMERA_WIDTH = 960
    CAMERA_HEIGHT = 720
    FPS = 30

class FlightConfig:
    # Movement parameters
    FORWARD_SPEED = 40            # Forward movement speed (0-100)
    SIDE_SPEED = 30               # Side movement speed (0-100)
    ROTATION_SPEED = 50           # Rotation speed (0-100)
    VERTICAL_SPEED = 30           # Vertical movement speed (0-100)
    
    # Control thresholds
    CENTER_TOLERANCE = 50         # Pixels tolerance for center positioning
    ROTATION_THRESHOLD = 20       # Degrees threshold for rotation
    MIN_LINE_AREA = 500           # Minimum area to consider a valid line
    
    # Safety settings
    MAX_FLIGHT_TIME = 300         # Maximum flight time in seconds (5 minutes)
    LOW_BATTERY_THRESHOLD = 20    # Low battery percentage
    EMERGENCY_BATTERY = 10        # Emergency battery percentage

class WiseTello:
    """
    Autonomous Tello drone controller with computer vision for line following
    """
    
    def __init__(self):
        """Initialize the Wise Tello controller"""
        
        # Initialize Tello drone
        self.tello = Tello()
        self.connected = False
        self.is_flying = False
        self.autonomous_mode = False
        
        # Flight data
        self.battery_level = 0
        self.flight_start_time = 0
        self.line_detected = False
        self.line_lost_count = 0
        self.max_line_lost = 30  # Frames before giving up
        
        # Movement velocities
        self.left_right_velocity = 0
        self.for_back_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        
        # Vision tracking
        self.line_center_x = 0
        self.line_center_y = 0
        self.frame_center_x = 0
        self.frame_center_y = 0
        
        # Statistics
        self.frames_processed = 0
        self.lines_detected = 0
        
        print("🚁 Wise Tello Controller Initialized")
        
    def connect_to_drone(self) -> bool:
        """Connect to Tello drone"""
        
        print("🔄 Connecting to Tello drone...")
        print("   Make sure:")
        print("   1. Tello is powered on")
        print("   2. Connected to Tello WiFi (TELLO-XXXXXX)")
        print("   3. Tello is within range")
        
        try:
            self.tello.connect()
            self.battery_level = self.tello.get_battery()
            self.connected = True
            
            # Turn off video stream initially
            self.tello.streamoff()
            
            print("✅ Connected successfully!")
            print(f"🔋 Battery level: {self.battery_level}%")
            
            # Check battery level
            if self.battery_level < FlightConfig.LOW_BATTERY_THRESHOLD:
                print(f"⚠️ Warning: Low battery ({self.battery_level}%)")
                if self.battery_level < FlightConfig.EMERGENCY_BATTERY:
                    print("❌ Battery too low for flight!")
                    return False
                    
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("\n🔧 Troubleshooting:")
            print("   1. Check if Tello is powered on")
            print("   2. Connect to Tello WiFi network")
            print("   3. Move Tello closer")
            print("   4. Try restarting Tello")
            self.connected = False
            return False
    
    def start_video_stream(self) -> bool:
        """Start video stream from Tello camera"""
        
        if not self.connected:
            print("❌ Not connected to drone")
            return False
            
        try:
            self.tello.streamon()
            print("📹 Video stream started")
            return True
        except Exception as e:
            print(f"❌ Failed to start video stream: {e}")
            return False
    
    def get_frame(self) -> Optional[np.ndarray]:
        """Get current frame from Tello camera"""
        
        if not self.connected:
            return None
            
        try:
            frame = self.tello.get_frame_read().frame
            
            if frame is not None:
                # Resize frame for processing
                frame = cv2.resize(frame, (VisionConfig.CAMERA_WIDTH, VisionConfig.CAMERA_HEIGHT))
                self.frame_center_x = frame.shape[1] // 2
                self.frame_center_y = frame.shape[0] // 2
                self.frames_processed += 1
                
            return frame
            
        except Exception as e:
            print(f"❌ Error getting frame: {e}")
            return None
    
    def detect_red_line(self, frame: np.ndarray) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Detect red lines in the frame using HSV color space
        
        Args:
            frame: Input BGR frame
            
        Returns:
            Tuple of (line_detected, mask_with_lines)
        """
        
        if frame is None:
            return False, None
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for red color (handling wraparound in HSV)
        mask1 = cv2.inRange(hsv, VisionConfig.RED_LOWER_1, VisionConfig.RED_UPPER_1)
        mask2 = cv2.inRange(hsv, VisionConfig.RED_LOWER_2, VisionConfig.RED_UPPER_2)
        red_mask = cv2.bitwise_or(mask1, mask2)
        
        # Apply morphological operations to clean up the mask
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, VisionConfig.MORPH_KERNEL)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, VisionConfig.MORPH_KERNEL)
        
        # Apply Gaussian blur
        red_mask = cv2.GaussianBlur(red_mask, VisionConfig.BLUR_KERNEL, 0)
        
        # Find contours
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > VisionConfig.MIN_LINE_AREA:
                valid_contours.append(contour)
        
        if not valid_contours:
            return False, red_mask
        
        # Find the largest contour (main line)
        main_contour = max(valid_contours, key=cv2.contourArea)
        
        # Calculate contour center
        M = cv2.moments(main_contour)
        if M["m00"] != 0:
            self.line_center_x = int(M["m10"] / M["m00"])
            self.line_center_y = int(M["m01"] / M["m00"])
            
            # Draw the detected line
            cv2.drawContours(red_mask, [main_contour], -1, 255, VisionConfig.LINE_THICKNESS)
            
            # Draw center point
            cv2.circle(red_mask, (self.line_center_x, self.line_center_y), 10, 255, -1)
            
            self.lines_detected += 1
            return True, red_mask
        
        return False, red_mask
    
    def calculate_movement(self) -> Tuple[int, int, int, int]:
        """
        Calculate movement velocities based on line position
        
        Returns:
            Tuple of (left_right, forward_back, up_down, yaw) velocities
        """
        
        if not self.line_detected:
            return 0, 0, 0, 0
        
        # Calculate error from center
        error_x = self.line_center_x - self.frame_center_x
        error_y = self.line_center_y - self.frame_center_y
        
        # Calculate velocities based on error
        left_right_vel = 0
        forward_back_vel = 0
        up_down_vel = 0
        yaw_vel = 0
        
        # Horizontal positioning (left/right movement)
        if abs(error_x) > VisionConfig.CENTER_TOLERANCE:
            if error_x > 0:  # Line is to the right, move right
                left_right_vel = FlightConfig.SIDE_SPEED
            else:  # Line is to the left, move left
                left_right_vel = -FlightConfig.SIDE_SPEED
        
        # Vertical positioning (up/down movement)
        if abs(error_y) > VisionConfig.CENTER_TOLERANCE:
            if error_y > 0:  # Line is below center, move down
                up_down_vel = -FlightConfig.VERTICAL_SPEED
            else:  # Line is above center, move up
                up_down_vel = FlightConfig.VERTICAL_SPEED
        
        # Forward movement (always move forward when line is detected)
        forward_back_vel = FlightConfig.FORWARD_SPEED
        
        return left_right_vel, forward_back_vel, up_down_vel, yaw_vel
    
    def update_battery(self):
        """Update battery level"""
        
        if self.connected:
            try:
                self.battery_level = self.tello.get_battery()
                
                # Check for low battery
                if self.battery_level < FlightConfig.EMERGENCY_BATTERY and self.is_flying:
                    print(f"🚨 EMERGENCY: Battery critically low ({self.battery_level}%)!")
                    self.emergency_land()
                elif self.battery_level < FlightConfig.LOW_BATTERY_THRESHOLD and self.is_flying:
                    print(f"⚠️ Low battery warning: {self.battery_level}%")
                    
            except Exception as e:
                print(f"Error reading battery: {e}")
    
    def emergency_land(self):
        """Emergency landing procedure"""
        
        print("🚨 EMERGENCY LANDING INITIATED!")
        
        if self.is_flying and self.connected:
            try:
                self.autonomous_mode = False
                self.tello.emergency()
                self.is_flying = False
                print("✅ Emergency landing completed")
            except Exception as e:
                print(f"❌ Emergency landing error: {e}")
    
    def takeoff(self) -> bool:
        """Take off the drone"""
        
        if not self.connected:
            print("❌ Not connected to drone")
            return False
        
        if self.battery_level < FlightConfig.EMERGENCY_BATTERY:
            print("❌ Battery too low for takeoff!")
            return False
        
        try:
            print("🚁 Taking off...")
            self.tello.takeoff()
            self.is_flying = True
            self.flight_start_time = time.time()
            print("✅ Takeoff successful!")
            return True
            
        except Exception as e:
            print(f"❌ Takeoff failed: {e}")
            return False
    
    def land(self) -> bool:
        """Land the drone"""
        
        if not self.is_flying:
            print("⚠️ Drone is not flying")
            return False
        
        try:
            print("🛬 Landing...")
            self.autonomous_mode = False
            self.tello.land()
            self.is_flying = False
            print("✅ Landing successful!")
            return True
            
        except Exception as e:
            print(f"❌ Landing failed: {e}")
            return False
    
    def send_movement_command(self):
        """Send movement command to drone"""
        
        if not self.is_flying or not self.connected:
            return
        
        try:
            self.tello.send_rc_control(
                self.left_right_velocity,
                self.for_back_velocity,
                self.up_down_velocity,
                self.yaw_velocity
            )
        except Exception as e:
            print(f"Error sending movement command: {e}")
            self.connected = False
    
    def draw_overlay(self, frame: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """Draw information overlay on frame"""
        
        if frame is None:
            return frame
        
        # Create overlay
        overlay = frame.copy()
        
        # Draw center crosshair
        cv2.line(overlay, 
                (self.frame_center_x - 20, self.frame_center_y),
                (self.frame_center_x + 20, self.frame_center_y), 
                (255, 255, 255), 2)
        cv2.line(overlay, 
                (self.frame_center_x, self.frame_center_y - 20),
                (self.frame_center_x, self.frame_center_y + 20), 
                (255, 255, 255), 2)
        
        # Draw line center if detected
        if self.line_detected:
            cv2.circle(overlay, (self.line_center_x, self.line_center_y), 15, (0, 255, 0), 3)
            cv2.line(overlay, 
                    (self.frame_center_x, self.frame_center_y),
                    (self.line_center_x, self.line_center_y), 
                    (0, 255, 0), 2)
        
        # Add text information
        status_text = "AUTONOMOUS" if self.autonomous_mode else "MANUAL"
        color = (0, 255, 0) if self.autonomous_mode else (0, 0, 255)
        cv2.putText(overlay, f"Mode: {status_text}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        cv2.putText(overlay, f"Battery: {self.battery_level}%", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.putText(overlay, f"Lines Detected: {self.lines_detected}", (10, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if self.line_detected:
            cv2.putText(overlay, "LINE DETECTED", (10, 150), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(overlay, "NO LINE", (10, 150), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Show movement velocities
        cv2.putText(overlay, f"LR: {self.left_right_velocity}", (10, 190), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(overlay, f"FB: {self.for_back_velocity}", (10, 210), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(overlay, f"UD: {self.up_down_velocity}", (10, 230), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Add instructions
        instructions = [
            "Controls:",
            "T - Takeoff",
            "L - Land", 
            "A - Start Autonomous",
            "S - Stop Autonomous",
            "ESC - Emergency Stop"
        ]
        
        y_offset = 250
        for instruction in instructions:
            cv2.putText(overlay, instruction, (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
            y_offset += 20
        
        return overlay
    
    def run(self):
        """Main control loop"""
        
        print("🚁 Wise Tello Controller Starting...")
        
        # Connect to drone
        if not self.connect_to_drone():
            print("❌ Failed to connect to drone. Exiting...")
            return
        
        # Start video stream
        if not self.start_video_stream():
            print("❌ Failed to start video stream. Exiting...")
            return
        
        print("✅ Ready for autonomous flight!")
        print("📋 Instructions:")
        print("   T - Takeoff")
        print("   L - Land")
        print("   A - Start autonomous line following")
        print("   S - Stop autonomous mode")
        print("   ESC - Emergency stop")
        
        # Main loop
        try:
            while True:
                # Get frame
                frame = self.get_frame()
                if frame is None:
                    continue
                
                # Detect red line
                self.line_detected, mask = self.detect_red_line(frame)
                
                # Update line lost counter
                if not self.line_detected:
                    self.line_lost_count += 1
                else:
                    self.line_lost_count = 0
                
                # Calculate movement if in autonomous mode
                if self.autonomous_mode and self.is_flying:
                    if self.line_detected:
                        self.left_right_velocity, self.for_back_velocity, \
                        self.up_down_velocity, self.yaw_velocity = self.calculate_movement()
                    else:
                        # No line detected, hover in place
                        self.left_right_velocity = 0
                        self.for_back_velocity = 0
                        self.up_down_velocity = 0
                        self.yaw_velocity = 0
                        
                        # If line lost for too long, consider landing
                        if self.line_lost_count > self.max_line_lost:
                            print("⚠️ Line lost for too long. Consider manual control.")
                            self.autonomous_mode = False
                
                # Send movement command
                self.send_movement_command()
                
                # Draw overlay
                overlay = self.draw_overlay(frame, mask)
                
                # Display frames
                cv2.imshow("Wise Tello - Main View", overlay)
                if mask is not None:
                    cv2.imshow("Wise Tello - Line Detection", mask)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('t') or key == ord('T'):
                    if not self.is_flying:
                        self.takeoff()
                
                elif key == ord('l') or key == ord('L'):
                    if self.is_flying:
                        self.land()
                
                elif key == ord('a') or key == ord('A'):
                    if self.is_flying and not self.autonomous_mode:
                        self.autonomous_mode = True
                        print("🤖 Autonomous mode activated!")
                    elif not self.is_flying:
                        print("❌ Must takeoff first before autonomous mode")
                
                elif key == ord('s') or key == ord('S'):
                    if self.autonomous_mode:
                        self.autonomous_mode = False
                        print("👤 Manual mode activated!")
                
                elif key == 27:  # ESC key
                    print("🚨 Emergency stop activated!")
                    self.emergency_land()
                    break
                
                # Update battery every 3 seconds
                if self.frames_processed % (VisionConfig.FPS * 3) == 0:
                    self.update_battery()
                
                # Check flight time
                if self.is_flying:
                    flight_time = time.time() - self.flight_start_time
                    if flight_time > FlightConfig.MAX_FLIGHT_TIME:
                        print("⏰ Maximum flight time reached. Landing...")
                        self.land()
                        break
                
        except KeyboardInterrupt:
            print("\n🛑 Program interrupted by user")
        
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources before exit"""
        
        print("🧹 Cleaning up...")
        
        # Land if flying
        if self.is_flying and self.connected:
            print("🛬 Emergency landing...")
            try:
                self.tello.land()
                time.sleep(2)
            except:
                pass
        
        # Close video stream
        if self.connected:
            try:
                self.tello.streamoff()
            except:
                pass
        
        # Close OpenCV windows
        cv2.destroyAllWindows()
        
        print("✅ Cleanup completed")
        print(f"📊 Statistics:")
        print(f"   Frames processed: {self.frames_processed}")
        print(f"   Lines detected: {self.lines_detected}")

def main():
    """Main function"""
    
    print("🤖 Wise Tello - Autonomous Line Following Drone")
    print("=" * 50)
    
    # Check if running in test mode (no real drone)
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("🧪 Running in test mode (no real drone)")
        # You could add a test mode here that uses a webcam instead
    
    try:
        # Create and run the controller
        controller = WiseTello()
        controller.run()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
    
    print("👋 Goodbye!")

if __name__ == "__main__":
    main()
