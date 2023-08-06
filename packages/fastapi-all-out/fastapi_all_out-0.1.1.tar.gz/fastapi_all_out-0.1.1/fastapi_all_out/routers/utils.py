from typing import Optional, Any, Type, Callable, TYPE_CHECKING

from fastapi import Depends, Query, Request
from pydantic import NonNegativeInt

from fastapi_all_out.pydantic import CommaSeparatedOf, snake_case

if TYPE_CHECKING:
    from fastapi_all_out.routers.filters import BaseFilter


ROUTE = bool | dict[str, Any]
PAGINATION = tuple[Optional[int], Optional[int]]


def pagination_factory(max_limit: Optional[int], default_limit: Optional[int] = 50) -> Any:
    """
    Created the pagination dependency to be used in the router
    """

    if max_limit and default_limit > max_limit:
        default_limit = max_limit

    def pagination(
            skip: Optional[NonNegativeInt] = Query(None),
            limit: Optional[int] = Query(default_limit, ge=1, le=max_limit)
    ) -> PAGINATION:
        return skip, limit

    return Depends(pagination)


def get_filters(filters: list[Type["BaseFilter"]]):
    def wrapper(request: Request) -> list["BaseFilter"]:
        qp = request.query_params
        return [final_f for f in filters if (final_f := f.from_qs(qp))]
    return wrapper


def sort_factory(available: set[str]) -> Callable[[...], set[str]]:
    def sort(fields: CommaSeparatedOf(str, wrapper=snake_case, in_query=True) = Query(
        None,
        alias='sort',
        description=f'Пиши,поля,через,запятую. Доступно: {", ".join(available)}'
    )) -> set[str]:
        result: set[str] = set()
        if fields:
            for field in fields:
                if field in available:
                    result.add(field)
        return result

    return sort
