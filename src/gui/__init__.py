# src/gui/__init__.py
"""Графический интерфейс Graphite"""

from .main_window import MainWindow
from .graph_window import GraphWindow
from .persons_window import PersonsWindow
from .organizations_window import OrganizationsWindow
from .industries_window import IndustriesWindow

__all__ = [
    'MainWindow',
    'GraphWindow',
    'PersonsWindow',
    'OrganizationsWindow',
    'IndustriesWindow',
]