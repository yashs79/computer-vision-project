# HARDWARE & SOFTWARE REQUIREMENTS

## Hardware Requirements

### Minimum System Requirements

| Component | Specification |
|-----------|---------------|
| Processor | Intel Core i3 / AMD Ryzen 3 or equivalent |
| RAM | 4 GB minimum |
| Storage | 500 MB free space |
| Display | 1280 x 720 resolution |
| Camera | Not required (processes existing images) |

### Recommended System Requirements

| Component | Specification |
|-----------|---------------|
| Processor | Intel Core i5 / AMD Ryzen 5 or higher |
| RAM | 8 GB or more |
| Storage | 2 GB free space (for sample images and outputs) |
| Display | 1920 x 1080 resolution or higher |
| GPU | Optional (OpenCV can utilize GPU acceleration) |

### Additional Hardware Considerations

- Camera for Image Capture (Optional):
  - Smartphone camera (8MP or higher) for capturing document images
  - Digital camera or webcam for real-time scanning
  - Minimum 5MP resolution recommended for quality results

- Storage for Document Archive:
  - External hard drive or cloud storage for document backups
  - SSD recommended for faster processing of large batches

---

## Software Requirements

### Operating System

The application is cross-platform and supports:

| OS | Version |
|----|---------|
| Windows | Windows 10/11 (64-bit) |
| macOS | macOS 10.14 (Mojave) or later |
| Linux | Ubuntu 18.04+, Fedora 30+, or equivalent |

### Programming Language

- Python: Version 3.7 or higher
  - Python 3.8 or 3.9 recommended for optimal compatibility
  - Python 3.10+ supported

### Core Libraries and Dependencies

#### 1. OpenCV (cv2)
- Version: 4.5.0 or higher
- Purpose: Core computer vision operations
- Modules Used:
  - Image I/O and preprocessing
  - Edge detection (Canny)
  - Contour detection and analysis
  - Geometric transformations
  - Morphological operations
  - Hough Transform

Installation:
```bash
pip install opencv-python>=4.5.0
pip install opencv-contrib-python>=4.5.0
```

#### 2. NumPy
- Version: 1.19.0 or higher
- Purpose: Numerical computations and array operations
- Usage:
  - Matrix operations for transformations
  - Array manipulations
  - Mathematical computations

Installation:
```bash
pip install numpy>=1.19.0
```

#### 3. Matplotlib
- Version: 3.3.0 or higher
- Purpose: Visualization and plotting
- Usage:
  - Pipeline visualization
  - Result display
  - Comparative analysis plots

Installation:
```bash
pip install matplotlib>=3.3.0
```

### Complete Dependency Installation

All dependencies can be installed using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

requirements.txt contents:
```
opencv-python>=4.5.0
opencv-contrib-python>=4.5.0
numpy>=1.19.0
matplotlib>=3.3.0
```

---

## Development Environment

### Recommended IDEs and Editors

1. Visual Studio Code
   - Python extension
   - Jupyter extension (for notebook support)
   - IntelliSense for code completion

2. PyCharm
   - Professional or Community Edition
   - Built-in Python support
   - Integrated debugger

3. Jupyter Notebook/Lab
   - Interactive development
   - Inline visualization
   - Step-by-step execution

4. Spyder
   - Scientific Python development
   - Variable explorer
   - Integrated plotting

### Version Control

- Git: Version 2.0 or higher
- GitHub/GitLab: For repository management (optional)

---

## System Setup Instructions

### Step 1: Install Python

Windows:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer and check "Add Python to PATH"
3. Verify installation: `python --version`

macOS:
```bash
# Using Homebrew
brew install python3

# Verify
python3 --version
```

Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip

# Verify
python3 --version
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd "/Users/yash/computer-vision-project/project 4"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installations
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import numpy; print('NumPy:', numpy.__version__)"
python -c "import matplotlib; print('Matplotlib:', matplotlib.__version__)"
```

### Step 4: Verify Installation

Run the test script to ensure everything is working:

```bash
python test_all_modules.py
```

---

## Optional Software

### For Enhanced Functionality

1. Tesseract OCR (for text extraction)
   ```bash
   # macOS
   brew install tesseract
   
   # Ubuntu/Debian
   sudo apt install tesseract-ocr
   
   # Windows: Download from GitHub
   ```

2. Pillow (additional image processing)
   ```bash
   pip install Pillow
   ```

3. scikit-image (advanced image processing)
   ```bash
   pip install scikit-image
   ```

---

## Storage Requirements

### Disk Space Breakdown

| Component | Size |
|-----------|------|
| Python installation | ~100 MB |
| OpenCV library | ~50 MB |
| NumPy library | ~15 MB |
| Matplotlib library | ~30 MB |
| Project source code | ~5 MB |
| Sample images | ~20 MB |
| Output images | ~50 MB (varies) |
| Total | ~270 MB minimum |

### Recommended Free Space
- 2 GB for comfortable operation and batch processing

---

## Network Requirements

- Internet connection required for:
  - Initial package installation via pip
  - Downloading sample images (if needed)
  - Accessing online documentation

- No internet required for:
  - Running the application
  - Processing documents
  - Generating outputs

---

## Performance Considerations

### Processing Speed Factors

1. Image Resolution
   - Higher resolution = longer processing time
   - Automatic resizing to 1000px max dimension for efficiency

2. CPU Performance
   - Multi-core processors benefit from NumPy optimizations
   - Expected processing time: 2-5 seconds per image

3. RAM Usage
   - Typical usage: 200-500 MB per image
   - Batch processing may require more memory

### Optimization Tips

- Use SSD for faster I/O operations
- Close unnecessary applications during batch processing
- Process images in batches of 10-20 for optimal performance
- Consider GPU acceleration for large-scale operations

---

## Compatibility Matrix

| Python Version | OpenCV | NumPy | Matplotlib | Status |
|----------------|--------|-------|------------|--------|
| 3.7 | 4.5.0+ | 1.19.0+ | 3.3.0+ | ✅ Supported |
| 3.8 | 4.5.0+ | 1.19.0+ | 3.3.0+ | ✅ Recommended |
| 3.9 | 4.5.0+ | 1.19.0+ | 3.3.0+ | ✅ Recommended |
| 3.10 | 4.5.0+ | 1.21.0+ | 3.5.0+ | ✅ Supported |
| 3.11 | 4.6.0+ | 1.23.0+ | 3.6.0+ | ✅ Supported |

---

## Troubleshooting Common Issues

### Issue 1: OpenCV Import Error
```bash
# Solution
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python opencv-contrib-python
```

### Issue 2: Display Issues on macOS
```bash
# Solution: Use different matplotlib backend
export MPLBACKEND=TkAgg
```

### Issue 3: Permission Denied
```bash
# Solution: Use --user flag
pip install --user -r requirements.txt
```

---

Next: Concepts and Theoretical Foundations
