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

    def _lock(self):
        import os
        from time import sleep
        while os.path.isfile(self.db_path+".lock"):
            print("Another process is using DB.json. Waiting for release.")
            sleep(1)
        with open(self.db_path+".lock", 'w') as fp:
            pass

    def _unlock(self):
        from os import remove
        remove(self.db_path + ".lock")

    def json_to_dict(self) -> bool:
        try:
            self._lock()
            with open(self.db_path) as json_file:
                self.db_data = json.load(json_file)
            self._unlock()
            return True
        except FileNotFoundError:
            print("The file", self.db_path, "does not exist or inaccessible.")
            print(self.db_path, "Will be created on write")
            return True
        except json.decoder.JSONDecodeError:
            print("File is either empty or corrupted.")
            return False
        except:
            print("Unable to read", self.db_path)
            return False

    def dict_to_json(self) -> bool:
        try:
            self._lock()
            with open(self.db_path, "w") as outfile:
                json.dump(self.db_data, outfile)
            self._unlock()
            return True
        except:
            return False

    def read(self, key: str):
        if self.json_to_dict():
            if key in self.db_data.keys():
                return(self.db_data[key])
            else:
                return False
        else:
            return False
                
            
    def _print_all_objects(self) -> bool:
        if self.json_to_dict():
            print(json.dumps(self.db_data, indent=3))
            return True
        else:
            print("Unable to Print all JSON Objects")
            return False

    def delete(self, key: str) -> bool:
        if self.json_to_dict():
            #print(self.db_data[key][1],"hello")
            curr_time = datetime.now().timestamp()
            try:
                print(curr_time , self.db_data[key][1]['expiration_time'])
                if(self.db_data[key][1]['expiration_time']==-1):
                    self.db_data.pop(key)
                if (curr_time - self.db_data[key][1]['expiration_time']) < -1:
                    print("Object Life Expired")
                    return False
                self.db_data.pop(key)
                if not self.dict_to_json():
                    return False
            except KeyError:
                print("Object with", key, "does not exist.")
                return False
            return True
        else:
            print("Unable to delete Object ID =", id)
            return False

    def create(self, key: str, obj: dict, life: int = -1):
        """ Create and pushes object to the JSON DS

        Args:
            key (str): Primary Key for the $obj 
            obj (dict): The Dictionary object to be pushed
            life (int, optional): Time in Secondsdele the key is retained in the DS. Defaults to -1.

        Returns:
            bool: Returns True upon successful insertion
        """
        if self.json_to_dict():
            from datetime import datetime, timedelta
            from sys import getsizeof

            # Check if the size limit is reached
            if getsizeof(str(obj)) > 16*1024:
                print("Object size exceeded 16 KB limit")
                return False

            # Check if the Key length limit is reached
            if len(key) > 32:
                print("Object contains Key(s) with more than 32 Characters.")
                return False

            # Determining Current and Expiration Time
            curr_time = datetime.now()
            if life == -1:
                expiration_time = -1
            else:
                expiration_time = curr_time + timedelta(seconds=life)
                expiration_time = expiration_time.timestamp()
            curr_time = curr_time.timestamp()
            ts = int(str(curr_time).replace(".", ""))

            # Creating JSON Object
            if key in self.db_data.keys():
                print("Key already Exist. Object not Created.")
                return False
            else:
                meta_data = {
                    'inserted_time': curr_time,
                    'expiration_time': expiration_time
                }
                self.db_data[key] = (obj, meta_data)
            if not self.dict_to_json():
                return False
            print("Object created with ID =", key)
            return True
        else:
            print("Unable to add Object")
            return False
