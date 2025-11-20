"""
Configuration for Distributed Quantum Computing Simulation
"""

NETWORK_CONFIG = {
    'default_num_nodes': 2,
    'default_qubits_per_node': 3,
    'communication_latency': 0.1,
    'gate_execution_time': 0.01,
    'entanglement_time': 0.15
}

SIMULATION_CONFIG = {
    'num_operations': 50,
    'random_seed': 42,
    'fidelity_threshold': 0.95
}

ALGORITHM_CONFIG = {
    'grover_iterations': 2,
    'qft_optimize': True
}

VISUALIZATION_CONFIG = {
    'figure_size': (12, 8),
    'dpi': 300,
    'style': 'seaborn-v0_8-whitegrid'
}