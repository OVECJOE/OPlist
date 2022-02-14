"""Contains the model for the user's search query."""
from datetime import datetime


class QueryModel:
    """This class models the user's search query"""
    count = 0

    def __init__(self, *args, **kwargs):
        """Initializes the QueryModel class

        Note: You can use only positional arguments or keyword arguments;
        If both are used, it defaults to keyword arguments.
        """
        QueryModel.count += 1
        if kwargs:
            if 'created_at' in kwargs:
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                         '%Y-%m-%dT%H:%M:%S.%f')
            else:
                kwargs['created_at'] = datetime.now()

            self.__dict__.update(kwargs)
        else:
            self.king = args[0]
            self.head = args[1]
            self.body = args[2]
            self.created_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        return "({}) [{}, {}]".format(
            self.king, self.head, self.body)

    def to_dict(self):
        """Converts object to dictionary"""
        new = self.__dict__.copy()
        new['created_at'] = new['created_at'].isoformat()
        return new
