#!/usr/bin/env python3
"""
Test script to verify visualization fixes
"""

import sys
import os
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.visualizer import ResultVisualizer

def test_fixed_visualizations():
    """Test with realistic simulation data"""
    print("Testing fixed visualizations with realistic data...")
    
    # Create realistic protocol metrics
    protocol_metrics = {
        'teleportation_times': np.random.normal(0.32, 0.04, 75).tolist(),  # ~0.32s ± 0.04s
        'fidelities': np.random.normal(0.95, 0.02, 75).tolist(),  # ~0.95 ± 0.02
        'entanglement_consumption': list(range(1, 76)),  # Cumulative count
        'node_utilizations': [0.65, 0.58]  # Realistic utilization
    }
    
    # Create comparison data
    comparison_data = {
        "2_nodes_3_qubits": {
            'avg_teleportation_time': 0.315,
            'avg_fidelity': 0.947,
            'total_entanglements': 25,
            'total_operations': 75
        },
        "3_nodes_2_qubits": {
            'avg_teleportation_time': 0.285,
            'avg_fidelity': 0.952,
            'total_entanglements': 30,
            'total_operations': 80
        }
    }
    
    visualizer = ResultVisualizer()
    
    # Generate plots
    visualizer.plot_protocol_performance(protocol_metrics, "test_protocol_performance.png")
    visualizer.plot_comparison_analysis(comparison_data, "test_comparison_analysis.png")
    
    print("✅ Test visualizations generated successfully!")
    print("Check 'results/plots/' directory for:")
    print("  - test_protocol_performance.png")
    print("  - test_comparison_analysis.png")

if __name__ == "__main__":
    test_fixed_visualizations()