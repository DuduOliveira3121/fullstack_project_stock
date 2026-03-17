import random
from werkzeug.security import generate_password_hash
from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from src.Infrastructure.http.whats_app import Whatsapp


class UserService:

    @staticmethod
    def create_user(name, email, password, phone):

        # validação de campos obrigatórios
        if not name or not email or not password or not phone:
            raise ValueError("Todos os campos são obrigatórios")

        # verificar se usuário já existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise ValueError("Usuário com este email já existe")

        # gerar código aleatório
        code = random.randint(10000, 99999)

        # hash da senha
        hashed_password = generate_password_hash(password)

        # envio do WhatsApp com tratamento de erro
        try:
            response = Whatsapp.send_message(phone, code)
        except Exception as e:
            raise Exception(f"Erro ao enviar mensagem de verificação: {str(e)}")

        # criação do usuário
        user = User(
            name=name,
            email=email,
            phone=phone,
            password=hashed_password,
            code=code
        )

        db.session.add(user)
        db.session.commit()

        return UserDomain(
            user.id,
            user.name,
            user.email,
            user.password
        )