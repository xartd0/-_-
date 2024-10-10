"""
Assembler for simple virtual machine.

This module provides a class for assembling code for simple virtual machine.

The class is called Assembler and it has the following methods:

*   `__init__`: Initializes the assembler.
*   `assemble`: Assembles the code from a source file and writes it to a binary file.
*   `parse_instruction`: Parses an instruction from a line of source code.
*   `parse_memory_expression`: Parses a memory expression from a string.
*   `encode_instruction`: Encodes an instruction into a binary format.
*   `create_log_entry`: Creates a log entry for an instruction.

The class also has a dictionary of commands with their corresponding opcodes.
"""

import struct
import yaml

class Assembler:
    """
    Assembler for simple virtual machine.
    """

    def __init__(self):
        """
        Initializes the assembler.
        """
        self.commands = {
            'LOAD_CONST': 79,  # Код операции для загрузки константы
            'READ_MEM': 220,   # Код операции для чтения значения из памяти
            'WRITE_MEM': 74,   # Код операции для записи значения в память
            'EQUAL': 131       # Код операции для бинарной операции "=="
        }

    def assemble(self, source_path, binary_path, log_path):
        """
        Assembles the code from a source file and writes it to a binary file.

        :param source_path: Path to the source file.
        :param binary_path: Path to the binary file.
        :param log_path: Path to the log file.
        """
        with open(source_path, 'r') as source_file, open(binary_path, 'wb') as binary_file, open(log_path, 'w') as log_file:
            log_data = []
            for line in source_file:
                command, args = self.parse_instruction(line.strip())
                if command is None:
                    continue
                binary_instruction = self.encode_instruction(command, args)
                binary_file.write(binary_instruction)
                log_data.append(self.create_log_entry(command, args, binary_instruction))
            yaml.dump(log_data, log_file)

    def parse_instruction(self, line):
        """
        Parses an instruction from a line of source code.

        :param line: The line of source code.
        :return: The command and its arguments.
        """
        if not line.strip():
            return None, None

        # Удаляем комментарии
        line = line.split('#', 1)[0].strip()
        if not line:
            return None, None

        parts = line.replace(',', '').split()
        command = parts[0]

        if command in ['WRITE_MEM', 'READ_MEM']:
            reg = parts[1].replace('R', '')
            mem_expr = ' '.join(parts[2:])
            offset, reg_c = self.parse_memory_expression(mem_expr)
            args = [int(offset), int(reg_c), int(reg)]
        elif command == 'EQUAL':
            args = [int(arg.replace('R', '')) for arg in parts[1:]]
            if len(args) != 3:
                raise ValueError(f"Команда {command} требует три аргумента, получено: {len(args)}")
        else:
            args = [int(arg.replace('R', '')) for arg in parts[1:]]
        return command, args

    def parse_memory_expression(self, expr):
        """
        Parses a memory expression from a string.

        :param expr: The memory expression.
        :return: The offset and the register.
        """
        expr = expr.strip()
        if not (expr.startswith('[') and expr.endswith(']')):
            raise ValueError(f"Некорректное выражение памяти: {expr}")

        expr = expr[1:-1]  # Убираем квадратные скобки
        reg_part, offset_part = expr.split('+')
        reg_c = reg_part.strip().replace('R', '')
        offset = offset_part.strip()
        return offset, reg_c

    def encode_instruction(self, command, args):
        """
        Encodes an instruction into a binary format.

        :param command: The command.
        :param args: The arguments.
        :return: The binary instruction.
        """
        if command == 'LOAD_CONST':
            opcode = self.commands[command]
            B = args[0]
            C = args[1]
            return struct.pack('<BHI', opcode, B, C)
        elif command == 'READ_MEM':
            opcode = self.commands[command]
            B = args[0]  # offset
            C = args[1]  # reg_c
            D = args[2]  # reg_d
            return struct.pack('<BHBB', opcode, B, C, D)
        elif command == 'WRITE_MEM':
            opcode = self.commands[command]
            B = args[0]  # offset
            C = args[1]  # reg_c
            D = args[2]  # reg_d
            return struct.pack('<BHBB', opcode, B, C, D)
        elif command == 'EQUAL':
            opcode = self.commands[command]
            D = args[0]  # Регистр для результата
            B = args[1]
            C = args[2]
            return struct.pack('<BBBB', opcode, D, B, C)
        else:
            raise ValueError(f"Неизвестная команда {command}")

    def create_log_entry(self, command, args, binary_instruction):
        """
        Creates a log entry for an instruction.

        :param command: The command.
        :param args: The arguments.
        :param binary_instruction: The binary instruction.
        :return: The log entry.
        """
        return {
            'command': command,
            'args': args,
            'binary': binary_instruction.hex()
        }

