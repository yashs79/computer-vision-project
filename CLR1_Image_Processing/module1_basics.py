"""
CLR-1: Foundations of Image Processing Techniques
==================================================
This module demonstrates fundamental image processing operations:
- Image loading and color space conversions
- Image filtering (Gaussian blur, bilateral filter)
- Edge detection (Canny, Sobel)
- Morphological operations
- Image thresholding techniques

Testable Output: Processed images showing various filtering and edge detection results
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


class ImageProcessingFoundations:
    """Class to demonstrate fundamental image processing techniques"""
    
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
        self.results = {}
        
    def grayscale_conversion(self):
        """Convert image to grayscale"""
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.results['Grayscale'] = gray
        print("✓ Grayscale conversion completed")
        return gray
    
    def apply_gaussian_blur(self, kernel_size=(5, 5), sigma=1.0):
        """
        Apply Gaussian blur for noise reduction
        
        Args:
            kernel_size: Size of the Gaussian kernel
            sigma: Standard deviation
        """
        gray = self.grayscale_conversion()
        blurred = cv2.GaussianBlur(gray, kernel_size, sigma)
        self.results['Gaussian Blur'] = blurred
        print(f"✓ Gaussian blur applied (kernel={kernel_size}, sigma={sigma})")
        return blurred
    
    def apply_bilateral_filter(self, d=9, sigma_color=75, sigma_space=75):
        """
        Apply bilateral filter (edge-preserving smoothing)
        
        Args:
            d: Diameter of pixel neighborhood
            sigma_color: Filter sigma in color space
            sigma_space: Filter sigma in coordinate space
        """
        gray = self.grayscale_conversion()
        bilateral = cv2.bilateralFilter(gray, d, sigma_color, sigma_space)
        self.results['Bilateral Filter'] = bilateral
        print(f"✓ Bilateral filter applied (d={d}, σ_color={sigma_color})")
        return bilateral
    
    def detect_edges_canny(self, threshold1=50, threshold2=150):
        """
        Detect edges using Canny edge detector
        
        Args:
            threshold1: Lower threshold for hysteresis
            threshold2: Upper threshold for hysteresis
        """
        gray = self.grayscale_conversion()
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.0)
        edges = cv2.Canny(blurred, threshold1, threshold2)
        self.results['Canny Edges'] = edges
        print(f"✓ Canny edge detection (thresholds: {threshold1}, {threshold2})")
        return edges
    
    def detect_edges_sobel(self):
        """Detect edges using Sobel operator"""
        gray = self.grayscale_conversion()
        
        # Sobel X and Y
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Compute magnitude
        sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        sobel_magnitude = np.uint8(sobel_magnitude / sobel_magnitude.max() * 255)
        
        self.results['Sobel X'] = np.uint8(np.absolute(sobel_x))
        self.results['Sobel Y'] = np.uint8(np.absolute(sobel_y))
        self.results['Sobel Magnitude'] = sobel_magnitude
        
        print("✓ Sobel edge detection (X, Y, Magnitude)")
        return sobel_magnitude
    
    def apply_thresholding(self):
        """Apply various thresholding techniques"""
        gray = self.grayscale_conversion()
        
        # Simple binary threshold
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Otsu's thresholding
        _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Adaptive thresholding
        adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY, 11, 2)
        
        self.results['Binary Threshold'] = binary
        self.results['Otsu Threshold'] = otsu
        self.results['Adaptive Threshold'] = adaptive
        
        print("✓ Thresholding applied (Binary, Otsu, Adaptive)")
        return otsu
    
    def apply_morphological_operations(self):
        """Apply morphological operations (erosion, dilation, opening, closing)"""
        gray = self.grayscale_conversion()
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        kernel = np.ones((5, 5), np.uint8)
        
        erosion = cv2.erode(binary, kernel, iterations=1)
        dilation = cv2.dilate(binary, kernel, iterations=1)
        opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        self.results['Erosion'] = erosion
        self.results['Dilation'] = dilation
        self.results['Opening'] = opening
        self.results['Closing'] = closing
        
        print("✓ Morphological operations (Erosion, Dilation, Opening, Closing)")
        return closing
    
    def visualize_results(self, output_path='CLR1_output'):
        """
        Visualize all processing results
        
        Args:
            output_path: Directory to save output images
        """
        os.makedirs(output_path, exist_ok=True)
        
        # Calculate grid size
        n_results = len(self.results) + 1  # +1 for original
        cols = 3
        rows = (n_results + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
        axes = axes.flatten() if n_results > 1 else [axes]
        
        # Plot original
        axes[0].imshow(cv2.cvtColor(self.original, cv2.COLOR_BGR2RGB))
        axes[0].set_title('Original Image', fontweight='bold', fontsize=12)
        axes[0].axis('off')
        
        # Plot results
        for idx, (title, img) in enumerate(self.results.items(), 1):
            if len(img.shape) == 2:  # Grayscale
                axes[idx].imshow(img, cmap='gray')
            else:
                axes[idx].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            axes[idx].set_title(title, fontweight='bold', fontsize=12)
            axes[idx].axis('off')
        
        # Hide extra subplots
        for idx in range(n_results, len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        output_file = os.path.join(output_path, 'image_processing_results.png')
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\n✓ Visualization saved to: {output_file}")
        plt.show()
        
    def generate_report(self):
        """Generate a report of all operations performed"""
        print("\n" + "="*70)
        print("CLR-1: IMAGE PROCESSING TECHNIQUES - REPORT")
        print("="*70)
        print(f"Original Image Shape: {self.original.shape}")
        print(f"Image Size: {self.original.shape[1]} x {self.original.shape[0]} pixels")
        print(f"\nTotal Operations Performed: {len(self.results)}")
        print("\nOperations List:")
        for idx, operation in enumerate(self.results.keys(), 1):
            print(f"  {idx}. {operation}")
        print("="*70)


def test_clr1(image_path):
    """
    Test function for CLR-1 module
    
    Args:
        image_path: Path to test image
    """
    print("\n" + "="*70)
    print("TESTING CLR-1: IMAGE PROCESSING FOUNDATIONS")
    print("="*70 + "\n")
    
    # Initialize processor
    processor = ImageProcessingFoundations(image_path)
    
    # Apply all techniques
    processor.apply_gaussian_blur()
    processor.apply_bilateral_filter()
    processor.detect_edges_canny()
    processor.detect_edges_sobel()
    processor.apply_thresholding()
    processor.apply_morphological_operations()
    
    # Generate report and visualize
    processor.generate_report()
    processor.visualize_results()
    
    return processor


if __name__ == "__main__":
    # Test with a sample image
    # Replace with actual image path
    test_image = "../OpenCV-Document-Scanner/sample_images/desk.JPG"
    
    if os.path.exists(test_image):
        processor = test_clr1(test_image)
    else:
        print(f"Error: Test image not found at {test_image}")
        print("Please provide a valid image path")
