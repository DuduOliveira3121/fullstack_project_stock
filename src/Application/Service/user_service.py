import random
from werkzeug.security import generate_password_hash
from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from src.Infrastructure.http.whats_app import Whatsapp

class UserService:

    @staticmethod
    def create_user(name, email, password, phone):
        if not name or not email or not password or not phone:
            raise ValueError("Todos os campos são obrigatórios")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise ValueError("Usuário com este email já existe")

        # Ajustado para 4 dígitos conforme o requisito
        code = random.randint(1000, 9999)

        hashed_password = generate_password_hash(password)

        # O envio agora é real via Twilio
        try:
            Whatsapp.send_message(phone, code)
        except Exception as e:
            # Se o WhatsApp falhar, interrompemos a criação para não gerar lixo no banco
            raise Exception(f"Falha na verificação de WhatsApp: {str(e)}")

        user = User(
            name=name,
            email=email,
            phone=phone,
            password=hashed_password,
            code=code,
            is_verified=False # O seller começa desativado
        )

        db.session.add(user)
        db.session.commit()

        return UserDomain(user.id, user.name, user.email)

    @staticmethod
    def activate_user(user_id, input_code):
        """Novo método para validar o código inserido pelo Seller"""
        user = User.query.get(user_id)
        
        if not user:
            raise ValueError("Usuário não encontrado")
        
        if str(user.code) == str(input_code):
            user.is_active = True
            user.code = None # Limpa o código após sucesso
            db.session.commit()
            return True
        
        return False