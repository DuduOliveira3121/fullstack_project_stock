from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user():
        try:
            data = request.get_json()
            nome = data.get('nome')
            cnpj = data.get('cnpj')
            email = data.get('email')
            celular = data.get('celular')
            senha = data.get('senha')

            if not nome or not cnpj or not email or not celular or not senha:
                return make_response(jsonify({"erro": "Campo obrigatório faltando"}), 400)

            user = UserService.create_user(nome, cnpj, email, celular, senha)
            return make_response(jsonify({
                "mensagem": "Seller cadastrado com sucesso",
                "usuario": user.to_dict()
            }), 200)
        
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro ao cadastrar: {str(e)}"}), 500)

    @staticmethod
    def activate_user():
        try:
            data = request.get_json()
            celular = data.get('celular')
            codigo = data.get('codigo')

            if not celular or not codigo:
                return make_response(jsonify({"erro": "celular e codigo são obrigatórios"}), 400)

            result = UserService.activate_user(celular, codigo)
            
            if result:
                return make_response(jsonify({
                    "mensagem": "Seller ativado com sucesso!"
                }), 200)
            else:
                return make_response(jsonify({"erro": "Código de ativação inválido"}), 400)
        
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro ao ativar: {str(e)}"}), 500)

    @staticmethod
    def login():
        try:
            data = request.get_json()
            email = data.get('email')
            senha = data.get('senha')

            if not email or not senha:
                return make_response(jsonify({"erro": "Email e senha são obrigatórios"}), 400)

            user = UserService.authenticate_user(email, senha)
            if not user:
                return make_response(jsonify({"erro": "Credenciais inválidas ou usuário inativo"}), 401)

            token = create_access_token(identity=user.id)
            return make_response(jsonify({
                "mensagem": "Login com sucesso",
                "token": token
            }), 200)

        except Exception as e:
            return make_response(jsonify({"erro": f"Erro no login: {str(e)}"}), 500)
