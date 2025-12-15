import argparse
from uvm_asm import full_asm, print_ir_test_mode

def main():
    parser = argparse.ArgumentParser(description="Ассемблер УВМ (вариант 14)")
    parser.add_argument("input", help="Входной ASM файл")
    parser.add_argument("output", help="Выходной бинарный файл")
    parser.add_argument("-t", "--test", action="store_true", help="Режим тестирования")
    
    args = parser.parse_args()
    
    with open(args.input, 'r') as f:
        source = f.read()
    
    try:
        bytecode, IR = full_asm(source)
        
        if args.test:
            print_ir_test_mode(IR, bytecode)
            print(f"\n[INFO] Сгенерировано команд: {len(IR)}")
        
        with open(args.output, 'wb') as f:
            f.write(bytecode)
            
        print(f"[INFO] Успешно ассемблировано. Размер: {len(bytecode)} байт")
        
    except Exception as e:
        print(f"[ERROR] Ошибка ассемблирования: {e}")
        exit(1)

if __name__ == "__main__":
    main()