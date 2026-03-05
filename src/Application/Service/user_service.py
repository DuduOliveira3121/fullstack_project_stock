from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from src.Infrastructure.http.whats_app import Whatsapp

class UserService:
    @staticmethod
    def create_user(name, email, password):

        code = 23453

        response = Whatsapp.send_message(code)
        #verificar se houve sucesso no envio da mensagem
        
        user = User(name=name, email=email, password=password, code=code)        
        db.session.add(user)
        db.session.commit()       
        return UserDomain(user.id, user.name, user.email, user.password)