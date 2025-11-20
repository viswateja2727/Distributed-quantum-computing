#!/usr/bin/env python3
"""
Alternative runner with better error handling
"""

import os
import sys
import logging

# Get the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(SCRIPT_DIR, 'src')

# Add src to Python path
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

def setup_logging():
    """Setup logging with proper file paths"""
    log_dir = os.path.join(SCRIPT_DIR, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'dqc_simulation.log')),
            logging.StreamHandler(),
        ],
    )

def main():
    print("DQC Simulation - Alternative Runner")
    print("=" * 50)
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Import after path setup
        from src.network.quantum_network import DistributedQuantumNetwork
        from src.network.protocols import QuantumProtocols
        
        logger.info("Starting simulation...")
        
        # Simple test
        network = DistributedQuantumNetwork(2, 3)
        protocols = QuantumProtocols(network)
        
        # Run a few operations
        for i in range(5):
            tele_time, fidelity = protocols.teleport_qubit(0, 0, 1, 0)
            logger.info(f"Operation {i+1}: Time={tele_time:.3f}s, Fidelity={fidelity:.3f}")
        
        logger.info("Simulation completed successfully!")
        print("✅ Simulation ran successfully!")
        
    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        print(f"❌ Simulation failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()