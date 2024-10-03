import pytest
import tempfile
import os
import shutil
from core import (
    parse_config, get_tag_commit_sha1, read_object, parse_commit,
    build_commit_graph, generate_dot, write_dot_file, generate_graph_image
)
from unittest.mock import patch
from datetime import datetime, timezone, timedelta
import zlib
import subprocess

@pytest.fixture
def temp_repo():
    # Создаем временный каталог для репозитория
    repo_dir = tempfile.mkdtemp()
    try:
        # Инициализируем Git-репозиторий
        subprocess.run(['git', 'init'], cwd=repo_dir, check=True)
        
        # Настраиваем имя пользователя и email для Git
        subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=repo_dir, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=repo_dir, check=True)
        
        # Создаем файл и делаем коммит
        test_file = os.path.join(repo_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('This is a test file.')

        subprocess.run(['git', 'add', 'test.txt'], cwd=repo_dir, check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=repo_dir, check=True)
        
        # Получаем SHA1 последнего коммита
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=repo_dir, stdout=subprocess.PIPE, text=True, check=True)
        commit_sha1 = result.stdout.strip()
        
        # Создаем тег
        tag_name = 'test_tag'
        subprocess.run(['git', 'tag', tag_name], cwd=repo_dir, check=True)

        yield repo_dir, tag_name, commit_sha1
    finally:
        # Удаляем временный репозиторий после тестов
        shutil.rmtree(repo_dir)

def test_parse_config():
    config_xml = '''<config>
        <graphviz_path>/usr/bin/dot</graphviz_path>
        <repo_path>/path/to/repo</repo_path>
        <output_path>/path/to/output/graph.png</output_path>
        <tag_name>v1.0.0</tag_name>
    </config>'''
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        f.write(config_xml)
        config_path = f.name
    config = parse_config(config_path)
    os.unlink(config_path)
    assert config['graphviz_path'] == '/usr/bin/dot'
    assert config['repo_path'] == '/path/to/repo'
    assert config['output_path'] == '/path/to/output/graph.png'
    assert config['tag_name'] == 'v1.0.0'

def test_get_tag_commit_sha1(temp_repo):
    repo_dir, tag_name, commit_sha1 = temp_repo
    sha1 = get_tag_commit_sha1(repo_dir, tag_name)
    assert sha1 == commit_sha1

def test_read_object(temp_repo):
    repo_dir, tag_name, commit_sha1 = temp_repo
    obj = read_object(repo_dir, commit_sha1)
    assert obj.type == 'commit'
    assert 'author Test User' in obj.content

def test_parse_commit(temp_repo):
    repo_dir, tag_name, commit_sha1 = temp_repo
    obj = read_object(repo_dir, commit_sha1)
    commit_node = parse_commit(obj)
    assert commit_node.sha1 == commit_sha1
    assert commit_node.author == 'Test User <test@example.com>'
    assert commit_node.parents == []
    assert commit_node.message == 'Initial commit'
    # Здесь мы не можем заранее знать точную дату, поэтому проверим, что дата не пуста
    assert commit_node.date != ''


def test_build_commit_graph(temp_repo):
    repo_dir, tag_name, commit_sha1 = temp_repo
    graph = build_commit_graph(repo_dir, commit_sha1)
    assert commit_sha1 in graph
    commit_node = graph[commit_sha1]
    assert commit_node.sha1 == commit_sha1

def test_generate_dot(temp_repo):
    repo_dir, tag_name, commit_sha1 = temp_repo
    graph = build_commit_graph(repo_dir, commit_sha1)
    dot_content = generate_dot(graph)
    assert f'"{commit_sha1}"' in dot_content

def test_write_dot_file():
    dot_content = 'digraph G {}'
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        dot_path = f.name
    write_dot_file(dot_content, dot_path)
    with open(dot_path, 'r') as f:
        content = f.read()
    os.unlink(dot_path)
    assert content == dot_content

@patch('subprocess.run')
def test_generate_graph_image(mock_run):
    graphviz_path = '/usr/bin/dot'
    dot_path = '/path/to/graph.dot'
    output_path = '/path/to/output.png'
    generate_graph_image(graphviz_path, dot_path, output_path, layout='dot')
    mock_run.assert_called_with(
        [graphviz_path, '-K', 'dot', '-Tpng', dot_path, '-o', output_path],
        check=True
    )

def test_main(temp_repo):
    repo_dir, tag_name, commit_sha1 = temp_repo
    config_xml = f'''<config>
        <graphviz_path>/usr/bin/dot</graphviz_path>
        <repo_path>{repo_dir}</repo_path>
        <output_path>/tmp/graph.png</output_path>
        <tag_name>{tag_name}</tag_name>
    </config>'''
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        config_path = f.name
        f.write(config_xml)

    # Патчим функции generate_graph_image и print, чтобы не вызывать реальные команды
    with patch('core.generate_graph_image') as mock_generate_graph_image, \
         patch('builtins.print') as mock_print:
        from core import main
        main(config_path)
        mock_generate_graph_image.assert_called()
        mock_print.assert_called_with("Graph generated successfully.")

    os.unlink(config_path)
