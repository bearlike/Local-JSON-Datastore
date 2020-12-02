# Local JSON Datastore

## Introduction
A file-based JSON data store exposed as a library that supports CRD operations with a lock-unlock mechanism to establish a thread-safe environment.
### Features

- A Python package for an user to import and instantiate the class to perform **CRD** operations.
- A lock-unlock mechanism to make the data store thread safe.
- 85% Testing Coverage for the application using PyTest.
- Read, Write and Delete operations performed on a custom local data store in a user-specified location.
### In-Progress
- Currently Building Unit Test Modules
## Getting Started
### Requirements

This package required Python 3.x.x to run. Install python from [here](https://www.python.org/).

### Getting the package

To get the package clone this repository into your local system and make it the current working directory using the following commands.

```bash
git clone https://github.com/bearlike/Local-JSON-Datastore.git
cd Local-JSON-Datastore
```

### Using the package

####  Importing the package

Import the package using the following command.

```python
import datastore
```

#### Creating an object

By default an object is created with the storage file called `DB.json` in the root of the present working directory as follows.

```python
db = datastore.Datastore()
```

In case a file path is required it can be specified while instantiating the class.

```python
db = Datastore(path="test/file/path")
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
is_object_inserted = db.add_obj(key='alphabets', obj=test_object)
```

 If an object has to be inserted with a specific **Time-To-Live** it can be passed as a separate argument (in seconds) to the add function. 

```python
test_object = {
    'a':'apple',
    'b':'ball',
    'c':'cat',
    'd':'dog'
}
is_object_inserted = db.add_obj(key='alphabets', obj=test_object, life=100)
```

#### Deleting an Object

To delete an object that has not crossed its **Time-To-Live** the key of that object can be passed as an argument to the `delete_object()` function. Return `True` if the object has been deleted successfully else a `False`.

```python
is_object_deleted = db.delete_object(key='alphabets')
```

#### Retrieve an Object

To retrieve an object provide the key of the object as an argument to the `get_object()` function.

```python
key = db.get_object(key='alphabet')
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

