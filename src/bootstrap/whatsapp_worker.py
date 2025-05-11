from PyQt5.QtCore import QRunnable, pyqtSlot
import pywhatkit
from datetime import datetime
import random
from src.bootstrap.open_ai import OpenAIDriver

class WhatsAppWorker(QRunnable):
    def __init__(self, row, prompt, callback, send_time):
        super().__init__()
        self.row = row
        self.prompt = prompt
        self.openai = OpenAIDriver()
        self.callback = callback
        self.send_time = send_time

    @pyqtSlot()
    def run(self):
        response = self.openai.get_response(self.prompt)
        whatsapp_active = False
        
        random_time = random.randint(10, 15)
        extra_hours = self.send_time[0]
        extra_minutes = self.send_time[1]
        try:
            print(f"Enviando mensaje a {self.row['Telefono']} en {self.send_time[0]}:{self.send_time[1]}")
            
            pywhatkit.sendwhatmsg(
                f"+{str(self.row['Telefono'])}",
                response,
                extra_hours,
                extra_minutes,
                random_time,
                True,
                5
            )
            whatsapp_active = True
        except Exception as e:
            print(f"Error enviando mensaje: {e}")

        self.callback(self.row, response, whatsapp_active)
