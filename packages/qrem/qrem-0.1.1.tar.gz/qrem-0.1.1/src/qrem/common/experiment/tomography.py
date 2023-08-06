from qrem.data_structures.circuit_collection import CircuitCollection
from typing import List, Dict, Optional, Callable, Tuple
import numpy as np

def create_circuits(experiment_type: str,number_of_qubits: int,number_of_circuits: int,device_name: Optional[str] = 'basic_collection')-> CircuitCollection:
    """Creates a basic circuit collection in the experiment preparation stage

    Parameters:
        experiment_type (str): DDOT or QDOT (Diagonal/Quantum Detector Overlapping Tomography)
        number_of_qubits (int): number of qubits in the experiment
        number_of_circuits (int): maximal number of circuits
        device_name (str): name of the created circuit collection
    Returns:
        CircuitCollection with given parameters
    Raises:
        an error for a wrong experiment_type


    """
    symbol_lists_dict = {"qdot": 6,"QDOT": 6,"ddot": 2,"DDOT": 2}

    try:
        number_of_symbols = symbol_lists_dict[experiment_type]
    except:
        print("Error: wrong experiment type")

    circuits_list = [[np.random.randint(0,number_of_symbols) for i in range(number_of_qubits)] for j in range(number_of_circuits)]

    circuits = CircuitCollection(device_name)
    dictionary_to_load = {'experiment_type': experiment_type,
                          'circuits_list': circuits_list,
                          'qubit_indices': list(range(number_of_qubits))}
    circuits.load_from_dict(dictionary_to_load)

    return circuits

