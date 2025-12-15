# uvm_memory_var14.py
import csv

# --- Opcode-to-Name Mapping (по полю A) ---
OPCODE_NAMES = {
    14: "load_const",   # A=14
    11: "read_value",   # A=11
    7:  "write_value",  # A=7
    4:  "sgn",          # A=4
}


class UVMMemory:
    """Модель памяти и стека для УВМ (вариант 14)."""

    def __init__(self, data_size=2048):
        self.data = [0] * data_size
        self.stack = []       # основной стек для операций
        self.ip = 0           # instruction pointer

    def push(self, value: int):
        """Помещает значение на стек."""
        self.stack.append(value)

    def pop(self) -> int:
        """Снимает значение с вершины стека."""
        if not self.stack:
            raise IndexError("Стек пуст при выполнении POP.")
        return self.stack.pop()

    def peek(self) -> int:
        """Возвращает значение с вершины стека без удаления."""
        if not self.stack:
            raise IndexError("Стек пуст при выполнении PEEK.")
        return self.stack[-1]

    def read_data(self, address: int) -> int:
        """Чтение из памяти данных."""
        if 0 <= address < len(self.data):
            return self.data[address]
        raise IndexError(f"Недопустимый адрес для чтения: {address}")

    def write_data(self, address: int, value: int):
        """Запись в память данных."""
        if 0 <= address < len(self.data):
            self.data[address] = value
        else:
            raise IndexError(f"Недопустимый адрес для записи: {address}")

    def stack_size(self) -> int:
        """Возвращает текущий размер стека."""
        return len(self.stack)


def dump_memory_to_csv_str(memory: UVMMemory, start_addr: int, end_addr: int) -> str:
    """Генерирует дамп памяти в CSV формате и возвращает его как строку."""
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Заголовок
    writer.writerow(["Тип", "Адрес/Индекс", "Значение"])
    
    # 1. Стек
    writer.writerow(["СТЕК", "РАЗМЕР", memory.stack_size()])
    for i, value in enumerate(reversed(memory.stack)):
        writer.writerow(["СТЕК", f"stack[{i}]", value])
    
    # 2. Регистры
    writer.writerow(["РЕГИСТРЫ", "IP", memory.ip])
    
    # 3. Память данных
    writer.writerow(["ПАМЯТЬ", "ДИАПАЗОН", f"{start_addr}-{end_addr}"])
    for addr in range(start_addr, min(end_addr + 1, len(memory.data))):
        writer.writerow(["ПАМЯТЬ", addr, memory.data[addr]])
    
    return output.getvalue()


def dump_memory_to_csv(memory: UVMMemory, start_addr: int, end_addr: int, filename: str):
    """Сохраняет дамп памяти в CSV формате в файл."""
    csv_str = dump_memory_to_csv_str(memory, start_addr, end_addr)
    with open(filename, "w", encoding="utf-8", newline='') as f:
        f.write(csv_str)
    print(f"\n[INFO] Дамп памяти сохранен в файл: {filename}")