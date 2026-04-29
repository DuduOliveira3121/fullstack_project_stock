from src.Infrastructure.Adapters.UserRepositoryAdapter import UserRepositoryAdapter
from src.Infrastructure.Adapters.WhatsappAdapter import WhatsappAdapter


class DIContainer:
    _repositories = {}
    _services = {}

    @classmethod
    def setup(cls):
        """Registra todas as implementações concretas dos adaptadores."""
        cls._repositories['user'] = UserRepositoryAdapter()
        cls._services['whatsapp'] = WhatsappAdapter()

    @classmethod
    def get_user_repository(cls):
        return cls._repositories['user']

    @classmethod
    def get_whatsapp_service(cls):
        return cls._services['whatsapp']
