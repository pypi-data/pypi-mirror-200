import json
import threading
import time
from contextlib import contextmanager
from typing import Any, Dict, List, Optional

class MemeDB:
    """
    A simple key-value store with advanced features like indexing, querying, and caching.
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.data = {}
        self.indexes = {}
        self.lock = threading.Lock()  # lock to ensure isolation
        self.load_data()

    def load_data(self) -> None:
        """
        Load data from the file.
        """
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self.data = data
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and 'key' in item and 'value' in item:
                            key = item['key']
                            value = item['value']
                            self.data[key] = value
        except FileNotFoundError:
            print(f"{self.filename} not found.")
            self.save_data()

    @contextmanager
    def transaction(self):
        """
        A context manager to wrap each data operation in a transaction.
        """
        self.lock.acquire()  # acquire the lock
        try:
            yield  # execute the operation(s)
            self.save_data()  # save the updated data after the operation(s) completes
        except Exception as e:
            print("Transaction failed, rolling back changes.")
            print(e)
            self.load_data()  # rollback the current operation by reloading the data from disk
        finally:
            self.lock.release()  # release the lock after the operation(s) completes or fails

    def get(self, key: str) -> Optional[Any]:
        """
        Get the value for the given key.
        """
        return self.data.get(key)

    def set(self, key: str, value: Any) -> None:
        """
        Set the value for the given key.
        """
        with self.transaction():
            self.data[key] = value
            self.update_indexes(key, value)

    def delete(self, key: str) -> None:
        """
        Delete the value for the given key.
        """
        with self.transaction():
            self.data.pop(key, None)
            self.remove_from_indexes(key)

    def save_data(self) -> None:
        """
        Save the data to the file.
        """
        with open(self.filename, 'w') as f:
            data = []
            for key, value in self.data.items():
                data.append({'key': key, 'value': value})
            json.dump(data, f)

    def create_index(self, name: str, func: Optional[callable] = None) -> None:
        """
        Create an index on the database.
        """
        if name in self.indexes:
            raise ValueError(f"Index {name} already exists.")
        self.indexes[name] = {'func': func, 'data': {}}
        for key, value in self.data.items():
            self.update_index(name, key, value)

    def update_indexes(self, key: str, value: Any) -> None:
        """
        Update all the indexes for the given key-value pair.
        """
        for index_name, index in self.indexes.items():
            if index['func']:
                index_value = index['func'](value)
            else:
                index_value = value
            if index_value not in index['data']:
                index['data'][index_value] = set()
            index['data'][index_value].add(key)


