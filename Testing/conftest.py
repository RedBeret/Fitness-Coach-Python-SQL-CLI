import pytest

def pytest_itemcollected(item):
    """ Customize test node ID based on class and method docstrings """
    class_doc = item.cls.__doc__.strip() if item.cls and item.cls.__doc__ else item.cls.__name__ if item.cls else ''
    method_doc = item.function.__doc__.strip() if item.function.__doc__ else item.function.__name__
    custom_name = f"{class_doc}: {method_doc}" if class_doc or method_doc else item._nodeid
    item._nodeid = custom_name
