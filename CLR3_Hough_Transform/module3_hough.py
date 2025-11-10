"""
CLR-3: Hough Transform and its Applications
============================================
This module demonstrates Hough Transform for detecting:
- Straight lines (Standard and Probabilistic Hough Transform)
- Circles (Hough Circle Transform)
- Document edges using line detection

Testable Output: Images with detected lines, circles, and geometric shapes overlaid
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import defaultdict


class HoughTransformDetector:
    """Class to demonstrate Hough Transform techniques"""
    
    def __init__(self, image_path):
        """
        Initialize with an image
        
        Args:
            image_path: Path to the input image
        """
        self.original = cv2.imread(image_path)
        if self.original is None:
            raise ValueError(f"Could not load image from {image_path}")
        self.image = self.original.copy()
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.lines = []
        self.circles = []
        
    def preprocess_for_lines(self):
        """Preprocess image for line detection"""
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(self.gray, (5, 5), 1.0)
        
        # Apply Canny edge detection
        edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
        
        print("✓ Preprocessed image for line detection")
        return edges
    
    def detect_lines_standard(self, rho=1, theta=np.pi/180, threshold=100):
        """
        Detect lines using Standard Hough Transform
        
        Args:
            rho: Distance resolution in pixels
            theta: Angle resolution in radians
            threshold: Accumulator threshold
        """
        edges = self.preprocess_for_lines()
        
        # Detect lines
        lines = cv2.HoughLines(edges, rho, theta, threshold)
        
        if lines is not None:
            self.lines = lines
            print(f"✓ Standard Hough: Detected {len(lines)} lines")
        else:
            print("✓ Standard Hough: No lines detected")
            self.lines = []
        
        return lines
    
    def detect_lines_probabilistic(self, rho=1, theta=np.pi/180, threshold=50,
                                   min_line_length=100, max_line_gap=10):
        """
        Detect lines using Probabilistic Hough Transform
        
        Args:
            rho: Distance resolution in pixels
            theta: Angle resolution in radians
            threshold: Accumulator threshold
            min_line_length: Minimum line length
            max_line_gap: Maximum gap between line segments
        """
        edges = self.preprocess_for_lines()
        
        # Detect line segments
        lines = cv2.HoughLinesP(edges, rho, theta, threshold,
                               minLineLength=min_line_length,
                               maxLineGap=max_line_gap)
        
        if lines is not None:
            print(f"✓ Probabilistic Hough: Detected {len(lines)} line segments")
            return lines
        else:
            print("✓ Probabilistic Hough: No lines detected")
            return []
    
    def detect_circles(self, dp=1, min_dist=50, param1=100, param2=30,
                      min_radius=10, max_radius=200):
        """
        Detect circles using Hough Circle Transform
        
        Args:
            dp: Inverse ratio of accumulator resolution
            min_dist: Minimum distance between circle centers
            param1: Upper threshold for Canny edge detector
            param2: Accumulator threshold for circle centers
            min_radius: Minimum circle radius
            max_radius: Maximum circle radius
        """
        # Apply median blur for noise reduction
        blurred = cv2.medianBlur(self.gray, 5)
        
        # Detect circles
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp, min_dist,
                                  param1=param1, param2=param2,
                                  minRadius=min_radius, maxRadius=max_radius)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            self.circles = circles[0]
            print(f"✓ Hough Circle Transform: Detected {len(self.circles)} circles")
        else:
            print("✓ Hough Circle Transform: No circles detected")
            self.circles = []
        
        return self.circles
    
    def detect_document_edges(self):
        """
        Detect document edges using Hough Line Transform
        This is specifically useful for document scanning applications
        """
        edges = self.preprocess_for_lines()
        
        # Use probabilistic Hough transform for better edge detection
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100,
                               minLineLength=100, maxLineGap=10)
        
        if lines is None:
            print("✓ Document edges: No lines detected")
            return []
        
        # Classify lines as horizontal or vertical
        horizontal_lines = []
        vertical_lines = []
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Calculate angle
            angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
            
            # Classify based on angle
            if angle < 45 or angle > 135:
                horizontal_lines.append(line)
            else:
                vertical_lines.append(line)
        
        print(f"✓ Document edges: {len(horizontal_lines)} horizontal, {len(vertical_lines)} vertical")
        
        return {
            'horizontal': horizontal_lines,
            'vertical': vertical_lines,
            'all': lines
        }
    
    def find_line_intersections(self, lines):
        """
        Find intersection points of detected lines
        Useful for finding document corners
        
        Args:
            lines: List of lines in [x1, y1, x2, y2] format
        """
        intersections = []
        
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                line1 = lines[i][0]
                line2 = lines[j][0]
                
                # Calculate intersection
                intersection = self._line_intersection(line1, line2)
                if intersection is not None:
                    intersections.append(intersection)
        
        print(f"✓ Found {len(intersections)} line intersections")
        return intersections
    
    def _line_intersection(self, line1, line2):
        """
        Calculate intersection point of two lines
        
        Args:
            line1: [x1, y1, x2, y2]
            line2: [x1, y1, x2, y2]
        """
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2
        
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        
        if abs(denom) < 1e-10:
            return None
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        
        return (int(x), int(y))
    
    def visualize_results(self, output_path='CLR3_output'):
        """
        Visualize Hough Transform results
        
        Args:
            output_path: Directory to save output images
        """
        os.makedirs(output_path, exist_ok=True)
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # 1. Original image
        axes[0, 0].imshow(cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('Original Image', fontweight='bold', fontsize=12)
        axes[0, 0].axis('off')
        
        # 2. Edge detection
        edges = self.preprocess_for_lines()
        axes[0, 1].imshow(edges, cmap='gray')
        axes[0, 1].set_title('Canny Edge Detection', fontweight='bold', fontsize=12)
        axes[0, 1].axis('off')
        
        # 3. Standard Hough Lines
        img_standard = self.original.copy()
        if len(self.lines) > 0:
            for line in self.lines[:50]:  # Limit to 50 lines for clarity
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(img_standard, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        axes[0, 2].imshow(cv2.cvtColor(img_standard, cv2.COLOR_BGR2RGB))
        axes[0, 2].set_title(f'Standard Hough Lines ({len(self.lines)})', 
                            fontweight='bold', fontsize=12)
        axes[0, 2].axis('off')
        
        # 4. Probabilistic Hough Lines
        img_prob = self.original.copy()
        prob_lines = self.detect_lines_probabilistic()
        if prob_lines is not None and len(prob_lines) > 0:
            for line in prob_lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img_prob, (x1, y1), (x2, y2), (255, 0, 0), 2)
        
        axes[1, 0].imshow(cv2.cvtColor(img_prob, cv2.COLOR_BGR2RGB))
        axes[1, 0].set_title(f'Probabilistic Hough Lines ({len(prob_lines) if prob_lines is not None else 0})',
                            fontweight='bold', fontsize=12)
        axes[1, 0].axis('off')
        
        # 5. Hough Circles
        img_circles = self.original.copy()
        if len(self.circles) > 0:
            for circle in self.circles:
                x, y, r = circle
                cv2.circle(img_circles, (x, y), r, (0, 255, 255), 2)
                cv2.circle(img_circles, (x, y), 2, (0, 0, 255), 3)
        
        axes[1, 1].imshow(cv2.cvtColor(img_circles, cv2.COLOR_BGR2RGB))
        axes[1, 1].set_title(f'Hough Circles ({len(self.circles)})',
                            fontweight='bold', fontsize=12)
        axes[1, 1].axis('off')
        
        # 6. Document Edges (Horizontal and Vertical)
        img_doc = self.original.copy()
        doc_edges = self.detect_document_edges()
        if doc_edges:
            for line in doc_edges['horizontal']:
                x1, y1, x2, y2 = line[0]
                cv2.line(img_doc, (x1, y1), (x2, y2), (0, 255, 0), 2)
            for line in doc_edges['vertical']:
                x1, y1, x2, y2 = line[0]
                cv2.line(img_doc, (x1, y1), (x2, y2), (255, 0, 0), 2)
        
        axes[1, 2].imshow(cv2.cvtColor(img_doc, cv2.COLOR_BGR2RGB))
        axes[1, 2].set_title('Document Edges (H: Green, V: Blue)',
                            fontweight='bold', fontsize=12)
        axes[1, 2].axis('off')
        
        plt.tight_layout()
        output_file = os.path.join(output_path, 'hough_transform_results.png')
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\n✓ Visualization saved to: {output_file}")
        plt.show()
    
    def generate_report(self):
        """Generate detailed report of Hough Transform analysis"""
        print("\n" + "="*70)
        print("CLR-3: HOUGH TRANSFORM - REPORT")
        print("="*70)
        print(f"\nStandard Hough Transform:")
        print(f"  Lines detected: {len(self.lines)}")
        
        # Analyze line orientations
        if len(self.lines) > 0:
            angles = [line[0][1] * 180 / np.pi for line in self.lines]
            print(f"  Angle range: {min(angles):.1f}° to {max(angles):.1f}°")
            print(f"  Mean angle: {np.mean(angles):.1f}°")
        
        print(f"\nHough Circle Transform:")
        print(f"  Circles detected: {len(self.circles)}")
        
        if len(self.circles) > 0:
            radii = [c[2] for c in self.circles]
            print(f"  Radius range: {min(radii)} to {max(radii)} pixels")
            print(f"  Mean radius: {np.mean(radii):.1f} pixels")
        
        print("="*70)


def test_clr3(image_path):
    """
    Test function for CLR-3 module
    
    Args:
        image_path: Path to test image
    """
    print("\n" + "="*70)
    print("TESTING CLR-3: HOUGH TRANSFORM")
    print("="*70 + "\n")
    
    # Initialize detector
    detector = HoughTransformDetector(image_path)
    
    # Detect lines and circles
    detector.detect_lines_standard()
    detector.detect_circles()
    
    # Generate report and visualize
    detector.generate_report()
    detector.visualize_results()
    
    return detector


if __name__ == "__main__":
    # Test with a sample image
    test_image = "../OpenCV-Document-Scanner/sample_images/desk.JPG"
    
    if os.path.exists(test_image):
        detector = test_clr3(test_image)
    else:
        print(f"Error: Test image not found at {test_image}")
        print("Please provide a valid image path")
