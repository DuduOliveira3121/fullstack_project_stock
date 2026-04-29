from enum import Enum
from datetime import datetime


class UserStatus(Enum):
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"


class UserDomain:

    def __init__(self, id=None, name=None, email=None, phone=None,
                 cnpj=None, status=None, is_verified=False,
                 created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.cnpj = cnpj
        self.status = status if status is not None else UserStatus.INACTIVE
        self.is_verified = is_verified
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def activate(self) -> None:
        if not self.is_verified:
            raise ValueError("Usuário deve ser verificado antes de ser ativado")
        self.status = UserStatus.ACTIVE
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        self.status = UserStatus.INACTIVE
        self.updated_at = datetime.utcnow()

    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE

    def can_login(self) -> bool:
        return self.is_active() and self.is_verified

    def can_manage_products(self) -> bool:
        return self.can_login()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "cnpj": self.cnpj,
            "status": self.status.value,
            "is_verified": self.is_verified,
        }

