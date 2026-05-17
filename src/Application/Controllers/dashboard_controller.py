from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.Application.UseCases.GetDashboardStatsUseCase import GetDashboardStatsUseCase


class DashboardController:

    @staticmethod
    @jwt_required()
    def get_stats():
        try:
            seller_id = int(get_jwt_identity())
            stats     = GetDashboardStatsUseCase.execute(seller_id)
            return make_response(jsonify(stats), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
