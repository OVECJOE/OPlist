"""Contains the FileStorage class implementation"""
import json
from models.query_model import QueryModel


class FileStorage:
    """This class stores QueryModel objects into a file"""
    __filename = 'file.json'
    __objects = {}

    def all(self):
        """Returns a dictionary of QueryModel objs currently in storage"""
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({QueryModel.count: obj})

    def remove(self, key):
        """Removes an object from the dictionary"""
        for k in FileStorage.__objects:
            if k == key:
                FileStorage.__objects.pop(key)
                break

    def save(self):
        """Saves the objects to a file."""
        with open(FileStorage.__filename, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for k, v in temp.items():
                temp[k] = v.toDict()
            json.dump(temp, f, indent=4)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(FileStorage.__filename, 'r', encoding='utf-8') as f:
                temp = json.load(f)
                for k, v in temp.items():
                    self.all()[int(k)] = QueryModel(**v)
        except FileNotFoundError:
            pass
