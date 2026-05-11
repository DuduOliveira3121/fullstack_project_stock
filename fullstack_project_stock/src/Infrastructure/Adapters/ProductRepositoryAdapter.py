from typing import List, Optional

from src.Application.Ports.ProductRepositoryPort import ProductRepositoryPort
from src.Domain.product import ProductDomain, ProductStatus
from src.Infrastructure.Model.product import Product
from src.config.data_base import db


class ProductRepositoryAdapter(ProductRepositoryPort):

    def save(self, p: ProductDomain) -> int:
        product = Product(
            seller_id=p.seller_id,
            name=p.name,
            price=p.price,
            quantity=p.quantity,
            image_url=p.image_url,
            status=p.status.value,
        )
        db.session.add(product)
        db.session.commit()
        return product.id

    def find_by_id(self, product_id: int) -> Optional[ProductDomain]:
        product = Product.query.get(product_id)
        return self._to_domain(product) if product else None

    def find_by_seller_id(self, seller_id: int) -> List[ProductDomain]:
        products = Product.query.filter_by(seller_id=seller_id).all()
        return [self._to_domain(p) for p in products]

    def update(self, product_id: int, p: ProductDomain) -> bool:
        product = Product.query.get(product_id)
        if not product:
            return False

        product.name = p.name
        product.price = p.price
        product.quantity = p.quantity
        product.image_url = p.image_url
        product.status = p.status.value
        db.session.commit()
        return True

    def delete(self, product_id: int) -> bool:
        product = Product.query.get(product_id)
        if not product:
            return False

        product.status = "INACTIVE"
        db.session.commit()
        return True

    def _to_domain(self, p: Product) -> ProductDomain:
        return ProductDomain(
            id=p.id,
            seller_id=p.seller_id,
            name=p.name,
            price=p.price,
            quantity=p.quantity,
            image_url=p.image_url,
            status=ProductStatus(p.status),
            created_at=p.created_at,
        )
