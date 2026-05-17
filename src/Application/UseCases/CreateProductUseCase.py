from src.config.di_container import DIContainer
from src.Domain.product import ProductDomain


class CreateProductUseCase:

    @staticmethod
    def execute(seller_id: int, name: str, price: float,
                quantity: int = 0, image_url: str = None) -> ProductDomain:
        if not name:
            raise ValueError("Nome do produto é obrigatório")
        if price is None or price <= 0:
            raise ValueError("Preço deve ser maior que zero")
        if quantity < 0:
            raise ValueError("Quantidade não pode ser negativa")

        product_repo = DIContainer.get_product_repository()

        product = ProductDomain(
            seller_id=seller_id,
            name=name,
            price=price,
            quantity=quantity,
            image_url=image_url,
        )
        product_id = product_repo.save(product)
        return product_repo.find_by_id(product_id)
