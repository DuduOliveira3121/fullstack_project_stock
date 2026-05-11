"""
Script de teste do fluxo completo: Criar Seller -> Receber Código via Twilio -> Ativar Seller
Execute com: python test_fluxo_vendedor.py
"""

import requests
import json
from time import sleep

# Configurações
BASE_URL = "http://localhost:5000"
HEADERS = {"Content-Type": "application/json"}

# Dados de teste - SUBSTITUA com um número de telefone REAL ou use sandbox do Twilio
TEST_USER = {
    "nome": "Mini Mercado 2025",
    "cnpj": "13.421.678/0001-90",
    "email": f"vendedor_{int(__import__('time').time())}@example.com",
    "senha": "SenhaForte!",
    "celular": "+5511960708710"  # 🔴 SUBSTITUA COM SEU NÚMERO
}

def print_step(number, title):
    """Imprime um passo numerado"""
    print(f"\n{'='*70}")
    print(f"  PASSO {number}: {title}")
    print(f"{'='*70}\n")

def print_success(msg):
    """Imprime mensagem de sucesso"""
    print(f"✅ {msg}")

def print_error(msg):
    """Imprime mensagem de erro"""
    print(f"❌ {msg}")

def print_info(msg):
    """Imprime mensagem informativa"""
    print(f"ℹ️  {msg}")

# ==================== PASSO 1: VERIFICAR API ====================
def passo_1_verificar_api():
    print_step(1, "VERIFICANDO SE API ESTÁ RODANDO")
    
    try:
        response = requests.get(f"{BASE_URL}/api", timeout=5)
        if response.status_code == 200:
            print_success("API está em execução!")
            print(f"   Resposta: {response.json()['mensagem']}")
            return True
        else:
            print_error(f"API retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Não conseguiu conectar à API")
        print_info("Inicie a API com: python run.py")
        return False
    except Exception as e:
        print_error(f"Erro: {str(e)}")
        return False

# ==================== PASSO 2: CRIAR SELLER ====================
def passo_2_criar_seller():
    print_step(2, "CRIANDO NOVO SELLER")
    
    print_info("Dados do novo seller:")
    for chave, valor in TEST_USER.items():
        if chave == "celular":
            print(f"   • {chave}: {valor}")
            print_info("⚠️  IMPORTANTE: Este é o número que receberá o código Twilio!")
        elif chave != "senha":
            print(f"   • {chave}: {valor}")
    
    try:
        print_info("\nEnviando requisição POST /api/sellers...")
        response = requests.post(
            f"{BASE_URL}/api/sellers",
            json=TEST_USER,
            headers=HEADERS,
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        response_data = response.json()
        
        if response.status_code == 200:
            print_success("Seller criado com sucesso!")
            user_id = response_data.get("usuario", {}).get("id")
            print_info(f"ID do novo seller: {user_id}")
            print_info(f"Email: {response_data.get('usuario', {}).get('email')}")
            print_info(f"CNPJ: {response_data.get('usuario', {}).get('cnpj')}")
            
            print_info("\n📱 Um código de 4 dígitos foi ENVIADO via WhatsApp!")
            print_info(f"   Destino: {TEST_USER['celular']}")
            print_info("   Você receberá uma mensagem do Twilio nos próximos segundos")
            
            return user_id
        else:
            print_error(f"Erro ao criar seller: {response_data.get('erro')}")
            return None
            
    except requests.exceptions.ConnectionError:
        print_error("Não conseguiu conectar à API em /api/sellers")
        return None
    except Exception as e:
        print_error(f"Erro: {str(e)}")
        return None

# ==================== PASSO 3: AGUARDAR E OBTER CÓDIGO ====================
def passo_3_obter_codigo():
    print_step(3, "AGUARDANDO CÓDIGO TWILIO")
    
    print_info("As opções são:")
    print("   a) Aguardar mensagem WhatsApp (recomendado)")
    print("   b) Digitar o código manualmente")
    print("   c) Usar código de teste")
    
    escolha = input("\nEscolha (a/b/c): ").strip().lower()
    
    if escolha == "a":
        print_info("Aguardando mensagem WhatsApp... (timeout: 60 segundos)")
        print("   Você receberá uma mensagem como:")
        print("   'Seu codigo de ativacao Stock Project: 5427'")
        
        # Simular teste
        for i in range(6):
            print(".", end="", flush=True)
            sleep(10)
        print("\n")
        print_info("⏰ Tempo limite atingido. Por favor, use a opção 'b' para digitar manualmente")
        return passo_3_obter_codigo()
    
    elif escolha == "b":
        codigo = input("   Digite o código de 4 dígitos: ").strip()
        if len(codigo) == 4 and codigo.isdigit():
            print_success(f"Código registrado: {codigo}")
            return codigo
        else:
            print_error("Código deve ter exatamente 4 dígitos!")
            return passo_3_obter_codigo()
    
    elif escolha == "c":
        print_info("⚠️  Usando código de teste '1234'")
        print_info("   (Só funciona se o banco de dados contiver este código)")
        return "1234"
    
    else:
        print_error("Opção inválida!")
        return passo_3_obter_codigo()

# ==================== PASSO 4: ATIVAR SELLER ====================
def passo_4_ativar_seller(codigo):
    print_step(4, "ATIVANDO SELLER COM CÓDIGO")
    
    payload = {
        "celular": TEST_USER["celular"],
        "codigo": codigo
    }
    
    print_info(f"Enviando requisição POST /api/sellers/activate")
    print_info(f"   celular: {TEST_USER['celular']}")
    print_info(f"   codigo: {codigo}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/sellers/activate",
            json=payload,
            headers=HEADERS,
            timeout=10
        )
        
        print(f"\nStatus: {response.status_code}")
        response_data = response.json()
        
        if response.status_code == 200:
            print_success("Seller ATIVADO COM SUCESSO! ✨")
            print_info(f"Mensagem: {response_data.get('mensagem')}")
            return True
        else:
            print_error(f"Falha na ativação: {response_data.get('erro')}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Não conseguiu conectar à API em /api/sellers/activate")
        return False
    except Exception as e:
        print_error(f"Erro: {str(e)}")
        return False

# ==================== MAIN ====================
def main():
    print("\n" + "="*70)
    print("  🎯 TESTE COMPLETO: CRIAR E ATIVAR SELLER VIA TWILIO")
    print("="*70)
    
    print(f"\n📋 Resumo do fluxo:")
    print(f"   1️⃣  Verificar se API está rodando")
    print(f"   2️⃣  Criar novo seller (POST /api/sellers)")
    print(f"   3️⃣  Código é enviado via WhatsApp (Twilio)")
    print(f"   4️⃣  Ativar seller com código (POST /api/sellers/activate)")
    
    # PASSO 1
    if not passo_1_verificar_api():
        print_error("\n❌ Teste abortado. Inicie a API com: python run.py")
        return
    
    sleep(2)
    
    # PASSO 2
    seller_id = passo_2_criar_seller()
    if not seller_id:
        print_error("\n❌ Teste abortado. Não foi possível criar seller.")
        return
    
    sleep(3)
    
    # PASSO 3
    codigo = passo_3_obter_codigo()
    if not codigo:
        print_error("\n❌ Teste abortado. Código não fornecido.")
        return
    
    sleep(1)
    
    # PASSO 4
    sucesso = passo_4_ativar_seller(codigo)
    
    if sucesso:
        # PASSO 5: Teste de autenticação JWT conforme README
        print_info("\n🔐 Iniciando teste de autenticação JWT...")
        jwt_token = passo_5_testar_login_jwt()
    else:
        jwt_token = None

    # RESULTADO FINAL
    print_step("RESUMO", "RESULTADO FINAL")
    
    if sucesso and jwt_token:
        print_success("✨ FLUXO COMPLETO FINALIZADO COM SUCESSO! ✨")
        print("\n📊 Resumo:")
        print(f"   • Seller criado: {TEST_USER['email']}")
        print(f"   • CNPJ: {TEST_USER['cnpj']}")
        print(f"   • Celular: {TEST_USER['celular']}")
        print(f"   • Código recebido: {codigo}")
        print(f"   • Status: ATIVADO")
        print(f"   • JWT Token: {jwt_token[:30]}...")
    elif sucesso:
        print_error("🚨 Seller ativado, mas falha no login JWT")
    else:
        print_error("Teste finalizado com erro na ativação")
    
    print("\n" + "="*70)

# ==================== PASSO 5: TESTAR LOGIN JWT APÓS ATIVAÇÃO ====================
def passo_5_testar_login_jwt():
    print_step(5, "TESTANDO LOGIN JWT (USUÁRIO ATIVADO)")

    payload = {
        "email": TEST_USER["email"],
        "senha": TEST_USER["senha"]
    }

    print_info("Tentando obter token JWT via /api/auth/login...")

    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=payload,
            headers=HEADERS,
            timeout=10
        )

        print(f"Status: {response.status_code}")
        response_data = response.json()

        if response.status_code == 200:
            print_success("✅ Login JWT bem-sucedido!")
            token = response_data.get('token')
            if token:
                print_info(f"Token JWT: {token[:30]}...")
                return token
            else:
                print_error("❌ Nenhum token JWT retornado")
                return None
        else:
            print_error(f"❌ Falha no login JWT: {response_data.get('erro')}")
            return None

    except requests.exceptions.ConnectionError:
        print_error("Não conseguiu conectar à API em /api/auth/login para JWT")
        return None
    except Exception as e:
        print_error(f"Erro: {str(e)}")
        return None

if __name__ == "__main__":
    main()
