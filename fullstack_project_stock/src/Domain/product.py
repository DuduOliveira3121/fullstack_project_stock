from enum import Enum
from datetime import datetime


class ProductStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class ProductDomain:

    def __init__(self, id=None, seller_id=None, name=None, price=None,
                 quantity=None, image_url=None, status=None, created_at=None):
        self.id = id
        self.seller_id = seller_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.image_url = image_url
        self.status = status if status is not None else ProductStatus.ACTIVE
        self.created_at = created_at or datetime.utcnow()

    def decrease_stock(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        if amount > self.quantity:
            raise ValueError("Estoque insuficiente")
        self.quantity -= amount

    def increase_stock(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        self.quantity += amount

    def can_be_sold(self, amount: int) -> bool:
        return self.status == ProductStatus.ACTIVE and self.quantity >= amount

    def deactivate(self) -> None:
        self.status = ProductStatus.INACTIVE

    def activate(self) -> None:
        self.status = ProductStatus.ACTIVE

    def is_active(self) -> bool:
        return self.status == ProductStatus.ACTIVE

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "image_url": self.image_url,
            "status": self.status.value,
        }
