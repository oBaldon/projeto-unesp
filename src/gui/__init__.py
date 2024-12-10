# src/gui/__init__.py

from .menu_window import MenuWindow
from .alunos_window import AlunosWindow
from .projetos_window import ProjetosWindow
from .alocacao_window import AlocacaoWindow
from .base_data_window import BaseDataWindow

# Defina __all__ para controle explícito do que é exportado
__all__ = [
    "MenuWindow",
    "AlunosWindow",
    "ProjetosWindow",
    "AlocacaoWindow",
    "BaseDataWindow",
]
