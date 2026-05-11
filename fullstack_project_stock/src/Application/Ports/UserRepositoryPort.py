from abc import ABC, abstractmethod
from typing import Optional


class UserRepositoryPort(ABC):

    @abstractmethod
    def save(self, user_domain) -> int:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[object]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[object]:
        pass

    @abstractmethod
    def find_by_phone(self, phone: str) -> Optional[object]:
        pass

    @abstractmethod
    def find_by_cnpj(self, cnpj: str) -> Optional[object]:
        pass

    @abstractmethod
    def update(self, user_id: int, user_domain) -> bool:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass
