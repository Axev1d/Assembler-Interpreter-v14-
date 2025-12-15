# interpreter_var14.py
import argparse
from pathlib import Path
import sys

from uvm_memory import UVMMemory, OPCODE_NAMES, dump_memory_to_csv


def decode_instruction(instruction_bytes: bytes):
    """
    Декодирует 3 байта в (cmd_name, B).

    Формат:
        value = int.from_bytes(3 байта, 'little')
        A = value & 0xF
        B = value >> 4
    """
    if len(instruction_bytes) != 3:
        raise ValueError(f"Ожидалось 3 байта инструкции, получено {len(instruction_bytes)}")

    value = int.from_bytes(instruction_bytes, byteorder="little")
    a = value & 0xF
    b = value >> 4

    cmd_name = OPCODE_NAMES.get(a)
    if cmd_name is None:
        raise ValueError(f"Неизвестный opcode (поле A): {a}")
    return cmd_name, b


def run_program(bytecode: bytes, memory: UVMMemory) -> str:
    """
    Реализует основной цикл интерпретатора (стековая архитектура).
    Возвращает лог выполнения в виде строки.

    Команды:
      - load_const (A=14, B=константа):
          PUSH(B)
      - read_value (A=11, B=адрес):
          PUSH(MEM[B])
      - write_value (A=7, B=адрес):
          value = POP()
          MEM[B] = value
      - sgn (A=4, B=адрес):
          value = MEM[B]
          result = 1 if value > 0 else (-1 if value < 0 else 0)
          PUSH(result)
    """
    # Разбиваем байт-код по 3 байта
    instructions = [bytecode[i:i + 3] for i in range(0, len(bytecode), 3)]
    log_messages = []

    log_messages.append(f"[INFO] Запуск программы. Всего инструкций: {len(instructions)}")
    log_messages.append(f"[INFO] Начальное состояние стека: {memory.stack}")

    while memory.ip < len(instructions):
        instruction_bytes = instructions[memory.ip]
        current_ip = memory.ip

        try:
            cmd, operand = decode_instruction(instruction_bytes)
        except Exception as e:
            log_messages.append(f"[RUNTIME ERROR] На адресе {memory.ip}: {e}")
            break

        log_messages.append(
            f"[{current_ip:03d}] Выполняется: {cmd:<12} | B (операнд): {operand} | Стек: {memory.stack}"
        )

        new_ip = current_ip + 1

        # --- ВЫПОЛНЕНИЕ КОМАНД ---
        try:
            if cmd == "load_const":
                memory.push(operand)

            elif cmd == "read_value":
                value = memory.read_data(operand)
                memory.push(value)

            elif cmd == "write_value":
                value = memory.pop()
                memory.write_data(operand, value)

            elif cmd == "sgn":
                value = memory.read_data(operand)
                if value > 0:
                    result = 1
                elif value < 0:
                    result = -1
                else:
                    result = 0
                memory.push(result)

            else:
                log_messages.append(f"[RUNTIME ERROR] Неизвестная команда: {cmd}")
                break

        except IndexError as e:
            log_messages.append(f"[RUNTIME ERROR] Ошибка стека: {e}")
            break
        except Exception as e:
            log_messages.append(f"[RUNTIME ERROR] Ошибка выполнения: {e}")
            break

        memory.ip = new_ip

    log_messages.append(f"\n--- Выполнение программы завершено на IP={memory.ip} ---")
    log_messages.append(f"Финальное состояние стека: {memory.stack}")
    log_messages.append(f"Память (первые 16 ячеек): {memory.data[:16]}")

    return "\n".join(log_messages)


# --- CLI-оболочка (для запуска из консоли) ---

def parse_args():
    """Обрабатывает аргументы командной строки."""
    parser = argparse.ArgumentParser(description="UVM Interpreter (Вариант 14)")
    parser.add_argument("program", help="Путь к бинарному файлу с ассемблированной программой.")
    parser.add_argument("dump_file", help="Путь к файлу-результату для дампа памяти (CSV).")
    parser.add_argument(
        "dump_range",
        help="Диапазон адресов памяти для дампа (например, 0:10).",
        type=str
    )
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        program_path = Path(args.program)
        dump_file = args.dump_file

        # Парсинг диапазона дампа
        if ":" not in args.dump_range:
            raise ValueError("Диапазон дампа должен быть в формате START:END.")
        start_str, end_str = args.dump_range.split(":")
        start_addr = int(start_str)
        end_addr = int(end_str)

        with open(program_path, "rb") as f:
            bytecode = f.read()

        memory = UVMMemory()

        # Запуск и вывод лога в консоль
        log = run_program(bytecode, memory)
        print(log)

        # Дамп памяти после выполнения
        dump_memory_to_csv(memory, start_addr, end_addr, dump_file)

    except FileNotFoundError:
        print(f"[ERROR] Файл программы не найден: {args.program}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Произошла ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()