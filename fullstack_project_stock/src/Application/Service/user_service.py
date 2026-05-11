import random
from werkzeug.security import generate_password_hash, check_password_hash

from src.config.di_container import DIContainer
from src.Domain.user import UserDomain


class UserService:

    @staticmethod
    def create_user(nome, cnpj, email, celular, senha):
        if not nome or not cnpj or not email or not celular or not senha:
            raise ValueError("Todos os campos são obrigatórios")

        user_repo = DIContainer.get_user_repository()
        whatsapp = DIContainer.get_whatsapp_service()

        if user_repo.find_by_email(email):
            raise ValueError("Usuário com este email já existe")

        if user_repo.find_by_cnpj(cnpj):
            raise ValueError("Usuário com este CNPJ já existe")

        if user_repo.find_by_phone(celular):
            raise ValueError("Usuário com este celular já existe")

        code = random.randint(1000, 9999)
        hashed_password = generate_password_hash(senha)

        whatsapp.send_verification_code(celular, str(code))

        new_user = UserDomain(
            name=nome,
            cnpj=cnpj,
            email=email,
            phone=celular,
            is_verified=False,
        )
        new_user.password = hashed_password
        new_user.code = code

        user_id = user_repo.save(new_user)
        saved = user_repo.find_by_id(user_id)
        return saved

    @staticmethod
    def activate_user(celular, codigo):
        """Ativa o Seller validando o código enviado via WhatsApp"""
        user_repo = DIContainer.get_user_repository()

        user = user_repo.find_by_phone(celular)
        if not user:
            raise ValueError("Usuário não encontrado")

        if str(user.code) == str(codigo):
            user.is_verified = True
            user.code = None
            user.activate()
            user_repo.update(user.id, user)
            return True

        return False

    @staticmethod
    def authenticate_user(email, senha):
        user_repo = DIContainer.get_user_repository()

        user = user_repo.find_by_email(email)
        if user is None:
            return None

        if not user.is_verified:
            return None

        if not check_password_hash(user.password, senha):
            return None

        return user