from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.Application.UseCases.CreateProductUseCase     import CreateProductUseCase
from src.Application.UseCases.ListProductsUseCase      import ListProductsUseCase
from src.Application.UseCases.GetProductDetailsUseCase import GetProductDetailsUseCase
from src.Application.UseCases.UpdateProductUseCase     import UpdateProductUseCase
from src.Application.UseCases.DeactivateProductUseCase import DeactivateProductUseCase


class ProductController:

    @staticmethod
    @jwt_required()
    def create_product():
        try:
            seller_id = int(get_jwt_identity())
            data      = request.get_json()
            product   = CreateProductUseCase.execute(
                seller_id,
                data.get('name'),
                data.get('price'),
                data.get('quantity', 0),
                data.get('image_url'),
            )
            return make_response(jsonify({
                "mensagem": "Produto criado com sucesso",
                "produto": product.to_dict(),
            }), 201)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro interno: {str(e)}"}), 500)

    @staticmethod
    @jwt_required()
    def list_products():
        try:
            seller_id = int(get_jwt_identity())
            products  = ListProductsUseCase.execute(seller_id)
            return make_response(jsonify([p.to_dict() for p in products]), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    @jwt_required()
    def get_product(product_id):
        try:
            seller_id = int(get_jwt_identity())
            product   = GetProductDetailsUseCase.execute(product_id, seller_id)
            return make_response(jsonify(product.to_dict()), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    @jwt_required()
    def update_product(product_id):
        try:
            seller_id = int(get_jwt_identity())
            data      = request.get_json()
            product   = UpdateProductUseCase.execute(product_id, seller_id, **data)
            return make_response(jsonify({
                "mensagem": "Produto atualizado",
                "produto": product.to_dict(),
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    @jwt_required()
    def deactivate_product(product_id):
        try:
            seller_id = int(get_jwt_identity())
            DeactivateProductUseCase.execute(product_id, seller_id)
            return make_response(jsonify({"mensagem": "Produto desativado"}), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
