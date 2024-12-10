import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox,
    QTableWidget, QTableWidgetItem, QFileDialog
)
from PyQt5.QtCore import Qt
import pandas as pd


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
        data = getattr(self.parent, self.data_attr)
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
                self.display_data(data)
                setattr(self.parent, self.data_attr, data)  # Armazena os dados no MenuWindow
                self.parent.enable_alocacao_button()
                QMessageBox.information(self, "Sucesso", f"Dados importados com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao importar dados: {e}")

    def display_data(self, data):
        """Exibe os dados importados na tabela."""
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data.columns))
        self.table.setHorizontalHeaderLabels(data.columns)

        for i, row in data.iterrows():
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def highlight_row(self):
        """Destaca a linha correspondente à célula selecionada."""
        for i in range(self.table.rowCount()):
            # Remove o estilo de todas as linhas
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                if item:
                    item.setBackground(Qt.white)

        for item in self.table.selectedItems():
            row = item.row()
            for col in range(self.table.columnCount()):
                cell = self.table.item(row, col)
                if cell:
                    cell.setBackground(Qt.lightGray)

    def update_data(self, item):
        """Atualiza os dados na variável associada ao modificar uma célula."""
        # Obtém os dados atuais
        data = getattr(self.parent, self.data_attr)
        if data is not None:
            # Identifica a célula que foi modificada
            row = item.row()
            column = item.column()
            column_name = data.columns[column]

            # Obtém o tipo original da coluna
            column_dtype = data[column_name].dtype

            # Converte o valor editado para o tipo correto
            try:
                if pd.api.types.is_integer_dtype(column_dtype):
                    value = int(item.text())
                elif pd.api.types.is_float_dtype(column_dtype):
                    value = float(item.text())
                else:
                    value = item.text()  # Mantém como string para outros tipos

                # Atualiza o DataFrame
                data.at[row, column_name] = value

                # Atualiza a variável associada no MenuWindow
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


class AlunosWindow(BaseDataWindow):
    """Tela de gerenciamento de alunos."""
    def __init__(self, parent):
        super().__init__(parent, "Alunos", "alunos_data")

    def update_table_for_projects(self):
        """Habilita as colunas 'Projeto 1' e 'Projeto 2' com base no valor da quarta coluna."""
        for row in range(self.table.rowCount()):
            # Obtém o valor da quarta coluna (índice 3)
            projetos_count = int(self.table.item(row, 3).text())

            # Configura os campos 'Projeto 1' (penúltima coluna) e 'Projeto 2' (última coluna)
            for col_offset, col_name in enumerate(["Projeto 1", "Projeto 2"]):
                col_index = self.table.columnCount() - 2 + col_offset  # Índices das colunas finais
                item = self.table.item(row, col_index)

                if item is not None:
                    if projetos_count > col_offset:
                        item.setFlags(item.flags() | Qt.ItemIsEditable)  # Habilita edição
                    else:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Desabilita edição



                    
    def display_data(self, data):
        """Exibe os dados importados na tabela, adicionando colunas 'Projeto 1' e 'Projeto 2'."""
        # Adiciona as colunas 'Projeto 1' e 'Projeto 2' ao DataFrame, se ainda não existirem
        if "Projeto 1" not in data.columns:
            data["Projeto 1"] = ""  # Inicializa com vazio
        if "Projeto 2" not in data.columns:
            data["Projeto 2"] = ""  # Inicializa com vazio

        # Atualiza a tabela com o novo número de colunas
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data.columns))
        self.table.setHorizontalHeaderLabels(data.columns)

        for i, row in data.iterrows():
            for j, value in enumerate(row):
                # Cria um item na tabela com o valor correspondente
                item = QTableWidgetItem(str(value))
                if data.columns[j] in ["Projeto 1", "Projeto 2"]:  # Identifica as colunas de projeto
                    item.setFlags(item.flags() | Qt.ItemIsEditable)  # Permitir edição
                self.table.setItem(i, j, item)

        # Atualiza a variável global (alunos_data)
        self.parent.alunos_data = data

        # Chama a lógica para habilitar/desabilitar as colunas de projetos
        self.update_table_for_projects()





class ProjetosWindow(BaseDataWindow):
    """Tela de gerenciamento de projetos."""
    def __init__(self, parent):
        super().__init__(parent, "Projetos", "projetos_data")
        



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
        label = QLabel("Processo de alocação ainda não implementado.")
        layout.addWidget(label)

        # Botão para voltar ao menu
        back_button = QPushButton("Voltar ao Menu")
        back_button.clicked.connect(self.return_to_menu)
        layout.addWidget(back_button)

    def return_to_menu(self):
        """Retorna para o menu principal."""
        self.parent.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    sys.exit(app.exec_())
