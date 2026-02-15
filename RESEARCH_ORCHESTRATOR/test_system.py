#!/usr/bin/env python3
"""
Test script for Constellation Research Toolchain
"""

import os
from pathlib import Path
import yaml

def test_config():
    """Test if config exists and is valid"""
    print("Testing configuration...")
    
    if not os.path.exists("config.yaml"):
        print("❌ config.yaml not found")
        return False
    
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        print("✅ Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return False

def test_dependencies():
    """Test if required dependencies are available"""
    print("\nTesting dependencies...")
    
    # Test Python packages
    packages = [
        ("requests", "requests"),
        ("yaml", "yaml"),
        ("networkx", "networkx"), 
        ("matplotlib", "matplotlib"),
        ("chromadb", "chromadb"),
        ("sentence_transformers", "sentence_transformers")
    ]
    
    success = True
    for name, import_name in packages:
        try:
            __import__(import_name)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} (pip install {name})")
            success = False
    
    # Test ripgrep
    import subprocess
    try:
        result = subprocess.run(['rg', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ ripgrep")
        else:
            print("❌ ripgrep (install with: sudo apt install ripgrep)")
            success = False
    except FileNotFoundError:
        print("❌ ripgrep (install with: sudo apt install ripgrep)")
        success = False
    except subprocess.TimeoutExpired:
        print("❌ ripgrep (timeout)")
        success = False
    
    return success

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directories...")
    
    dirs = [
        "modules",
        "tools", 
        "samples",
        "docs",
        "research_outputs"
    ]
    
    success = True
    for d in dirs:
        if os.path.exists(d):
            print(f"✅ {d}")
        else:
            print(f"❌ {d}")
            # Create if missing
            try:
                os.makedirs(d, exist_ok=True)
                print(f"   Created {d}")
            except Exception as e:
                print(f"   Failed to create {d}: {e}")
                success = False
    
    return success

def test_modules():
    """Test if core modules can be imported"""
    print("\nTesting modules...")
    
    modules = [
        "modules.local_search",
        "modules.model_runner", 
        "modules.evidence",
        "modules.pattern_recognition",
        "modules.synthesis",
        "modules.report_generator",
        "modules.rag_engine"
    ]
    
    success = True
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            success = False
    
    return success

def test_sample_run():
    """Test a simple research run"""
    print("\nTesting sample research run...")
    
    # Create a simple test file to search
    test_dir = "test_data"
    os.makedirs(test_dir, exist_ok=True)
    
    test_file = os.path.join(test_dir, "test.md")
    with open(test_file, 'w') as f:
        f.write("# Test Research\n\nThis is a test file for research purposes.\n\nResearch is important.")
    
    try:
        from modules.local_search import LocalSearch
        search = LocalSearch(root_path=test_dir)
        results = search.search(["research"], file_extensions=["md"])
        
        print(f"✅ Sample search completed: found {len(results)} results")
        
        # Clean up
        os.remove(test_file)
        os.rmdir(test_dir)
        
        return True
    except Exception as e:
        print(f"❌ Sample research failed: {e}")
        return False

def main():
    print("Constellation Research Toolchain - System Test")
    print("=" * 50)
    
    all_tests = [
        ("Configuration", test_config),
        ("Dependencies", test_dependencies), 
        ("Directories", test_directories),
        ("Modules", test_modules),
        ("Sample Run", test_sample_run)
    ]
    
    results = []
    for name, test_func in all_tests:
        result = test_func()
        results.append((name, result))
        print()
    
    print("Test Results:")
    print("-" * 20)
    all_passed = True
    for name, result in results:
        status = "PASS" if result else "FAIL"
        icon = "✅" if result else "❌"
        print(f"{icon} {name}: {status}")
        if not result:
            all_passed = False
    
    print("-" * 20)
    if all_passed:
        print("🎉 All tests passed! System is ready.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    return all_passed

if __name__ == "__main__":
    main()