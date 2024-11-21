import sys
from PyQt5.QtWidgets import QApplication, QLabel

# Criação da aplicação
app = QApplication(sys.argv)

# Janela simples
label = QLabel("PyQt5 instalado com sucesso!")
label.show()

# Executa o evento
sys.exit(app.exec_())
