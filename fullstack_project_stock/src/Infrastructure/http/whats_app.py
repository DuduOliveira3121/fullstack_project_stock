import os
from twilio.rest import Client

class Whatsapp:
    # Pega das variáveis de ambiente do seu PC ou servidor
    ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    FROM_WHATSAPP = "whatsapp:+14155238886"

    @staticmethod
    def send_message(phone, code):
        try:
            client = Client(Whatsapp.ACCOUNT_SID, Whatsapp.AUTH_TOKEN)
            clean_phone = phone.strip().replace(" ", "")
            message = client.messages.create(
                from_=Whatsapp.FROM_WHATSAPP,
                body=f"Seu codigo de ativacao Stock Project: {code}",
                to=f"whatsapp:{clean_phone}"
            )
            return {"success": True, "sid": message.sid}
        except Exception as e:
            raise Exception(f"Erro Twilio: {str(e)}")