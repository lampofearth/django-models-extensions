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
            key_idx = names.index(getattr(queryset, '_as_dict_key', None))
        except ValueError as e:
            raise ValueError(f"key {key_idx} is not fount in result row")

        for row in compiler.results_iter(chunked_fetch=self.chunked_fetch,
                                         chunk_size=self.chunk_size):
            yield {names[i]: row[i] for i in indexes}
