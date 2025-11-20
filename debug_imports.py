#!/usr/bin/env python3
"""
Debug script to check imports and file structure
"""

import os
import sys

def check_structure():
    print("🔍 Checking project structure...")
    
    # Check if we're in the right directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    # Check for essential files
    essential_files = [
        'run_simulation.py',
        'config.py', 
        'requirements.txt',
        'src/__init__.py',
        'src/network/__init__.py',
        'src/algorithms/__init__.py',
        'src/scheduler/__init__.py',
        'src/utils/__init__.py'
    ]
    
    missing_files = []
    for file in essential_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
    else:
        print("✅ All essential files found")
    
    return len(missing_files) == 0

def check_imports():
    print("\n🔍 Checking imports...")
    
    # Add src to Python path
    sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
    
    imports_to_test = [
        ('network.quantum_network', 'DistributedQuantumNetwork'),
        ('network.protocols', 'QuantumProtocols'),
        ('algorithms.grover', 'DistributedGrover'),
        ('algorithms.qft', 'DistributedQFT'),
        ('scheduler.quantum_scheduler', 'QuantumScheduler'),
        ('utils.visualizer', 'ResultVisualizer')
    ]
    
    failed_imports = []
    
    for module_name, class_name in imports_to_test:
        try:
            module = __import__(f'src.{module_name}', fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
        except ImportError as e:
            print(f"❌ {module_name}.{class_name}: {e}")
            failed_imports.append((module_name, class_name, str(e)))
        except AttributeError as e:
            print(f"❌ {module_name}.{class_name}: {e}")
            failed_imports.append((module_name, class_name, str(e)))
    
    return len(failed_imports) == 0

def check_config():
    print("\n🔍 Checking config...")
    try:
        from config import NETWORK_CONFIG, SIMULATION_CONFIG
        print("✅ config.py loaded successfully")
        print(f"   Network config: {NETWORK_CONFIG}")
        print(f"   Simulation config: {SIMULATION_CONFIG}")
        return True
    except Exception as e:
        print(f"❌ config.py error: {e}")
        return False

if __name__ == "__main__":
    print("DQC Project Debug Tool")
    print("=" * 50)
    
    structure_ok = check_structure()
    imports_ok = check_imports()
    config_ok = check_config()
    
    print("\n" + "=" * 50)
    if all([structure_ok, imports_ok, config_ok]):
        print("🎉 All checks passed! Your project should run correctly.")
    else:
        print("⚠️  Some issues found. Please fix them before running the simulation.")  