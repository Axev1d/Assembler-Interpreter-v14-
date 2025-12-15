# test.asm
# Тестовая программа для варианта 14
# Проверяет все команды спецификации

# 1. Загрузка константы на стек (A=14, B=831)
load_const 831

# 2. Чтение значения из памяти на стек (A=11, B=97)
#    Сначала положим что-то в память для чтения
load_const 42
write_value 97   # MEM[97] = 42
read_value 97    # должно прочитать 42

# 3. Запись значения с вершины стека в память (A=7, B=291)
load_const 777
write_value 291  # MEM[291] = 777

# 4. Вычисление знака (A=4, B=158)
#    Подготовим разные значения в памяти
load_const 10
write_value 200   # положительное
load_const 0
write_value 201   # ноль
load_const -5
write_value 202   # отрицательное

# Теперь sgn для каждого
sgn 200   # должно дать 1
sgn 201   # должно дать 0
sgn 202   # должно дать -1

# 5. Пример для тестовой задачи: sgn над вектором длины 10
#    Создаем вектор [5, -3, 0, 7, -2, 0, 1, -8, 0, 4] по адресам 500-509
load_const 5
write_value 500
load_const -3
write_value 501
load_const 0
write_value 502
load_const 7
write_value 503
load_const -2
write_value 504
load_const 0
write_value 505
load_const 1
write_value 506
load_const -8
write_value 507
load_const 0
write_value 508
load_const 4
write_value 509

# Применяем sgn ко всем элементам, сохраняем в новый вектор по адресам 600-609
read_value 500
sgn 500
write_value 600

read_value 501
sgn 501
write_value 601

read_value 502
sgn 502
write_value 602

read_value 503
sgn 503
write_value 603

read_value 504
sgn 504
write_value 604

read_value 505
sgn 505
write_value 605

read_value 506
sgn 506
write_value 606

read_value 507
sgn 507
write_value 607

read_value 508
sgn 508
write_value 608

read_value 509
sgn 509
write_value 609