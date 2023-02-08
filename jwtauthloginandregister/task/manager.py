from django.db import models
from django.db.models.query import EmptyQuerySet, QuerySet


class CustomManager(models.Manager):
    """
    Easily override QuerySet by setting the QuerySet and EmptyQuerySet
    inside of the class using inheritance.
    """
    EmptyQuerySet = EmptyQuerySet
    QuerySet = QuerySet

    def get_empty_query_set(self):
        return self.EmptyQuerySet(self.model, self._db)

    def get_query_set(self):
        return self.QuerySet(self.model, self._db)

    # Overriding create methods since Django omits the *args.
    # This makes it difficult for you to override since you will have to
    # define in both the QuerySet and Manager.  Overly redundant.
    def get_or_create(self, *args, **kwargs):
        return self.get_query_set().get_or_create(*args, **kwargs)

    def create(self, *args, **kwargs):
        return self.get_query_set().create(*args, **kwargs)

    def __getattr__(self, attr):
        if attr.startswith('_'):
            raise AttributeError
        return getattr(self.get_query_set(), attr)


# # Example usage:


# class MyManager(CustomManager):
#     class QuerySet(CustomManager.QuerySet):
#         def first(self, *args, **kwargs):
#             """Returns the first object or raises DoesNotExist."""
#             return self.filter(*args, **kwargs)[:1].get()
