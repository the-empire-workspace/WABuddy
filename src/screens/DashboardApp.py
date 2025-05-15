from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDialog, QTableWidget, QTableWidgetItem, QProgressBar
from PyQt5.QtCore import QThreadPool, QTimer
from src.components.label import build_label
from src.components.text_input import build_text_input
from src.components.button import build_button
from src.utils.load_excel import load_excel, export_to_excel
from datetime import datetime, timedelta
from dotenv import load_dotenv
from src.bootstrap.whatsapp_worker import WhatsAppWorker
from src.screens.FacebookAuth import FacebookAuth
import random
import os
load_dotenv()


class DashboardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.widgets = []
        
        self.token = None
        self.facebook_auth = FacebookAuth(os.getenv("FACEBOOK_APP_ID"), os.getenv(
            "FACEBOOK_APP_SECRET"), "whatsapp_business_messaging,business_management", self.on_login_success)
        self.init_ui()
        self.add_widgets()
        self.thread_pool = QThreadPool()

    def init_ui(self):
        if self.token is None:
            self.facebook_auth.show()
        else:
            self.setWindowTitle("WABuddy")
            self.layout = QVBoxLayout()
            button_layout = QHBoxLayout()
            button_layout.setSpacing(10)
            label = build_label("Ingrese texto:")
            self.status_label = build_label("")
            self.widgets.append(label)

            self.text_input = build_text_input("")
            self.widgets.append(self.text_input)

            load_button = build_button("Cargar Excel", on_click=load_excel(self))

            start_button = build_button(
                "Iniciar", on_click=self.process_ia_response)
            button_layout.addWidget(load_button)
            button_layout.addWidget(start_button)
            self.widgets.append(self.status_label)
            self.layout.addLayout(button_layout)
            self.setLayout(self.layout)
            self.excel_data = None
            self.setFixedSize(600, 400)

    def process_ia_response(self):

        if self.excel_data is None:
            self.status_label.setText("No se ha cargado ningún archivo Excel")
            return

        text = self.text_input.toPlainText()

        if text == "":
            self.status_label.setText("No se ha ingresado ningún texto")
            return

        self.show_excel_data_dynamic()
        total_rows = len(self.excel_data)
        self.progress_bar.setMaximum(total_rows)
        self.progress_bar.setValue(0)
        self.progress_label.setText("Procesando...")

        self.current_progress = 0
        self.extra_time = 0

        current_time = datetime.now() + timedelta(minutes=3)

        for _, row in self.excel_data.iterrows():
            prompt = f'''
                
                Datos del usuario: 
                Nombre: {row["Nombre"]}
                DNI: {row["DNI"]}
                Telefono: {row["Telefono"]}
                Orden: {row["Orden"]}
                Grupo: {row["Grupo"]}
                
                Genera un mensaje utilizando el texto como base y sigue las siguientes instrucciones:
                - El mensaje debe ser preciso y directo.
                - El mensaje debe ser personalizado para el usuario.
                - No utilices el mismo mensaje para todos los usuarios.
                - Solo responde el mensaje, no agregues nada más.
                - Debe incluir el nombre del usuario en el mensaje.
                - Debe incluir el DNI del usuario en el mensaje.
                - Debe incluir la orden del usuario en el mensaje.
                - Debe incluir el grupo del usuario en el mensaje.

                Genera un mensaje único para el usuario basado en el texto ingresado, este texto puedes modificarlo para que sea más personalizado, solo responde el mensaje, no agregues nada más:
                {text}
            '''

            worker = WhatsAppWorker(row, prompt, self.update_progress(), self.token)

            self.thread_pool.start(worker)

            delay = random.randint(4, 10)
            current_time += timedelta(minutes=delay)

    def update_progress(self):
        def handle_result(row, response, whatsapp_active):
            def update_ui():
                index = self.table.rowCount()
                self.table.insertRow(index)
                self.table.setItem(index, 0, QTableWidgetItem(row["Nombre"]))
                self.table.setItem(index, 1, QTableWidgetItem(str(row["DNI"])))
                self.table.setItem(
                    index, 2, QTableWidgetItem(str(row["Telefono"])))
                self.table.setItem(index, 3, QTableWidgetItem(
                    'Activo' if whatsapp_active else 'Inactivo'))
                print(response)
                self.table.setItem(index, 4, QTableWidgetItem(response))
                self.table.setItem(index, 5, QTableWidgetItem(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                self.current_progress += 1
                self.progress_bar.setValue(self.current_progress)
                self.progress_label.setText(
                    f"Procesado: {row['Nombre']} ({row['Telefono']})")

                if self.current_progress == self.progress_bar.maximum():
                    self.progress_label.setText("Finalizado ✅")
            update_ui()
        return handle_result

    def show_excel_data_dynamic(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Vista de Datos Excel Dinámica")
        self.dialog_layout = QVBoxLayout()
        self.table = QTableWidget()

        self.table.setRowCount(0)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Nombre", "DNI", "Telefono", "Whatsapp Activo", "Mensaje enviado", "Fecha y hora"])
        self.table.setStyleSheet('width: 100%;')

        self.progress_label = build_label("Esperando inicio...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(0)

        self.dialog_layout.addWidget(self.progress_label)
        self.dialog_layout.addWidget(self.progress_bar)
        self.dialog_layout.addWidget(self.table)
        self.export_button = build_button(
            "Exportar a Excel", on_click=export_to_excel(self))
        self.dialog_layout.addWidget(self.export_button)
        self.dialog.setLayout(self.dialog_layout)
        self.dialog.setFixedSize(self.table.width() + 200, 400)
        self.dialog.show()

        self.row_index = 0

    def add_widgets(self):
        for widget in self.widgets:
            self.layout.addWidget(widget)

    def on_login_success(self, token):
        self.token = token
        print(self.token)
        self.facebook_auth.hide()
        self.init_ui()
        self.add_widgets()