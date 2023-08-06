from tortoise.queryset import QuerySet

from fastapi_all_out.routers.filters import BaseStrStartswithFilter, BaseStrIstartswithFilter


class StrStartswithFilter(BaseStrStartswithFilter):
    def filter(self, query: QuerySet) -> QuerySet:
        return query.filter(**{f'{self.field_name}__startswith': self.value})


class StrIstartswithFilter(BaseStrIstartswithFilter):
    def filter(self, query: QuerySet) -> QuerySet:
        return query.filter(**{f'{self.field_name}__istartswith': self.value})
