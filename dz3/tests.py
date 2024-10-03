import pytest
import xml.etree.ElementTree as ET
from core import convert_element

def test_simple_struct():
    xml = """<person>
                <name>John</name>
                <age>30</age>
             </person>"""
    root = ET.fromstring(xml)
    config = convert_element(root)
    expected = '''struct {
  name = "John",
  age = 30,
}'''
    assert config.strip() == expected.strip()

def test_array():
    xml = """<numbers>
                <number>1</number>
                <number>2</number>
                <number>3</number>
             </numbers>"""
    root = ET.fromstring(xml)
    config = convert_element(root)
    expected = '''struct {
  number = (list
    struct {
      value = 1,
    }
    struct {
      value = 2,
    }
    struct {
      value = 3,
    }
  ),
}'''
    assert config.strip() == expected.strip()

def test_constants():
    xml = """<root>
                <const name="PI" value="3.14"/>
                <compute name="PI"/>
             </root>"""
    root = ET.fromstring(xml)
    config = convert_element(root)
    expected = '''struct {
  3.14 -> pi
  ![pi]
}'''
    assert config.strip() == expected.strip()

def test_nested_structures():
    xml = """<library>
                <books>
                    <book>
                        <title>Book One</title>
                        <author>Author A</author>
                    </book>
                    <book>
                        <title>Book Two</title>
                        <author>Author B</author>
                    </book>
                </books>
             </library>"""
    root = ET.fromstring(xml)
    config = convert_element(root)
    expected = '''struct {
  books = struct {
    book = (list
      struct {
        title = "Book One",
        author = "Author A",
      }
      struct {
        title = "Book Two",
        author = "Author B",
      }
    ),
  }
}'''
    assert config.strip() == expected.strip()

def test_error_handling():
    xml = """<root>
                <compute name="UNKNOWN"/>
             </root>"""
    root = ET.fromstring(xml)
    with pytest.raises(ValueError):
        convert_element(root)
