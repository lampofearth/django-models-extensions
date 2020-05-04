from django.db.models import QuerySet
from .query import ValuesExtensionIterable


class QuerysetExtension(QuerySet):

    def as_dict(self, key=None, fields=None, **expressions):
        fields = [] if fields is None else fields
        fields = fields + tuple(expressions)

        clone = self._values(*fields, **expressions)
        clone._as_dict_key = key
        clone._iterable_class = ValuesExtensionIterable
        return clone

    def as_df(self, *fields, **expressions):
        try:
            import pandas as pd
        except ImportError:
            raise ImportError('for use "as_df" please install pandas')

        values = self.values(*fields, **expressions)
        return pd.DataFrame(values, columns=fields)
