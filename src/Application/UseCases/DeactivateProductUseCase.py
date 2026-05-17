from src.config.di_container import DIContainer


class DeactivateProductUseCase:

    @staticmethod
    def execute(product_id: int, seller_id: int) -> None:
        product_repo = DIContainer.get_product_repository()

        product = product_repo.find_by_id(product_id)
        if not product:
            raise ValueError("Produto não encontrado")
        if product.seller_id != seller_id:
            raise ValueError("Produto não pertence a este vendedor")

        product.deactivate()
        product_repo.update(product_id, product)
