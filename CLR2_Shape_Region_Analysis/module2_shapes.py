"""
CLR-2: Shape and Region Analysis
=================================
This module demonstrates shape analysis and region detection:
- Contour detection and analysis
- Shape approximation (polygonal approximation)
- Convex hull computation
- Shape properties (area, perimeter, centroid)
- Quadrilateral detection
- Bounding rectangle computation

Testable Output: Annotated images showing detected shapes, contours, and geometric properties
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


class ShapeRegionAnalyzer:
    """Class to demonstrate shape and region analysis techniques"""
    
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
        self.contours = []
        self.shape_info = []
        
    def detect_contours(self, use_canny=True):
        """
        Detect contours in the image
        
        Args:
            use_canny: Use Canny edge detection before finding contours
        """
        if use_canny:
            # Apply Gaussian blur and Canny edge detection
            blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 50, 150)
        else:
            # Use thresholding
            _, edges = cv2.threshold(self.gray, 127, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, 
                                               cv2.CHAIN_APPROX_SIMPLE)
        
        self.contours = sorted(contours, key=cv2.contourArea, reverse=True)
        print(f"✓ Detected {len(self.contours)} contours")
        
        return self.contours
    
    def analyze_shapes(self, min_area=1000):
        """
        Analyze geometric properties of detected shapes
        
        Args:
            min_area: Minimum contour area to consider
        """
        self.shape_info = []
        
        for idx, contour in enumerate(self.contours):
            area = cv2.contourArea(contour)
            
            if area < min_area:
                continue
            
            # Calculate properties
            perimeter = cv2.arcLength(contour, True)
            
            # Moments for centroid
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0
            
            # Approximation
            epsilon = 0.02 * perimeter
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Convex hull
            hull = cv2.convexHull(contour)
            
            # Bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Shape classification based on number of vertices
            vertices = len(approx)
            if vertices == 3:
                shape_name = "Triangle"
            elif vertices == 4:
                shape_name = "Quadrilateral"
                # Check if it's a square or rectangle
                aspect_ratio = float(w) / h
                if 0.95 <= aspect_ratio <= 1.05:
                    shape_name = "Square"
                else:
                    shape_name = "Rectangle"
            elif vertices == 5:
                shape_name = "Pentagon"
            elif vertices == 6:
                shape_name = "Hexagon"
            elif vertices > 6:
                # Check circularity
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                if circularity > 0.8:
                    shape_name = "Circle"
                else:
                    shape_name = f"Polygon ({vertices} sides)"
            else:
                shape_name = "Unknown"
            
            info = {
                'contour': contour,
                'approx': approx,
                'hull': hull,
                'area': area,
                'perimeter': perimeter,
                'centroid': (cx, cy),
                'vertices': vertices,
                'shape_name': shape_name,
                'bbox': (x, y, w, h),
                'aspect_ratio': float(w) / h if h != 0 else 0
            }
            
            self.shape_info.append(info)
        
        print(f"✓ Analyzed {len(self.shape_info)} shapes (area > {min_area})")
        return self.shape_info
    
    def detect_quadrilaterals(self):
        """
        Specifically detect quadrilateral shapes (useful for document detection)
        """
        quadrilaterals = []
        
        for info in self.shape_info:
            if info['vertices'] == 4:
                quadrilaterals.append(info)
        
        print(f"✓ Found {len(quadrilaterals)} quadrilaterals")
        return quadrilaterals
    
    def compute_shape_descriptors(self):
        """Compute advanced shape descriptors"""
        for info in self.shape_info:
            contour = info['contour']
            
            # Hu Moments (shape descriptor)
            moments = cv2.moments(contour)
            hu_moments = cv2.HuMoments(moments)
            
            # Extent (ratio of contour area to bounding rectangle area)
            x, y, w, h = info['bbox']
            rect_area = w * h
            extent = float(info['area']) / rect_area if rect_area > 0 else 0
            
            # Solidity (ratio of contour area to convex hull area)
            hull_area = cv2.contourArea(info['hull'])
            solidity = float(info['area']) / hull_area if hull_area > 0 else 0
            
            # Equivalent diameter
            equiv_diameter = np.sqrt(4 * info['area'] / np.pi)
            
            info['hu_moments'] = hu_moments.flatten()
            info['extent'] = extent
            info['solidity'] = solidity
            info['equiv_diameter'] = equiv_diameter
        
        print("✓ Computed advanced shape descriptors")
    
    def visualize_contours(self, output_path='CLR2_output'):
        """
        Visualize detected contours
        
        Args:
            output_path: Directory to save output images
        """
        os.makedirs(output_path, exist_ok=True)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Original image
        axes[0, 0].imshow(cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('Original Image', fontweight='bold', fontsize=14)
        axes[0, 0].axis('off')
        
        # 2. All contours
        img_contours = self.original.copy()
        cv2.drawContours(img_contours, self.contours, -1, (0, 255, 0), 2)
        axes[0, 1].imshow(cv2.cvtColor(img_contours, cv2.COLOR_BGR2RGB))
        axes[0, 1].set_title(f'All Contours ({len(self.contours)})', 
                            fontweight='bold', fontsize=14)
        axes[0, 1].axis('off')
        
        # 3. Analyzed shapes with labels
        img_shapes = self.original.copy()
        for idx, info in enumerate(self.shape_info):
            # Draw contour
            cv2.drawContours(img_shapes, [info['contour']], -1, (0, 255, 0), 2)
            
            # Draw approximation
            cv2.drawContours(img_shapes, [info['approx']], -1, (255, 0, 0), 2)
            
            # Draw centroid
            cx, cy = info['centroid']
            cv2.circle(img_shapes, (cx, cy), 5, (0, 0, 255), -1)
            
            # Add text label
            label = f"{info['shape_name']}"
            cv2.putText(img_shapes, label, (cx - 30, cy - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        axes[1, 0].imshow(cv2.cvtColor(img_shapes, cv2.COLOR_BGR2RGB))
        axes[1, 0].set_title(f'Shape Analysis ({len(self.shape_info)} shapes)',
                            fontweight='bold', fontsize=14)
        axes[1, 0].axis('off')
        
        # 4. Convex hulls
        img_hulls = self.original.copy()
        for info in self.shape_info:
            cv2.drawContours(img_hulls, [info['hull']], -1, (0, 255, 255), 2)
        
        axes[1, 1].imshow(cv2.cvtColor(img_hulls, cv2.COLOR_BGR2RGB))
        axes[1, 1].set_title('Convex Hulls', fontweight='bold', fontsize=14)
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        output_file = os.path.join(output_path, 'shape_analysis_results.png')
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\n✓ Visualization saved to: {output_file}")
        plt.show()
    
    def generate_report(self):
        """Generate detailed report of shape analysis"""
        print("\n" + "="*70)
        print("CLR-2: SHAPE AND REGION ANALYSIS - REPORT")
        print("="*70)
        print(f"Total Contours Detected: {len(self.contours)}")
        print(f"Shapes Analyzed: {len(self.shape_info)}")
        
        if self.shape_info:
            print("\nShape Details:")
            print("-" * 70)
            for idx, info in enumerate(self.shape_info, 1):
                print(f"\nShape {idx}: {info['shape_name']}")
                print(f"  Vertices: {info['vertices']}")
                print(f"  Area: {info['area']:.2f} pixels²")
                print(f"  Perimeter: {info['perimeter']:.2f} pixels")
                print(f"  Centroid: {info['centroid']}")
                print(f"  Aspect Ratio: {info['aspect_ratio']:.2f}")
                if 'extent' in info:
                    print(f"  Extent: {info['extent']:.3f}")
                    print(f"  Solidity: {info['solidity']:.3f}")
                    print(f"  Equivalent Diameter: {info['equiv_diameter']:.2f}")
        
        print("="*70)


def test_clr2(image_path):
    """
    Test function for CLR-2 module
    
    Args:
        image_path: Path to test image
    """
    print("\n" + "="*70)
    print("TESTING CLR-2: SHAPE AND REGION ANALYSIS")
    print("="*70 + "\n")
    
    # Initialize analyzer
    analyzer = ShapeRegionAnalyzer(image_path)
    
    # Detect and analyze shapes
    analyzer.detect_contours(use_canny=True)
    analyzer.analyze_shapes(min_area=500)
    analyzer.compute_shape_descriptors()
    analyzer.detect_quadrilaterals()
    
    # Generate report and visualize
    analyzer.generate_report()
    analyzer.visualize_contours()
    
    return analyzer


if __name__ == "__main__":
    # Test with a sample image
    test_image = "../OpenCV-Document-Scanner/sample_images/desk.JPG"
    
    if os.path.exists(test_image):
        analyzer = test_clr2(test_image)
    else:
        print(f"Error: Test image not found at {test_image}")
        print("Please provide a valid image path")
