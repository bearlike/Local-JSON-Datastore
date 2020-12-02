#!/usr/bin/python3
""" Test stub using PyTest"""
import datastore
import pytest
from random import randint

obj = datastore.Datastore(str(randint(1000, 9999))+".json")
t_dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}


def test_create():
    """ Test Stub for datastore.Datastore.create()

    Returns:
        bool: True if test cases are passed, False otherwise
    """
    return obj.create("1", t_dict)


def test_read():
    """ Test Stub for datastore.Datastore.read()

    Returns:
        bool: True if test cases are passed, False otherwise
    """
    t = obj.read("1")[0]
    return t == t_dict


def test_delete():
    """ Test Stub for datastore.Datastore.create()

    Returns:
        bool: True if test cases are passed, False otherwise
    """
    return obj.delete("1")


if __name__ == "__main__":
    assert test_create()
    assert test_read()
    assert test_delete()
