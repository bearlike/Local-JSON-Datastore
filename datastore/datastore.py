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
        """ Create a file ($self.db_path.lock) to denote the DS is
            being used by another process.
        """
        import os
        from time import sleep
        # Waits until another process completes it's process
        while os.path.isfile(self.db_path+".lock"):
            print("Another process is using",
                    self.db_path, ". Waiting for release.")
            sleep(1)
        with open(self.db_path+".lock", 'w') as fp:
            pass

    def _unlock(self):
        """ Deletes a file ($self.db_path.lock) that denotes the DS is
            being used by another process.
        """
        from os import remove
        remove(self.db_path + ".lock")

    def _json_to_dict(self):
        """ Reads the JSON file into a dictionary 

        Returns:
            bool: Returns True upon successful read and False otherwise
        """
        try:
            self._lock()
            with open(self.db_path) as json_file:
                self.db_data = json.load(json_file)
            self._unlock()
            return True
        except FileNotFoundError:
            print("The file", self.db_path, "does not exist or inaccessible.")
            print(self.db_path, "Will be created on write")
            self._unlock()
            return True
        except json.decoder.JSONDecodeError:
            print("File is either empty or corrupted.")
            return False
        except:
            print("Unable to read", self.db_path)
            return False

    def _dict_to_json(self):
        """ Writes the dictionary into a JSON file  

        Returns:
            bool: Returns True upon successful write and False otherwise
        """
        try:
            from os.path import getsize
            if getsize(self.db_path)/1024 > 1024**3:
                print("File Size Limit reached (> 1 GB)")
                return False
        except FileNotFoundError:
            pass
        try:
            self._lock()
            with open(self.db_path, "w") as outfile:
                json.dump(self.db_data, outfile)
            self._unlock()
            return True
        except:
            return False

    def _print_all_objects(self):
        """ Prints all objects ignore Time-To-Live property

        Returns:
            bool: Returns True upon successful insertion and False otherwise        
        """
        if self._json_to_dict():
            print(json.dumps(self.db_data, indent=3))
            return True
        else:
            print("Unable to Print all JSON Objects")
            return False

    def read(self, key: str):
        """ Return the requested Python object

        Args:
            key (str): Primary Key for the $obj

        Returns:
            dict: Upon success, returns the desired object
            bool: Returns False upon runtime failiure
        """
        if self._json_to_dict():
            curr_time = datetime.now().timestamp()
            if(self.db_data[key][1]['expiration_time'] == -1) or \
                    (curr_time < self.db_data[key][1]['expiration_time']):
                if key in self.db_data.keys():
                    return(self.db_data[key])
                else:
                    print("Object with", key, "does not exist.")
                    return False
            else:
                print("Object Life Expired")
                return False
        else:
            return False

    def delete(self, key: str):
        """ Delete object with $key Key and pushes object to the JSON DS

        Args:
            key (str): Primary Key for the $obj

        Returns:
            bool: Returns True upon successful deletion and False otherwise
        """
        if self._json_to_dict():
            curr_time = datetime.now().timestamp()
            try:
                if(self.db_data[key][1]['expiration_time'] == -1):
                    self.db_data.pop(key)
                    return True
                elif (curr_time > self.db_data[key][1]['expiration_time']):
                    print("Object Life Expired")
                    return False
                self.db_data.pop(key)
                if not self._dict_to_json():
                    return False
            except KeyError:
                print("Object with", key, "does not exist.")
                return False
            return True
        else:
            print("Unable to delete Object ID =", id)
            return False

    def create(self, key: str, obj: dict, life: int = -1):
        """ Create an object with $key Key and pushes object to the JSON DS

        Args:
            key (str): Primary Key for the $obj 
            obj (dict): The Dictionary object to be pushed
            life (int, optional): Time in Secondsdele the key is retained in the DS. Defaults to -1.

        Returns:
            bool: Returns True upon successful insertion and False otherwise
        """
        if self._json_to_dict():
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
            if not self._dict_to_json():
                return False
            print("Object created with ID =", key)
            return True
        else:
            print("Unable to add Object")
            return False


if __name__ == "__main__":
    print("This is a Package File meant to be imported in other python3 programs.\
            \nVisit https://github.com/bearlike/Local-JSON-Datastore to understand more.\
            \nOr Execute the test file to perform Automated Testing")
