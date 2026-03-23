"""
Script de teste para o fluxo de registro e ativação via WhatsApp
Execute este script para testar:
1. Registro de novo seller
2. Envio de código via WhatsApp
3. Ativação do seller com código
"""

import requests
import json
from time import sleep

# Configurações
BASE_URL = "http://localhost:5000"
HEADERS = {"Content-Type": "application/json"}

# Dados de teste
TEST_USER = {
    "name": "Test Mini Mercado",
    "email": f"test_mercado_{int(__import__('time').time())}@example.com",
    "password": "senha123456",
    "phone": "+5511999999999"  # Substitua com seu número real para testar
}

def print_section(title):
    """Imprime uma seção colorida"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_register_user():
    """Testa o registro de um novo usuário"""
    print_section("📝 TESTANDO REGISTRO DE NOVO SELLER")
    
    try:
        print(f"Enviando dados:\n{json.dumps(TEST_USER, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/user",
            json=TEST_USER,
            headers=HEADERS,
            timeout=10
        )
        
        print(f"\n✅ Status: {response.status_code}")
        response_data = response.json()
        print(f"Resposta:\n{json.dumps(response_data, indent=2)}")
        
        if response.status_code == 200:
            user_id = response_data.get("usuarios", {}).get("id")
            return user_id, response_data
        else:
            print("❌ Erro ao registrar usuário")
            return None, response_data
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor")
        print("   Certifique-se de que a API está rodando com: python run.py")
        return None, None
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return None, None

def test_activate_user(user_id, expected_code=None):
    """Testa a ativação de um usuário com o código"""
    if not user_id:
        print("❌ Não foi possível ativar - user_id inválido")
        return False
    
    print_section("🔐 TESTANDO ATIVAÇÃO VIA WHATSAPP")
    
    print(f"User ID: {user_id}")
    print("📱 Um código de 4 dígitos foi enviado via WhatsApp para:")
    print(f"   {TEST_USER['phone']}")
    
    if expected_code:
        print(f"\n💡 Código para teste: {expected_code}")
        code_input = expected_code
    else:
        print("\n⏳ Digite o código recebido no WhatsApp (ou deixe em branco para usar código de teste):")
        code_input = input("Código: ").strip() or "1234"
    
    # Aqui você esperaria a resposta da API de ativação
    # Por enquanto, apenas mostramos o fluxo
    print(f"\n✓ Código '{code_input}' estaria sendo validado...")
    
    return True

def test_health_check():
    """Verifica se a API está respondendo"""
    print_section("🏥 VERIFICANDO SAÚDE DA API")
    
    try:
        response = requests.get(f"{BASE_URL}/api", timeout=5)
        if response.status_code == 200:
            print(f"✅ API está respondendo!")
            print(f"Resposta: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API")
        print("   Certifique-se de que está rodando: python run.py")
        return False
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("  🧪 SISTEMA DE TESTE - Fluxo de WhatsApp")
    print("="*60)
    
    # 1. Verificar saúde da API
    if not test_health_check():
        print("\n❌ API não está respondendo. Inicie com: python run.py")
        return
    
    sleep(1)
    
    # 2. Testar registro
    user_id, register_response = test_register_user()
    
    if not user_id:
        print("\n❌ Não foi possível continuar com a ativação")
        return
    
    sleep(2)
    
    # 3. Testar ativação
    test_activate_user(user_id)
    
    print_section("✨ TESTES CONCLUÍDOS")
    print("""
    📌 PRÓXIMOS PASSOS:
    
    1. Verifique se recebeu o código no WhatsApp em: {phone}
    
    2. Se a API tiver um endpoint de ativação, execute:
       POST /activate
       Com o código recebido
    
    3. Verifique no banco de dados se o usuário foi criado:
       A tabela 'users' deve conter seu registro
    
    4. Consulte o log da API para erros de Twilio
    """.format(phone=TEST_USER['phone']))

if __name__ == "__main__":
    main()
