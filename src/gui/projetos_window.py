from .base_data_window import BaseDataWindow


class ProjetosWindow(BaseDataWindow):
    """Tela de gerenciamento de projetos."""
    def __init__(self, parent):
        super().__init__(parent, "Projetos", "projetos_data")
