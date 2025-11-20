#!/usr/bin/env python3
"""
Minimal test to verify core functionality
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_components():
    print("Testing basic components...")
    
    try:
        from src.network.quantum_network import DistributedQuantumNetwork
        from src.network.protocols import QuantumProtocols
        
        # Create a simple network
        network = DistributedQuantumNetwork(2, 2)
        protocols = QuantumProtocols(network)
        
        print("✅ Network and protocols created")
        
        # Test a simple operation
        tele_time, fidelity = protocols.teleport_qubit(0, 0, 1, 0)
        print(f"✅ Teleportation test: {tele_time:.3f}s, fidelity: {fidelity:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_basic_components()
    if success:
        print("\n🎉 Basic test passed! You can now run the full simulation.")
    else:
        print("\n⚠️  Basic test failed. Check the error above.")