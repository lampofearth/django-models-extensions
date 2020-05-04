from collections import defaultdict

from django.db.models.query import BaseIterable


class ValuesExtensionIterable(BaseIterable):

    def __iter__(self):
        queryset = self.queryset
        query = queryset.query
        compiler = query.get_compiler(queryset.db)

        names = [
            *query.extra_select,
            *query.values_select,
            *query.annotation_select,
        ]
        indexes = range(len(names))

        try:
            key_value = getattr(self.queryset, '_as_dict_key', None)
            key_idx = names.index(key_value)
        except ValueError:
            raise KeyError(f'key "{key_value}" not found in QuerySet fields')

        if key_idx is None:
            for row in compiler.results_iter(chunked_fetch=self.chunked_fetch,
                                             chunk_size=self.chunk_size):
                yield {names[i]: row[i] for i in indexes}
            return

        result = defaultdict(list)
        for row in compiler.results_iter(chunked_fetch=self.chunked_fetch,
                                         chunk_size=self.chunk_size):
            result[row[key_idx]].append({names[i]: row[i] for i in indexes})
        yield result
