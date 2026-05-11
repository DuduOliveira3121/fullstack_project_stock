from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import date


class SaleRepositoryPort(ABC):

    @abstractmethod
    def save(self, sale_domain) -> int:
        pass

    @abstractmethod
    def find_by_id(self, sale_id: int) -> Optional[object]:
        pass

    @abstractmethod
    def find_by_seller_id(self, seller_id: int) -> List[object]:
        pass

    @abstractmethod
    def get_total_sales(self, seller_id: int) -> float:
        pass

    @abstractmethod
    def get_sales_by_period(self, seller_id: int, start_date: date, end_date: date) -> List[object]:
        pass
