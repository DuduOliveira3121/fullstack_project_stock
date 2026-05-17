from src.config.di_container import DIContainer


class GetDashboardStatsUseCase:

    @staticmethod
    def execute(seller_id: int) -> dict:
        product_repo = DIContainer.get_product_repository()
        sale_repo    = DIContainer.get_sale_repository()

        products = product_repo.find_by_seller_id(seller_id)
        sales    = sale_repo.find_by_seller_id(seller_id)

        ativos        = [p for p in products if p.is_active()]
        total_estoque = sum(p.quantity for p in ativos)
        baixo_estoque = [p.to_dict() for p in ativos if p.quantity < 10]
        total_vendido = sale_repo.get_total_sales(seller_id)
        ticket_medio  = (total_vendido / len(sales)) if sales else 0.0

        return {
            "total_vendido":           round(total_vendido, 2),
            "total_produtos":          len(ativos),
            "total_estoque":           total_estoque,
            "produtos_baixo_estoque":  baixo_estoque,
            "ticket_medio":            round(ticket_medio, 2),
        }
