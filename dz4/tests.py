import pytest
from assembly import Assembler
from virtual_machine import VirtualMachine

@pytest.fixture
def setup_test_environment(tmp_path):
    test_asm_path = tmp_path / "test_vector.asm"
    binary_path = tmp_path / "output.bin"
    log_path = tmp_path / "log.yaml"
    result_path = tmp_path / "result.yaml"

    return test_asm_path, binary_path, log_path, result_path

def test_load_const(setup_test_environment):
    test_asm_path, binary_path, log_path, result_path = setup_test_environment
    assembler = Assembler()
    asm_code = "LOAD_CONST R1, 100"
    with open(test_asm_path, 'w') as f:
        f.write(asm_code)
    assembler.assemble(test_asm_path, binary_path, log_path)
    vm = VirtualMachine(memory_size=1024)
    vm.execute(binary_path, result_path, memory_range=(0, 4))
    assert vm.registers[1] == 100, "LOAD_CONST не загрузил значение правильно."

def test_equal_operation(setup_test_environment):
    test_asm_path, binary_path, log_path, result_path = setup_test_environment
    asm_code = """
    LOAD_CONST R1, 247
    LOAD_CONST R2, 247
    EQUAL R3, R1, R2
    """
    with open(test_asm_path, 'w') as f:
        f.write(asm_code)
    assembler = Assembler()
    assembler.assemble(test_asm_path, binary_path, log_path)
    vm = VirtualMachine(memory_size=1024)
    vm.execute(binary_path, result_path, memory_range=(0, 4))
    assert vm.registers[3] == 1, "EQUAL должен вернуть 1, если регистры равны."

def test_vector_comparison(setup_test_environment):
    """
    Тест для выполнения сравнения элементов вектора с числом 247.
    """
    test_asm_path, binary_path, log_path, result_path = setup_test_environment
    asm_code = """
    # Инициализация чисел и адресов
    LOAD_CONST R1, 100        # Начальный адрес вектора
    LOAD_CONST R2, 247        # Число для сравнения
    LOAD_CONST R3, 200        # Начальный адрес для результатов

    # Инициализация элементов вектора
    LOAD_CONST R10, 250
    WRITE_MEM R10, [R1 + 0]

    LOAD_CONST R10, 247
    WRITE_MEM R10, [R1 + 1]

    LOAD_CONST R10, 123
    WRITE_MEM R10, [R1 + 2]

    LOAD_CONST R10, 247
    WRITE_MEM R10, [R1 + 3]

    # Сравнение элементов без цикла
    # Элемент 0
    READ_MEM R4, [R1 + 0]
    EQUAL R5, R4, R2
    WRITE_MEM R5, [R3 + 0]

    # Элемент 1
    READ_MEM R4, [R1 + 1]
    EQUAL R5, R4, R2
    WRITE_MEM R5, [R3 + 1]

    # Элемент 2
    READ_MEM R4, [R1 + 2]
    EQUAL R5, R4, R2
    WRITE_MEM R5, [R3 + 2]

    # Элемент 3
    READ_MEM R4, [R1 + 3]
    EQUAL R5, R4, R2
    WRITE_MEM R5, [R3 + 3]
    """
    with open(test_asm_path, 'w') as f:
        f.write(asm_code)
    assembler = Assembler()
    assembler.assemble(test_asm_path, binary_path, log_path)
    vm = VirtualMachine(memory_size=1024)
    vm.execute(binary_path, result_path, memory_range=(200, 204))
    # Проверяем, что результаты сравнения вектора с 247 корректны
    assert vm.memory[200] == 0, "Первый элемент должен быть 0 (250 != 247)."
    assert vm.memory[201] == 1, "Второй элемент должен быть 1 (247 == 247)."
    assert vm.memory[202] == 0, "Третий элемент должен быть 0 (123 != 247)."
    assert vm.memory[203] == 1, "Четвертый элемент должен быть 1 (247 == 247)."
