from datetime import datetime


class SaleDomain:

    def __init__(self, id=None, product_id=None, seller_id=None,
                 quantity=None, unit_price=None, sale_date=None):
        self.id = id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = self.calculate_total()
        self.sale_date = sale_date or datetime.utcnow()

    def calculate_total(self) -> float:
        if self.quantity is None or self.unit_price is None:
            return 0.0
        return self.quantity * self.unit_price

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "seller_id": self.seller_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "sale_date": self.sale_date.isoformat() if self.sale_date else None,
        }
