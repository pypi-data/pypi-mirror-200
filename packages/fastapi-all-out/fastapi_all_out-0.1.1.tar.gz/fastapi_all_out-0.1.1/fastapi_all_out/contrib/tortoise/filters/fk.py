from tortoise.queryset import QuerySet
from fastapi_all_out.routers.filters import BaseIntForeignKeyFilter


class IntForeignKeyFilter(BaseIntForeignKeyFilter):
    def filter(self, query: QuerySet) -> QuerySet:
        return query.filter(**{self.field_name: self.value})
