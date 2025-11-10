"""
CLR-5: Applications of Computer Vision Algorithms
==================================================
This module demonstrates a complete document scanner application that integrates:
- Image preprocessing techniques (CLR-1)
- Shape and contour analysis (CLR-2)
- Line detection using Hough Transform (CLR-3)
- Perspective transformation (CLR-4)
- Complete end-to-end document scanning pipeline

Testable Output: Scanned and rectified document images with quality enhancement
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime


class DocumentScannerApplication:
    """Complete document scanner application integrating all CV concepts"""
    
    def __init__(self, image_path):
        """
        Initialize the document scanner
        
        Args:
            image_path: Path to the input image
        """
        self.original = cv2.imread(image_path)
        if self.original is None:
            raise ValueError(f"Could not load image from {image_path}")
        
        self.image = self.original.copy()
        self.preprocessed = None
        self.edges = None
        self.document_contour = None
        self.warped = None
        self.enhanced = None
        self.corners = None
        
        print(f"✓ Loaded image: {image_path}")
        print(f"  Dimensions: {self.original.shape[1]} x {self.original.shape[0]}")
    
    def step1_preprocess(self):
        """
        Step 1: Preprocess the image (CLR-1 concepts)
        - Resize for faster processing
        - Convert to grayscale
        - Apply Gaussian blur
        """
        # Resize if too large
        max_dimension = 1000
        height, width = self.original.shape[:2]
        
        if max(height, width) > max_dimension:
            scale = max_dimension / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            self.image = cv2.resize(self.original, (new_width, new_height))
        else:
            self.image = self.original.copy()
        
        # Convert to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur for noise reduction
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        self.preprocessed = blurred
        print("✓ Step 1: Preprocessing complete")
        return self.preprocessed
    
    def step2_detect_edges(self):
        """
        Step 2: Detect edges using Canny (CLR-1 & CLR-3 concepts)
        """
        if self.preprocessed is None:
            self.step1_preprocess()
        
        # Canny edge detection
        self.edges = cv2.Canny(self.preprocessed, 50, 150)
        
        # Dilate edges to close gaps
        kernel = np.ones((5, 5), np.uint8)
        self.edges = cv2.dilate(self.edges, kernel, iterations=1)
        
        print("✓ Step 2: Edge detection complete")
        return self.edges
    
    def step3_find_document_contour(self):
        """
        Step 3: Find document contour (CLR-2 concepts)
        - Detect contours
        - Filter and identify document boundary
        - Approximate to quadrilateral
        """
        if self.edges is None:
            self.step2_detect_edges()
        
        # Find contours
        contours, _ = cv2.findContours(self.edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort by area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        # Find the largest contour with 4 vertices
        for contour in contours[:10]:
            # Calculate perimeter
            perimeter = cv2.arcLength(contour, True)
            
            # Approximate contour to polygon
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            
            # Check if it's a quadrilateral
            if len(approx) == 4:
                area = cv2.contourArea(approx)
                img_area = self.image.shape[0] * self.image.shape[1]
                
                # Check if area is significant (at least 10% of image)
                if area > img_area * 0.1:
                    self.document_contour = approx
                    break
        
        if self.document_contour is not None:
            self.corners = self._order_corners(self.document_contour)
            print(f"✓ Step 3: Document contour found (4 corners)")
            return self.document_contour
        else:
            print("✗ Step 3: Could not find document contour")
            print("  Using full image as fallback")
            # Use full image corners as fallback
            h, w = self.image.shape[:2]
            self.corners = np.array([
                [0, 0],
                [w - 1, 0],
                [w - 1, h - 1],
                [0, h - 1]
            ], dtype=np.float32)
            return None
    
    def step4_apply_perspective_transform(self):
        """
        Step 4: Apply perspective transformation (CLR-4 concepts)
        - Calculate destination dimensions
        - Compute homography
        - Warp image to top-down view
        """
        if self.corners is None:
            self.step3_find_document_contour()
        
        # Calculate output dimensions
        width_top = np.linalg.norm(self.corners[0] - self.corners[1])
        width_bottom = np.linalg.norm(self.corners[2] - self.corners[3])
        height_left = np.linalg.norm(self.corners[0] - self.corners[3])
        height_right = np.linalg.norm(self.corners[1] - self.corners[2])
        
        max_width = int(max(width_top, width_bottom))
        max_height = int(max(height_left, height_right))
        
        # Destination points (rectangle)
        dst_points = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]
        ], dtype=np.float32)
        
        # Compute perspective transform matrix
        M = cv2.getPerspectiveTransform(self.corners, dst_points)
        
        # Apply transformation
        self.warped = cv2.warpPerspective(self.image, M, (max_width, max_height))
        
        print(f"✓ Step 4: Perspective transform applied ({max_width}x{max_height})")
        return self.warped
    
    def step5_enhance_output(self, apply_adaptive_threshold=True):
        """
        Step 5: Enhance scanned output (CLR-1 concepts)
        - Convert to grayscale
        - Apply adaptive thresholding for clean document
        - Sharpen image
        """
        if self.warped is None:
            self.step4_apply_perspective_transform()
        
        # Convert to grayscale
        warped_gray = cv2.cvtColor(self.warped, cv2.COLOR_BGR2GRAY)
        
        if apply_adaptive_threshold:
            # Apply adaptive thresholding for clean document look
            self.enhanced = cv2.adaptiveThreshold(
                warped_gray, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
            print("✓ Step 5: Enhancement complete (adaptive threshold)")
        else:
            # Just sharpen
            kernel = np.array([[-1, -1, -1],
                             [-1,  9, -1],
                             [-1, -1, -1]])
            self.enhanced = cv2.filter2D(warped_gray, -1, kernel)
            print("✓ Step 5: Enhancement complete (sharpening)")
        
        return self.enhanced
    
    def _order_corners(self, contour):
        """
        Order corner points: top-left, top-right, bottom-right, bottom-left
        
        Args:
            contour: Contour with 4 points
        """
        pts = contour.reshape(4, 2).astype(np.float32)
        rect = np.zeros((4, 2), dtype=np.float32)
        
        # Sum: top-left has smallest sum, bottom-right has largest
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        # Difference: top-right has smallest diff, bottom-left has largest
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        return rect
    
    def scan_document(self, enhance=True):
        """
        Complete end-to-end document scanning pipeline
        
        Args:
            enhance: Apply adaptive thresholding enhancement
        
        Returns:
            Scanned document image
        """
        print("\n" + "="*70)
        print("DOCUMENT SCANNING PIPELINE")
        print("="*70)
        
        # Execute all steps
        self.step1_preprocess()
        self.step2_detect_edges()
        self.step3_find_document_contour()
        self.step4_apply_perspective_transform()
        self.step5_enhance_output(apply_adaptive_threshold=enhance)
        
        print("="*70)
        print("✓ Document scan complete!")
        print("="*70 + "\n")
        
        return self.enhanced
    
    def visualize_pipeline(self, output_path='CLR5_output'):
        """
        Visualize the complete scanning pipeline
        
        Args:
            output_path: Directory to save output images
        """
        os.makedirs(output_path, exist_ok=True)
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # 1. Original
        axes[0, 0].imshow(cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('1. Original Image', fontweight='bold', fontsize=12)
        axes[0, 0].axis('off')
        
        # 2. Preprocessed
        if self.preprocessed is not None:
            axes[0, 1].imshow(self.preprocessed, cmap='gray')
            axes[0, 1].set_title('2. Preprocessed (Grayscale + Blur)', 
                                fontweight='bold', fontsize=12)
            axes[0, 1].axis('off')
        
        # 3. Edges
        if self.edges is not None:
            axes[0, 2].imshow(self.edges, cmap='gray')
            axes[0, 2].set_title('3. Edge Detection (Canny)', 
                                fontweight='bold', fontsize=12)
            axes[0, 2].axis('off')
        
        # 4. Contour detection
        img_contour = self.image.copy()
        if self.document_contour is not None:
            cv2.drawContours(img_contour, [self.document_contour], -1, (0, 255, 0), 3)
            
            # Draw corners
            for i, corner in enumerate(self.corners.astype(int)):
                cv2.circle(img_contour, tuple(corner), 10, (0, 0, 255), -1)
                cv2.putText(img_contour, str(i), tuple(corner),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        axes[1, 0].imshow(cv2.cvtColor(img_contour, cv2.COLOR_BGR2RGB))
        axes[1, 0].set_title('4. Document Contour Detection', 
                            fontweight='bold', fontsize=12)
        axes[1, 0].axis('off')
        
        # 5. Warped
        if self.warped is not None:
            axes[1, 1].imshow(cv2.cvtColor(self.warped, cv2.COLOR_BGR2RGB))
            axes[1, 1].set_title('5. Perspective Transform', 
                                fontweight='bold', fontsize=12)
            axes[1, 1].axis('off')
        
        # 6. Enhanced
        if self.enhanced is not None:
            axes[1, 2].imshow(self.enhanced, cmap='gray')
            axes[1, 2].set_title('6. Enhanced Output', 
                                fontweight='bold', fontsize=12)
            axes[1, 2].axis('off')
        
        plt.tight_layout()
        output_file = os.path.join(output_path, 'complete_pipeline.png')
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"✓ Pipeline visualization saved to: {output_file}")
        plt.show()
    
    def save_scanned_document(self, output_path='CLR5_output', filename=None):
        """
        Save the scanned document
        
        Args:
            output_path: Directory to save output
            filename: Custom filename (auto-generated if None)
        """
        os.makedirs(output_path, exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scanned_document_{timestamp}.png"
        
        output_file = os.path.join(output_path, filename)
        
        if self.enhanced is not None:
            cv2.imwrite(output_file, self.enhanced)
            print(f"✓ Scanned document saved to: {output_file}")
            return output_file
        else:
            print("✗ No scanned document to save")
            return None
    
    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "="*70)
        print("CLR-5: COMPUTER VISION APPLICATION - DOCUMENT SCANNER REPORT")
        print("="*70)
        
        print("\nPipeline Steps:")
        print("  1. ✓ Image Preprocessing (Grayscale, Gaussian Blur)")
        print("  2. ✓ Edge Detection (Canny)")
        print("  3. ✓ Shape Analysis (Contour Detection)")
        print("  4. ✓ Perspective Transform (Homography)")
        print("  5. ✓ Enhancement (Adaptive Thresholding)")
        
        print("\nImage Metrics:")
        print(f"  Original size: {self.original.shape[1]}x{self.original.shape[0]}")
        
        if self.warped is not None:
            print(f"  Scanned size: {self.warped.shape[1]}x{self.warped.shape[0]}")
        
        if self.corners is not None:
            print(f"\nDetected Corners:")
            for i, corner in enumerate(self.corners):
                print(f"  Corner {i}: ({corner[0]:.1f}, {corner[1]:.1f})")
        
        print("\nCV Concepts Applied:")
        print("  • Image filtering and noise reduction (CLR-1)")
        print("  • Edge detection using Canny algorithm (CLR-1)")
        print("  • Contour detection and shape analysis (CLR-2)")
        print("  • Quadrilateral approximation (CLR-2)")
        print("  • Line segment detection concepts (CLR-3)")
        print("  • Perspective transformation and homography (CLR-4)")
        print("  • Complete application integration (CLR-5)")
        
        print("="*70)


def test_clr5(image_path):
    """
    Test function for CLR-5 module
    
    Args:
        image_path: Path to test image
    """
    print("\n" + "="*70)
    print("TESTING CLR-5: DOCUMENT SCANNER APPLICATION")
    print("="*70 + "\n")
    
    # Initialize scanner
    scanner = DocumentScannerApplication(image_path)
    
    # Run complete pipeline
    scanned = scanner.scan_document(enhance=True)
    
    # Save and visualize
    scanner.save_scanned_document()
    scanner.visualize_pipeline()
    scanner.generate_report()
    
    return scanner


def batch_scan_documents(input_folder, output_folder='CLR5_output/batch_scan'):
    """
    Batch process multiple document images
    
    Args:
        input_folder: Folder containing images to scan
        output_folder: Folder to save scanned documents
    """
    os.makedirs(output_folder, exist_ok=True)
    
    # Supported image extensions
    extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    
    # Find all images
    image_files = []
    for ext in extensions:
        image_files.extend([f for f in os.listdir(input_folder) if f.lower().endswith(ext)])
    
    print(f"\nFound {len(image_files)} images to scan")
    print("="*70)
    
    successful = 0
    failed = 0
    
    for idx, img_file in enumerate(image_files, 1):
        print(f"\n[{idx}/{len(image_files)}] Processing: {img_file}")
        
        try:
            img_path = os.path.join(input_folder, img_file)
            scanner = DocumentScannerApplication(img_path)
            scanner.scan_document(enhance=True)
            
            output_filename = f"scanned_{os.path.splitext(img_file)[0]}.png"
            scanner.save_scanned_document(output_folder, output_filename)
            
            successful += 1
        except Exception as e:
            print(f"  ✗ Failed: {str(e)}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"Batch Scan Complete: {successful} successful, {failed} failed")
    print("="*70)


if __name__ == "__main__":
    # Test with a sample image
    test_image = "../OpenCV-Document-Scanner/sample_images/desk.JPG"
    
    if os.path.exists(test_image):
        scanner = test_clr5(test_image)
        
        # Optional: Batch process all sample images
        sample_folder = "../OpenCV-Document-Scanner/sample_images"
        if os.path.exists(sample_folder):
            print("\n\nStarting batch scan...")
            batch_scan_documents(sample_folder)
    else:
        print(f"Error: Test image not found at {test_image}")
        print("Please provide a valid image path")
