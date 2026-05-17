from typing import List
from src.config.di_container import DIContainer
from src.Domain.product import ProductDomain


class ListProductsUseCase:

    @staticmethod
    def execute(seller_id: int) -> List[ProductDomain]:
        product_repo = DIContainer.get_product_repository()
        return product_repo.find_by_seller_id(seller_id)
