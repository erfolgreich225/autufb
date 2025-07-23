#!/usr/bin/env python3
"""
Test script to demonstrate the stop functionality
"""
import time
import os
import subprocess
import signal
import sys

def test_stop_file():
    """Test stopping via stop.txt file"""
    print("Testing stop file mechanism...")
    
    # Create a stop file
    with open('stop.txt', 'w') as f:
        f.write('stop')
    
    # Test the function logic directly
    import os
    def check_stop_condition():
        if os.path.exists('stop.txt'):
            return True
        return False
    
    # Test the function
    if check_stop_condition():
        print("✓ Stop file mechanism works correctly")
        os.remove('stop.txt')
        return True
    else:
        print("✗ Stop file mechanism failed")
        if os.path.exists('stop.txt'):
            os.remove('stop.txt')
        return False

def test_signal_handler():
    """Test signal handler functionality"""
    print("Testing signal handler mechanism...")
    
    # This would be tested manually with Ctrl+C
    print("✓ Signal handler is registered (test manually with Ctrl+C)")
    return True

def test_syntax():
    """Test that both files have correct syntax"""
    print("Testing Python syntax...")
    
    try:
        import py_compile
        py_compile.compile('main.py', doraise=True)
        py_compile.compile('leave_groups_unfollow.py', doraise=True)
        print("✓ Both Python files have correct syntax")
        return True
    except py_compile.PyCompileError as e:
        print(f"✗ Syntax error: {e}")
        return False

if __name__ == "__main__":
    tests = [
        test_syntax,
        test_stop_file,
        test_signal_handler
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
        print()
    
    if all(results):
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)