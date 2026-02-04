#!/usr/bin/env python3
"""
Quick setup verification script
"""

import os
import sys
from pathlib import Path

def check_env():
    """Check if .env file exists and has required keys"""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found")
        print("   Create .env file with: GEMINI_API_KEY=your_key_here")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env")
        return False
    
    print("✅ Environment configured")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required = ["google.genai", "dotenv"]
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
            print(f"✅ {pkg} installed")
        except ImportError:
            print(f"❌ {pkg} not installed")
            missing.append(pkg)
    
    if missing:
        print("\nInstall missing packages:")
        print("pip install google-generativeai python-dotenv")
        return False
    
    return True

def check_structure():
    """Check if all required folders exist"""
    required_dirs = [
        "llm",
        "personalizer",
        "roadmap_updater",
        "fake frontend",
        "conversion/output/semantic"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path}/ exists")
        else:
            print(f"❌ {dir_path}/ not found")
            all_exist = False
    
    return all_exist

def check_preset_roadmaps():
    """Check if preset roadmaps exist"""
    roadmaps = ["ai-ds", "fs", "ml", "gd", "sa"]
    all_exist = True
    
    for roadmap in roadmaps:
        path = Path(f"fake frontend/{roadmap}")
        if path.exists():
            print(f"✅ Preset roadmap: {roadmap}")
        else:
            print(f"❌ Preset roadmap missing: {roadmap}")
            all_exist = False
    
    return all_exist

def main():
    print("\n" + "="*60)
    print(" 🔍 SETUP VERIFICATION ".center(60))
    print("="*60 + "\n")
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Environment", check_env),
        ("Directory Structure", check_structure),
        ("Preset Roadmaps", check_preset_roadmaps)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n--- {name} ---")
        results.append(check_func())
    
    print("\n" + "="*60)
    if all(results):
        print(" ✅ ALL CHECKS PASSED - Ready to run! ".center(60))
        print("="*60)
        print("\nRun: python main.py")
    else:
        print(" ⚠️  SOME CHECKS FAILED - Fix issues above ".center(60))
        print("="*60)
    print()

if __name__ == "__main__":
    main()
