from typing import Optional

from src.Application.Ports.UserRepositoryPort import UserRepositoryPort
from src.config.data_base import db
from src.Domain.user import UserDomain, UserStatus
from src.Infrastructure.Model.user import User


class UserRepositoryAdapter(UserRepositoryPort):

    def save(self, user_domain: UserDomain) -> int:
        user = User(
            name=user_domain.name,
            cnpj=user_domain.cnpj,
            email=user_domain.email,
            phone=user_domain.phone,
            password=getattr(user_domain, 'password', ''),
            code=getattr(user_domain, 'code', None),
            is_verified=user_domain.is_verified,
        )
        db.session.add(user)
        db.session.commit()
        return user.id

    def find_by_id(self, user_id: int) -> Optional[UserDomain]:
        user = User.query.get(user_id)
        return self._to_domain(user) if user else None

    def find_by_email(self, email: str) -> Optional[UserDomain]:
        user = User.query.filter_by(email=email).first()
        return self._to_domain(user) if user else None

    def find_by_phone(self, phone: str) -> Optional[UserDomain]:
        user = User.query.filter_by(phone=phone).first()
        return self._to_domain(user) if user else None

    def find_by_cnpj(self, cnpj: str) -> Optional[UserDomain]:
        user = User.query.filter_by(cnpj=cnpj).first()
        return self._to_domain(user) if user else None

    def update(self, user_id: int, user_domain: UserDomain) -> bool:
        user = User.query.get(user_id)
        if not user:
            return False
        user.name = user_domain.name
        user.is_verified = user_domain.is_verified
        if hasattr(user_domain, 'code'):
            user.code = user_domain.code
        db.session.commit()
        return True

    def delete(self, user_id: int) -> bool:
        user = User.query.get(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True

    def _to_domain(self, user: User) -> UserDomain:
        domain = UserDomain(
            id=user.id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            cnpj=user.cnpj,
            is_verified=user.is_verified,
            status=UserStatus.ACTIVE if user.is_verified else UserStatus.INACTIVE,
        )
        # Preserva campos extras que o serviço precisa
        domain.password = user.password
        domain.code = user.code
        return domain
