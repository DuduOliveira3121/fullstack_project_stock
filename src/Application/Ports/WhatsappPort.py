from abc import ABC, abstractmethod


class WhatsappPort(ABC):

    @abstractmethod
    def send_verification_code(self, phone: str, code: str) -> bool:
        pass

    @abstractmethod
    def send_message(self, phone: str, message: str) -> bool:
        pass
