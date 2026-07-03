# src/graph/builder.py
"""
Модуль для построения графа социальных связей
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import networkx as nx

from src.models import Person, Organization, Connection


def build_graph(
        persons: List[Person],
        organizations: List[Organization],
        connections: List[Connection]
) -> nx.Graph:
    """
    Строит граф из данных

    Args:
        persons: Список людей
        organizations: Список организаций
        connections: Список связей

    Returns:
        NetworkX Graph
    """
    G = nx.Graph()

    # Добавляем людей
    for person in persons:
        label = person.full_name or person.name or "Неизвестный"
        G.add_node(
            f"person_{person.id}",
            label=label,
            type="person",
            gender=person.gender.value if person.gender else None
        )

    # Добавляем организации
    for org in organizations:
        G.add_node(
            f"org_{org.id}",
            label=org.name,
            type="organization"
        )

    # Добавляем связи
    for conn in connections:
        if conn.source_type == "person" and conn.target_type == "person":
            source = f"person_{conn.source_id}"
            target = f"person_{conn.target_id}"
            G.add_edge(
                source, target,
                label=conn.relation_type,
                strength=conn.strength or 3
            )
        elif conn.source_type == "person" and conn.target_type == "organization":
            source = f"person_{conn.source_id}"
            target = f"org_{conn.target_id}"
            G.add_edge(
                source, target,
                label=conn.relation_type,
                strength=conn.strength or 3
            )
        elif conn.source_type == "organization" and conn.target_type == "person":
            source = f"org_{conn.source_id}"
            target = f"person_{conn.target_id}"
            G.add_edge(
                source, target,
                label=conn.relation_type,
                strength=conn.strength or 3
            )

    return G


def save_graph_html(G: nx.Graph, output_path: Optional[Path] = None) -> Path:
    """
    Сохраняет граф в HTML с использованием pyvis

    Args:
        G: NetworkX Graph
        output_path: Путь для сохранения

    Returns:
        Path к сохранённому файлу
    """
    try:
        from pyvis.network import Network
    except ImportError:
        raise ImportError("Установите pyvis: pip install pyvis")

    if output_path is None:
        output_path = Path("output/graph.html")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Создаём сеть
    net = Network(height="800px", width="100%", directed=False)

    # Настройки
    net.set_options("""
    {
        "nodes": {
            "font": {"size": 14},
            "borderWidth": 2,
            "shadow": true
        },
        "edges": {
            "font": {"size": 12, "align": "middle"},
            "smooth": {"type": "continuous", "roundness": 0.2},
            "width": 2
        },
        "physics": {
            "enabled": true,
            "stabilization": {"iterations": 100}
        },
        "interaction": {
            "hover": true,
            "navigationButtons": true,
            "zoomView": true,
            "dragView": true
        }
    }
    """)

    # Добавляем узлы с цветами в зависимости от типа
    for node, data in G.nodes(data=True):
        node_type = data.get('type', 'unknown')

        # Цвета в зависимости от типа
        color_map = {
            'person': '#4CAF50',  # Зелёный
            'organization': '#2196F3',  # Синий
            'unknown': '#9E9E9E'  # Серый
        }

        # Для людей добавляем цвет в зависимости от пола
        if node_type == 'person':
            gender = data.get('gender')
            if gender == 'male':
                color = '#2196F3'  # Синий (мужчина)
            elif gender == 'female':
                color = '#E91E63'  # Розовый (женщина)
            else:
                color = '#4CAF50'  # Зелёный (не указан)
        else:
            color = color_map.get(node_type, '#9E9E9E')

        net.add_node(
            node,
            label=data.get('label', node),
            title=data.get('label', node),
            color=color
        )

    # Добавляем рёбра
    for source, target, data in G.edges(data=True):
        net.add_edge(
            source, target,
            label=data.get('label', ''),
            title=f"Связь: {data.get('label', 'неизвестно')}",
            width=data.get('strength', 3)
        )

    # Сохраняем
    net.save_graph(str(output_path))

    return output_path


def get_graph_info(html_path: Path) -> Dict[str, int]:
    """
    Извлекает информацию о графе из HTML-файла
    """
    if not html_path.exists():
        return {}

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Пытаемся найти количество узлов и рёбер в HTML
        import re
        nodes_match = re.search(r'nodes:\s*\[(.*?)\]', content, re.DOTALL)
        edges_match = re.search(r'edges:\s*\[(.*?)\]', content, re.DOTALL)

        nodes_count = 0
        edges_count = 0

        if nodes_match:
            nodes_text = nodes_match.group(1)
            nodes_count = nodes_text.count('{') if nodes_text.strip() else 0

        if edges_match:
            edges_text = edges_match.group(1)
            edges_count = edges_text.count('{') if edges_text.strip() else 0

        return {
            'nodes': nodes_count,
            'edges': edges_count
        }
    except Exception:
        return {}