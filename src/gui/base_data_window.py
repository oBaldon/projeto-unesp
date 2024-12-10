import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt


class BaseDataWindow(QWidget):
    """Classe base para telas de gerenciamento de dados."""
    
    def __init__(self, parent, title, data_attr):
        super().__init__()
        self.parent = parent
        self.setWindowTitle(title)
        self.data_attr = data_attr
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Botão para importar dados
        self.import_button = QPushButton(f"Importar Dados de {title}")
        self.import_button.clicked.connect(self.import_data)
        layout.addWidget(self.import_button)

        # Tabela para exibir os dados
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)  # Habilita a ordenação por colunas
        self.table.setSelectionBehavior(QTableWidget.SelectItems)  # Seleção de células individuais
        self.table.itemSelectionChanged.connect(self.highlight_row)  # Destaca a linha ao selecionar
        self.table.setEditTriggers(QTableWidget.DoubleClicked)  # Permite edição ao dar um duplo clique
        self.table.itemChanged.connect(self.update_data)  # Captura alterações nas células
        layout.addWidget(self.table)

        # Preencher a tabela se os dados já foram importados
        data = getattr(self.parent, self.data_attr, None)
        if data is not None:
            self.display_data(data)

        # Botão para voltar ao menu
        self.back_button = QPushButton("Voltar ao Menu")
        self.back_button.clicked.connect(self.return_to_menu)
        layout.addWidget(self.back_button)

    def import_data(self):
        """Importa os dados de um arquivo CSV e exibe na tabela."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecione o arquivo CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                data = pd.read_csv(file_path)
                setattr(self.parent, self.data_attr, data)  # Armazena os dados no MenuWindow
                self.display_data(data)
                self.parent.enable_alocacao_button()
                QMessageBox.information(self, "Sucesso", "Dados importados com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao importar dados: {e}")

    def display_data(self, data):
        """Exibe os dados importados na tabela."""
        # Atualiza a tabela com o número de linhas e colunas do DataFrame
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data.columns))
        self.table.setHorizontalHeaderLabels(data.columns)

        # Preenche a tabela com os dados
        for i, row in data.iterrows():
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def highlight_row(self):
        """Destaca a linha correspondente à célula selecionada."""
        # Remove destaque de todas as linhas
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                if item:
                    item.setBackground(Qt.white)

        # Adiciona destaque à linha selecionada
        for item in self.table.selectedItems():
            row = item.row()
            for col in range(self.table.columnCount()):
                cell = self.table.item(row, col)
                if cell:
                    cell.setBackground(Qt.lightGray)

    def update_data(self, item):
        """Atualiza os dados na variável associada ao modificar uma célula."""
        data = getattr(self.parent, self.data_attr, None)
        if data is not None:
            row = item.row()
            column = item.column()
            column_name = data.columns[column]
            column_dtype = data[column_name].dtype

            try:
                # Converte o valor para o tipo adequado antes de atualizar
                if pd.api.types.is_integer_dtype(column_dtype):
                    value = int(item.text())
                elif pd.api.types.is_float_dtype(column_dtype):
                    value = float(item.text())
                else:
                    value = item.text()

                # Atualiza o DataFrame
                data.at[row, column_name] = value
                setattr(self.parent, self.data_attr, data)
            except ValueError:
                QMessageBox.critical(
                    self,
                    "Erro de Tipo",
                    f"Não foi possível converter '{item.text()}' para o tipo {column_dtype}."
                )
                # Restaura o valor original na tabela
                self.table.blockSignals(True)  # Evita loop de sinais
                self.table.setItem(row, column, QTableWidgetItem(str(data.at[row, column_name])))
                self.table.blockSignals(False)

    def return_to_menu(self):
        """Retorna para o menu principal."""
        self.parent.show()
        self.close()
