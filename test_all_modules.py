"""
Master Test Script for All CLR Modules
=======================================
This script tests all 5 CLR modules sequentially and generates a comprehensive report.

Usage:
    python test_all_modules.py [image_path]
    
If no image path is provided, uses default sample image.
"""

import sys
import os
import time
from datetime import datetime

# Add module paths
sys.path.append('CLR1_Image_Processing')
sys.path.append('CLR2_Shape_Region_Analysis')
sys.path.append('CLR3_Hough_Transform')
sys.path.append('CLR4_3D_Motion_Analysis')
sys.path.append('CLR5_CV_Applications')

# Import modules
try:
    from module1_basics import test_clr1
    from module2_shapes import test_clr2
    from module3_hough import test_clr3
    from module4_3d_motion import test_clr4
    from module5_document_scanner import test_clr5
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all module files are present in their respective directories.")
    sys.exit(1)


def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def test_all_modules(image_path):
    """
    Test all CLR modules sequentially
    
    Args:
        image_path: Path to test image
    """
    print_header("COMPREHENSIVE CLR MODULE TESTING")
    print(f"Test Image: {image_path}")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'CLR-1': {'status': 'pending', 'time': 0, 'error': None},
        'CLR-2': {'status': 'pending', 'time': 0, 'error': None},
        'CLR-3': {'status': 'pending', 'time': 0, 'error': None},
        'CLR-4': {'status': 'pending', 'time': 0, 'error': None},
        'CLR-5': {'status': 'pending', 'time': 0, 'error': None},
    }
    
    # Test CLR-1
    print_header("TESTING CLR-1: IMAGE PROCESSING FOUNDATIONS")
    try:
        start_time = time.time()
        test_clr1(image_path)
        elapsed = time.time() - start_time
        results['CLR-1']['status'] = 'success'
        results['CLR-1']['time'] = elapsed
        print(f"✓ CLR-1 completed in {elapsed:.2f} seconds")
    except Exception as e:
        results['CLR-1']['status'] = 'failed'
        results['CLR-1']['error'] = str(e)
        print(f"✗ CLR-1 failed: {e}")
    
    # Test CLR-2
    print_header("TESTING CLR-2: SHAPE AND REGION ANALYSIS")
    try:
        start_time = time.time()
        test_clr2(image_path)
        elapsed = time.time() - start_time
        results['CLR-2']['status'] = 'success'
        results['CLR-2']['time'] = elapsed
        print(f"✓ CLR-2 completed in {elapsed:.2f} seconds")
    except Exception as e:
        results['CLR-2']['status'] = 'failed'
        results['CLR-2']['error'] = str(e)
        print(f"✗ CLR-2 failed: {e}")
    
    # Test CLR-3
    print_header("TESTING CLR-3: HOUGH TRANSFORM")
    try:
        start_time = time.time()
        test_clr3(image_path)
        elapsed = time.time() - start_time
        results['CLR-3']['status'] = 'success'
        results['CLR-3']['time'] = elapsed
        print(f"✓ CLR-3 completed in {elapsed:.2f} seconds")
    except Exception as e:
        results['CLR-3']['status'] = 'failed'
        results['CLR-3']['error'] = str(e)
        print(f"✗ CLR-3 failed: {e}")
    
    # Test CLR-4
    print_header("TESTING CLR-4: 3D ANALYSIS AND MOTION")
    try:
        start_time = time.time()
        test_clr4(image_path)
        elapsed = time.time() - start_time
        results['CLR-4']['status'] = 'success'
        results['CLR-4']['time'] = elapsed
        print(f"✓ CLR-4 completed in {elapsed:.2f} seconds")
    except Exception as e:
        results['CLR-4']['status'] = 'failed'
        results['CLR-4']['error'] = str(e)
        print(f"✗ CLR-4 failed: {e}")
    
    # Test CLR-5
    print_header("TESTING CLR-5: DOCUMENT SCANNER APPLICATION")
    try:
        start_time = time.time()
        test_clr5(image_path)
        elapsed = time.time() - start_time
        results['CLR-5']['status'] = 'success'
        results['CLR-5']['time'] = elapsed
        print(f"✓ CLR-5 completed in {elapsed:.2f} seconds")
    except Exception as e:
        results['CLR-5']['status'] = 'failed'
        results['CLR-5']['error'] = str(e)
        print(f"✗ CLR-5 failed: {e}")
    
    # Generate final report
    generate_final_report(results)


def generate_final_report(results):
    """
    Generate comprehensive test report
    
    Args:
        results: Dictionary of test results
    """
    print_header("FINAL TEST REPORT")
    
    total_time = sum(r['time'] for r in results.values())
    successful = sum(1 for r in results.values() if r['status'] == 'success')
    failed = sum(1 for r in results.values() if r['status'] == 'failed')
    
    print("Module Test Results:")
    print("-" * 80)
    
    for module, result in results.items():
        status_symbol = "✓" if result['status'] == 'success' else "✗"
        status_text = result['status'].upper()
        time_text = f"{result['time']:.2f}s" if result['time'] > 0 else "N/A"
        
        print(f"  {status_symbol} {module}: {status_text:<10} (Time: {time_text})")
        
        if result['error']:
            print(f"      Error: {result['error']}")
    
    print("-" * 80)
    print(f"\nSummary:")
    print(f"  Total Modules: {len(results)}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total Time: {total_time:.2f} seconds")
    print(f"  Average Time per Module: {total_time/len(results):.2f} seconds")
    
    # Output locations
    print(f"\nGenerated Outputs:")
    print(f"  CLR-1: CLR1_Image_Processing/CLR1_output/")
    print(f"  CLR-2: CLR2_Shape_Region_Analysis/CLR2_output/")
    print(f"  CLR-3: CLR3_Hough_Transform/CLR3_output/")
    print(f"  CLR-4: CLR4_3D_Motion_Analysis/CLR4_output/")
    print(f"  CLR-5: CLR5_CV_Applications/CLR5_output/")
    
    print("\n" + "="*80)
    
    if failed == 0:
        print("  ✓ ALL MODULES PASSED SUCCESSFULLY!")
    else:
        print(f"  ⚠ {failed} MODULE(S) FAILED - CHECK ERRORS ABOVE")
    
    print("="*80 + "\n")


def main():
    """Main function"""
    # Check command line arguments
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Use default sample image
        image_path = "OpenCV-Document-Scanner/sample_images/desk.JPG"
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        print("\nUsage: python test_all_modules.py [image_path]")
        print("\nAvailable sample images:")
        sample_dir = "OpenCV-Document-Scanner/sample_images"
        if os.path.exists(sample_dir):
            for f in os.listdir(sample_dir):
                if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    print(f"  - {os.path.join(sample_dir, f)}")
        sys.exit(1)
    
    # Run tests
    test_all_modules(image_path)


if __name__ == "__main__":
    main()
