from tortoise.queryset import QuerySet

from fastapi_all_out.routers.filters import \
    BaseStrFilter, \
    BaseIntFilter, \
    BaseBoolFilter


__all__ = ["StrFilter", "IntFilter", "BoolFilter"]


class SimpleFilterMixin:
    def filter(self, query: QuerySet) -> QuerySet:
        return query.filter(**{self.field_name: self.value})


class StrFilter(SimpleFilterMixin, BaseStrFilter):
    pass


class IntFilter(SimpleFilterMixin, BaseIntFilter):
    pass


class BoolFilter(SimpleFilterMixin, BaseBoolFilter):
    pass
