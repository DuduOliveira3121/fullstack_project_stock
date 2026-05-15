from src.Infrastructure.Adapters.UserRepositoryAdapter import UserRepositoryAdapter
from src.Infrastructure.Adapters.WhatsappAdapter import WhatsappAdapter
from src.Infrastructure.Adapters.ProductRepositoryAdapter import ProductRepositoryAdapter
from src.Infrastructure.Adapters.SaleRepositoryAdapter import SaleRepositoryAdapter


class DIContainer:
    _repositories = {}
    _services = {}

    @classmethod
    def setup(cls):
        """Registra todas as implementações concretas dos adaptadores."""
        cls._repositories['user']    = UserRepositoryAdapter()
        cls._repositories['product'] = ProductRepositoryAdapter()
        cls._repositories['sale']    = SaleRepositoryAdapter()
        cls._services['whatsapp']    = WhatsappAdapter()

    @classmethod
    def get_user_repository(cls):
        return cls._repositories['user']

    @classmethod
    def get_product_repository(cls):
        return cls._repositories['product']

    @classmethod
    def get_sale_repository(cls):
        return cls._repositories['sale']

    @classmethod
    def get_whatsapp_service(cls):
        return cls._services['whatsapp']
