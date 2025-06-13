"""Module to save current circuit as a json file"""

import json


class FileSaver:
    """Simple class to save current circuit in json"""

    def __init__(self, file_name, circuit, name):
        # TODO add better file path management
        with open(f"components/{file_name}", "w", encoding="utf-8") as f:
            data = {
                "name": name,
                **circuit.to_dict(),  # merge the rest of the circuit data
            }

            json.dump(data, f, indent=2)
