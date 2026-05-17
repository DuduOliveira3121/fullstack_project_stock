from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.Application.UseCases.CreateSaleUseCase import CreateSaleUseCase
from src.Application.UseCases.ListSalesUseCase  import ListSalesUseCase


class SaleController:

    @staticmethod
    @jwt_required()
    def create_sale():
        try:
            seller_id = int(get_jwt_identity())
            data      = request.get_json()
            sale      = CreateSaleUseCase.execute(
                data.get('product_id'),
                seller_id,
                data.get('quantity'),
            )
            return make_response(jsonify({
                "mensagem": "Venda registrada",
                "venda": sale.to_dict(),
            }), 201)
        except ValueError as e:
            status = 409 if "insuficiente" in str(e).lower() else 400
            return make_response(jsonify({"erro": str(e)}), status)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    @jwt_required()
    def list_sales():
        try:
            seller_id = int(get_jwt_identity())
            sales     = ListSalesUseCase.execute(seller_id)
            return make_response(jsonify([s.to_dict() for s in sales]), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
