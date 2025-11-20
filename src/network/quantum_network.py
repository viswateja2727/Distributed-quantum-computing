import numpy as np
import time
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class QuantumNetworkNode:
    """Represents a single QPU in the distributed quantum network"""
    
    def __init__(self, node_id: int, num_qubits: int):
        self.node_id = node_id
        self.num_qubits = num_qubits
        self.qubits = [{
            'state': None,
            'entangled_with': (None, None),
            'last_operation': None
        } for _ in range(num_qubits)]
        self.available_qubits = set(range(num_qubits))
        self.operation_history = []
        self.total_operations = 0
        
        logger.debug(f"Initialized Node {node_id} with {num_qubits} qubits")
    
    def execute_gate(self, gate_type: str, qubits: List[int], duration: float = 0.01) -> float:
        """Execute a quantum gate on specified qubits"""
        if not all(0 <= q < self.num_qubits for q in qubits):
            raise ValueError(f"Invalid qubit indices: {qubits}")
        
        # Simulate gate execution time
        time.sleep(duration)
        
        operation_record = {
            'gate': gate_type,
            'qubits': qubits,
            'timestamp': time.time(),
            'duration': duration,
            'node_id': self.node_id
        }
        
        self.operation_history.append(operation_record)
        self.total_operations += 1
        
        logger.debug(f"Node {self.node_id}: Executed {gate_type} on qubits {qubits}")
        return duration
    
    def get_utilization(self) -> float:
        """Calculate node utilization based on operation history"""
        if not self.operation_history:
            return 0.0
        return len(self.operation_history) / max(self.total_operations, 1)
    
    def reset_qubit(self, qubit_idx: int):
        """Reset a qubit to its initial state"""
        if 0 <= qubit_idx < self.num_qubits:
            self.qubits[qubit_idx] = {
                'state': None,
                'entangled_with': (None, None),
                'last_operation': None
            }
            self.available_qubits.add(qubit_idx)
            logger.debug(f"Node {self.node_id}: Reset qubit {qubit_idx}")

class DistributedQuantumNetwork:
    """Manages the distributed quantum computing network"""
    
    def __init__(self, num_nodes: int, qubits_per_node: int, communication_latency: float = 0.1):
        self.nodes = [QuantumNetworkNode(i, qubits_per_node) for i in range(num_nodes)]
        self.communication_latency = communication_latency
        self.entanglement_pairs = []
        self.communication_history = []
        self.global_time = 0.0
        
        logger.info(f"Initialized quantum network with {num_nodes} nodes, {qubits_per_node} qubits each")
    
    def create_entanglement(self, node1: int, qubit1: int, node2: int, qubit2: int) -> float:
        """Create entanglement between two qubits on different nodes"""
        if node1 == node2:
            raise ValueError("Entanglement must be between different nodes")
        
        if not (0 <= node1 < len(self.nodes) and 0 <= node2 < len(self.nodes)):
            raise ValueError(f"Invalid node indices: {node1}, {node2}")
        
        # Check qubit indices
        if not (0 <= qubit1 < self.nodes[node1].num_qubits and 0 <= qubit2 < self.nodes[node2].num_qubits):
            raise ValueError(f"Invalid qubit indices: {qubit1}, {qubit2}")
        
        # Simulate entanglement creation time
        entanglement_time = self.communication_latency * 1.5  # Entanglement takes longer
        self.global_time += entanglement_time
        
        # Record entanglement
        entanglement_pair = ((node1, qubit1), (node2, qubit2))
        self.entanglement_pairs.append(entanglement_pair)
        
        # Update qubit states
        self.nodes[node1].qubits[qubit1]['entangled_with'] = (node2, qubit2)
        self.nodes[node2].qubits[qubit2]['entangled_with'] = (node1, qubit1)
        
        logger.info(f"Created entanglement: Node{node1}.Q{qubit1} <-> Node{node2}.Q{qubit2}")
        return entanglement_time
    
    def get_network_stats(self) -> Dict:
        """Get comprehensive network statistics"""
        stats = {
            'total_nodes': len(self.nodes),
            'total_qubits': sum(node.num_qubits for node in self.nodes),
            'active_entanglements': len(self.entanglement_pairs),
            'total_operations': sum(node.total_operations for node in self.nodes),
            'node_utilizations': [node.get_utilization() for node in self.nodes],
            'global_time': self.global_time
        }
        return stats