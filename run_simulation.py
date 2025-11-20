#!/usr/bin/env python3
"""
Main simulation runner for Distributed Quantum Computing Project
"""

import logging
import time
from typing import Optional

import numpy as np

# Project imports
from src.network.quantum_network import DistributedQuantumNetwork
from src.network.protocols import QuantumProtocols
from src.algorithms.grover import DistributedGrover
from src.algorithms.qft import DistributedQFT
from src.scheduler.quantum_scheduler import QuantumScheduler
from src.utils.visualizer import ResultVisualizer
from src.utils.metrics import calculate_efficiency_metrics, compare_configurations

# Configuration
try:
    from config import NETWORK_CONFIG, SIMULATION_CONFIG
except ImportError:
    print("config.py not found. Using default configuration...")
    NETWORK_CONFIG = {
        "default_num_nodes": 2,
        "default_qubits_per_node": 3,
        "communication_latency": 0.1,
        "gate_execution_time": 0.01,
        "entanglement_time": 0.15,
    }

    SIMULATION_CONFIG = {
        "num_operations": 50,
        "random_seed": 42,
        "fidelity_threshold": 0.95,
    }

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("dqc_simulation.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


class DQCSimulation:
    """Main simulation class for Distributed Quantum Computing"""

    def __init__(self):
        self.network: Optional[DistributedQuantumNetwork] = None
        self.protocols: Optional[QuantumProtocols] = None
        self.scheduler: Optional[QuantumScheduler] = None
        self.visualizer = ResultVisualizer()
        self.results = {}

    def setup_network(
        self,
        num_nodes: Optional[int] = None,
        qubits_per_node: Optional[int] = None,
    ):
        """Setup the quantum network"""
        if num_nodes is None:
            num_nodes = NETWORK_CONFIG["default_num_nodes"]
        if qubits_per_node is None:
            qubits_per_node = NETWORK_CONFIG["default_qubits_per_node"]

        if num_nodes is None or qubits_per_node is None:
            raise ValueError(
                "num_nodes and qubits_per_node must be integers or convertible to int"
            )

        try:
            num_nodes = int(num_nodes)
            qubits_per_node = int(qubits_per_node)
        except (TypeError, ValueError):
            raise ValueError(
                "num_nodes and qubits_per_node must be integers or convertible to int"
            )

        self.network = DistributedQuantumNetwork(
            num_nodes=num_nodes,
            qubits_per_node=qubits_per_node,
            communication_latency=NETWORK_CONFIG["communication_latency"],
        )

        self.protocols = QuantumProtocols(self.network)
        self.scheduler = QuantumScheduler(self.network)

        logger.info(
            f"Setup quantum network with {num_nodes} nodes, {qubits_per_node} qubits each"
        )

    def run_protocol_simulation(self, num_operations: Optional[int] = None):
        """Run quantum networking protocol simulations"""
        if num_operations is None:
            num_operations = SIMULATION_CONFIG["num_operations"]

        logger.info(f"Starting protocol simulation with {num_operations} operations")

        # Ensure the network and protocols are initialized
        if self.protocols is None or self.network is None:
            logger.info("Network/protocols not initialized, setting up default network")
            self.setup_network()

        try:
            assert num_operations is not None
            num_operations = int(num_operations)
        except (TypeError, ValueError, AssertionError):
            raise ValueError(
                "num_operations must be an integer or convertible to int"
            )

        assert (
            self.protocols is not None and self.network is not None
        ), "Network/protocols not initialized"
        protocols = self.protocols

        # TeleData (teleportation)
        for i in range(num_operations):
            node1, node2 = self._get_random_nodes()
            qubit1 = self._get_random_qubit()
            qubit2 = self._get_random_qubit()

            try:
                protocols.teleport_qubit(node1, qubit1, node2, qubit2)

                if (i + 1) % 20 == 0:
                    logger.info(
                        f"Completed {i + 1}/{num_operations} teleportation operations"
                    )
            except Exception as e:
                logger.warning(f"Operation {i + 1} failed: {e}")
                continue

        # TeleGate (remote gates)
        for i in range(num_operations // 2):
            node1, node2 = self._get_random_nodes()
            qubit1 = self._get_random_qubit()
            qubit2 = self._get_random_qubit()

            try:
                protocols.remote_gate_operation(
                    node1,
                    qubit1,
                    node2,
                    qubit2,
                    "CNOT",
                )
            except Exception as e:
                logger.warning(f"Gate operation {i + 1} failed: {e}")
                continue

        protocol_metrics = self.protocols.get_protocol_metrics()
        network_stats = self.network.get_network_stats()

        self.results["protocol_metrics"] = protocol_metrics
        self.results["network_stats"] = network_stats
        self.results["detailed_metrics"] = self.protocols.protocol_metrics

        logger.info("Protocol simulation completed")

        return protocol_metrics

    def run_algorithm_simulation(self):
        """Run distributed quantum algorithm simulations"""
        logger.info("Starting algorithm simulation")

        algorithm_results = {}

        # Grover
        grover_sim = DistributedGrover(num_qubits=4)
        grover_results = grover_sim.prepare_distributed_execution(num_partitions=2)
        algorithm_results["grover"] = grover_results

        # QFT
        qft_sim = DistributedQFT(num_qubits=4)
        qft_results = qft_sim.prepare_distributed_execution(num_partitions=2)
        algorithm_results["qft"] = qft_results

        self.results["algorithm_results"] = algorithm_results
        logger.info("Algorithm simulation completed")

        return algorithm_results

    def run_scheduling_simulation(self):
        """Run scheduling simulation"""
        logger.info("Starting scheduling simulation")

        if "algorithm_results" in self.results:
            grover_subcircuits = self.results["algorithm_results"]["grover"][
                "subcircuits"
            ]

            if self.scheduler is None:
                if self.network is None:
                    self.setup_network()
                self.scheduler = QuantumScheduler(self.network)

            self.scheduler.schedule_circuit(grover_subcircuits, priority=1)
            schedule_results = self.scheduler.execute_schedule()

            self.results["scheduling_results"] = schedule_results
            logger.info("Scheduling simulation completed")

            return schedule_results

        logger.warning("No algorithm results available for scheduling")
        return {}

    def _get_random_nodes(self) -> tuple:
        """Get two different random nodes"""
        if self.network is None or not hasattr(self.network, "nodes"):
            raise ValueError("Network is not initialized or missing 'nodes' attribute")

        nodes = list(range(len(self.network.nodes)))
        return tuple(np.random.choice(nodes, 2, replace=False))

    def _get_random_qubit(self) -> int:
        """Get a random qubit index"""
        if (
            self.network is None
            or not hasattr(self.network, "nodes")
            or not self.network.nodes
        ):
            raise ValueError("Network is not initialized or missing 'nodes' attribute")

        return int(np.random.randint(0, self.network.nodes[0].num_qubits))

    def analyze_results(self):
        """Analyze simulation results and identify bottlenecks"""
        logger.info("Analyzing simulation results")

        bottlenecks = {}

        if "protocol_metrics" in self.results:
            metrics = self.results["protocol_metrics"]

            avg_latency = metrics.get("avg_teleportation_time", 0)
            bottlenecks["high_communication_latency"] = avg_latency > 0.2

            avg_fidelity = metrics.get("avg_fidelity", 1.0)
            bottlenecks["low_fidelity"] = avg_fidelity < 0.95

            total_entanglements = metrics.get("total_entanglements", 0)
            total_qubits = self.results["network_stats"]["total_qubits"]
            bottlenecks["high_resource_usage"] = total_entanglements > total_qubits * 0.6

        self.results["bottlenecks"] = bottlenecks
        logger.info("Bottleneck analysis completed")

        return bottlenecks

    def generate_recommendations(self):
        """Generate optimization recommendations based on analysis"""
        bottlenecks = self.results.get("bottlenecks", {})
        recommendations = []

        if bottlenecks.get("high_communication_latency"):
            recommendations.extend(
                [
                    "Implement parallel entanglement distribution protocols",
                    "Use entanglement purification to reduce retry attempts",
                    "Optimize classical communication channels",
                ]
            )

        if bottlenecks.get("low_fidelity"):
            recommendations.extend(
                [
                    "Implement quantum error correction codes",
                    "Use entanglement purification techniques",
                    "Increase resource allocation for fidelity-critical operations",
                ]
            )

        if bottlenecks.get("high_resource_usage"):
            recommendations.extend(
                [
                    "Implement dynamic resource allocation strategies",
                    "Use entanglement recycling where possible",
                    "Optimize circuit partitioning to reduce cross-partition operations",
                ]
            )

        recommendations.extend(
            [
                "Use adaptive scheduling based on real-time network conditions",
                "Implement hybrid classical-quantum approaches for complex circuits",
                "Consider circuit compression techniques to reduce operation count",
            ]
        )

        self.results["recommendations"] = recommendations

        print("\n=== OPTIMIZATION RECOMMENDATIONS ===")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")

        return recommendations

    def visualize_results(self):
        """Create visualizations of simulation results"""
        logger.info("Generating visualizations")

        if "detailed_metrics" in self.results:
            self.visualizer.plot_protocol_performance(
                self.results["detailed_metrics"],
                "protocol_performance.png",
            )

        comparison_data = {
            "2_nodes_3_qubits": self.results.get("protocol_metrics", {}),
        }
        self.visualizer.plot_comparison_analysis(
            comparison_data,
            "single_configuration.png",
        )

        logger.info("Visualization generation completed")

    def run_complete_simulation(self):
        """Run the complete simulation pipeline"""
        logger.info("Starting complete DQC simulation")
        start_time = time.time()

        try:
            self.setup_network()
            self.run_protocol_simulation(num_operations=50)
            self.run_algorithm_simulation()
            self.run_scheduling_simulation()
            self.analyze_results()
            self.generate_recommendations()
            self.visualize_results()

            total_time = time.time() - start_time
            logger.info(f"Complete simulation finished in {total_time:.2f} seconds")

            self._print_summary()
            return self.results

        except Exception as e:
            logger.error(f"Simulation failed: {e}")
            raise

    def _print_summary(self):
        """Print a summary of simulation results"""
        print("\n" + "=" * 60)
        print("DISTRIBUTED QUANTUM COMPUTING SIMULATION SUMMARY")
        print("=" * 60)

        if "protocol_metrics" in self.results:
            metrics = self.results["protocol_metrics"]
            print("\nPROTOCOL PERFORMANCE:")
            print(
                f"  Average Teleportation Time: {metrics.get('avg_teleportation_time', 0):.3f}s"
            )
            print(f"  Average Fidelity: {metrics.get('avg_fidelity', 0):.3f}")
            print(f"  Total Operations: {metrics.get('total_operations', 0)}")
            print(f"  Total Entanglements: {metrics.get('total_entanglements', 0)}")

        if "network_stats" in self.results:
            stats = self.results["network_stats"]
            print("\nNETWORK STATISTICS:")
            print(f"  Total Nodes: {stats.get('total_nodes', 0)}")
            print(f"  Total Qubits: {stats.get('total_qubits', 0)}")
            print(f"  Global Time: {stats.get('global_time', 0):.2f}s")

        if "bottlenecks" in self.results:
            bottlenecks = self.results["bottlenecks"]
            print("\nBOTTLENECKS IDENTIFIED:")
            for bottleneck, exists in bottlenecks.items():
                status = "YES" if exists else "NO"
                print(f"  {bottleneck.replace('_', ' ').title()}: {status}")

        print("=" * 60)


def main():
    """Main entry point for the simulation"""
    print("Distributed Quantum Computing Simulation")
    print("=======================================")

    sim = DQCSimulation()
    results = sim.run_complete_simulation()

    print("\nSimulation completed successfully!")
    print("Results saved to: results/plots/")
    print("Log file: dqc_simulation.log")

    return results


if __name__ == "__main__":
    main()
