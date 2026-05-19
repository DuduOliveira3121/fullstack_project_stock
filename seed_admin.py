"""
Cria usuários de exemplo no banco de dados (admin + vendedores).
Execute: python seed_admin.py
"""

from werkzeug.security import generate_password_hash
from run import create_app
from src.config.data_base import db
from src.Infrastructure.Model.user import User

# ── Usuários a criar ──────────────────────────────────────
USUARIOS = [
    {
        "nome":    "Administrador",
        "email":   "admin@estoque.com",
        "senha":   "Admin@2025",
        "cnpj":    "00.000.000/0001-00",
        "celular": "+5511900000000",
    },
    {
        "nome":    "Carlos Vendedor",
        "email":   "carlos@estoque.com",
        "senha":   "Carlos@2025",
        "cnpj":    "11.111.111/0001-11",
        "celular": "+5511911111111",
    },
    {
        "nome":    "Maria Vendedora",
        "email":   "maria@estoque.com",
        "senha":   "Maria@2025",
        "cnpj":    "22.222.222/0001-22",
        "celular": "+5511922222222",
    },
]
# ─────────────────────────────────────────────────────────

app = create_app({"DISABLE_WHATSAPP": True})

with app.app_context():
    print()
    for u in USUARIOS:
        existente = User.query.filter_by(email=u["email"]).first()
        if existente:
            print(f"  ✔  Já existe  →  {u['email']}")
        else:
            novo = User(
                name=u["nome"],
                email=u["email"],
                password=generate_password_hash(u["senha"]),
                cnpj=u["cnpj"],
                phone=u["celular"],
                is_verified=True,
                code=None,
            )
            db.session.add(novo)
            db.session.commit()
            print(f"  ✔  Criado  →  {u['email']}  |  senha: {u['senha']}  |  id: {novo.id}")
    print()
