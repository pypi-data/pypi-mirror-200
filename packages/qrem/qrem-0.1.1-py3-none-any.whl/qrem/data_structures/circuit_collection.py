from datetime import datetime
from qrem.data_structures.datastructure_base import DataStructureBase


#maybe we will also need:
# self.circuits = np.array([],dt) # some data type (for circuits it should be probably list of np.arrays or array of arrays)

class CircuitCollection(DataStructureBase):
    """
    The class contains data about circuits to be prepared on a certain device, for a specified experiment.
    Parameters
    ----------
    device (str): name of the device on which the circuits will be run
    experiment_type (str): DDOT or QDOT (Diagonal/Quantum Detector Overlapping Tomography)
    circuits_list (list[str]): list of circuits, where each circuit is a string of symbols (0-1 for DDOT, 0-5 for QDOT)
    qubit_indices (list[int]): list of indices of qubits on which the circuits are to be executed
    gate_error_threshold (float): gate error on qubit above which qubits are disregarded (we don't execute circuits there)
    locality (int): what degree marginals we wish to characterize
    no_shots (int): how many times each circuit is executed
    datetime_created_utc: when the circuit collection was created
    author (str): creator of collection
    """
    def __init__(self, device):
        # [X] default value definitions
        super().__init__()
        self.device = device
        self.experiment_type = ''
        self.circuits_list = []
        self.qubit_indices = []
        self.gate_error_threshold = None  # 0.01
        self.locality = None  # 2
        self.no_shots = None  # 10000
        self.datetime_created_utc = datetime.utcnow()
        self.author = None
        self.notes = ''

    def load_from_dict(self, dictionary):
        for key in dictionary:
            if key in self.get_dict_format():
                setattr(self, key,
                        dictionary[key])  # TODO: secure against bad data, e.g mismatched qubit and circuit len?
        pass



# tests:
if __name__ == "__main__":
    test_collection = CircuitCollection('test_name')
    print(test_collection.get_dict_format())
    dictionary_to_load = {'experiment_type': 'qdot',
                          'circuits_list': [[0, 5, 3], [1, 2, 0], [3, 1, 4]],
                          'qubit_indices': [0, 2, 5],
                          'gate_error_threshold': 0.005,
                          'no_shots': 1,
                          'datetime_created_utc': datetime.utcnow(),
                          'author': 'tester',
                          'notes': 'some string note'}
    test_collection.load_from_dict(dictionary_to_load)
    print('after loading:\n', test_collection.get_dict_format())
    json_dict_test = test_collection.to_json()
    test_collection.export_json('exported_json', overwrite=True)
    test_collection.import_json('exported_json')
    pickle_dict_test = test_collection.get_pickle()
    test_collection.export_pickle('exported_pickle', overwrite=True)
    test_collection.notes = 'changed note'
    print('after change:\n', test_collection.get_dict_format())
    test_collection.import_pickle('exported_pickle')
