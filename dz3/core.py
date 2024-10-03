#!/usr/bin/env python3
"""
XML to Configuration Language Converter

This script reads an XML file and converts it into a configuration language
with a specific syntax. The configuration language supports various constructs
like comments, arrays, dictionaries, constants, and more.

Usage:
    python converter.py -f input.xml

"""

import argparse
import sys
import re
import xml.etree.ElementTree as ET

def sanitize_name(name):
    """
    Sanitizes a name to match the [a-z]+ pattern required by the configuration language.

    Parameters:
        name (str): The original name.

    Returns:
        str: The sanitized name containing only lowercase letters.
    """
    name = name.lower()
    name = re.sub('[^a-z]', '', name)
    if not name:
        name = 'unnamed'
    return name

def is_number(s):
    """
    Checks if a string represents a number.

    Parameters:
        s (str): The string to check.

    Returns:
        bool: True if the string is a number, False otherwise.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

def convert_value(value):
    """
    Converts a value to its configuration language representation.

    Parameters:
        value (str): The value to convert.

    Returns:
        str: The value in the configuration language format.
    """
    value = value.strip()
    if is_number(value):
        return value
    else:
        return f"\"{value}\""

def convert_element(element, indent=0, constants=None):
    """
    Recursively converts an XML element into the configuration language representation.

    Parameters:
        element (xml.etree.ElementTree.Element): The XML element to convert.
        indent (int): The current indentation level.
        constants (dict): A dictionary to store constants.

    Returns:
        str: The configuration language representation of the element.

    Raises:
        ValueError: If there is a syntax error in the XML structure.
    """
    if constants is None:
        constants = {}

    indent_str = '  ' * indent
    items = []

    # Handle constant declaration
    if element.tag == 'const':
        name = element.get('name')
        value = element.get('value')
        if name and value:
            sanitized_name = sanitize_name(name)
            constants[sanitized_name] = value
            result = f"{indent_str}{convert_value(value)} -> {sanitized_name}"
            return result
        else:
            raise ValueError(f"Const element must have 'name' and 'value' attributes.")
    # Handle constant computation
    elif element.tag == 'compute':
        name = element.get('name')
        if name:
            sanitized_name = sanitize_name(name)
            if sanitized_name in constants:
                result = f"{indent_str}![{sanitized_name}]"
                return result
            else:
                raise ValueError(f"Constant '{sanitized_name}' not found.")
        else:
            raise ValueError(f"Compute element must have 'name' attribute.")
    else:
        # Start struct
        result = indent_str + "struct {\n"

        # Process attributes
        for attr_name, attr_value in element.attrib.items():
            name = sanitize_name(attr_name)
            value = convert_value(attr_value)
            items.append(f"{indent_str}  {name} = {value},")

        # Process child elements
        children = list(element)
        if children:
            # Group children by tag name
            child_groups = {}
            for child in children:
                tag = sanitize_name(child.tag)
                if tag not in child_groups:
                    child_groups[tag] = []
                child_groups[tag].append(child)

            for tag, group in child_groups.items():
                if len(group) == 1:
                    # Single child element
                    value = convert_element(group[0], indent+1, constants)
                    items.append(f"{indent_str}  {tag} = {value},")
                else:
                    # Multiple child elements with the same tag (array)
                    list_items = []
                    for elem in group:
                        item = convert_element(elem, indent+2, constants)
                        list_items.append(item)
                    list_str = f"(list\n" + '\n'.join(list_items) + f"\n{indent_str}  )"
                    items.append(f"{indent_str}  {tag} = {list_str},")
        else:
            # No child elements, process text content
            text = element.text.strip() if element.text else ''
            if text:
                value = convert_value(text)
                items.append(f"{indent_str}  value = {value},")

        result += '\n'.join(items)
        result += f"\n{indent_str}}}"
        return result

def main():
    """
    Main function that parses command-line arguments and initiates the conversion process.
    """
    parser = argparse.ArgumentParser(description='XML to Configuration Language Converter')
    parser.add_argument('-f', '--file', required=True, help='Path to input XML file')
    args = parser.parse_args()

    try:
        tree = ET.parse(args.file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"File not found: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        config = convert_element(root)
        print(config)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
