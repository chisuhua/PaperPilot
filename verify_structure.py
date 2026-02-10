#!/usr/bin/env python3
"""
Verify PaperPilot project structure.
Tests that all modules are properly organized and accessible.
"""

import os
import sys
from pathlib import Path


def check_directory_structure():
    """Verify the directory structure exists."""
    print("Checking directory structure...")
    
    required_dirs = [
        "paperpilot",
        "paperpilot/core",
        "paperpilot/ui",
        "examples",
        "tests",
        "docs",
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  ✗ {dir_path}/ NOT FOUND")
            all_exist = False
    
    return all_exist


def check_core_modules():
    """Verify core module files exist."""
    print("\nChecking core modules...")
    
    core_modules = [
        "paperpilot/__init__.py",
        "paperpilot/core/__init__.py",
        "paperpilot/core/pdf_extractor.py",
        "paperpilot/core/text_chunker.py",
        "paperpilot/core/vector_store.py",
        "paperpilot/core/paper_manager.py",
        "paperpilot/core/search_engine.py",
    ]
    
    all_exist = True
    for module in core_modules:
        if os.path.isfile(module):
            print(f"  ✓ {module}")
        else:
            print(f"  ✗ {module} NOT FOUND")
            all_exist = False
    
    return all_exist


def check_ui_files():
    """Verify UI files exist."""
    print("\nChecking UI files...")
    
    ui_files = [
        "paperpilot/ui/__init__.py",
        "paperpilot/ui/app.py",
        "paperpilot/ui/app_demo.py",
    ]
    
    all_exist = True
    for file in ui_files:
        if os.path.isfile(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} NOT FOUND")
            all_exist = False
    
    return all_exist


def check_examples():
    """Verify example files exist."""
    print("\nChecking example files...")
    
    example_files = [
        "examples/demo.py",
        "examples/example.py",
    ]
    
    all_exist = True
    for file in example_files:
        if os.path.isfile(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} NOT FOUND")
            all_exist = False
    
    return all_exist


def check_tests():
    """Verify test files exist."""
    print("\nChecking test files...")
    
    test_files = [
        "tests/test_components.py",
        "tests/create_test_pdf.py",
    ]
    
    all_exist = True
    for file in test_files:
        if os.path.isfile(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} NOT FOUND")
            all_exist = False
    
    return all_exist


def check_docs():
    """Verify documentation files exist."""
    print("\nChecking documentation files...")
    
    doc_files = [
        "docs/ARCHITECTURE_COMPARISON.md",
        "docs/MIGRATION_GUIDE.md",
        "docs/PLAN.md",
        "docs/RECOMMENDATION.md",
        "docs/USAGE.md",
    ]
    
    all_exist = True
    for file in doc_files:
        if os.path.isfile(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} NOT FOUND")
            all_exist = False
    
    return all_exist


def check_config_files():
    """Verify configuration files exist."""
    print("\nChecking configuration files...")
    
    config_files = [
        "config.yaml",
        "requirements.txt",
        "README.md",
        ".gitignore",
    ]
    
    all_exist = True
    for file in config_files:
        if os.path.isfile(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} NOT FOUND")
            all_exist = False
    
    return all_exist


def main():
    """Main verification function."""
    print("=" * 80)
    print("PaperPilot Project Structure Verification")
    print("=" * 80)
    print()
    
    checks = [
        check_directory_structure(),
        check_core_modules(),
        check_ui_files(),
        check_examples(),
        check_tests(),
        check_docs(),
        check_config_files(),
    ]
    
    print()
    print("=" * 80)
    if all(checks):
        print("✓ All structure checks passed!")
        print("=" * 80)
        return 0
    else:
        print("✗ Some structure checks failed!")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
