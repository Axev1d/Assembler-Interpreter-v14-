# uvm_asm_var14.py
import sys

# ------------------------------------------------------------
# Кодирование инструкции по спецификации варианта 14:
#   Биты 0–3: поле A (opcode) - 4 бита
#   Биты 4–18: поле B (операнд) - 15 бит
# Размер команды: 3 байта, порядок little-endian.
# ------------------------------------------------------------

def pack_instruction(a: int, b: int) -> bytes:
    """
    Упаковывает A и B в 3 байта по спецификации:
        value = A | (B << 4)
    """
    if a < 0 or a >= (1 << 4):
        raise ValueError(f"Поле A (opcode) должно помещаться в 4 бита: 0..15, получено {a}")
    if b < 0 or b >= (1 << 15):
        raise ValueError(f"Поле B (операнд) должно помещаться в 15 бит: 0..32767, получено {b}")

    value = a | (b << 4)
    return value.to_bytes(3, "little")


# --- Коды операций согласно спецификации УВМ (поле A, биты 0–3) ---
OP_LOAD_CONST = 14  # Загрузка константы на стек
OP_READ       = 11  # Чтение значения из памяти на стек
OP_WRITE      = 7   # Запись значения с вершины стека в память
OP_SGN        = 4   # Вычисление знака числа из памяти


# --- Функции генерации байт-кода ---

def asm_load_const(const: int) -> bytes:
    """
    Загрузка константы на стек.
    A = 14, B = const.
    Тест (A=14, B=831):
        0xFE, 0x33, 0x00
    """
    return pack_instruction(OP_LOAD_CONST, const)


def asm_read_value(address: int) -> bytes:
    """
    Чтение значения из памяти на стек.
    A = 11, B = address.
    Тест (A=11, B=97):
        0x1B, 0x06, 0x00
    """
    return pack_instruction(OP_READ, address)


def asm_write_value(address: int) -> bytes:
    """
    Запись значения с вершины стека в память.
    A = 7, B = address.
    Тест (A=7, B=291):
        0x37, 0x12, 0x00
    """
    return pack_instruction(OP_WRITE, address)


def asm_sgn(address: int) -> bytes:
    """
    Вычисление знака числа из памяти.
    A = 4, B = address.
    Тест (A=4, B=158):
        0xE4, 0x09, 0x00
    """
    return pack_instruction(OP_SGN, address)


# --- Главная функция трансляции IR в байт-код ---

def asm(IR: list) -> bytes:
    """
    Транслирует промежуточное представление (IR) в последовательность байт-кода.
    IR — список кортежей вида:
        ('load_const', value)
        ('read_value', address)
        ('write_value', address)
        ('sgn', address)
    """
    bytecode = bytes()
    for op, *arg in IR:
        if op == "load_const":
            bytecode += asm_load_const(arg[0])
        elif op == "read_value":
            bytecode += asm_read_value(arg[0])
        elif op == "write_value":
            bytecode += asm_write_value(arg[0])
        elif op == "sgn":
            bytecode += asm_sgn(arg[0])
        else:
            raise ValueError(f"Неизвестная команда ассемблера: {op}")
    return bytecode


# --- Парсер исходного текста ASM в IR ---

def full_asm(text: str) -> tuple[bytes, list]:
    """
    Читает текст программы, преобразует его в байт-код и IR.
    Формат строки: "команда аргумент" (пробел-разделитель)
        load_const 831
        read_value 97
        write_value 291
        sgn 158
    Комментарии после '#' игнорируются.
    """
    text = text.strip()
    IR = []

    for line_num, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.strip()

        # 1. Удаляем хвостовой комментарий
        if "#" in line:
            line = line.split("#")[0].strip()

        # 2. Пустые строки игнорируем
        if not line:
            continue

        # 3. Парсинг "cmd arg"
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"Строка {line_num}: ожидается 'команда аргумент', получено: '{line}'")
        
        cmd = parts[0].strip()
        arg_str = parts[1].strip()
        
        try:
            arg = int(arg_str)
        except ValueError:
            raise ValueError(f"Строка {line_num}: аргумент должен быть числом, получено: '{arg_str}'")

        IR.append((cmd, arg))

    # Генерируем байт-код
    bytecode = asm(IR)
    return bytecode, IR


# --- Тестовый вывод IR и байт-кода ---

def print_ir_test_mode(IR: list, bytecode: bytes):
    """Выводит IR и байт-код, а также разбор по инструкциям (3 байта на команду)."""
    print("\n--- Промежуточное представление (IR) ---")
    for i, (op, arg) in enumerate(IR):
        print(f"[{i:02d}] {op:<12} {arg}")

    print("\n--- Сгенерированный байт-код (в байтовом формате) ---")
    print(*(f"0x{b:02X}" for b in bytecode))

    print("\n--- Представление по инструкциям (3 байта на команду) ---")
    current_byte_index = 0
    for i, (op, arg) in enumerate(IR):
        instruction_bytes = bytecode[current_byte_index: current_byte_index + 3]
        current_byte_index += 3

        opcode_hex = " ".join(f"{b:02X}" for b in instruction_bytes)
        print(f"[{i:02d}] {op:<12} | Bytes: {opcode_hex} | Аргумент: {arg}")


# --- Встроенные тесты по спецификации ---

def test_asm_functions():
    """Проверяет, что функции ассемблирования генерируют байты точно как в задании."""
    try:
        # Загрузка константы (A=14, B=831):
        assert list(asm_load_const(831)) == [0xFE, 0x33, 0x00], "Test load_const failed"
        # Чтение значения из памяти (A=11, B=97):
        assert list(asm_read_value(97)) == [0x1B, 0x06, 0x00], "Test read_value failed"
        # Запись значения в память (A=7, B=291):
        assert list(asm_write_value(291)) == [0x37, 0x12, 0x00], "Test write_value failed"
        # Вычисление знака (A=4, B=158):
        assert list(asm_sgn(158)) == [0xE4, 0x09, 0x00], "Test sgn failed"

        print("[INFO] Встроенные тесты asm_функций пройдены успешно.")
    except AssertionError as e:
        print(f"[ERROR] Тест не пройден: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_asm_functions()