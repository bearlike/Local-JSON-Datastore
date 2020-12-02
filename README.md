# Local JSON Datastore
![Work in Progress](https://img.shields.io/badge/-Work%20in%20Progress-red)

## Introduction
A file-based JSON data store exposed as a library.
## Getting Started
### Requirements

This package required Python 3.x.x to run. Install python from [here](https://www.python.org/).

### Getting the package

To get the package clone this repository into your local system and make it the current working directory using the following commands.

```bash
https://github.com/bearlike/Local-JSON-Datastore.git
cd Local-JSON-Datastore
```

### Using the package

####  Importing the package

Import the package using the following command.

```python
from datastore import Datastore
```

#### Creating an object

By default an object is created with the storage file called `db.json` in the root of the present working directory as follows.

```python
data_store = Datastore()
```

In case a file path is required it can be specified while instantiating the class.

```python
data_store = Datastore(path="test/file/path")
```

#### Inserting an object

An object can be inserted into the data store using the `add_obj()` method which takes in a user-created dictionary as an argument and returns a `True` if an object has been successfully inserted or false otherwise.

```python
test_object = {
    'a':'apple',
    'b':'ball',
    'c':'cat',
    'd':'dog'
}
is_object_inserted = data_store.add_obj(key='alphabets', obj=test_object)
```

 If an object has to be inserted with a specific **Time-To-Live** it can be passed as a separate argument (in seconds) to the add function. 

```python
test_object = {
    'a':'apple',
    'b':'ball',
    'c':'cat',
    'd':'dog'
}
is_object_inserted = data_store.add_obj(key='alphabets', obj=test_object, life=100)
```

#### Deleting an Object

To delete an object that has not crossed its **Time-To-Live** the key of that object can be passed as an argument to the `delete_object()` function. Return `True` if the object has been deleted successfully else a `False`.

```python
is_object_deleted = data_store.delete_object(key='alphabets')
```

#### Retrieve an Object

To retrieve an object provide the key of the object as an argument to the `get_object()` function.

```python
key = data_store.get_object(key='alphabet')
print(key)
```

```bash
{
    'a':'apple',
    'b':'ball',
    'c':'cat',
    'd':'dog'
}
```

