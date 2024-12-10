import sys
from PyQt5.QtWidgets import QApplication
from gui import MenuWindow  # Importa a classe MenuWindow do pacote gui

def main():
    """Função principal para iniciar o aplicativo."""
    app = QApplication(sys.argv)
    window = MenuWindow()  # Cria a janela principal (MenuWindow)
    window.show()
    sys.exit(app.exec_())  # Executa o loop do aplicativo

if __name__ == "__main__":
    main()
