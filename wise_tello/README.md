# 🤖 Wise Tello - Autonomous Line Following Drone

An intelligent Tello drone controller that uses computer vision to autonomously follow lines of different colors using both Hough Transform and Contour detection algorithms.

![Tello Drone](https://img.shields.io/badge/Drone-Ryze%20Tello-blue) ![Python](https://img.shields.io/badge/Python-3.7+-green) ![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚁 Overview

Wise Tello is a collection of autonomous drone controllers that enable your Ryze Tello drone to follow colored lines using computer vision. The project includes multiple detection algorithms and supports various line colors for different applications.

## ✨ Features

### 🎨 Multi-Color Support
- **White, Red, Green, Yellow, Blue** line detection
- Real-time color switching during flight
- Optimized HSV color ranges for each color

### 🔍 Dual Detection Algorithms
- **Hough Transform**: Precise line detection with angle information
- **Contour Detection**: Fast blob-based detection for thick lines
- Real-time algorithm switching during flight

### 🛡️ Safety Features
- Battery monitoring with low battery warnings
- Emergency stop functionality
- Maximum flight time limits
- Automatic emergency landing

### 🎮 Interactive Controls
- Manual override capabilities
- Real-time parameter adjustment
- Visual feedback and statistics
- Multiple control modes

## 📁 Project Structure

```
wise_tello/
├── README.md                           # This file
├── wise_tello.py                       # Basic red line following
├── wise_tello_multiplecolors.py        # Multi-color with contour detection
└── wise_tello_multiplecolor_Hf.py      # Multi-color with Hough Transform
```

## 🔧 Requirements

### Hardware
- **Ryze Tello Drone** (any model)
- **Computer** with WiFi capability
- **Colored tape/markers** for line following

### Software Dependencies
```bash
pip install djitellopy opencv-python numpy
```

**Detailed requirements:**
- `djitellopy` - Tello drone control library
- `opencv-python` - Computer vision processing
- `numpy` - Numerical computations
- `pygame` (optional) - For display interface

## 🚀 Quick Start

### 1. Hardware Setup
1. **Power on** your Tello drone
2. **Connect** your computer to Tello WiFi network (`TELLO-XXXXXX`)
3. **Prepare** colored lines using tape or markers

### 2. Software Setup
```bash
# Clone or download the project
cd wise_tello

# Install dependencies
pip install -r requirements.txt  # If available
# OR
pip install djitellopy opencv-python numpy

# Run the program
python wise_tello_multiplecolor_Hf.py
```

### 3. Basic Usage
1. **Press T** - Takeoff
2. **Press 1-5** - Select line color (White, Red, Green, Yellow, Blue)
3. **Press H** - Switch to Hough Transform (recommended)
4. **Press A** - Start autonomous following
5. **Press L** - Land when done

## 📖 Detailed Usage

### Available Programs

#### 1. `wise_tello.py` - Basic Line Following
- **Purpose**: Simple red line following
- **Best for**: Learning and basic applications
- **Detection**: Contour-based only

#### 2. `wise_tello_multiplecolors.py` - Multi-Color Contour
- **Purpose**: Multi-color line following with contour detection
- **Best for**: Thick, solid lines
- **Features**: 5 colors, fast processing

#### 3. `wise_tello_multiplecolor_Hf.py` - Advanced Hough Transform ⭐
- **Purpose**: Advanced line following with dual algorithms
- **Best for**: Professional applications, thin lines, vertical lines
- **Features**: Hough Transform + Contour, line angle detection

### Keyboard Controls

| Key | Action | Description |
|-----|--------|-------------|
| **T** | Takeoff | Start the drone |
| **L** | Land | Safe landing |
| **A** | Autonomous | Start line following |
| **S** | Stop | Stop autonomous mode |
| **1-5** | Color Select | White, Red, Green, Yellow, Blue |
| **C** | Cycle Colors | Cycle through all colors |
| **H** | Hough Transform | Switch to Hough detection |
| **O** | Contour | Switch to Contour detection |
| **ESC** | Emergency Stop | Immediate stop and land |

## 🎯 Detection Algorithms

### Hough Transform Detection
**Best for:** Thin lines, precise following, vertical lines
- ✅ Accurate line angle detection
- ✅ Works with thin tape or string
- ✅ Handles broken/dashed lines
- ✅ Provides line orientation
- ⚠️ Slower processing

### Contour Detection
**Best for:** Thick lines, fast processing
- ✅ Fast real-time processing
- ✅ Excellent for wide tape
- ✅ Simple center-point following
- ✅ Good for solid lines
- ⚠️ Less precise for thin lines

## 🎨 Color Configuration

### Supported Colors
| Color | HSV Range | Best For |
|-------|-----------|----------|
| **White** | `[0,0,200]` to `[180,30,255]` | Indoor, good lighting |
| **Red** | Dual ranges for wraparound | High contrast |
| **Green** | `[40,120,70]` to `[80,255,255]` | Natural environments |
| **Yellow** | `[20,120,70]` to `[40,255,255]` | High visibility |
| **Blue** | `[100,120,70]` to `[130,255,255]` | Sky contrast |

### Customizing Colors
Edit the `COLOR_RANGES` in `VisionConfig` class to adjust detection sensitivity.

## 🛠️ Configuration

### Flight Parameters
```python
# In FlightConfig class
FORWARD_SPEED = 40      # Forward movement (0-100)
SIDE_SPEED = 30         # Left/right movement (0-100)
VERTICAL_SPEED = 30     # Up/down movement (0-100)
ROTATION_SPEED = 50     # Rotation speed (0-100)
```

### Detection Parameters
```python
# In VisionConfig class
MIN_LINE_AREA = 500     # Minimum line area to detect
CENTER_TOLERANCE = 50   # Center positioning tolerance
HOUGH_THRESHOLD = 50    # Hough Transform threshold
```

## 🚨 Safety Guidelines

### Pre-Flight Checklist
- ✅ Battery level > 20%
- ✅ Clear flight area
- ✅ Line clearly visible
- ✅ Good lighting conditions
- ✅ Emergency stop ready

### During Flight
- 👀 **Monitor battery** - Land if < 20%
- 🛑 **Keep emergency stop** accessible
- 📏 **Maintain safe altitude** (1-3 meters)
- 🌞 **Ensure good lighting** for line detection

### Emergency Procedures
1. **Press ESC** - Emergency stop
2. **Manual landing** - Use 'L' key
3. **Power cycle** - If drone becomes unresponsive

## 🔧 Troubleshooting

### Common Issues

#### "Connection Failed"
- ✅ Check Tello is powered on
- ✅ Connect to Tello WiFi (`TELLO-XXXXXX`)
- ✅ Move closer to drone
- ✅ Restart Tello if needed

#### "No Line Detected"
- ✅ Check lighting conditions
- ✅ Ensure line is thick enough (>2cm)
- ✅ Try different colors
- ✅ Adjust camera angle

#### "Poor Following Performance"
- ✅ Switch to Hough Transform (H key)
- ✅ Adjust `CENTER_TOLERANCE`
- ✅ Check line contrast
- ✅ Reduce movement speeds

#### "Multiple Windows Opening"
- ✅ Use the latest version (`wise_tello_multiplecolor_Hf.py`)
- ✅ Press H/O keys to switch cleanly
- ✅ Close program and restart if needed

### Performance Optimization

#### For Better Detection:
```python
# Increase detection sensitivity
MIN_LINE_AREA = 300  # Lower threshold
CENTER_TOLERANCE = 80  # More tolerance
```

#### For Smoother Flight:
```python
# Reduce movement speeds
FORWARD_SPEED = 30
SIDE_SPEED = 20
VERTICAL_SPEED = 20
```

## 📊 Technical Details

### Computer Vision Pipeline
1. **Color Filtering** - HSV color space filtering
2. **Preprocessing** - Morphological operations, blur
3. **Detection** - Hough Transform or Contour analysis
4. **Tracking** - Center point calculation
5. **Control** - Movement command generation

### Flight Control
- **Translational Movement** - Left/right, forward/back, up/down
- **Rotational Movement** - Yaw rotation (Hough Transform only)
- **Proportional Control** - Error-based movement calculation

### Real-time Processing
- **Frame Rate**: 30 FPS
- **Processing Time**: < 33ms per frame
- **Latency**: ~100ms total (camera + processing + control)

## 🤝 Contributing

We welcome contributions! Please feel free to:

1. **Report bugs** - Open an issue with details
2. **Suggest features** - Describe your use case
3. **Submit improvements** - Pull requests welcome
4. **Share results** - Show us your line following videos!

### Development Setup
```bash
git clone [repository-url]
cd wise_tello
pip install -r requirements.txt
python wise_tello_multiplecolor_Hf.py
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Ryze Technology** - For the amazing Tello drone
- **djitellopy** - For the excellent Python Tello library
- **OpenCV Community** - For powerful computer vision tools
- **Contributors** - Thanks to everyone who helped improve this project

## 📞 Support

If you encounter any issues or have questions:

1. **Check the troubleshooting section** above
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information
4. **Include system details** (OS, Python version, etc.)

## 🎥 Demo Videos

*Coming soon - Share your line following videos with us!*

---

**Happy Flying! 🚁✨**

*Built with ❤️ for the Tello drone community*
