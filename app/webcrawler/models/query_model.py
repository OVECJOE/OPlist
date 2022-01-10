"""Contains the model for the user's search query."""
from datetime import datetime


class QueryModel:
    """This class models the user's search query"""
    count = 0

    def __init__(self, *args, **kwargs):
        """Initializes the QueryModel class"""
        from models import storage
        QueryModel.count += 1
        if kwargs:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')

            self.__dict__.update(kwargs)
        else:
            if len(args) != 3:
                raise IndexError(
                    "3 positional arguments required, but {:d} provided"
                    .format(len(self.__dict__)))
            self.king = args[0]
            self.head = args[1]
            self.body = args[2]
            self.created_at = self.updated_at = datetime.now()
        storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        return "({}) [{}, {}]".format(
            self.king, self.head, self.body)

    def toDict(self):
        """Converts object to dictionary"""
        new = self.__dict__.copy()
        new['created_at'] = new['created_at'].isoformat()
        new['updated_at'] = new['updated_at'].isoformat()
        return new

    def save(self):
        """Updates updated_at with the current time when obj is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()
