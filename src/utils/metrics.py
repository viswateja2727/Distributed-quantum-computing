import numpy as np
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

def calculate_efficiency_metrics(protocol_metrics: Dict, network_stats: Dict) -> Dict:
    """Calculate comprehensive efficiency metrics for the distributed system"""
    
    efficiency = {}
    
    # Communication efficiency
    avg_teleport_time = protocol_metrics.get('avg_teleportation_time', 0)
    efficiency['communication_efficiency'] = 1.0 / max(avg_teleport_time, 0.001)  # Avoid division by zero
    
    # Resource utilization
    total_qubits = network_stats.get('total_qubits', 1)
    total_entanglements = protocol_metrics.get('total_entanglements', 0)
    efficiency['resource_utilization'] = total_entanglements / total_qubits
    
    # Fidelity efficiency
    avg_fidelity = protocol_metrics.get('avg_fidelity', 1.0)
    efficiency['fidelity_efficiency'] = avg_fidelity
    
    # Throughput
    total_operations = protocol_metrics.get('total_operations', 0)
    total_time = network_stats.get('global_time', 1)
    efficiency['throughput'] = total_operations / total_time
    
    # Overall efficiency score (weighted combination)
    weights = {
        'communication': 0.3,
        'resource': 0.25,
        'fidelity': 0.3,
        'throughput': 0.15
    }
    
    # Normalize scores to 0-1 range
    comm_score = min(efficiency['communication_efficiency'] / 10, 1.0)  # Assuming 10 is max reasonable
    resource_score = min(efficiency['resource_utilization'], 1.0)
    fidelity_score = efficiency['fidelity_efficiency']
    throughput_score = min(efficiency['throughput'] / 5, 1.0)  # Assuming 5 ops/sec is max reasonable
    
    efficiency['overall_score'] = (
        weights['communication'] * comm_score +
        weights['resource'] * resource_score +
        weights['fidelity'] * fidelity_score +
        weights['throughput'] * throughput_score
    )
    
    efficiency['normalized_scores'] = {
        'communication': comm_score,
        'resource': resource_score,
        'fidelity': fidelity_score,
        'throughput': throughput_score
    }
    
    logger.info(f"Calculated efficiency metrics: overall_score={efficiency['overall_score']:.3f}")
    
    return efficiency

def compare_configurations(config_results: Dict) -> Dict:
    """Compare results across different network configurations"""
    comparison = {}
    
    for config_name, results in config_results.items():
        protocol_metrics = results.get('protocol_metrics', {})
        network_stats = results.get('network_stats', {})
        
        comparison[config_name] = {
            'avg_teleportation_time': protocol_metrics.get('avg_teleportation_time', 0),
            'avg_fidelity': protocol_metrics.get('avg_fidelity', 0),
            'throughput': protocol_metrics.get('total_operations', 0) / max(network_stats.get('global_time', 1), 1),
            'resource_efficiency': protocol_metrics.get('total_entanglements', 0) / max(network_stats.get('total_qubits', 1), 1),
            'total_operations': protocol_metrics.get('total_operations', 0)
        }
    
    # Rank configurations
    ranked_configs = sorted(
        comparison.items(),
        key=lambda x: (
            -x[1]['avg_fidelity'],  # Higher fidelity better
            x[1]['avg_teleportation_time'],  # Lower time better
            -x[1]['throughput']  # Higher throughput better
        )
    )
    
    comparison['ranking'] = [config[0] for config in ranked_configs]
    comparison['best_config'] = ranked_configs[0][0] if ranked_configs else None
    
    return comparison