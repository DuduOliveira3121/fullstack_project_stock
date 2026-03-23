"""
Script de teste da integração Twilio
Valida:
1. Credenciais Twilio
2. Conexão com API Twilio
3. Envio de mensagem WhatsApp
"""

import os
import sys
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

def print_header(text):
    """Imprime cabeçalho formatado"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def test_env_variables():
    """Verifica se as variáveis de ambiente estão configuradas"""
    print_header("VALIDANDO VARIÁVEIS DE AMBIENTE")
    
    errors = []
    
    if not TWILIO_ACCOUNT_SID or TWILIO_ACCOUNT_SID == "your_account_sid_here":
        errors.append("[ERRO] TWILIO_ACCOUNT_SID não configurado")
    else:
        print(f"[OK] TWILIO_ACCOUNT_SID: {TWILIO_ACCOUNT_SID[:10]}...***")
    
    if not TWILIO_AUTH_TOKEN or TWILIO_AUTH_TOKEN == "your_auth_token_here":
        errors.append("[ERRO] TWILIO_AUTH_TOKEN não configurado")
    else:
        print(f"[OK] TWILIO_AUTH_TOKEN: ***{TWILIO_AUTH_TOKEN[-4:]}")
    
    if errors:
        print("\n" + "\n".join(errors))
        return False
    
    return True

def test_twilio_connection():
    """Testa a conexão com Twilio"""
    print_header("TESTANDO CONEXAO COM TWILIO")
    
    try:
        from twilio.rest import Client
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Tenta fazer uma chamada simples para validar credenciais
        account_info = client.api.accounts(TWILIO_ACCOUNT_SID).fetch()
        
        print("[SUCESSO] Conexao com Twilio estabelecida!")
        print(f"Nome da Conta: {account_info.friendly_name}")
        print(f"Status: {account_info.status}")
        
        return True
        
    except ImportError:
        print("[ERRO] Biblioteca 'twilio' nao esta instalada")
        print("Execute: pip install twilio")
        return False
    except Exception as e:
        print(f"[ERRO] Falha ao conectar com Twilio: {str(e)}")
        return False

def test_send_message(phone_number):
    """Testa o envio de uma mensagem WhatsApp"""
    print_header("TESTANDO ENVIO DE MENSAGEM WHATSAPP")
    
    if not phone_number:
        print("[ERRO] Numero de telefone nao fornecido")
        return False
    
    try:
        from twilio.rest import Client
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Numero de teste Twilio (sandbox)
        FROM_WHATSAPP = "whatsapp:+14155238886"
        to_number = f"whatsapp:{phone_number.strip()}"
        
        print("Enviando mensagem de teste...")
        print(f"De: {FROM_WHATSAPP}")
        print(f"Para: {to_number}")
        
        message = client.messages.create(
            from_=FROM_WHATSAPP,
            body="Teste de integracao Twilio - Fullstack Project Stock",
            to=to_number
        )
        
        print("\n[SUCESSO] Mensagem enviada com sucesso!")
        print(f"Message SID: {message.sid}")
        print(f"Status: {message.status}")
        
        return True
        
    except Exception as e:
        print(f"[ERRO] Falha ao enviar mensagem: {str(e)}")
        return False

def test_generate_code():
    """Testa a geracao de codigo aleatorio"""
    print_header("TESTANDO GERACAO DE CODIGO")
    
    import random
    
    codes = [random.randint(1000, 9999) for _ in range(5)]
    print("5 codigos gerados (exemplo):")
    for code in codes:
        print(f"  - {code}")
    
    return True

def main():
    """Executa todos os testes"""
    print("\n" + "="*70)
    print("  SISTEMA DE TESTES - INTEGRACAO TWILIO")
    print("="*70)
    
    all_passed = True
    
    # Teste 1: Variáveis de ambiente
    if not test_env_variables():
        print("\n[AVISO] Configure as credenciais Twilio no arquivo .env")
        print("   Obtenha em: https://www.twilio.com/console")
        all_passed = False
        
        print_header("COMO CONFIGURAR")
        print("""
1. Acesse https://www.twilio.com/console
2. Copie seu Account SID
3. Copie seu Auth Token
4. Edite o arquivo .env:
   
   TWILIO_ACCOUNT_SID=seu_account_sid_aqui
   TWILIO_AUTH_TOKEN=seu_auth_token_aqui

5. Execute novamente este script
        """)
        return
    
    # Teste 2: Conexao Twilio
    if not test_twilio_connection():
        all_passed = False
    
    # Teste 3: Geracao de codigo
    if not test_generate_code():
        all_passed = False
    
    # Teste 4: Envio de mensagem (opcional)
    print_header("TESTE DE ENVIO (OPCIONAL)")
    phone = input("Digite seu numero de WhatsApp com codigo de pais (ex: +55119999999999)\nOu pressione Enter para pular: ").strip()
    
    if phone and len(phone) >= 10:
        test_send_message(phone)
    else:
        print("[INFO] Teste de envio pulado")
    
    # Resumo final
    print_header("RESUMO DOS TESTES")
    
    if all_passed:
        print("[SUCESSO] TODOS OS TESTES PASSARAM!")
        print("\n- Seu ambiente esta pronto para usar Twilio")
        print("- Execute 'python run.py' para iniciar o servidor")
    else:
        print("[AVISO] Alguns testes falharam - verifique as instrucoes acima")

if __name__ == "__main__":
    main()
