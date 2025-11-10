"""
CLR-4: Three-Dimensional Image Analysis and Motion Analysis
============================================================
This module demonstrates:
- Perspective transformation (2D to 3D projection concepts)
- Homography computation
- Image warping and rectification
- Motion detection and optical flow
- Frame differencing for motion analysis

Testable Output: Warped images, perspective-corrected documents, motion detection visualization
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


class ThreeDimensionalMotionAnalyzer:
    """Class to demonstrate 3D analysis and motion detection techniques"""
    
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
        self.warped = None
        self.homography_matrix = None
        
    def compute_perspective_transform(self, src_points, dst_points):
        """
        Compute perspective transformation matrix (homography)
        
        Args:
            src_points: Source points (4 corners) in original image
            dst_points: Destination points (4 corners) in transformed image
        """
        # Compute homography matrix
        self.homography_matrix, status = cv2.findHomography(src_points, dst_points)
        
        print("✓ Computed homography matrix:")
        print(self.homography_matrix)
        
        return self.homography_matrix
    
    def apply_perspective_transform(self, src_points, width, height):
        """
        Apply perspective transformation to rectify image
        
        Args:
            src_points: Source points (4 corners in clockwise order: TL, TR, BR, BL)
            width: Width of output image
            height: Height of output image
        """
        # Define destination points (rectangle)
        dst_points = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype=np.float32)
        
        # Compute perspective transform matrix
        M = cv2.getPerspectiveTransform(src_points, dst_points)
        self.homography_matrix = M
        
        # Apply transformation
        self.warped = cv2.warpPerspective(self.original, M, (width, height))
        
        print(f"✓ Applied perspective transform: {width}x{height} output")
        return self.warped
    
    def auto_detect_and_transform(self):
        """
        Automatically detect document and apply perspective transform
        """
        # Convert to grayscale
        gray = self.gray.copy()
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort by area and get largest
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        document_contour = None
        for contour in contours[:5]:
            # Approximate contour
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            # If 4 points, we found a rectangle
            if len(approx) == 4:
                document_contour = approx
                break
        
        if document_contour is not None:
            # Order points: top-left, top-right, bottom-right, bottom-left
            points = document_contour.reshape(4, 2)
            ordered_points = self._order_points(points)
            
            # Calculate output dimensions
            width = max(
                np.linalg.norm(ordered_points[0] - ordered_points[1]),
                np.linalg.norm(ordered_points[2] - ordered_points[3])
            )
            height = max(
                np.linalg.norm(ordered_points[0] - ordered_points[3]),
                np.linalg.norm(ordered_points[1] - ordered_points[2])
            )
            
            # Apply transform
            self.apply_perspective_transform(
                ordered_points.astype(np.float32),
                int(width), int(height)
            )
            
            print(f"✓ Auto-detected document with corners: {ordered_points}")
            return self.warped, ordered_points
        else:
            print("✗ Could not detect document automatically")
            return None, None
    
    def _order_points(self, pts):
        """
        Order points in clockwise order: top-left, top-right, bottom-right, bottom-left
        
        Args:
            pts: Array of 4 points
        """
        rect = np.zeros((4, 2), dtype=np.float32)
        
        # Sum: top-left will have smallest sum, bottom-right largest
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        # Difference: top-right will have smallest diff, bottom-left largest
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        return rect
    
    def compute_affine_transform(self, src_points, dst_points):
        """
        Compute affine transformation (subset of homography with 6 DOF)
        
        Args:
            src_points: 3 source points
            dst_points: 3 destination points
        """
        M = cv2.getAffineTransform(src_points, dst_points)
        
        print("✓ Computed affine transform matrix")
        return M
    
    def detect_motion_frame_diff(self, video_path=None, num_frames=30):
        """
        Detect motion using frame differencing
        
        Args:
            video_path: Path to video file (if None, uses webcam)
            num_frames: Number of frames to process
        """
        if video_path is None:
            print("Note: Video path not provided. Motion detection requires video input.")
            return None
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"✗ Could not open video: {video_path}")
            return None
        
        # Read first frame
        ret, frame1 = cap.read()
        if not ret:
            print("✗ Could not read video frame")
            return None
        
        prev_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        motion_frames = []
        
        frame_count = 0
        while frame_count < num_frames:
            ret, frame2 = cap.read()
            if not ret:
                break
            
            curr_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            
            # Compute frame difference
            frame_diff = cv2.absdiff(prev_gray, curr_gray)
            
            # Threshold
            _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)
            
            # Dilate to fill holes
            kernel = np.ones((5, 5), np.uint8)
            dilated = cv2.dilate(thresh, kernel, iterations=2)
            
            motion_frames.append((frame2, dilated))
            prev_gray = curr_gray
            frame_count += 1
        
        cap.release()
        print(f"✓ Motion detection: Processed {frame_count} frames")
        return motion_frames
    
    def compute_optical_flow(self, video_path=None):
        """
        Compute dense optical flow using Farneback method
        
        Args:
            video_path: Path to video file
        """
        if video_path is None:
            print("Note: Video path not provided. Optical flow requires video input.")
            return None
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"✗ Could not open video: {video_path}")
            return None
        
        # Read first frame
        ret, frame1 = cap.read()
        if not ret:
            return None
        
        prev_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        hsv = np.zeros_like(frame1)
        hsv[..., 1] = 255
        
        flow_frames = []
        
        for i in range(10):  # Process 10 frames
            ret, frame2 = cap.read()
            if not ret:
                break
            
            curr_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            
            # Compute optical flow
            flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None,
                                               0.5, 3, 15, 3, 5, 1.2, 0)
            
            # Convert flow to HSV
            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            hsv[..., 0] = ang * 180 / np.pi / 2
            hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
            rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            
            flow_frames.append((frame2, rgb))
            prev_gray = curr_gray
        
        cap.release()
        print(f"✓ Optical flow: Processed {len(flow_frames)} frames")
        return flow_frames
    
    def visualize_results(self, corners=None, output_path='CLR4_output'):
        """
        Visualize 3D transformation results
        
        Args:
            corners: Detected corner points
            output_path: Directory to save output images
        """
        os.makedirs(output_path, exist_ok=True)
        
        num_plots = 3 if self.warped is not None else 2
        fig, axes = plt.subplots(1, num_plots, figsize=(6 * num_plots, 6))
        
        if num_plots == 2:
            axes = [axes[0], axes[1]]
        
        # 1. Original image with corners
        img_corners = self.original.copy()
        if corners is not None:
            # Draw detected corners
            for i, point in enumerate(corners):
                cv2.circle(img_corners, tuple(point.astype(int)), 10, (0, 255, 0), -1)
                cv2.putText(img_corners, str(i), tuple(point.astype(int)),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Draw lines connecting corners
            for i in range(4):
                pt1 = tuple(corners[i].astype(int))
                pt2 = tuple(corners[(i + 1) % 4].astype(int))
                cv2.line(img_corners, pt1, pt2, (0, 0, 255), 3)
        
        axes[0].imshow(cv2.cvtColor(img_corners, cv2.COLOR_BGR2RGB))
        axes[0].set_title('Original with Detected Corners', fontweight='bold', fontsize=12)
        axes[0].axis('off')
        
        # 2. Homography matrix visualization
        if self.homography_matrix is not None:
            # Create text representation of matrix
            axes[1].axis('off')
            matrix_text = "Homography Matrix:\n\n"
            for row in self.homography_matrix:
                matrix_text += "  ".join([f"{val:8.4f}" for val in row]) + "\n"
            
            axes[1].text(0.1, 0.5, matrix_text, fontsize=10, family='monospace',
                        verticalalignment='center', transform=axes[1].transAxes)
            axes[1].set_title('Perspective Transform Matrix', fontweight='bold', fontsize=12)
        else:
            axes[1].axis('off')
            axes[1].text(0.5, 0.5, 'No homography computed', ha='center', va='center')
            axes[1].set_title('Homography Matrix', fontweight='bold', fontsize=12)
        
        # 3. Warped result
        if self.warped is not None:
            axes[2].imshow(cv2.cvtColor(self.warped, cv2.COLOR_BGR2RGB))
            axes[2].set_title('Perspective-Corrected Result', fontweight='bold', fontsize=12)
            axes[2].axis('off')
        
        plt.tight_layout()
        output_file = os.path.join(output_path, '3d_transform_results.png')
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\n✓ Visualization saved to: {output_file}")
        plt.show()
    
    def generate_report(self, corners=None):
        """Generate detailed report of 3D analysis"""
        print("\n" + "="*70)
        print("CLR-4: 3D IMAGE ANALYSIS AND MOTION - REPORT")
        print("="*70)
        
        if self.homography_matrix is not None:
            print("\nHomography Matrix:")
            print(self.homography_matrix)
            
            # Analyze transformation properties
            det = np.linalg.det(self.homography_matrix[:2, :2])
            print(f"\nTransformation Properties:")
            print(f"  Determinant (scale factor): {det:.4f}")
        
        if corners is not None:
            print(f"\nDetected Corners:")
            for i, corner in enumerate(corners):
                print(f"  Corner {i}: ({corner[0]:.1f}, {corner[1]:.1f})")
            
            # Calculate dimensions
            width1 = np.linalg.norm(corners[0] - corners[1])
            width2 = np.linalg.norm(corners[2] - corners[3])
            height1 = np.linalg.norm(corners[0] - corners[3])
            height2 = np.linalg.norm(corners[1] - corners[2])
            
            print(f"\nOriginal Dimensions:")
            print(f"  Top width: {width1:.1f} px")
            print(f"  Bottom width: {width2:.1f} px")
            print(f"  Left height: {height1:.1f} px")
            print(f"  Right height: {height2:.1f} px")
        
        if self.warped is not None:
            print(f"\nWarped Image Dimensions: {self.warped.shape[1]} x {self.warped.shape[0]}")
        
        print("="*70)


def test_clr4(image_path):
    """
    Test function for CLR-4 module
    
    Args:
        image_path: Path to test image
    """
    print("\n" + "="*70)
    print("TESTING CLR-4: 3D ANALYSIS AND MOTION")
    print("="*70 + "\n")
    
    # Initialize analyzer
    analyzer = ThreeDimensionalMotionAnalyzer(image_path)
    
    # Auto-detect and transform
    warped, corners = analyzer.auto_detect_and_transform()
    
    # Generate report and visualize
    analyzer.generate_report(corners)
    analyzer.visualize_results(corners)
    
    return analyzer


if __name__ == "__main__":
    # Test with a sample image
    test_image = "../OpenCV-Document-Scanner/sample_images/desk.JPG"
    
    if os.path.exists(test_image):
        analyzer = test_clr4(test_image)
    else:
        print(f"Error: Test image not found at {test_image}")
        print("Please provide a valid image path")
