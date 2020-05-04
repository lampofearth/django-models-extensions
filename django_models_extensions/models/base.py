import operator
from collections import defaultdict

from django.db.models import QuerySet
from .query import ValuesExtensionIterable


class QuerysetExtension(QuerySet):

    def as_dict(self, key=None, values=None, unique_key=True, **expressions):
        """
        Convert queryset to dict or defaultdict(list) with 'key', as dict key,
        and 'values' as array dict values or dict

        :param key: <string> dictionary key
        :param values: <iterable> iterator with values for the key-value pair
        :param unique_key: <bool> if True, return dict. If False - return defaultdict(list)
        :param expressions: like kwarg data. Other field for the key-value pair
        :return: <dict> or <defaultdict(list)>
        """

        values = () if values is None else tuple(values) + (key,)
        fields = values + tuple(expressions)
        clone = self._values(*fields, **expressions)
        clone._iterable_class = ValuesExtensionIterable
        clone._as_dict_key = key

        result = dict() if unique_key else defaultdict(list)
        func = (lambda d, k, v: operator.setitem(d, k, v)) if unique_key else \
            (lambda d, k, v: d[k].append(v))

        for row in clone.iterator():
            _key = row.pop(key)
            func(result, _key, row)
        return result

    def as_df(self, *fields, **expressions):
        """
        Return pandas dataFrame with columns in *fields

        :param *fields: <string> columns names as queryset field
        :param expressions: like kwarg data. Other field for DataFrame columns
        :return: <DataFrame object>
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError('for use "as_df" please install pandas')

        values = self.values_list(*fields, named=True, **expressions)
        return pd.DataFrame(values, columns=values.query.values_select)
