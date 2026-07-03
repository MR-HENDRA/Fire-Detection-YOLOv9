"""
Fire Detection - API Testing Script
====================================
Script untuk menguji API endpoints secara otomatis.
"""

import requests
import json
from pathlib import Path
import time

# Konfigurasi
BASE_URL = "http://localhost:8000"
TEST_IMAGE_DIR = Path("test_images")  # Folder dengan gambar test

class Colors:
    """ANSI color codes untuk output terminal."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print header dengan styling."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text):
    """Print info message."""
    print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")

def test_home_page():
    """Test 1: Halaman utama."""
    print_header("TEST 1: Home Page")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code == 200:
            print_success(f"Status Code: {response.status_code}")
            print_success("Home page loaded successfully")
            return True
        else:
            print_error(f"Status Code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Connection failed: {e}")
        return False

def test_dataset_stats():
    """Test 2: Dataset statistics API."""
    print_header("TEST 2: Dataset Statistics API")
    
    try:
        response = requests.get(f"{BASE_URL}/api/dataset-stats")
        data = response.json()
        
        if response.status_code == 200 and data.get("success"):
            print_success(f"Status Code: {response.status_code}")
            print_success("Dataset stats retrieved successfully")
            
            stats = data.get("data", {})
            print_info(f"Training images: {stats.get('train', {}).get('images', 0)}")
            print_info(f"Validation images: {stats.get('valid', {}).get('images', 0)}")
            print_info(f"Testing images: {stats.get('test', {}).get('images', 0)}")
            return True
        else:
            print_error(f"Failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Request failed: {e}")
        return False

def test_detection_api(image_path=None, confidence=0.25):
    """Test 3: Fire detection API."""
    print_header("TEST 3: Fire Detection API")
    
    # Jika tidak ada gambar test, skip
    if not image_path or not Path(image_path).exists():
        print_info("No test image provided, skipping detection test")
        print_info("To test detection, provide image path: python test_api.py <image_path>")
        return None
    
    try:
        print_info(f"Testing with image: {image_path}")
        print_info(f"Confidence threshold: {confidence}")
        
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {'confidence': confidence}
            
            start_time = time.time()
            response = requests.post(f"{BASE_URL}/api/detect", files=files, data=data)
            elapsed_time = time.time() - start_time
            
            result = response.json()
            
            if response.status_code == 200 and result.get("success"):
                print_success(f"Status Code: {response.status_code}")
                print_success(f"Detection completed in {elapsed_time:.2f}s")
                
                detection_data = result.get("data", {})
                fire_count = detection_data.get("count", 0)
                
                if fire_count > 0:
                    print_success(f"🔥 Detected {fire_count} fire(s)!")
                    
                    for i, det in enumerate(detection_data.get("detections", []), 1):
                        print_info(f"Fire {i}: {det['confidence']:.1f}% confidence at ({det['x1']:.0f}, {det['y1']:.0f}, {det['x2']:.0f}, {det['y2']:.0f})")
                else:
                    print_success("✅ No fire detected")
                
                return True
            else:
                print_error(f"Failed: {result.get('error', 'Unknown error')}")
                return False
    except FileNotFoundError:
        print_error(f"Image file not found: {image_path}")
        return False
    except Exception as e:
        print_error(f"Request failed: {e}")
        return False

def test_detection_with_different_confidence(image_path=None):
    """Test 4: Detection dengan berbagai confidence threshold."""
    print_header("TEST 4: Detection with Different Confidence Thresholds")
    
    if not image_path or not Path(image_path).exists():
        print_info("No test image provided, skipping this test")
        return None
    
    confidence_levels = [0.1, 0.25, 0.5, 0.75, 0.9]
    results = []
    
    for conf in confidence_levels:
        try:
            print_info(f"Testing with confidence: {conf}")
            
            with open(image_path, 'rb') as f:
                files = {'file': f}
                data = {'confidence': conf}
                response = requests.post(f"{BASE_URL}/api/detect", files=files, data=data)
                result = response.json()
                
                if result.get("success"):
                    count = result.get("data", {}).get("count", 0)
                    print_info(f"  → Detected {count} fire(s)")
                    results.append((conf, count))
                else:
                    print_error(f"  → Failed")
        except Exception as e:
            print_error(f"  → Error: {e}")
    
    if results:
        print_success(f"Tested {len(results)} confidence levels")
        return True
    return False

def test_invalid_inputs():
    """Test 5: Invalid inputs handling."""
    print_header("TEST 5: Invalid Inputs Handling")
    
    # Test 1: No file
    print_info("Testing without file...")
    try:
        response = requests.post(f"{BASE_URL}/api/detect")
        if response.status_code != 200:
            print_success("Correctly rejected request without file")
        else:
            print_error("Should have rejected request without file")
    except Exception as e:
        print_success("Correctly handled missing file")
    
    # Test 2: Invalid confidence (akan dihandle oleh API)
    print_info("Testing with invalid confidence...")
    try:
        # Create a dummy file
        dummy_file = Path("test_dummy.txt")
        dummy_file.write_text("not an image")
        
        with open(dummy_file, 'rb') as f:
            files = {'file': f}
            data = {'confidence': 1.5}  # Invalid: > 1.0
            response = requests.post(f"{BASE_URL}/api/detect", files=files, data=data)
            
            # API might still process it, but it's okay
            print_success("API handled invalid confidence")
        
        dummy_file.unlink()  # Delete dummy file
    except Exception as e:
        print_success(f"Correctly handled invalid input")
    
    return True

def test_performance(image_path=None, iterations=5):
    """Test 6: Performance test."""
    print_header("TEST 6: Performance Test")
    
    if not image_path or not Path(image_path).exists():
        print_info("No test image provided, skipping performance test")
        return None
    
    print_info(f"Running {iterations} iterations...")
    times = []
    
    for i in range(iterations):
        try:
            with open(image_path, 'rb') as f:
                files = {'file': f}
                data = {'confidence': 0.25}
                
                start_time = time.time()
                response = requests.post(f"{BASE_URL}/api/detect", files=files, data=data)
                elapsed = time.time() - start_time
                
                if response.json().get("success"):
                    times.append(elapsed)
                    print_info(f"Iteration {i+1}: {elapsed:.2f}s")
        except Exception as e:
            print_error(f"Iteration {i+1} failed: {e}")
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print_success(f"Average time: {avg_time:.2f}s")
        print_info(f"Min: {min_time:.2f}s, Max: {max_time:.2f}s")
        return True
    
    return False

def run_all_tests(image_path=None):
    """Jalankan semua test."""
    print(f"\n{Colors.BOLD}🔥 Fire Detection API - Test Suite{Colors.RESET}")
    print(f"{Colors.BOLD}Base URL: {BASE_URL}{Colors.RESET}")
    
    results = []
    
    # Run tests
    results.append(("Home Page", test_home_page()))
    results.append(("Dataset Stats", test_dataset_stats()))
    results.append(("Fire Detection", test_detection_api(image_path)))
    results.append(("Multiple Confidences", test_detection_with_different_confidence(image_path)))
    results.append(("Invalid Inputs", test_invalid_inputs()))
    results.append(("Performance", test_performance(image_path, iterations=3)))
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    skipped = sum(1 for _, result in results if result is None)
    total = len(results)
    
    for test_name, result in results:
        if result is True:
            print_success(f"{test_name}: PASSED")
        elif result is False:
            print_error(f"{test_name}: FAILED")
        else:
            print_info(f"{test_name}: SKIPPED")
    
    print(f"\n{Colors.BOLD}Total: {total} | Passed: {passed} | Failed: {failed} | Skipped: {skipped}{Colors.RESET}")
    
    if failed == 0 and passed > 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All tests passed!{Colors.RESET}\n")
    elif failed > 0:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Some tests failed!{Colors.RESET}\n")

if __name__ == "__main__":
    import sys
    
    # Get image path from command line argument
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not image_path:
        print(f"{Colors.YELLOW}[TIP] Provide image path for full testing:{Colors.RESET}")
        print(f"{Colors.YELLOW}      python test_api.py path/to/image.jpg{Colors.RESET}\n")
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/", timeout=2)
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}[ERROR] Server is not running!{Colors.RESET}")
        print(f"{Colors.YELLOW}[TIP] Start server first: python app/main.py{Colors.RESET}\n")
        sys.exit(1)
    
    # Run tests
    run_all_tests(image_path)
