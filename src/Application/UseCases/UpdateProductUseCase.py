from src.config.di_container import DIContainer
from src.Domain.product import ProductDomain


class UpdateProductUseCase:

    @staticmethod
    def execute(product_id: int, seller_id: int, **dados) -> ProductDomain:
        product_repo = DIContainer.get_product_repository()

        product = product_repo.find_by_id(product_id)
        if not product:
            raise ValueError("Produto não encontrado")
        if product.seller_id != seller_id:
            raise ValueError("Produto não pertence a este vendedor")

        if 'name' in dados and dados['name']:
            product.name = dados['name']
        if 'price' in dados:
            if dados['price'] <= 0:
                raise ValueError("Preço deve ser maior que zero")
            product.price = dados['price']
        if 'quantity' in dados:
            if dados['quantity'] < 0:
                raise ValueError("Quantidade não pode ser negativa")
            product.quantity = dados['quantity']
        if 'image_url' in dados:
            product.image_url = dados['image_url']

        product_repo.update(product_id, product)
        return product_repo.find_by_id(product_id)
