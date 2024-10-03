#!/usr/bin/env python3
"""
Git Commit Dependency Graph Visualizer

This script visualizes the commit dependency graph of a Git repository starting
from a specified tag. It reads configuration from an XML file, parses the Git
repository to extract commit information, generates a Graphviz DOT file, and
produces a PNG image of the graph.

Usage:
    python git_graph_visualizer.py /path/to/config.xml
"""

import os
import argparse
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Set

class GitObject:
    """Class representing a Git object."""

    def __init__(self, sha1: str, obj_type: str, content: bytes):
        self.sha1 = sha1
        self.type = obj_type
        self.content = content.decode('utf-8', errors='replace')

class CommitNode:
    """Class representing a commit in the dependency graph."""

    def __init__(self, sha1: str, author: str, date: str, message: str, parents: List[str]):
        self.sha1 = sha1
        self.author = author
        self.date = date
        self.message = message
        self.parents = parents

def parse_config(config_path: str) -> Dict[str, str]:
    """
    Parses the XML configuration file.

    Args:
        config_path: Path to the XML configuration file.

    Returns:
        A dictionary with configuration parameters.
    """
    tree = ET.parse(config_path)
    root = tree.getroot()
    config = {
        'graphviz_path': root.find('graphviz_path').text.strip(),
        'repo_path': root.find('repo_path').text.strip(),
        'output_path': root.find('output_path').text.strip(),
        'tag_name': root.find('tag_name').text.strip(),
    }
    return config

def get_tag_commit_sha1(repo_path: str, tag_name: str) -> str:
    """
    Retrieves the SHA1 of the commit that the tag points to.

    Args:
        repo_path: Path to the Git repository.
        tag_name: Name of the tag.

    Returns:
        The SHA1 hash of the commit.
    """
    tag_path = os.path.join(repo_path, '.git', 'refs', 'tags', tag_name)
    if not os.path.exists(tag_path):
        raise FileNotFoundError(f"Tag '{tag_name}' not found.")
    with open(tag_path, 'r') as f:
        sha1 = f.read().strip()
    return sha1

def read_object(repo_path: str, sha1: str) -> GitObject:
    """
    Reads a Git object from the repository using git cat-file.

    Args:
        repo_path: Path to the Git repository.
        sha1: SHA1 hash of the object.

    Returns:
        A GitObject instance.
    """
    import subprocess

    result = subprocess.run(
        ['git', 'cat-file', '-p', sha1],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise FileNotFoundError(f"Object '{sha1}' not found.")

    # Determine the type of the object
    type_result = subprocess.run(
        ['git', 'cat-file', '-t', sha1],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    obj_type = type_result.stdout.strip()

    return GitObject(sha1, obj_type, result.stdout.encode('utf-8'))



def parse_commit(obj: GitObject) -> CommitNode:
    """
    Parses a Git commit object.

    Args:
        obj: GitObject instance representing a commit.

    Returns:
        A CommitNode instance.
    """
    lines = obj.content.split('\n')
    parents = []
    author = ''
    date = ''
    message = ''
    in_message = False
    for line in lines:
        if line.startswith('parent '):
            parents.append(line[7:])
        elif line.startswith('author '):
            author_info = line[7:]
            # Разбиваем строку на части
            # Формат: "Имя <email> timestamp timezone"
            author_parts = author_info.rsplit(' ', 2)
            author_name_email = author_parts[0]
            timestamp = int(author_parts[1])
            timezone_str = author_parts[2]
            # Обработка временной зоны
            tz_sign = 1 if timezone_str.startswith('+') else -1
            tz_hours = int(timezone_str[1:3])
            tz_minutes = int(timezone_str[3:5])
            tz_offset = tz_sign * timedelta(hours=tz_hours, minutes=tz_minutes)
            # Создаём объект datetime с учётом временной зоны
            dt = datetime.fromtimestamp(timestamp, tz=timezone(tz_offset))
            date_time = dt.strftime('%Y-%m-%d %H:%M:%S %z')
            author = author_name_email
            date = date_time
        elif line == '':
            in_message = True
        elif in_message:
            message += line + '\n'
    return CommitNode(obj.sha1, author, date, message.strip(), parents)


def build_commit_graph(repo_path: str, start_sha1: str) -> Dict[str, CommitNode]:
    """
    Builds the commit graph starting from a specific commit.

    Args:
        repo_path: Path to the Git repository.
        start_sha1: SHA1 of the starting commit.

    Returns:
        A dictionary mapping commit SHA1 to CommitNode.
    """
    graph = {}
    stack = [start_sha1]
    visited: Set[str] = set()
    while stack:
        sha1 = stack.pop()
        if sha1 in visited:
            continue
        visited.add(sha1)
        obj = read_object(repo_path, sha1)
        if obj.type != 'commit':
            continue
        commit_node = parse_commit(obj)
        graph[sha1] = commit_node
        stack.extend(commit_node.parents)
    return graph


def generate_dot(graph: Dict[str, CommitNode]) -> str:
    """
    Generates a DOT representation of the commit graph.

    Args:
        graph: The commit graph.

    Returns:
        A string containing the DOT graph.
    """
    dot = 'digraph G {\n'
    dot += '  rankdir=TB;\n'  # Изменено на TB для вертикального расположения
    dot += '  node [shape=box, style=filled, color="lightblue"];\n'  # Добавлены стили для узлов
    dot += '  edge [color="gray"];\n'  # Добавлены стили для ребер

    for sha1, node in graph.items():
        label = f"{node.sha1[:7]}\\n{node.author}\\n{node.date}"
        dot += f'  "{sha1}" [label="{label}"];\n'
        for parent_sha1 in node.parents:
            dot += f'  "{sha1}" -> "{parent_sha1}";\n'
    dot += '}\n'
    return dot


def write_dot_file(dot_content: str, dot_path: str) -> None:
    """
    Writes the DOT content to a file.

    Args:
        dot_content: The DOT graph content.
        dot_path: Path to the output DOT file.
    """
    with open(dot_path, 'w') as f:
        f.write(dot_content)

def generate_graph_image(graphviz_path: str, dot_path: str, output_path: str, layout: str = 'dot') -> None:
    """
    Generates the graph image using Graphviz.

    Args:
        graphviz_path: Path to the Graphviz executable.
        dot_path: Path to the DOT file.
        output_path: Path to the output image file.
        layout: Graphviz layout engine to use.
    """
    subprocess.run([graphviz_path, '-K', layout, '-Tpng', dot_path, '-o', output_path], check=True)


def main(config_path: str) -> None:
    """
    Main function to execute the visualization process.

    Args:
        config_path: Path to the XML configuration file.
    """
    # Parse configuration
    config = parse_config(config_path)

    # Build commit graph
    start_sha1 = get_tag_commit_sha1(config['repo_path'], config['tag_name'])
    graph = build_commit_graph(config['repo_path'], start_sha1)

    # Generate DOT file
    dot_content = generate_dot(graph)
    dot_path = os.path.join(os.path.dirname(config['output_path']), 'graph.dot')
    write_dot_file(dot_content, dot_path)

    # Generate graph image
    generate_graph_image(config['graphviz_path'], dot_path, config['output_path'])

    print("Graph generated successfully.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Git Commit Dependency Graph Visualizer')
    parser.add_argument('config_path', help='Path to the XML configuration file')
    args = parser.parse_args()
    main(args.config_path)
