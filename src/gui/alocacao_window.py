from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class AlocacaoWindow(QWidget):
    """Tela de alocação."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Tela de Alocação")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Mensagem inicial
        label = QLabel("Processo de alocação.")
        layout.addWidget(label)

        # Botão para voltar ao menu
        back_button = QPushButton("Voltar ao Menu")
        back_button.clicked.connect(self.return_to_menu)
        layout.addWidget(back_button)

    def return_to_menu(self):
        """Retorna para o menu principal."""
        self.parent.show()
        self.close()
