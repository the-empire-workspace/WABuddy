
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QApplication
from PyQt5.QtCore import QThread
from src.bootstrap.facebook_worker import FacebookDeviceLoginWorker


class FacebookAuth(QMainWindow):
    def __init__(self, app_id, app_secret, scopes="whatsapp_business_messaging", on_login_success=None):
        super().__init__()
        self.setWindowTitle("Iniciar sesión con Facebook")
        self.app_id = app_id
        self.app_secret = app_secret
        self.scopes = scopes
        self.on_login_success = on_login_success

        self.label = QLabel("Solicitando código...")
        self.code_label = QLabel("")
        self.button = QPushButton("Reintentar")
        self.button.hide()
        self.copy_button = QPushButton("Copiar")
        self.copy_button.clicked.connect(self.copy_code_to_clipboard)


        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.code_label)
        layout.addWidget(self.button)
        layout.addWidget(self.copy_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.button.clicked.connect(self.start_login)
        self.start_login()

    def start_login(self):
        self.button.hide()
        self.label.setText("Solicitando código...")

        self.thread = QThread()
        self.worker = FacebookDeviceLoginWorker(
            self.app_id, self.app_secret, self.scopes)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.display_code.connect(self.update_ui_with_code)
        self.worker.finished.connect(self.login_successful)
        self.worker.error.connect(self.login_failed)

        self.thread.start()

    def update_ui_with_code(self, user_code, verification_uri):
        self.label.setText(
            f'Visita: <a href="{verification_uri}">{verification_uri}</a>')
        self.label.setOpenExternalLinks(True)

        self.code_label.setText(f"Código: {user_code}")
        
    def copy_code_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code_label.text().split(":")[1].strip())
        self.copy_button.setText("¡Copiado!")

    def login_successful(self, token_data):
        self.thread.quit()
        self.thread.wait()
        self.close()
        if self.on_login_success:
            self.on_login_success(token_data['access_token'])

    def login_failed(self, error_message):
        self.thread.quit()
        self.thread.wait()
        self.label.setText(f"Error: {error_message}")
        self.button.show()
