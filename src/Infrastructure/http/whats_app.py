class Whatsapp:
    @staticmethod
    def send_message(phone, code):
        # Por enquanto, apenas retorna sucesso
        # TODO: Implementar integração real com Twilio (Arthur!!!)
        return {"success": True, "message": f"Código {code} seria enviado para {phone}"}
