from abc import ABC, abstractmethod
from typing import Optional, List


class ProductRepositoryPort(ABC):

    @abstractmethod
    def save(self, product_domain) -> int:
        pass

    @abstractmethod
    def find_by_id(self, product_id: int) -> Optional[object]:
        pass

    @abstractmethod
    def find_by_seller_id(self, seller_id: int) -> List[object]:
        pass

    @abstractmethod
    def update(self, product_id: int, product_domain) -> bool:
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        pass
