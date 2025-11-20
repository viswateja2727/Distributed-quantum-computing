import heapq
import time
from typing import List, Dict, Tuple, Optional
from collections import deque
import logging

logger = logging.getLogger(__name__)

class QuantumScheduler:
    """Schedules quantum circuits on distributed QPUs"""
    
    def __init__(self, network):
        self.network = network
        self.schedule_queue = []
        self.completed_circuits = []
        self.scheduling_history = []
        
    def schedule_circuit(self, subcircuits: List[Dict], priority: int = 1):
        """Schedule subcircuits for execution"""
        timestamp = time.time()
        
        for i, subcircuit in enumerate(subcircuits):
            heapq.heappush(self.schedule_queue, 
                         (priority, timestamp, i, subcircuit))
        
        logger.info(f"Scheduled {len(subcircuits)} subcircuits with priority {priority}")
    
    def execute_schedule(self) -> Dict:
        """Execute the scheduled circuits"""
        start_time = self.network.global_time
        execution_results = []
        
        temp_queue = self.schedule_queue.copy()
        self.schedule_queue = []  # Clear the queue
        
        while temp_queue:
            priority, timestamp, circuit_id, subcircuit = heapq.heappop(temp_queue)
            
            # Find available node with sufficient qubits
            target_node = self._find_available_node(subcircuit['required_qubits'])
            
            if target_node is not None:
                # Execute on selected node
                result = self._execute_on_node(target_node, subcircuit)
                execution_results.append(result)
                
                logger.debug(f"Executed subcircuit {circuit_id} on node {target_node}")
            else:
                # No available node, reschedule
                heapq.heappush(self.schedule_queue, 
                             (priority + 1, timestamp, circuit_id, subcircuit))
        
        total_time = self.network.global_time - start_time
        
        schedule_analysis = {
            'total_execution_time': total_time,
            'circuits_executed': len(execution_results),
            'average_circuit_time': total_time / max(1, len(execution_results)),
            'node_utilization': self._calculate_node_utilization(),
            'schedule_efficiency': len(execution_results) / max(1, len(self.schedule_queue) + len(execution_results))
        }
        
        self.scheduling_history.append(schedule_analysis)
        
        return schedule_analysis
    
    def _find_available_node(self, required_qubits: int) -> Optional[int]:
        """Find a node with sufficient available qubits"""
        for node in self.network.nodes:
            if len(node.available_qubits) >= required_qubits:
                return node.node_id
        return None
    
    def _execute_on_node(self, node_id: int, subcircuit: Dict) -> Dict:
        """Execute subcircuit on specific node"""
        node = self.network.nodes[node_id]
        
        # Mark qubits as used
        used_qubits = list(node.available_qubits)[:subcircuit['required_qubits']]
        for qubit in used_qubits:
            node.available_qubits.remove(qubit)
        
        # Simulate circuit execution
        execution_time = 0.1  # Base execution time
        for i in range(subcircuit['required_qubits']):
            exec_time = node.execute_gate('H', [i], 0.01)
            execution_time += exec_time
        
        # Free qubits
        for qubit in used_qubits:
            node.available_qubits.add(qubit)
        
        return {
            'node_id': node_id,
            'subcircuit_id': subcircuit['partition_id'],
            'execution_time': execution_time,
            'qubits_used': used_qubits
        }
    
    def _calculate_node_utilization(self) -> List[float]:
        """Calculate utilization for each node"""
        utilizations = []
        for node in self.network.nodes:
            utilization = node.get_utilization()
            utilizations.append(utilization)
        return utilizations