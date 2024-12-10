from .base_data_window import BaseDataWindow
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox, QMessageBox
from PyQt5.QtCore import Qt


class AlunosWindow(BaseDataWindow):
    """Tela de gerenciamento de alunos."""
    def __init__(self, parent):
        super().__init__(parent, "Alunos", "alunos_data")

    def update_table_for_projects(self):
        """Habilita ou desabilita os comboboxes 'Projeto 1' e 'Projeto 2' com base na quarta coluna."""
        for row in range(self.table.rowCount()):
            projetos_count = int(self.table.item(row, 3).text())  # Valor da quarta coluna

            for col_offset, col_name in enumerate(["Projeto 1", "Projeto 2"]):
                combobox = self.table.cellWidget(row, self.table.columnCount() - 2 + col_offset)
                if combobox is not None:
                    combobox.setEnabled(projetos_count > col_offset)
                    if projetos_count <= col_offset:
                        combobox.setCurrentText("")  # Limpa o valor se desabilitado


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

        # Obtem os nomes dos projetos (coluna 0 da tabela de projetos) ou lista vazia
        projetos_nomes = self.parent.projetos_data.iloc[:, 1].tolist() if self.parent.projetos_data is not None else []

        for i, row in data.iterrows():
            for j, value in enumerate(row):
                if data.columns[j] in ["Projeto 1", "Projeto 2"]:
                    combobox = QComboBox()
                    combobox.addItems([""] + projetos_nomes)  # Adiciona opções vazias + nomes dos projetos
                    combobox.setCurrentText(str(value))
                    combobox.currentTextChanged.connect(lambda text, row=i, col=j: self.update_project_data(text, row, col))
                    self.table.setCellWidget(i, j, combobox)
                else:
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(i, j, item)

        # Atualiza a variável global (alunos_data)
        self.parent.alunos_data = data

        # Chama a lógica para habilitar/desabilitar as colunas de projetos
        self.update_table_for_projects()


    def update_project_data(self, text, row, col):
        """Atualiza os dados do projeto no DataFrame ao alterar o valor do combobox."""
        data = self.parent.alunos_data
        column_name = data.columns[col]  # Nome da coluna (Projeto 1 ou Projeto 2)
        
        # Atualiza o valor no DataFrame
        data.at[row, column_name] = text
        
        # Atualiza a variável global no MenuWindow
        self.parent.alunos_data = data

