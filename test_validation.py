# test_validation.py
def validate_test_sequences():
    """Проверяем соответствие тестовым последовательностям из ТЗ"""
    
    # Тест 1: load_const (A=14, B=831)
    # 14 | (831 << 4) = 14 + 13296 = 13310 = 0x33FE
    # В little-endian: FE 33 00
    test1 = bytes([0xFE, 0x33, 0x00])
    value = int.from_bytes(test1, 'little')
    a = value & 0x0F  # 14
    b = value >> 4    # 831
    print(f"Test 1: A={a}, B={b} (ожидается A=14, B=831)")
    
    # Тест 2: read_value (A=11, B=97)
    # 11 | (97 << 4) = 11 + 1552 = 1563 = 0x061B
    # Little-endian: 1B 06 00
    test2 = bytes([0x1B, 0x06, 0x00])
    value = int.from_bytes(test2, 'little')
    a = value & 0x0F  # 11
    b = value >> 4    # 97
    print(f"Test 2: A={a}, B={b} (ожидается A=11, B=97)")
    
    # Тест 3: write_value (A=7, B=291)
    # 7 | (291 << 4) = 7 + 4656 = 4663 = 0x1237
    # Little-endian: 37 12 00
    test3 = bytes([0x37, 0x12, 0x00])
    value = int.from_bytes(test3, 'little')
    a = value & 0x0F  # 7
    b = value >> 4    # 291
    print(f"Test 3: A={a}, B={b} (ожидается A=7, B=291)")
    
    # Тест 4: sgn (A=4, B=158)
    # 4 | (158 << 4) = 4 + 2528 = 2532 = 0x09E4
    # Little-endian: E4 09 00
    test4 = bytes([0xE4, 0x09, 0x00])
    value = int.from_bytes(test4, 'little')
    a = value & 0x0F  # 4
    b = value >> 4    # 158
    print(f"Test 4: A={a}, B={b} (ожидается A=4, B=158)")

if __name__ == "__main__":
    validate_test_sequences()