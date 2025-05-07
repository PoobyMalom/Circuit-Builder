import json

class FileSaver:
    def __init__(self, file_name, circuit, name):
        with open(f"components/{file_name}", 'w') as f:
            data = {
                "name": name,
                **circuit.to_dict()  # merge the rest of the circuit data
            }

            json.dump(data, f, indent=2)