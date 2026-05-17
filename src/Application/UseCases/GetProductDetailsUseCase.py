from src.config.di_container import DIContainer
from src.Domain.product import ProductDomain


class GetProductDetailsUseCase:

    @staticmethod
    def execute(product_id: int, seller_id: int) -> ProductDomain:
        product_repo = DIContainer.get_product_repository()

        product = product_repo.find_by_id(product_id)
        if not product:
            raise ValueError("Produto não encontrado")
        if product.seller_id != seller_id:
            raise ValueError("Produto não pertence a este vendedor")

        return product
