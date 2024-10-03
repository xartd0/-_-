import pytest
import xml.etree.ElementTree as ET
from core import convert_element

def clean_output(output):
    """
    Очистка вывода для тестов: удаление лишних запятых и пробелов в конце.
    """
    output = output.strip()
    # Удаление последней запятой перед закрывающей фигурной скобкой, если она есть
    output = output.replace(",\n}", "\n}")
    return output

def test_simple_struct():
    xml = """<person>
                <name>John</name>
                <age>30</age>
             </person>"""
    root = ET.fromstring(xml)
    config = convert_element(root)
    expected = '''struct {
  name =   struct {
    value = "John",
  },
  age =   struct {
    value = 30,
  },
}
'''
    assert clean_output(config) == clean_output(expected)

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
}
'''
    assert clean_output(config) == clean_output(expected)

def test_constants():
    xml = """<root>
                <const name="PI" value="3.14"/>
                <compute name="PI"/>
             </root>"""
    root = ET.fromstring(xml)
    config = convert_element(root)
    expected = '''struct {
  const =   3.14 -> pi,
  compute =   ![pi],
}
'''
    assert clean_output(config) == clean_output(expected)

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
  books =   struct {
    book = (list
      struct {
        title =         struct {
          value = "Book One",
        },
        author =         struct {
          value = "Author A",
        },
      }
      struct {
        title =         struct {
          value = "Book Two",
        },
        author =         struct {
          value = "Author B",
        },
      }
    ),
  },
}
'''
    assert clean_output(config) == clean_output(expected)

def test_error_handling():
    xml = """<root>
                <compute name="UNKNOWN"/>
             </root>"""
    root = ET.fromstring(xml)
    with pytest.raises(ValueError):
        convert_element(root)
