from django.db.models import Field, ExpressionWrapper
from django.db.models.query import QuerySet
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

__all__ = [
    'VirtualFunctionField',
]


class VirtualFunctionField(Field):
    empty_strings_allowed = False
    is_function = True
    description = _("Virtual function field. Returns function result ")

    def get_internal_type(self):
        return "VirtualFunctionField"

    def db_type(self, connection):
        return None

    def validate(self, value, model_instance):
        pass

    def formfield(self, **kwargs):
        return None

    def contribute_to_class(self, cls, name, private_only=True):
        super().contribute_to_class(cls, name, private_only)

    @cached_property
    def cached_col(self):
        _qs = QuerySet(model=self.model)
        _qs._fields = set(['id'], )
        _qs = _qs.annotate(
            **{self.attname: self.function}).values_list(self.attname)
        return _qs.query.annotations[self.attname]

    def get_col(self, alias, output_field=None):
        return self.cached_col

    def __init__(self, verbose_name=None, name=None, function=None,
                 output_field=None, **kwargs):
        self.output_field = output_field
        self.function = ExpressionWrapper(function, output_field)
        self.function.target = self
        super().__init__(verbose_name, name, **kwargs)

