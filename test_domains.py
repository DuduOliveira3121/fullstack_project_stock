# test_domains.py
# Execute com: .venv\Scripts\python.exe -m pytest test_domains.py -v

import pytest
from src.Domain.user import UserDomain, UserStatus
from src.Domain.product import ProductDomain, ProductStatus
from src.Domain.sale import SaleDomain


# ─────────────────────────────────────────────────────────────
# User
# ─────────────────────────────────────────────────────────────

def test_user_activate_sem_verificacao():
    """Seller não verificado não pode ser ativado."""
    u = UserDomain(is_verified=False)
    with pytest.raises(ValueError):
        u.activate()


def test_user_activate_com_verificacao():
    """Seller verificado é ativado com sucesso."""
    u = UserDomain(is_verified=True)
    u.activate()
    assert u.is_active() is True


def test_user_can_login():
    """Seller ativo e verificado pode fazer login."""
    u = UserDomain(is_verified=True)
    u.activate()
    assert u.can_login() is True


def test_user_inativo_nao_pode_login():
    """Seller sem verificação não pode fazer login."""
    u = UserDomain(is_verified=False)
    assert u.can_login() is False


# ─────────────────────────────────────────────────────────────
# Product
# ─────────────────────────────────────────────────────────────

def test_product_decrease_stock_ok():
    """Diminuir estoque com quantidade válida funciona."""
    p = ProductDomain(quantity=10)
    p.decrease_stock(3)
    assert p.quantity == 7


def test_product_decrease_stock_insuficiente():
    """Diminuir mais do que o estoque levanta ValueError."""
    p = ProductDomain(quantity=2)
    with pytest.raises(ValueError):
        p.decrease_stock(5)


def test_product_can_be_sold_ativo():
    """Produto ativo com estoque suficiente pode ser vendido."""
    p = ProductDomain(quantity=10, status=ProductStatus.ACTIVE)
    assert p.can_be_sold(5) is True


def test_product_can_be_sold_inativo():
    """Produto inativo não pode ser vendido, mesmo com estoque."""
    p = ProductDomain(quantity=10, status=ProductStatus.INACTIVE)
    assert p.can_be_sold(5) is False


def test_product_can_be_sold_sem_estoque():
    """Produto ativo sem estoque não pode ser vendido."""
    p = ProductDomain(quantity=0, status=ProductStatus.ACTIVE)
    assert p.can_be_sold(1) is False


def test_product_decrease_stock_exato():
    """Vender exatamente o estoque disponível é permitido."""
    p = ProductDomain(quantity=5, status=ProductStatus.ACTIVE)
    p.decrease_stock(5)
    assert p.quantity == 0


def test_product_deactivate():
    """Inativar produto muda status para INACTIVE."""
    p = ProductDomain(quantity=10, status=ProductStatus.ACTIVE)
    p.deactivate()
    assert p.status == ProductStatus.INACTIVE
    assert p.is_active() is False


# ─────────────────────────────────────────────────────────────
# Sale
# ─────────────────────────────────────────────────────────────

def test_sale_calculate_total():
    """total_price = quantity * unit_price."""
    s = SaleDomain(quantity=3, unit_price=5.0)
    assert s.total_price == 15.0


def test_sale_total_zero_sem_dados():
    """SaleDomain sem dados retorna total_price = 0."""
    s = SaleDomain()
    assert s.total_price == 0.0


def test_sale_total_preco_unitario_decimal():
    """Garante precisão com preço decimal."""
    s = SaleDomain(quantity=4, unit_price=2.50)
    assert s.total_price == 10.0
