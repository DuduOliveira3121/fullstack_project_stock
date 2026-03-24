from flask import Flask
from flask_jwt_extended import JWTManager
from src.config.data_base import init_db
from src.routes import init_routes

def create_app():
    """
    Função que cria e configura a aplicação Flask.
    """
    app = Flask(__name__)

    # Configuração JWT (em produção, use variável de ambiente segura)
    app.config['JWT_SECRET_KEY'] = 'super-seguro-por-exemplo'  # altere em produção
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    # Em desenvolvimento local, evite gerenciar Twilio de verdade
    app.config['DISABLE_WHATSAPP'] = False

    init_db(app)

    JWTManager(app)

    init_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
