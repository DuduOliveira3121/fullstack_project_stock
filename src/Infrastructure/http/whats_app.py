import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv() # Carrega o .env

class Whatsapp:
    ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    FROM_WHATSAPP = "whatsapp:+55155238886"

    @staticmethod
    def send_message(phone, code):
        try:
            client = Client(Whatsapp.ACCOUNT_SID, Whatsapp.AUTH_TOKEN)
            
            # Limpa o número e garante o prefixo correto
            clean_phone = phone.strip().replace(" ", "")
            to_number = f"whatsapp:{clean_phone}"
            
            message = client.messages.create(
                from_=Whatsapp.FROM_WHATSAPP,
                body=f"Seu código de ativação fullstack Project: {code}",
                to=to_number
            )
            return {"success": True, "sid": message.sid}
        except Exception as e:
            # Lança a exceção para ser capturada pelo Service
            raise Exception(str(e))