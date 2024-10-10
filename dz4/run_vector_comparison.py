from virtual_machine import VirtualMachine
import yaml

vm = VirtualMachine(memory_size=1024)
vm.execute('vector_comparison.bin', 'vector_result.yaml', memory_range=(200, 204))

# Загрузка результатов из файла
with open('vector_result.yaml', 'r') as f:
    result_vector = yaml.safe_load(f)

print("Результирующий вектор:")
for i, value in enumerate(result_vector):
    print(f"Элемент {i}: {value}")
