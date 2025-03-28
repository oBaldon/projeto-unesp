from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from core.allocation_solver import solve_allocation


class AlocacaoWindow(QWidget):
    """Tela de alocação (com pós-ajuste)."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Tela de Alocação")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Botão para executar alocação
        self.allocate_button = QPushButton("Executar Alocação")
        self.allocate_button.clicked.connect(self.run_allocation)
        self.layout.addWidget(self.allocate_button)

        # Tabela com resultados da alocação
        self.result_table = QTableWidget()
        self.result_table.setSortingEnabled(True)
        self.result_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.layout.addWidget(self.result_table)

        # Botão para exportar CSV
        self.export_button = QPushButton("Exportar Alocação para CSV")
        self.export_button.clicked.connect(self.export_csv)
        self.export_button.setEnabled(False)
        self.layout.addWidget(self.export_button)

        # Botão para voltar
        back_button = QPushButton("Voltar ao Menu")
        back_button.clicked.connect(self.return_to_menu)
        self.layout.addWidget(back_button)

    def run_allocation(self):
        """Executa a alocação e exibe os resultados."""
        alunos_data = self.parent.alunos_data
        projetos_data = self.parent.projetos_data

        if alunos_data is None or projetos_data is None:
            QMessageBox.warning(self, "Erro", "Importe os dados de alunos e projetos antes de continuar!")
            return

        try:
            allocation_result = solve_allocation(alunos_data, projetos_data)
            self.parent.alunos_info = allocation_result
            self.display_allocation(allocation_result)
            self.export_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro durante a alocação: {e}")

    def display_allocation(self, alunos_info):
        """Exibe os resultados com ComboBoxes para ajuste manual."""
        self.result_table.setRowCount(len(alunos_info))
        self.result_table.setColumnCount(len(alunos_info.columns))
        self.result_table.setHorizontalHeaderLabels(alunos_info.columns)

        # Lista de nomes de projetos
        projetos_nomes = (
            self.parent.projetos_data.iloc[:, 1].tolist()
            if self.parent.projetos_data is not None
            else []
        )

        for i, row in alunos_info.iterrows():
            for j, value in enumerate(row):
                column_name = alunos_info.columns[j]
                if column_name in ["Grupo", "Projeto", "Projeto 1", "Projeto 2"]:  # ajuste conforme necessário
                    combobox = QComboBox()
                    combobox.addItems([""] + projetos_nomes)
                    combobox.setCurrentText(str(value))
                    combobox.currentTextChanged.connect(
                        lambda text, row=i, col=j: self.update_allocation_data(text, row, col)
                    )
                    self.result_table.setCellWidget(i, j, combobox)
                else:
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.result_table.setItem(i, j, item)

    def update_allocation_data(self, text, row, col):
        """Atualiza o DataFrame global com alterações feitas nos ComboBoxes."""
        data = self.parent.alunos_info
        column_name = data.columns[col]
        data.at[row, column_name] = text
        self.parent.alunos_info = data

    def export_csv(self):
        """Abre um diálogo para salvar o arquivo CSV com os dados alocados."""
        try:
            path, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar Alocação como CSV",
                "alocacao_final.csv",
                "CSV Files (*.csv)"
            )
            if path:
                self.parent.alunos_info.to_csv(path, index=False)
                QMessageBox.information(self, "Exportação", f"Arquivo salvo com sucesso:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar CSV: {e}")

    def return_to_menu(self):
        """Retorna ao menu principal."""
        self.parent.show()
        self.close()
