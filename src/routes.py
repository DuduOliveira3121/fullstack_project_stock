from src.Application.Controllers.user_controller      import UserController
from src.Application.Controllers.product_controller   import ProductController
from src.Application.Controllers.sale_controller      import SaleController
from src.Application.Controllers.dashboard_controller import DashboardController
from flask import jsonify, make_response

def init_routes(app):

    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)

    # ─── Sellers ───
    @app.route('/api/sellers', methods=['POST'])
    def register_seller():
        return UserController.register_user()

    @app.route('/api/sellers/activate', methods=['POST'])
    def activate_seller():
        return UserController.activate_user()

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        return UserController.login()

    # ─── Produtos ───
    @app.route('/api/products', methods=['POST'])
    def create_product():
        return ProductController.create_product()

    @app.route('/api/products', methods=['GET'])
    def list_products():
        return ProductController.list_products()

    @app.route('/api/products/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        return ProductController.get_product(product_id)

    @app.route('/api/products/<int:product_id>', methods=['PUT'])
    def update_product(product_id):
        return ProductController.update_product(product_id)

    @app.route('/api/products/<int:product_id>/inactivate', methods=['PATCH'])
    def deactivate_product(product_id):
        return ProductController.deactivate_product(product_id)

    # ─── Vendas ───
    @app.route('/api/sales', methods=['POST'])
    def create_sale():
        return SaleController.create_sale()

    @app.route('/api/sales', methods=['GET'])
    def list_sales():
        return SaleController.list_sales()

    # ─── Dashboard ───
    @app.route('/api/dashboard', methods=['GET'])
    def get_dashboard():
        return DashboardController.get_stats()


