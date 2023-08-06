from typing import List

from fastapi_pagination import Page, Params, paginate
from page_query_model import PageQueryModel


def paginate_list(item_list: List[any], page: int, size: int) -> PageQueryModel:
    paginated_result: Page = paginate(
        item_list,
        params=Params(page=page + 1, size=size),
    )
    output_result: PageQueryModel = PageQueryModel(**paginated_result.__dict__)
    output_result.page -= 1
    return output_result
