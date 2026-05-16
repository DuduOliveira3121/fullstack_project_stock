# test_integration.py
# Execute com: .venv\Scripts\python.exe -m pytest test_integration.py -v

import pytest
from unittest.mock import patch
from run import create_app


# ─────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['DISABLE_WHATSAPP'] = True

    from src.config.data_base import db
    with app.app_context():
        db.create_all()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def registrar_seller(client):
    return client.post('/api/sellers', json={
        "nome": "Mercado Teste",
        "cnpj": "12.345.678/0001-99",
        "email": "teste@mercado.com",
        "celular": "+5511999999999",
        "senha": "senha123"
    })


def login(client):
    return client.post('/api/auth/login', json={
        "email": "teste@mercado.com",
        "senha": "senha123"
    })


def ativar_seller(app):
    """Ativa o seller diretamente no banco (simula ação do admin)."""
    from src.Infrastructure.Model.user import User
    from src.config.data_base import db
    with app.app_context():
        u = User.query.filter_by(email="teste@mercado.com").first()
        u.is_verified = True
        db.session.commit()


def auth_headers(client):
    r = login(client)
    token = r.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}


# ─────────────────────────────────────────────────────────────
# Testes básicos
# ─────────────────────────────────────────────────────────────

def test_health(client):
    r = client.get('/api')
    assert r.status_code == 200


def test_register_seller(client):
    r = registrar_seller(client)
    assert r.status_code == 200


def test_register_seller_duplicado(client):
    registrar_seller(client)
    r = registrar_seller(client)
    assert r.status_code == 400


def test_login_sem_ativacao(client):
    registrar_seller(client)
    r = login(client)
    assert r.status_code == 401  # não verificado ainda


# ─────────────────────────────────────────────────────────────
# Fluxo completo: produto → venda → dashboard
# ─────────────────────────────────────────────────────────────

def test_fluxo_completo_produto(client, app):
    registrar_seller(client)
    ativar_seller(app)

    headers = auth_headers(client)

    # Criar produto
    r = client.post('/api/products',
                    json={"name": "Arroz", "price": 5.0, "quantity": 20},
                    headers=headers)
    assert r.status_code == 201
    product_id = r.get_json()["produto"]["id"]

    # Listar produtos
    r = client.get('/api/products', headers=headers)
    assert r.status_code == 200
    assert len(r.get_json()) == 1

    # Criar venda
    r = client.post('/api/sales',
                    json={"product_id": product_id, "quantity": 5},
                    headers=headers)
    assert r.status_code == 201

    # Verificar estoque decrementou
    r = client.get(f'/api/products/{product_id}', headers=headers)
    assert r.get_json()["quantity"] == 15

    # Dashboard
    r = client.get('/api/dashboard', headers=headers)
    assert r.status_code == 200
    assert r.get_json()["total_vendido"] == 25.0  # 5 * R$5,00


# ─────────────────────────────────────────────────────────────
# Regras de negócio — estoque insuficiente
# ─────────────────────────────────────────────────────────────

def test_venda_estoque_insuficiente(client, app):
    registrar_seller(client)
    ativar_seller(app)
    headers = auth_headers(client)

    r = client.post('/api/products',
                    json={"name": "Feijão", "price": 8.0, "quantity": 2},
                    headers=headers)
    product_id = r.get_json()["produto"]["id"]

    r = client.post('/api/sales',
                    json={"product_id": product_id, "quantity": 10},
                    headers=headers)
    assert r.status_code == 409  # Conflict


# ─────────────────────────────────────────────────────────────
# Regras de negócio — produto inativo
# ─────────────────────────────────────────────────────────────

def test_venda_produto_inativo(client, app):
    registrar_seller(client)
    ativar_seller(app)
    headers = auth_headers(client)

    # Criar e inativar produto
    r = client.post('/api/products',
                    json={"name": "Macarrão", "price": 3.0, "quantity": 50},
                    headers=headers)
    product_id = r.get_json()["produto"]["id"]

    client.patch(f'/api/products/{product_id}/inactivate', headers=headers)

    # Tentar vender produto inativo
    r = client.post('/api/sales',
                    json={"product_id": product_id, "quantity": 1},
                    headers=headers)
    assert r.status_code in (400, 409)


# ─────────────────────────────────────────────────────────────
# Isolamento — seller não acessa produto de outro seller
# ─────────────────────────────────────────────────────────────

def test_seller_nao_acessa_produto_alheio(client, app):
    # Seller A cria produto
    registrar_seller(client)
    ativar_seller(app)
    headers_a = auth_headers(client)

    r = client.post('/api/products',
                    json={"name": "Óleo", "price": 7.0, "quantity": 10},
                    headers=headers_a)
    product_id = r.get_json()["produto"]["id"]

    # Seller B se registra e tenta acessar o produto do Seller A
    client.post('/api/sellers', json={
        "nome": "Outro Seller",
        "cnpj": "98.765.432/0001-00",
        "email": "outro@seller.com",
        "celular": "+5511888888888",
        "senha": "senha456"
    })
    from src.Infrastructure.Model.user import User
    from src.config.data_base import db
    with app.app_context():
        u = User.query.filter_by(email="outro@seller.com").first()
        u.is_verified = True
        db.session.commit()

    r = client.post('/api/auth/login',
                    json={"email": "outro@seller.com", "senha": "senha456"})
    token_b = r.get_json()["token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    r = client.get(f'/api/products/{product_id}', headers=headers_b)
    assert r.status_code in (403, 404)


# ─────────────────────────────────────────────────────────────
# Produto — validação de preço inválido
# ─────────────────────────────────────────────────────────────

def test_criar_produto_preco_invalido(client, app):
    registrar_seller(client)
    ativar_seller(app)
    headers = auth_headers(client)

    r = client.post('/api/products',
                    json={"name": "Produto Inválido", "price": -1.0, "quantity": 10},
                    headers=headers)
    assert r.status_code == 400


# ─────────────────────────────────────────────────────────────
# Dashboard — seller sem vendas
# ─────────────────────────────────────────────────────────────

def test_dashboard_sem_vendas(client, app):
    registrar_seller(client)
    ativar_seller(app)
    headers = auth_headers(client)

    r = client.get('/api/dashboard', headers=headers)
    assert r.status_code == 200
    data = r.get_json()
    assert data["total_vendido"] == 0.0
    assert data["ticket_medio"] == 0.0


# ─────────────────────────────────────────────────────────────
# Listagem de vendas
# ─────────────────────────────────────────────────────────────

def test_listar_vendas(client, app):
    registrar_seller(client)
    ativar_seller(app)
    headers = auth_headers(client)

    r = client.post('/api/products',
                    json={"name": "Açúcar", "price": 4.0, "quantity": 30},
                    headers=headers)
    product_id = r.get_json()["produto"]["id"]

    client.post('/api/sales',
                json={"product_id": product_id, "quantity": 3},
                headers=headers)
    client.post('/api/sales',
                json={"product_id": product_id, "quantity": 2},
                headers=headers)

    r = client.get('/api/sales', headers=headers)
    assert r.status_code == 200
    assert len(r.get_json()) == 2
