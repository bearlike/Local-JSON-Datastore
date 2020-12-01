#!/usr/bin/python3
# All Datastore connectors are here. Just call and run.
from datetime import datetime
import json
# from exceptions import InvalidLoginError, UsernameTakenError


class Datastore:
    """A connection to the data store."""

    def __init__(self, path: str):
        """ Class Constructor
        Args:
            path (str): Path to the JSON Datastore file
        """
        self.db_path = path
        self.db_data = dict()

    def json_to_dict(self) -> bool:
        try:
            with open(self.db_path) as json_file:
                self.db_data = json.load(json_file)
            return True
        except FileNotFoundError:
            print("The file", self.db_path, "does not exist or inaccessible")
            return False
        except:
            print("Unable to read", self.db_path)
            return False

    def dict_to_json(self) -> bool:
        with open(self.db_path, "w") as outfile:
            json.dump(self.db_data, outfile)

    def print_all_objects(self) -> bool:
        if self.json_to_dict():
            print(json.dumps(self.db_data, indent=3))
            return True
        else:
            print("Unable to Print all JSON Objects")
            return False

    def delete_object(self, id: int) -> bool:
        if self.json_to_dict():
            return True
        else:
            print("Unable to delete Object ID =", id)
            return False
