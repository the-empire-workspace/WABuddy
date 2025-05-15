from PyQt5.QtCore import QRunnable, pyqtSlot
from src.bootstrap.open_ai import OpenAIDriver
import os
import requests
from src.utils.generate_appsecret_proof import generate_appsecret_proof

class WhatsAppWorker(QRunnable):
    def __init__(self, row, prompt, callback, token):
        super().__init__()

        self.url = os.getenv("WHATSAPP_API")
        self.phone_id = os.getenv("WHATSAPP_PHONE_ID")
        self.row = row
        self.token = token
        self.prompt = prompt
        self.openai = OpenAIDriver()
        self.callback = callback

    @pyqtSlot()
    def run(self):
        message = self.openai.get_response(self.prompt)
        whatsapp_active = False

        try:
            print(f"Enviando mensaje a {self.row['Telefono']}")

            url = f"{self.url}{self.phone_id}/messages"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }

            data = {
                "messaging_product": "whatsapp",
                "to": f"{str(self.row['Telefono'])}",
                "type": "text",
                "text": {
                    "body": message
                }
            }
            appsecret_proof = generate_appsecret_proof(self.token)
            response = requests.post(f"{url}?appsecret_proof={appsecret_proof}", headers=headers, json=data)
            response.raise_for_status()
            whatsapp_active = True
        except Exception as e:
            print(f"Error enviando mensaje: {e}")

        self.callback(self.row, message, whatsapp_active)
