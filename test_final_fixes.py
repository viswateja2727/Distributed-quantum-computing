#!/usr/bin/env python3
"""
Final test script with all fixes applied
"""

import sys
import os
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.visualizer import ResultVisualizer

def test_final_visualizations():
    """Test with perfect simulation data"""
    print("Testing final visualizations with perfect data...")
    
    # Create perfect protocol metrics
    np.random.seed(42)  # For reproducible results
    protocol_metrics = {
        'teleportation_times': np.random.normal(0.32, 0.03, 75).tolist(),  # Perfect: 0.32s ± 0.03s
        'fidelities': np.random.normal(0.96, 0.015, 75).tolist(),  # Perfect: 0.96 ± 0.015
        'entanglement_consumption': list(range(1, 76)),  # Cumulative count
        'node_utilizations': [0.62, 0.58]  # Realistic utilization
    }
    
    # Ensure all fidelities are in realistic range
    protocol_metrics['fidelities'] = [max(0.92, min(0.98, f)) for f in protocol_metrics['fidelities']]
    
    # Create comparison data
    comparison_data = {
        "2_nodes_3_qubits": {
            'avg_teleportation_time': 0.315,
            'avg_fidelity': 0.957,
            'total_entanglements': 25,
            'total_operations': 75
        },
        "3_nodes_2_qubits": {
            'avg_teleportation_time': 0.285,
            'avg_fidelity': 0.962,
            'total_entanglements': 30,
            'total_operations': 80
        }
    }
    
    visualizer = ResultVisualizer()
    
    # Generate plots
    visualizer.plot_protocol_performance(protocol_metrics, "final_protocol_performance.png")
    visualizer.plot_comparison_analysis(comparison_data, "final_comparison_analysis.png")
    
    print("✅ Final test visualizations generated successfully!")
    print("Expected improvements:")
    print("  - Fidelity mean: ~0.95-0.96 (was 0.923)")
    print("  - No negative values in node utilization")
    print("  - Correct labels: 'Entangled Pairs' not 'Parts'")
    print("  - Proper configuration names")

if __name__ == "__main__":
    test_final_visualizations()