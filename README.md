# Computer Vision Project - OpenCV-Based Document Scanner
## Breaking Down Document Scanner into 5 Course Learning Requirements

---

## 📚 Project Overview

This project takes **PROJECT 4: OpenCV Document Scanner** and breaks it down into **5 independent, testable modules**, each aligned with specific Course Learning Requirements (CLRs). Each module demonstrates key computer vision concepts and produces verifiable outputs.

---

## 🎯 CLR Module Breakdown

### **CLR-1: Foundations of Image Processing Techniques**
📁 **Location:** `CLR1_Image_Processing/module1_basics.py`

**Concepts Covered:**
- Image loading and color space conversions
- Image filtering (Gaussian blur, bilateral filter)
- Edge detection (Canny, Sobel)
- Image thresholding (Binary, Otsu, Adaptive)
- Morphological operations (Erosion, Dilation, Opening, Closing)

**Testable Output:**
- Visualization grid showing all processing techniques
- Comparative analysis of filtering methods
- Edge detection results
- Thresholding comparisons

**How to Run:**
```bash
cd CLR1_Image_Processing
python module1_basics.py
```

**Expected Output:**
- `CLR1_output/image_processing_results.png` - Grid visualization of all techniques
- Console report with operation details

---

### **CLR-2: Shape and Region Analysis**
📁 **Location:** `CLR2_Shape_Region_Analysis/module2_shapes.py`

**Concepts Covered:**
- Contour detection and analysis
- Shape approximation (polygonal approximation)
- Convex hull computation
- Shape properties (area, perimeter, centroid)
- Quadrilateral detection
- Bounding rectangle computation
- Shape descriptors (Hu Moments, extent, solidity)

**Testable Output:**
- Detected contours with labels
- Shape classification (triangle, rectangle, circle, etc.)
- Geometric property measurements
- Convex hull visualization

**How to Run:**
```bash
cd CLR2_Shape_Region_Analysis
python module2_shapes.py
```

**Expected Output:**
- `CLR2_output/shape_analysis_results.png` - Annotated shape detections
- Detailed report of each shape's properties

---

### **CLR-3: Hough Transform and Applications**
📁 **Location:** `CLR3_Hough_Transform/module3_hough.py`

**Concepts Covered:**
- Standard Hough Transform for line detection
- Probabilistic Hough Transform
- Hough Circle Transform
- Line intersection computation
- Document edge detection (horizontal/vertical lines)

**Testable Output:**
- Detected straight lines overlaid on image
- Circle detection results
- Document edge classification (horizontal vs vertical)
- Line intersection points

**How to Run:**
```bash
cd CLR3_Hough_Transform
python module3_hough.py
```

**Expected Output:**
- `CLR3_output/hough_transform_results.png` - Multiple visualizations showing:
  - Standard Hough lines
  - Probabilistic Hough lines
  - Detected circles
  - Document edges

---

### **CLR-4: Three-Dimensional Image Analysis and Motion**
📁 **Location:** `CLR4_3D_Motion_Analysis/module4_3d_motion.py`

**Concepts Covered:**
- Perspective transformation (homography)
- 4-point perspective transform
- Automatic document corner detection
- Image warping and rectification
- Affine transformations
- Motion detection (frame differencing)
- Optical flow computation

**Testable Output:**
- Detected corner points
- Homography matrix visualization
- Perspective-corrected (warped) image
- Transformation property analysis

**How to Run:**
```bash
cd CLR4_3D_Motion_Analysis
python module4_3d_motion.py
```

**Expected Output:**
- `CLR4_output/3d_transform_results.png` - Shows:
  - Original with detected corners
  - Homography matrix
  - Perspective-corrected result
- Detailed transformation analysis report

---

### **CLR-5: Applications of Computer Vision Algorithms**
📁 **Location:** `CLR5_CV_Applications/module5_document_scanner.py`

**Concepts Covered:**
- Complete end-to-end document scanning pipeline
- Integration of all CLR-1 through CLR-4 concepts
- Multi-stage processing pipeline
- Quality enhancement
- Batch processing capability

**Pipeline Stages:**
1. **Preprocessing** - Grayscale conversion, Gaussian blur
2. **Edge Detection** - Canny edge detector
3. **Contour Detection** - Find document boundary
4. **Perspective Transform** - Rectify document
5. **Enhancement** - Adaptive thresholding for clean output

**Testable Output:**
- Complete pipeline visualization (all 6 stages)
- Scanned document image
- Batch scanning capability

**How to Run:**
```bash
cd CLR5_CV_Applications
python module5_document_scanner.py
```

**Expected Output:**
- `CLR5_output/complete_pipeline.png` - 6-stage visualization
- `CLR5_output/scanned_document_[timestamp].png` - Final scanned document
- Comprehensive pipeline report

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.7+
- OpenCV
- NumPy
- Matplotlib

### **Install Dependencies**
```bash
pip install opencv-python opencv-contrib-python numpy matplotlib
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

---

## 📊 Testing Each Module

### **Individual Module Testing**

Each module can be tested independently:

```bash
# Test CLR-1
python CLR1_Image_Processing/module1_basics.py

# Test CLR-2
python CLR2_Shape_Region_Analysis/module2_shapes.py

# Test CLR-3
python CLR3_Hough_Transform/module3_hough.py

# Test CLR-4
python CLR4_3D_Motion_Analysis/module4_3d_motion.py

# Test CLR-5
python CLR5_CV_Applications/module5_document_scanner.py
```

### **Using Custom Images**

Each module accepts custom image paths. Modify the `__main__` section:

```python
# In any module
if __name__ == "__main__":
    test_image = "path/to/your/image.jpg"
    # ... rest of code
```

---

## 📁 Project Structure

```
project 4/
├── CLR1_Image_Processing/
│   ├── module1_basics.py
│   └── CLR1_output/
│       └── image_processing_results.png
│
├── CLR2_Shape_Region_Analysis/
│   ├── module2_shapes.py
│   └── CLR2_output/
│       └── shape_analysis_results.png
│
├── CLR3_Hough_Transform/
│   ├── module3_hough.py
│   └── CLR3_output/
│       └── hough_transform_results.png
│
├── CLR4_3D_Motion_Analysis/
│   ├── module4_3d_motion.py
│   └── CLR4_output/
│       └── 3d_transform_results.png
│
├── CLR5_CV_Applications/
│   ├── module5_document_scanner.py
│   └── CLR5_output/
│       ├── complete_pipeline.png
│       └── scanned_document_*.png
│
├── OpenCV-Document-Scanner/
│   └── sample_images/
│       └── *.JPG (test images)
│
├── CLR_PROJECT_README.md
└── requirements.txt
```

---

## 🎓 Learning Outcomes

### **CLR-1 Learning Outcomes**
Students will understand:
- Basic image processing operations
- Filtering techniques for noise reduction
- Multiple edge detection algorithms
- Thresholding methods
- Morphological transformations

### **CLR-2 Learning Outcomes**
Students will understand:
- Contour detection algorithms
- Shape approximation techniques
- Geometric property calculation
- Shape classification methods
- Advanced shape descriptors

### **CLR-3 Learning Outcomes**
Students will understand:
- Hough Transform theory and applications
- Line detection methods
- Circle detection algorithms
- Geometric feature extraction
- Document structure analysis

### **CLR-4 Learning Outcomes**
Students will understand:
- Perspective transformation concepts
- Homography computation
- 3D to 2D projection principles
- Image rectification techniques
- Motion analysis fundamentals

### **CLR-5 Learning Outcomes**
Students will understand:
- Complete CV application development
- Pipeline design and integration
- Multi-stage processing
- Real-world application deployment
- Performance optimization

---

## 📸 Sample Outputs

Each module generates visual outputs demonstrating its capabilities:

1. **CLR-1**: Grid of 10+ image processing techniques
2. **CLR-2**: Annotated shapes with property labels
3. **CLR-3**: Multiple Hough Transform visualizations
4. **CLR-4**: Before/after perspective correction
5. **CLR-5**: 6-stage complete pipeline visualization

---

## 🔬 Verification & Validation

### **How to Verify Each Module Works**

1. **Run the module** - It should execute without errors
2. **Check console output** - Look for ✓ success messages
3. **View generated images** - Each module creates output in its respective folder
4. **Read the report** - Console prints detailed analysis

### **Success Criteria**

- ✅ Module runs without errors
- ✅ Output images are generated
- ✅ Console shows detailed report
- ✅ Visual results match expected output
- ✅ All processing steps complete

---

## 🛠️ Troubleshooting

### **Common Issues**

1. **Import Error: No module named 'cv2'**
   ```bash
   pip install opencv-python
   ```

2. **Image not found**
   - Check the image path in the `__main__` section
   - Use absolute path if relative path fails

3. **No output generated**
   - Check if output directory has write permissions
   - Ensure matplotlib is installed: `pip install matplotlib`

---

## 🎯 Key Features

### **Modularity**
- Each CLR module is independent
- Can be tested separately
- Easy to understand and modify

### **Testability**
- Every module produces verifiable output
- Visual and numerical results
- Detailed console reports

### **Educational Value**
- Clear concept separation
- Progressive complexity
- Comprehensive documentation

### **Real-world Application**
- Complete document scanning solution
- Batch processing support
- Production-ready code

---

## 📝 Assignment/Project Guidelines

### **For Students:**

1. **Run each module individually** and understand the concepts
2. **Analyze the outputs** - Compare results with theory
3. **Experiment with parameters** - Modify thresholds, kernels, etc.
4. **Test with different images** - Use your own test images
5. **Document observations** - Create a lab report

### **For Instructors:**

This project can be used for:
- **5 separate lab assignments** (one per CLR)
- **Progressive project milestones**
- **Final integrated project** (CLR-5)
- **Concept demonstration** in lectures
- **Hands-on workshops**

---

## 🏆 Advanced Extensions

Students can extend each module:

1. **CLR-1**: Add more filters (median, bilateral variants)
2. **CLR-2**: Implement shape matching algorithms
3. **CLR-3**: Add ellipse detection
4. **CLR-4**: Implement real-time video processing
5. **CLR-5**: Add OCR for text extraction

---

## 📚 References

- OpenCV Documentation: https://docs.opencv.org/
- Original Project: OpenCV-Document-Scanner
- Computer Vision: Algorithms and Applications (Szeliski)
- Digital Image Processing (Gonzalez & Woods)

---

## 👥 Credits

- **Original Project**: OpenCV Document Scanner
- **CLR Breakdown**: Structured for educational purposes
- **Framework**: OpenCV, NumPy, Matplotlib

---

## 📄 License

Educational use - Based on OpenCV Document Scanner project

---

## ✅ Quick Start Checklist

- [ ] Install Python 3.7+
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Navigate to any CLR module directory
- [ ] Run the module (`python module*.py`)
- [ ] Check output folder for results
- [ ] Review console report
- [ ] Repeat for all 5 modules

---

**Ready to start learning Computer Vision? Begin with CLR-1 and work your way up!** 🚀
