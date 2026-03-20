from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user():
        try:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            phone = data.get('phone')

            if not name or not email or not password or not phone:
                return make_response(jsonify({"erro": "Missing required fields"}), 400)

            user = UserService.create_user(name, email, password, phone)
            return make_response(jsonify({
                "mensagem": "User salvo com sucesso",
                "usuarios": user.to_dict()
            }), 200)
        
        except ValueError as e:
            # Erros de validação (email duplicado, etc)
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            # Outros erros
            return make_response(jsonify({"erro": f"Erro ao cadastrar: {str(e)}"}), 500)
