#!/usr/bin/python3
# All Datastore connectors are here. Just call and run.
from datetime import datetime
import json


class Datastore:
    """A connection to the data store."""

    def __init__(self, path: str = "DB.json"):
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
            print("Creating", self.db_path, "JSON Data store file")
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
            try:
                self.db_data.pop(id)
            except KeyError:
                print("Object with", id, "does not exist.")
                return False
            return True
        else:
            print("Unable to delete Object ID =", id)
            return False

    def add_obj(self, obj: dict, life: int = -1):
        if self.json_to_dict():
            from datetime import datetime, timedelta
            from random import randint
            from sys import getsizeof

            # Check if the size limit is reached
            if getsizeof(str(obj)) > 16*1024:
                print("Object size exceeded 16 KB limit")
                return False

            # Check if the Key length limit is reached
            for key in obj.keys():
                if len(key) > 32:
                    print("Object contains Key(s) with more than 32 Characters.")
                    return False

            # Generate Current UTC Time
            curr_time = datetime.now()
            if life == -1:
                expiration_time = -1
            else:
                expiration_time = curr_time + timedelta(seconds=life)
            ts = int(str(curr_time).replace(".", ""))
            flag = False
            while flag == False:
                n = randint(1000, 9999) + ts
                try:
                    if dict[n]:
                        flag = True
                        meta_data = {
                            'inserted_time': curr_time.timestamp(),
                            'expiration_time': expiration_time.timestamp()
                        }
                        self.db_data[n] = (obj, meta_data)
                except KeyError:
                    pass
            return True
        else:
            print("Unable to add Object")
            return False
