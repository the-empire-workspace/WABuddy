from PyQt5.QtCore import pyqtSignal, QObject
import requests
import time


class FacebookDeviceLoginWorker(QObject):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    display_code = pyqtSignal(str, str)

    def __init__(self, app_id, app_secret, scopes):
        super().__init__()
        self.app_id = app_id
        self.app_secret = app_secret
        self.scopes = scopes
        self.interval = 5
        self.code = None

    def run(self):
        try:
            response = requests.post("https://graph.facebook.com/v17.0/device/login", data={
                "access_token": f"{self.app_id}|{self.app_secret}",
                "scope": self.scopes
            })
            data = response.json()

            if "error" in data:
                self.error.emit("Error al solicitar código.")
                return

            self.code = data["code"]
            user_code = data["user_code"]
            verification_uri = data["verification_uri"]
            self.interval = data["interval"]
            self.display_code.emit(user_code, verification_uri)

            # Poll para el token
            while True:
                resp = requests.post("https://graph.facebook.com/v17.0/device/login_status", data={
                    "access_token": f"{self.app_id}|{self.app_secret}",
                    "code": self.code
                })
                result = resp.json()

                if "access_token" in result:
                    self.finished.emit(result)
                    return

                error_code = result.get("error", {}).get("code")

                if error_code == 1349172:  # authorization_pending
                    time.sleep(self.interval)
                    continue
                elif error_code == 31:  # slow_down
                    time.sleep(self.interval)
                elif error_code == 1349173:  # slow_down
                    self.interval += 5
                    time.sleep(self.interval)
                    continue
                elif error_code == 1349152:  # authorization_declined
                    self.error.emit("El usuario rechazó el acceso.")
                    return
                elif error_code == 1349153:  # code_expired
                    self.error.emit("El código expiró. Por favor, reintenta.")
                    return
                else:
                    self.error.emit(result.get("error", {}).get(
                        "message", "Error desconocido"))
                    return
        except Exception as e:
            self.error.emit(str(e))
