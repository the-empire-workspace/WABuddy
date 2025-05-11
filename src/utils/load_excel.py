import pandas as pd
import os
from PyQt5.QtWidgets import QFileDialog, QWidget


def load_excel(object: QWidget):
    def load_excel_callback():
        file_path, _ = QFileDialog.getOpenFileName(
            object, "Seleccionar archivo Excel", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            object.status_label.setText("Cargando archivo...")
            try:
                object.excel_data = pd.read_excel(file_path)
                file_name = os.path.basename(file_path)
                object.status_label.setText(f"Archivo cargado: {file_name}")
            except Exception as e:
                object.status_label.setText(
                    f"Error al cargar el archivo: {str(e)}")
    return load_excel_callback


def export_to_excel(object: QWidget):
    def export_to_excel_callback():
        row_count = object.table.rowCount()
        col_count = object.table.columnCount()
        headers = [object.table.horizontalHeaderItem(
            col).text() for col in range(col_count)]

        data = []

        for row in range(row_count):
            data.append([
                object.table.item(row, col).text(
                ) if object.table.item(row, col) else ""
                for col in range(col_count)
            ])

        df = pd.DataFrame(data, columns=headers)

        file_path, _ = QFileDialog.getSaveFileName(
            object, "Guardar como", "", "Excel Files (*.xlsx);;All Files (*)"
        )

        if file_path:
            if not file_path.endswith(".xlsx"):
                file_path += ".xlsx"
            df.to_excel(file_path, index=False)
            object.status_label.setText(
                "Datos exportados a Excel exitosamente ✅")
    return export_to_excel_callback
