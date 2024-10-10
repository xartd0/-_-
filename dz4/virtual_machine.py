"""
Virtual machine for executing binary code.

"""
import struct
import yaml

class VirtualMachine:
    """
    Virtual machine for executing binary code.

    Attributes:
        registers (list): Registers of the virtual machine.
        memory (list): Memory of the virtual machine.
    """

    def __init__(self, memory_size):
        """
        Initializes the virtual machine.

        :param memory_size: Size of the memory.
        """
        self.registers = [0] * 256  # Регистры УВМ
        self.memory = [0] * memory_size

    def execute(self, binary_path, result_path, memory_range):
        """
        Executes the binary code from a file and writes the result to a file.

        :param binary_path: Path to the binary file.
        :param result_path: Path to the result file.
        :param memory_range: Range of memory to write to the result file.
        """
        with open(binary_path, 'rb') as binary_file, open(result_path, 'w') as result_file:
            while True:
                opcode_byte = binary_file.read(1)
                if not opcode_byte:
                    break
                opcode = opcode_byte[0]
                if opcode == 79:  # LOAD_CONST
                    self.load_const(binary_file)
                elif opcode == 220:  # READ_MEM
                    self.read_mem(binary_file)
                elif opcode == 74:  # WRITE_MEM
                    self.write_mem(binary_file)
                elif opcode == 131:  # EQUAL
                    self.equal(binary_file)
                else:
                    raise ValueError(f"Неизвестный код операции: {opcode}")

            # Запись указанного диапазона памяти в файл результата
            yaml.dump(self.memory[memory_range[0]:memory_range[1]], result_file)

    def load_const(self, binary_file):
        """
        Executes the LOAD_CONST command.

        :param binary_file: File object with the binary code.
        """
        data = binary_file.read(6)
        if len(data) < 6:
            raise ValueError("Недостаточно данных для команды LOAD_CONST")
        B, C = struct.unpack('<HI', data)
        self.registers[B] = C

    def read_mem(self, binary_file):
        """
        Executes the READ_MEM command.

        :param binary_file: File object with the binary code.
        """
        data = binary_file.read(4)
        if len(data) < 4:
            raise ValueError("Недостаточно данных для команды READ_MEM")
        B, C, D = struct.unpack('<HBB', data)
        addr = self.registers[C] + B
        self.registers[D] = self.memory[addr]

    def write_mem(self, binary_file):
        """
        Executes the WRITE_MEM command.

        :param binary_file: File object with the binary code.
        """
        data = binary_file.read(4)
        if len(data) < 4:
            raise ValueError("Недостаточно данных для команды WRITE_MEM")
        B, C, D = struct.unpack('<HBB', data)
        addr = self.registers[C] + B
        self.memory[addr] = self.registers[D]

    def equal(self, binary_file):
        """
        Executes the EQUAL command.

        :param binary_file: File object with the binary code.
        """
        data = binary_file.read(3)
        if len(data) < 3:
            raise ValueError("Недостаточно данных для команды EQUAL")
        D, B, C = struct.unpack('<BBB', data)
        result = int(self.registers[B] == self.registers[C])
        self.registers[D] = result

