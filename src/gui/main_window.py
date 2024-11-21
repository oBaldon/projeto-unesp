# PyQt main window code will go here    
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QFileDialog
)
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projeto UNESP - Alocação de Alunos")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Botão para carregar arquivos
        self.load_button = QPushButton("Carregar Dados")
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)

        # Tabela para exibir dados
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

    def load_data(self):
        # Abre um diálogo para selecionar o arquivo
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecione um arquivo CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.display_data(file_path)

    def display_data(self, file_path):
        try:
            # Carrega os dados do CSV
            data = pd.read_csv(file_path)

            # Configura a tabela com os dados
            self.table.setRowCount(len(data))
            self.table.setColumnCount(len(data.columns))
            self.table.setHorizontalHeaderLabels(data.columns)

            for i, row in data.iterrows():
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
