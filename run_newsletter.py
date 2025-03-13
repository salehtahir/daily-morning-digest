#!/usr/bin/env python3
"""
Wrapper script to generate the newsletter and fix HTML formatting
"""

import os
import subprocess
import sys

def main():
    print("Step 1: Generating newsletter...")
    try:
        # Run the newsletter generator
        result1 = subprocess.run(["python", "generate_newsletter.py"], 
                                check=True, capture_output=True, text=True)
        print(result1.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error generating newsletter: {e}")
        print(e.stdout)
        print(e.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    print("\nStep 2: Fixing HTML formatting...")
    try:
        # Run the HTML fix script
        result2 = subprocess.run(["python", "fix_html.py"], 
                                check=True, capture_output=True, text=True)
        print(result2.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error fixing HTML: {e}")
        print(e.stdout)
        print(e.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    print("\nNewsletter generated and formatted successfully!")
    print("Open index.html in your browser to view it.")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 