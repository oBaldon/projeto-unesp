from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from core.allocation_solver import solve_allocation


class AlocacaoWindow(QWidget):
    """Tela de alocação."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Tela de Alocação")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Botão para realizar a alocação
        self.allocate_button = QPushButton("Executar Alocação")
        self.allocate_button.clicked.connect(self.run_allocation)
        self.layout.addWidget(self.allocate_button)

        # Tabela para exibir o resultado da alocação
        self.result_table = QTableWidget()
        self.result_table.setSortingEnabled(True)  # Habilita ordenação por colunas
        self.result_table.setSelectionBehavior(QTableWidget.SelectRows)  # Seleção de linhas completas
        self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Bloqueia edição
        self.layout.addWidget(self.result_table)

        # Botão para voltar ao menu
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
            # Chama o solver para realizar a alocação
            allocation_result = solve_allocation(alunos_data, projetos_data)

            # Atualiza os dados de alunos com os resultados da alocação
            self.parent.alunos_info = allocation_result

            # Exibe os dados atualizados na tabela
            self.display_allocation(allocation_result)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro durante a alocação: {e}")

    def display_allocation(self, alunos_info):
        """Exibe os resultados da alocação na tabela."""
        self.result_table.setRowCount(len(alunos_info))
        self.result_table.setColumnCount(len(alunos_info.columns))
        self.result_table.setHorizontalHeaderLabels(alunos_info.columns)

        for i, row in alunos_info.iterrows():
            for j, value in enumerate(row):
                self.result_table.setItem(i, j, QTableWidgetItem(str(value)))

    def return_to_menu(self):
        """Retorna para o menu principal."""
        self.parent.show()
        self.close()
