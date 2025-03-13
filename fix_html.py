#!/usr/bin/env python3
"""
Utility script to fix HTML output from Python f-strings.
This script replaces double curly braces with single ones for valid CSS.
"""

import os
import sys
import re

def fix_html_file(filename="index.html"):
    """Fix HTML file by replacing double curly braces with single ones for valid CSS."""
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found!")
        return False
    
    try:
        # Read the file content
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace double curly braces with single ones
        # We use a regex pattern to only replace in the CSS section
        fixed_content = re.sub(r'(\s*){{{{(\s*)', r'\1{\2', content)
        fixed_content = re.sub(r'(\s*)}}}}(\s*)', r'\1}\2', fixed_content)
        
        # Write back the fixed content
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(fixed_content)
        
        print(f"Successfully fixed {filename}")
        return True
    
    except Exception as e:
        print(f"Error fixing {filename}: {e}")
        return False

if __name__ == "__main__":
    # Use the first command-line argument as the filename, or default to index.html
    filename = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    success = fix_html_file(filename)
    sys.exit(0 if success else 1) 