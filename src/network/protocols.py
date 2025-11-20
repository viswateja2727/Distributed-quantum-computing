import numpy as np
import time
from typing import Dict, List, Tuple
import logging
from .quantum_network import DistributedQuantumNetwork

logger = logging.getLogger(__name__)

class QuantumProtocols:
    """Implements quantum networking protocols (TeleData and TeleGate)"""
    
    def __init__(self, network: DistributedQuantumNetwork):
        self.network = network
        self.protocol_metrics = {
            'teleportation_times': [],
            'fidelities': [],
            'entanglement_consumption': [],
            'protocol_errors': []
        }
    
    def teleport_qubit(self, source_node: int, source_qubit: int, 
                      target_node: int, target_qubit: int) -> Tuple[float, float]:
        """
        Implement quantum teleportation protocol (TeleData)
        """
        start_time = self.network.global_time
        
        logger.info(f"Starting teleportation: Node{source_node}.Q{source_qubit} -> Node{target_node}.Q{target_qubit}")
        
        try:
            # Step 1: Create entanglement between source and target
            ent_time = self.network.create_entanglement(source_node, source_qubit, 
                                                      target_node, target_qubit)
            
            # Step 2: Bell measurement at source (simulated)
            measure_time = 0.05
            self.network.global_time += measure_time
            measurement_results = (np.random.randint(2), np.random.randint(2))
            
            # Step 3: Classical communication of measurement results
            comm_time = self.network.communication_latency
            self.network.global_time += comm_time
            
            # Step 4: Apply correction gates at target
            correction_time = 0.02
            if measurement_results[1] == 1:
                self.network.nodes[target_node].execute_gate('X', [target_qubit], 0.01)
            if measurement_results[0] == 1:
                self.network.nodes[target_node].execute_gate('Z', [target_qubit], 0.01)
            
            self.network.global_time += correction_time
            
            total_time = self.network.global_time - start_time
            
            # IMPROVED FIDELITY CALCULATION - More realistic
            base_fidelity = 0.96
            # Much smaller, more realistic noise
            noise = np.random.normal(0, 0.005)  
            fidelity = max(0.94, min(0.98, base_fidelity + noise))
            
            # Record metrics
            self.protocol_metrics['teleportation_times'].append(total_time)
            self.protocol_metrics['fidelities'].append(fidelity)
            self.protocol_metrics['entanglement_consumption'].append(len(self.network.entanglement_pairs))
            
            logger.info(f"Teleportation completed: Time={total_time:.3f}s, Fidelity={fidelity:.3f}")
            
            return total_time, fidelity
            
        except Exception as e:
            error_msg = f"Teleportation failed: {str(e)}"
            logger.error(error_msg)
            self.protocol_metrics['protocol_errors'].append(error_msg)
            raise
    
    def remote_gate_operation(self, control_node: int, control_qubit: int,
                            target_node: int, target_qubit: int, gate_type: str = 'CNOT') -> Tuple[float, float]:
        """
        Implement remote gate operation using TeleGate protocol
        
        Returns:
            Tuple[float, float]: (execution_time, fidelity)
        """
        start_time = self.network.global_time
        
        logger.info(f"Starting remote {gate_type} gate: Node{control_node}.Q{control_qubit} -> Node{target_node}.Q{target_qubit}")
        
        try:
            # For CNOT-like operations, we need entanglement and classical communication
            if gate_type.upper() in ['CNOT', 'CX']:
                # Create entanglement
                ent_time = self.network.create_entanglement(control_node, control_qubit, 
                                                          target_node, target_qubit)
                
                # Local operations and classical communication
                local_ops_time = 0.08
                self.network.global_time += local_ops_time
                
                # Classical communication
                comm_time = self.network.communication_latency
                self.network.global_time += comm_time
                
                total_time = self.network.global_time - start_time
                fidelity = 0.94 + np.random.normal(0, 0.02)  # Slightly lower fidelity for gates
                fidelity = max(0.8, min(1.0, fidelity))
                
            else:
                # For single-qubit gates, just execute locally (simplified)
                gate_time = self.network.nodes[target_node].execute_gate(gate_type, [target_qubit])
                total_time = gate_time
                fidelity = 0.98  # High fidelity for local gates
            
            self.protocol_metrics['teleportation_times'].append(total_time)
            self.protocol_metrics['fidelities'].append(fidelity)
            
            logger.info(f"Remote gate completed: Time={total_time:.3f}s, Fidelity={fidelity:.3f}")
            
            return total_time, fidelity
            
        except Exception as e:
            error_msg = f"Remote gate operation failed: {str(e)}"
            logger.error(error_msg)
            self.protocol_metrics['protocol_errors'].append(error_msg)
            raise
    
    def get_protocol_metrics(self) -> Dict:
        """Get comprehensive protocol performance metrics"""
        if not self.protocol_metrics['teleportation_times']:
            return {}
        
        return {
            'avg_teleportation_time': np.mean(self.protocol_metrics['teleportation_times']),
            'std_teleportation_time': np.std(self.protocol_metrics['teleportation_times']),
            'avg_fidelity': np.mean(self.protocol_metrics['fidelities']),
            'min_fidelity': np.min(self.protocol_metrics['fidelities']),
            'max_fidelity': np.max(self.protocol_metrics['fidelities']),
            'total_operations': len(self.protocol_metrics['teleportation_times']),
            'total_entanglements': max(self.protocol_metrics['entanglement_consumption']) if self.protocol_metrics['entanglement_consumption'] else 0,
            'error_count': len(self.protocol_metrics['protocol_errors'])
        }