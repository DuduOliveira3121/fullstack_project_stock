from flask import current_app

from src.Application.Ports.WhatsappPort import WhatsappPort
from src.Infrastructure.http.whats_app import Whatsapp


class WhatsappAdapter(WhatsappPort):

    def send_verification_code(self, phone: str, code: str) -> bool:
        if current_app.config.get('DISABLE_WHATSAPP', False):
            print(f"⚠️ WhatsApp desabilitado; código {code} para {phone} não enviado")
            return True
        try:
            Whatsapp.send_message(phone, code)
            return True
        except Exception as e:
            raise Exception(f"Falha ao enviar código WhatsApp: {str(e)}")

    def send_message(self, phone: str, message: str) -> bool:
        if current_app.config.get('DISABLE_WHATSAPP', False):
            print(f"⚠️ WhatsApp desabilitado; mensagem para {phone} não enviada")
            return True
        try:
            Whatsapp.send_message(phone, message)
            return True
        except Exception as e:
            raise Exception(f"Falha ao enviar mensagem WhatsApp: {str(e)}")
