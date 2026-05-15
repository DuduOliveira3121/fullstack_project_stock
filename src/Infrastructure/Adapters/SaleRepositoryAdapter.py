from typing import Optional, List
from datetime import date

from src.Application.Ports.SaleRepositoryPort import SaleRepositoryPort
from src.Infrastructure.Model.sale import Sale
from src.Domain.sale import SaleDomain
from src.config.data_base import db


class SaleRepositoryAdapter(SaleRepositoryPort):

    def save(self, s: SaleDomain) -> int:
        sale = Sale(
            product_id=s.product_id,
            seller_id=s.seller_id,
            quantity=s.quantity,
            unit_price=s.unit_price,
            total_price=s.total_price,
        )
        db.session.add(sale)
        db.session.commit()
        return sale.id

    def find_by_id(self, sale_id: int) -> Optional[SaleDomain]:
        sale = Sale.query.get(sale_id)
        return self._to_domain(sale) if sale else None

    def find_by_seller_id(self, seller_id: int) -> List[SaleDomain]:
        sales = Sale.query.filter_by(seller_id=seller_id).all()
        return [self._to_domain(s) for s in sales]

    def get_total_sales(self, seller_id: int) -> float:
        result = db.session.query(
            db.func.sum(Sale.total_price)
        ).filter_by(seller_id=seller_id).scalar()
        return float(result) if result else 0.0

    def get_sales_by_period(self, seller_id: int,
                            start_date: date, end_date: date) -> List[SaleDomain]:
        sales = Sale.query.filter(
            Sale.seller_id == seller_id,
            Sale.sale_date >= start_date,
            Sale.sale_date <= end_date,
        ).all()
        return [self._to_domain(s) for s in sales]

    def _to_domain(self, s: Sale) -> SaleDomain:
        domain = SaleDomain(
            id=s.id,
            product_id=s.product_id,
            seller_id=s.seller_id,
            quantity=s.quantity,
            unit_price=s.unit_price,
            sale_date=s.sale_date,
        )
        domain.total_price = s.total_price
        return domain
