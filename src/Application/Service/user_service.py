import random
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from src.Infrastructure.http.whats_app import Whatsapp

class UserService:

    @staticmethod
    def create_user(nome, cnpj, email, celular, senha):
        if not nome or not cnpj or not email or not celular or not senha:
            raise ValueError("Todos os campos são obrigatórios")

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            raise ValueError("Usuário com este email já existe")
        
        existing_cnpj = User.query.filter_by(cnpj=cnpj).first()
        if existing_cnpj:
            raise ValueError("Usuário com este CNPJ já existe")
        
        existing_phone = User.query.filter_by(phone=celular).first()
        if existing_phone:
            raise ValueError("Usuário com este celular já existe")

        # Gera código de 4 dígitos
        code = random.randint(1000, 9999)

        hashed_password = generate_password_hash(senha)

        # Envio real via Twilio (pula se DESATIVADO)
        if not current_app.config.get('DISABLE_WHATSAPP', False):
            try:
                Whatsapp.send_message(celular, code)
            except Exception as e:
                raise Exception(f"Falha na verificação de WhatsApp: {str(e)}")
        else:
            print("⚠️ WhatsApp desabilitado no ambiente; código não será enviado")

        user = User(
            name=nome,
            cnpj=cnpj,
            email=email,
            phone=celular,
            password=hashed_password,
            code=code,
            is_verified=False
        )

        db.session.add(user)
        db.session.commit()

        return UserDomain(user.id, user.name, user.email)

    @staticmethod
    def activate_user(celular, codigo):
        """Ativa o Seller validando o código enviado via WhatsApp"""
        user = User.query.filter_by(phone=celular).first()
        
        if not user:
            raise ValueError("Usuário não encontrado")
        
        if str(user.code) == str(codigo):
            user.is_verified = True
            user.code = None
            db.session.commit()
            return True
        
        return False

    @staticmethod
    def authenticate_user(email, senha):
        user = User.query.filter_by(email=email).first()
        if user is None:
            return None

        if not user.is_verified:
            return None

        if not check_password_hash(user.password, senha):
            return None

        return user