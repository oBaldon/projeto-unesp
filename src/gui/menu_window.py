from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from .alunos_window import AlunosWindow
from .projetos_window import ProjetosWindow
from .alocacao_window import AlocacaoWindow


class MenuWindow(QWidget):
    """Tela inicial do menu principal."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projeto UNESP - Menu Principal")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Label de título
        title = QLabel("Menu Principal")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Botões
        self.alunos_button = QPushButton("Alunos")
        self.alunos_button.clicked.connect(self.open_alunos_screen)
        layout.addWidget(self.alunos_button)

        self.projetos_button = QPushButton("Projetos")
        self.projetos_button.clicked.connect(self.open_projetos_screen)
        layout.addWidget(self.projetos_button)

        self.alocacao_button = QPushButton("Alocação")
        self.alocacao_button.setEnabled(False)  # Inicialmente desabilitado
        self.alocacao_button.clicked.connect(self.open_alocacao_screen)
        layout.addWidget(self.alocacao_button)

        # Configurar layout
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        # Variáveis de estado
        self.alunos_data = None
        self.projetos_data = None
        
    def enable_alocacao_button(self):
        """Habilita o botão de alocação se os dados de alunos e projetos forem importados."""
        if self.alunos_data is not None and self.projetos_data is not None:
            self.alocacao_button.setEnabled(True)

    def open_alunos_screen(self):
        """Abre a tela de alunos."""
        self.alunos_window = AlunosWindow(self)
        self.alunos_window.show()
        self.hide()

    def open_projetos_screen(self):
        """Abre a tela de projetos."""
        self.projetos_window = ProjetosWindow(self)
        self.projetos_window.show()
        self.hide()

    def open_alocacao_screen(self):
        """Abre a tela de alocação."""
        self.alocacao_window = AlocacaoWindow(self)
        self.alocacao_window.show()
        self.hide()

