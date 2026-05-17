from typing import List
from src.config.di_container import DIContainer
from src.Domain.sale import SaleDomain


class ListSalesUseCase:

    @staticmethod
    def execute(seller_id: int) -> List[SaleDomain]:
        sale_repo = DIContainer.get_sale_repository()
        return sale_repo.find_by_seller_id(seller_id)
