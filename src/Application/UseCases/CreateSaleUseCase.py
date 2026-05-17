from src.config.di_container import DIContainer
from src.Domain.sale import SaleDomain


class CreateSaleUseCase:

    @staticmethod
    def execute(product_id: int, seller_id: int, quantity: int) -> SaleDomain:
        if not quantity or quantity <= 0:
            raise ValueError("Quantidade deve ser maior que zero")

        product_repo = DIContainer.get_product_repository()
        sale_repo    = DIContainer.get_sale_repository()

        product = product_repo.find_by_id(product_id)
        if not product:
            raise ValueError("Produto não encontrado")
        if product.seller_id != seller_id:
            raise ValueError("Produto não pertence a este vendedor")
        if not product.can_be_sold(quantity):
            raise ValueError("Estoque insuficiente ou produto inativo")

        product.decrease_stock(quantity)
        product_repo.update(product.id, product)

        sale = SaleDomain(
            product_id=product_id,
            seller_id=seller_id,
            quantity=quantity,
            unit_price=product.price,
        )
        sale_id = sale_repo.save(sale)
        return sale_repo.find_by_id(sale_id)
