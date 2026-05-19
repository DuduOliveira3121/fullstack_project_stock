from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.config.data_base import init_db
from src.config.di_container import DIContainer
from src.routes import init_routes

def create_app(test_config=None):
    """
    Função que cria e configura a aplicação Flask.
    """
    app = Flask(__name__)

    # Configuração JWT (em produção, use variável de ambiente segura)
    app.config['JWT_SECRET_KEY'] = 'super-seguro-por-exemplo'  # altere em produção
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    # Em desenvolvimento local, evite gerenciar Twilio de verdade
    app.config['DISABLE_WHATSAPP'] = False

    if test_config:
        app.config.update(test_config)

    # Habilita CORS para o frontend React (localhost:3000)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    init_db(app)

    JWTManager(app)

    with app.app_context():
        DIContainer.setup()

    init_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
