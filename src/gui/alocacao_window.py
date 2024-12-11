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
        self.layout.addWidget(self.result_table)

        # Botão para voltar ao menu
        back_button = QPushButton("Voltar ao Menu")
        back_button.clicked.connect(self.return_to_menu)
        self.layout.addWidget(back_button)

    def run_allocation(self):
        alunos_data = self.parent.alunos_data
        projetos_data = self.parent.projetos_data

        if alunos_data is None or projetos_data is None:
            QMessageBox.warning(self, "Erro", "Importe os dados de alunos e projetos antes de continuar!")
            return

        # Executar o solver
        allocation = solve_allocation(alunos_data, projetos_data)

        # Exibir o resultado na tabela
        self.result_table.setRowCount(len(allocation))
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(["Aluno", "Projetos Alocados"])

        for i, (aluno, projetos) in enumerate(allocation):
            self.result_table.setItem(i, 0, QTableWidgetItem(aluno))
            self.result_table.setItem(i, 1, QTableWidgetItem(", ".join(projetos)))

    def return_to_menu(self):
        """Retorna para o menu principal."""
        self.parent.show()
        self.close()
