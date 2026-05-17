"""
============================================================
  DEMO COMPLETO DE CRUDs — Sistema de Gestão de Estoque
  Faculdade Impacta — Frameworks Full Stack
============================================================
Execute: python demo_crud.py
"""

import sys
import json

# ── Cores ANSI ────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
GREEN   = "\033[92m"
RED     = "\033[91m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
DIM     = "\033[2m"

# ── Contadores globais ────────────────────────────────────
_passou = 0
_falhou = 0


def titulo(texto):
    largura = 62
    print()
    print(CYAN + BOLD + "═" * largura + RESET)
    print(CYAN + BOLD + f"  {texto}" + RESET)
    print(CYAN + BOLD + "═" * largura + RESET)


def secao(texto):
    print()
    print(BLUE + BOLD + f"  ┌─ {texto} " + "─" * max(0, 54 - len(texto)) + RESET)


def testar(descricao, resposta, status_esperado, validar_fn=None):
    global _passou, _falhou
    status = resposta.status_code
    try:
        corpo = resposta.get_json()
    except Exception:
        corpo = {}

    ok_status = (status == status_esperado)
    ok_extra  = validar_fn(corpo) if validar_fn else True
    passou    = ok_status and ok_extra

    icone = GREEN + "  ✔" + RESET if passou else RED + "  ✘" + RESET
    cor   = GREEN if passou else RED
    label = f"HTTP {status}"

    print(f"{icone}  {WHITE}{descricao:<44}{RESET} {cor}{label}{RESET}")

    if not ok_status:
        print(f"     {DIM}→ esperado HTTP {status_esperado}, recebido HTTP {status}{RESET}")
        print(f"     {DIM}→ corpo: {json.dumps(corpo, ensure_ascii=False)[:120]}{RESET}")

    if passou:
        _passou += 1
    else:
        _falhou += 1

    return corpo, passou


def info(msg):
    print(f"  {DIM}→  {msg}{RESET}")


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    # ── Bootstrap silencioso ─────────────────────────────
    import warnings
    warnings.filterwarnings("ignore")
    import os
    os.environ["SQLALCHEMY_SILENCE_UBER_WARNING"] = "1"
    os.environ["SQLALCHEMY_WARN_20"] = "0"

    from run import create_app
    from src.config.data_base import db
    from src.Infrastructure.Model.user import User

    print()
    print(CYAN + BOLD + "╔══════════════════════════════════════════════════════════╗" + RESET)
    print(CYAN + BOLD + "║     DEMO CRUDs — SISTEMA DE GESTÃO DE ESTOQUE           ║" + RESET)
    print(CYAN + BOLD + "║     Faculdade Impacta  •  Frameworks Full Stack          ║" + RESET)
    print(CYAN + BOLD + "╚══════════════════════════════════════════════════════════╝" + RESET)

    # Banco em memória: garante ambiente limpo a cada execução
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "DISABLE_WHATSAPP": True,
    })

    with app.app_context():
        db.create_all()

    client = app.test_client()

    # ══════════════════════════════════════════════════════
    titulo("1 · HEALTH CHECK")
    # ══════════════════════════════════════════════════════
    r = client.get("/api")
    testar("GET  /api  — API online", r, 200,
           lambda c: "mensagem" in c)

    # ══════════════════════════════════════════════════════
    titulo("2 · SELLERS  (Cadastro & Autenticação)")
    # ══════════════════════════════════════════════════════

    secao("CREATE — Registrar seller principal")
    payload_seller = {
        "nome":    "Mercadinho do João",
        "cnpj":   "12.345.678/0001-99",
        "email":  "joao@mercadinho.com",
        "celular": "+5511999990001",
        "senha":  "Senha@2025",
    }
    r = client.post("/api/sellers", json=payload_seller)
    corpo, ok = testar(
        "POST /api/sellers  — novo seller → 200",
        r, 200,
        lambda c: c.get("usuario", {}).get("email") == "joao@mercadinho.com",
    )
    if ok:
        info(f"seller criado  →  id={corpo['usuario']['id']}  |  is_verified=False")

    secao("CREATE — E-mail/CNPJ duplicado (erro esperado)")
    r = client.post("/api/sellers", json=payload_seller)
    testar("POST /api/sellers  — duplicado → 400", r, 400)

    secao("AUTH — Login antes da ativação (deve falhar)")
    r = client.post("/api/auth/login",
                    json={"email": "joao@mercadinho.com", "senha": "Senha@2025"})
    testar("POST /api/auth/login  — inativo → 401", r, 401)

    secao("ACTIVATE — Verificar código recebido via WhatsApp")
    with app.app_context():
        u = User.query.filter_by(email="joao@mercadinho.com").first()
        codigo = u.code  # código gerado e enviado via WhatsApp (simulado)
    info(f"código WhatsApp simulado  →  {codigo}")
    r = client.post("/api/sellers/activate",
                    json={"celular": "+5511999990001", "codigo": str(codigo)})
    testar("POST /api/sellers/activate  — ativado → 200", r, 200,
           lambda c: "sucesso" in c.get("mensagem", "").lower())

    secao("AUTH — Login após ativação")
    r = client.post("/api/auth/login",
                    json={"email": "joao@mercadinho.com", "senha": "Senha@2025"})
    corpo_login, ok = testar(
        "POST /api/auth/login  — ativo → 200 + token JWT",
        r, 200,
        lambda c: "token" in c,
    )
    if not ok:
        print(RED + "\n  Falha crítica: sem token JWT. Abortando demo." + RESET)
        sys.exit(1)

    token   = corpo_login["token"]
    headers = {"Authorization": f"Bearer {token}"}
    info("JWT Bearer token obtido com sucesso")

    # ══════════════════════════════════════════════════════
    titulo("3 · PRODUTOS  (CRUD completo)")
    # ══════════════════════════════════════════════════════

    secao("CREATE — Criar produto válido")
    r = client.post("/api/products", json={
        "name":     "Arroz Tipo 1",
        "price":    8.90,
        "quantity": 50,
    }, headers=headers)
    corpo_prod, ok = testar(
        "POST /api/products  — produto criado → 201",
        r, 201,
        lambda c: c.get("produto", {}).get("name") == "Arroz Tipo 1",
    )
    produto_id = None
    if ok:
        produto_id = corpo_prod["produto"]["id"]
        info(f"produto criado  →  id={produto_id}  |  preço=R${corpo_prod['produto']['price']}  |  estoque={corpo_prod['produto']['quantity']}")

    secao("CREATE — Segundo produto (para testar vendas)")
    r = client.post("/api/products", json={
        "name":     "Feijão Carioca",
        "price":    6.50,
        "quantity": 30,
    }, headers=headers)
    corpo_prod2, ok2 = testar(
        "POST /api/products  — segundo produto → 201",
        r, 201,
    )
    produto2_id = corpo_prod2["produto"]["id"] if ok2 else None

    secao("CREATE — Preço inválido (erro esperado)")
    r = client.post("/api/products", json={
        "name": "Produto Inválido", "price": -1.0, "quantity": 10,
    }, headers=headers)
    testar("POST /api/products  — preço negativo → 400", r, 400)

    secao("READ — Listar todos os produtos do seller")
    r = client.get("/api/products", headers=headers)
    corpo_lista, ok = testar(
        "GET  /api/products  — lista produtos → 200",
        r, 200,
        lambda c: isinstance(c, list) and len(c) >= 2,
    )
    if ok:
        for p in corpo_lista:
            info(f"  [{p['id']}] {p['name']:<20} R${p['price']:<8}  estoque={p['quantity']}  status={p['status']}")

    secao("READ — Buscar produto por ID")
    if produto_id:
        r = client.get(f"/api/products/{produto_id}", headers=headers)
        corpo_detalhe, ok = testar(
            f"GET  /api/products/{produto_id}  — detalhe → 200",
            r, 200,
            lambda c: c.get("id") == produto_id,
        )
        if ok:
            info(f"produto  →  nome='{corpo_detalhe['name']}'  |  status={corpo_detalhe['status']}")

    secao("UPDATE — Atualizar nome e preço")
    if produto_id:
        r = client.put(f"/api/products/{produto_id}", json={
            "name":  "Arroz Tipo 1 Premium",
            "price": 9.90,
        }, headers=headers)
        corpo_upd, ok = testar(
            f"PUT  /api/products/{produto_id}  — atualizado → 200",
            r, 200,
            lambda c: c.get("produto", {}).get("price") == 9.90,
        )
        if ok:
            info(f"novo nome='{corpo_upd['produto']['name']}'  |  novo preço=R${corpo_upd['produto']['price']}")

    secao("DELETE (soft) — Inativar produto")
    if produto_id:
        r = client.patch(f"/api/products/{produto_id}/inactivate", headers=headers)
        testar(
            f"PATCH /api/products/{produto_id}/inactivate → 200",
            r, 200,
            lambda c: "desativado" in c.get("mensagem", ""),
        )
        info("produto marcado como INACTIVE (exclusão lógica / soft delete)")

    secao("SEGURANÇA — Seller B não acessa produto do Seller A")
    client.post("/api/sellers", json={
        "nome": "Seller B", "cnpj": "98.765.432/0001-11",
        "email": "b@b.com", "celular": "+5511000000002", "senha": "SenhaB@2025",
    })
    with app.app_context():
        ub = User.query.filter_by(email="b@b.com").first()
        codigo_b = ub.code
    client.post("/api/sellers/activate",
                json={"celular": "+5511000000002", "codigo": str(codigo_b)})
    rB = client.post("/api/auth/login",
                     json={"email": "b@b.com", "senha": "SenhaB@2025"})
    token_b   = rB.get_json()["token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    if produto2_id:
        r = client.get(f"/api/products/{produto2_id}", headers=headers_b)
        ok_403_or_404 = r.status_code in (403, 404)
        icone = GREEN + "  ✔" + RESET if ok_403_or_404 else RED + "  ✘" + RESET
        cor   = GREEN if ok_403_or_404 else RED
        print(f"{icone}  {WHITE}{'GET produto alheio → acesso negado':<44}{RESET} {cor}HTTP {r.status_code}{RESET}")
        global _passou, _falhou
        if ok_403_or_404:
            _passou += 1
        else:
            _falhou += 1
        info("regra de isolamento entre sellers funcionando")

    # ══════════════════════════════════════════════════════
    titulo("4 · VENDAS  (CRUD)")
    # ══════════════════════════════════════════════════════

    secao("CREATE — Registrar venda com estoque suficiente")
    if produto2_id:
        r = client.post("/api/sales", json={
            "product_id": produto2_id,
            "quantity":   5,
        }, headers=headers)
        corpo_venda, ok = testar(
            "POST /api/sales  — venda registrada → 201",
            r, 201,
            lambda c: "venda" in c,
        )
        if ok:
            v = corpo_venda["venda"]
            info(f"venda  →  id={v['id']}  |  qty={v['quantity']}  |  total=R${v['total_price']}")

    secao("CREATE — Venda com estoque insuficiente (erro esperado)")
    if produto2_id:
        r = client.post("/api/sales", json={
            "product_id": produto2_id,
            "quantity":   9999,
        }, headers=headers)
        testar("POST /api/sales  — estoque insuficiente → 409", r, 409)

    secao("CREATE — Venda de produto inativo (erro esperado)")
    if produto_id:
        r = client.post("/api/sales", json={
            "product_id": produto_id,
            "quantity":   1,
        }, headers=headers)
        testar("POST /api/sales  — produto inativo → 409", r, 409)

    secao("CREATE — Segunda venda (enriquecer dashboard)")
    if produto2_id:
        r = client.post("/api/sales", json={
            "product_id": produto2_id,
            "quantity":   3,
        }, headers=headers)
        testar("POST /api/sales  — segunda venda → 201", r, 201)

    secao("READ — Listar todas as vendas do seller")
    r = client.get("/api/sales", headers=headers)
    corpo_vendas, ok = testar(
        "GET  /api/sales  — lista vendas → 200",
        r, 200,
        lambda c: isinstance(c, list) and len(c) >= 1,
    )
    if ok:
        for v in corpo_vendas:
            info(f"  [{v['id']}] produto={v['product_id']}  qty={v['quantity']}  total=R${v['total_price']}")

    # ══════════════════════════════════════════════════════
    titulo("5 · DASHBOARD  (Métricas Consolidadas)")
    # ══════════════════════════════════════════════════════

    secao("READ — Obter estatísticas do seller")
    r = client.get("/api/dashboard", headers=headers)
    corpo_dash, ok = testar(
        "GET  /api/dashboard  — métricas → 200",
        r, 200,
        lambda c: "total_vendido" in c and "total_produtos" in c,
    )
    if ok:
        print()
        baixo = corpo_dash.get('produtos_baixo_estoque', 0)
        if isinstance(baixo, list):
            baixo = len(baixo)
        print(MAGENTA + BOLD + "  ┌─────────────────────────────────────────┐" + RESET)
        print(MAGENTA + BOLD + "  │         PAINEL DO SELLER                │" + RESET)
        print(MAGENTA + BOLD + "  ├─────────────────────────────────────────┤" + RESET)
        print(MAGENTA + f"  │  $   Total vendido:    R$ {corpo_dash.get('total_vendido', 0):<12.2f}  │" + RESET)
        print(MAGENTA + f"  │  [P] Total produtos:   {corpo_dash.get('total_produtos', 0):<15}  │" + RESET)
        print(MAGENTA + f"  │  [E] Estoque total:    {corpo_dash.get('total_estoque', 0):<15}  │" + RESET)
        print(MAGENTA + f"  │  [T] Ticket medio:     R$ {corpo_dash.get('ticket_medio', 0):<12.2f}  │" + RESET)
        print(MAGENTA + f"  │  [!] Estoque baixo:    {baixo:<15}  │" + RESET)
        print(MAGENTA + BOLD + "  └─────────────────────────────────────────┘" + RESET)

    # ══════════════════════════════════════════════════════
    titulo("6 · RESUMO FINAL")
    # ══════════════════════════════════════════════════════
    total = _passou + _falhou
    print()
    print(f"  {GREEN + BOLD}Passaram:{RESET}  {GREEN}{_passou:>2} / {total}{RESET}")
    if _falhou:
        print(f"  {RED + BOLD}Falharam:{RESET}  {RED}{_falhou:>2} / {total}{RESET}")
    print()
    if _falhou == 0:
        print(GREEN + BOLD + "  ✔  TODOS OS CRUDs FUNCIONANDO CORRETAMENTE!" + RESET)
    else:
        print(RED + BOLD + f"  ✘  {_falhou} verificação(ões) com falha — revisar acima." + RESET)
    print()
    print(DIM + "  Tecnologias: Flask 2.1 · SQLAlchemy 1.4 · Flask-JWT-Extended 4.7" + RESET)
    print(DIM + "  Arquitetura: Hexagonal (Ports & Adapters) · SQLite in-memory (demo)" + RESET)
    print()


if __name__ == "__main__":
    main()
