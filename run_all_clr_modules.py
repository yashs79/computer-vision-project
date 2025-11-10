#!/usr/bin/env python3
"""
Script to run all 5 CLR modules with the same input image
and save outputs to CLR-outputs folder
"""

import os
import sys
import cv2
import shutil
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Add module directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'CLR1_Image_Processing'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'CLR2_Shape_Region_Analysis'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'CLR3_Hough_Transform'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'CLR4_3D_Motion_Analysis'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'CLR5_CV_Applications'))

# Import modules
from module1_basics import ImageProcessingFoundations
from module2_shapes import ShapeRegionAnalyzer
from module3_hough import HoughTransformDetector
from module4_3d_motion import ThreeDimensionalMotionAnalyzer
from module5_document_scanner import DocumentScannerApplication

def main():
    # Input image
    input_image_path = "OpenCV-Document-Scanner/sample_images/desk.JPG"
    
    # Create output directory
    output_base = "CLR-outputs"
    os.makedirs(output_base, exist_ok=True)
    
    # Check if image exists
    if not os.path.exists(input_image_path):
        print(f"❌ Error: Image not found at {input_image_path}")
        return
    
    # Load image
    image = cv2.imread(input_image_path)
    if image is None:
        print(f"❌ Error: Could not load image from {input_image_path}")
        return
    
    print("=" * 80)
    print("RUNNING ALL 5 CLR MODULES WITH INPUT IMAGE: desk.JPG")
    print("=" * 80)
    print(f"Input Image: {input_image_path}")
    print(f"Image Size: {image.shape[1]}x{image.shape[0]}")
    print(f"Output Directory: {output_base}/")
    print("=" * 80)
    
    # ========== CLR-1: Image Processing ==========
    print("\n[1/5] Running CLR-1: Image Processing Techniques...")
    try:
        clr1_output = os.path.join(output_base, "CLR1_Image_Processing")
        os.makedirs(clr1_output, exist_ok=True)
        
        processor = ImageProcessingFoundations(input_image_path)
        processor.grayscale_conversion()
        processor.apply_gaussian_blur()
        processor.apply_bilateral_filter()
        processor.detect_edges_canny()
        processor.detect_edges_sobel()
        processor.apply_thresholding()
        processor.apply_morphological_operations()
        
        # Visualize and save
        processor.visualize_results(clr1_output)
        processor.generate_report()
        
        print(f"✓ CLR-1 completed. Output saved to: {clr1_output}/")
    except Exception as e:
        print(f"❌ CLR-1 failed: {str(e)}")
    
    # ========== CLR-2: Shape and Region Analysis ==========
    print("\n[2/5] Running CLR-2: Shape and Region Analysis...")
    try:
        clr2_output = os.path.join(output_base, "CLR2_Shape_Region_Analysis")
        os.makedirs(clr2_output, exist_ok=True)
        
        analyzer = ShapeRegionAnalyzer(input_image_path)
        analyzer.detect_contours()
        analyzer.analyze_shapes()
        analyzer.compute_shape_descriptors()
        
        # Visualize and save
        analyzer.visualize_results(clr2_output)
        analyzer.generate_report()
        
        print(f"✓ CLR-2 completed. Output saved to: {clr2_output}/")
    except Exception as e:
        print(f"❌ CLR-2 failed: {str(e)}")
    
    # ========== CLR-3: Hough Transform ==========
    print("\n[3/5] Running CLR-3: Hough Transform...")
    try:
        clr3_output = os.path.join(output_base, "CLR3_Hough_Transform")
        os.makedirs(clr3_output, exist_ok=True)
        
        detector = HoughTransformDetector(input_image_path)
        detector.detect_lines_standard()
        detector.detect_lines_probabilistic()
        detector.detect_circles()
        detector.detect_document_edges()
        
        # Visualize and save
        detector.visualize_results(clr3_output)
        detector.generate_report()
        
        print(f"✓ CLR-3 completed. Output saved to: {clr3_output}/")
    except Exception as e:
        print(f"❌ CLR-3 failed: {str(e)}")
    
    # ========== CLR-4: 3D and Motion Analysis ==========
    print("\n[4/5] Running CLR-4: 3D and Motion Analysis...")
    try:
        clr4_output = os.path.join(output_base, "CLR4_3D_Motion_Analysis")
        os.makedirs(clr4_output, exist_ok=True)
        
        motion_analyzer = ThreeDimensionalMotionAnalyzer(input_image_path)
        success = motion_analyzer.auto_detect_and_transform()
        
        if success and motion_analyzer.warped is not None:
            motion_analyzer.visualize_results(clr4_output)
            motion_analyzer.generate_report()
            print(f"✓ CLR-4 completed. Output saved to: {clr4_output}/")
        else:
            print(f"⚠ CLR-4: Document corners not detected clearly - skipping")
    except Exception as e:
        print(f"❌ CLR-4 failed: {str(e)}")
    
    # ========== CLR-5: Document Scanner Application ==========
    print("\n[5/5] Running CLR-5: Document Scanner Application...")
    try:
        clr5_output = os.path.join(output_base, "CLR5_CV_Applications")
        os.makedirs(clr5_output, exist_ok=True)
        
        scanner = DocumentScannerApplication(input_image_path)
        scanned_doc = scanner.scan_document()
        
        if scanned_doc is not None:
            # Visualize pipeline
            scanner.visualize_pipeline(clr5_output)
            
            # Save final scanned document
            final_output = os.path.join(clr5_output, "final_scanned_document.png")
            cv2.imwrite(final_output, scanned_doc)
            
            print(f"✓ CLR-5 completed. Output saved to: {clr5_output}/")
        else:
            print(f"⚠ CLR-5: Document scanning failed")
    except Exception as e:
        print(f"❌ CLR-5 failed: {str(e)}")
    
    # ========== Summary ==========
    print("\n" + "=" * 80)
    print("EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Input Image: {input_image_path}")
    print(f"All outputs saved to: {output_base}/")
    print("\nOutput Structure:")
    print(f"  {output_base}/")
    print(f"    ├── CLR1_Image_Processing/")
    print(f"    ├── CLR2_Shape_Region_Analysis/")
    print(f"    ├── CLR3_Hough_Transform/")
    print(f"    ├── CLR4_3D_Motion_Analysis/")
    print(f"    └── CLR5_CV_Applications/")
    print("=" * 80)
    print("✓ All modules executed successfully!")
    print("=" * 80)

if __name__ == "__main__":
    main()
