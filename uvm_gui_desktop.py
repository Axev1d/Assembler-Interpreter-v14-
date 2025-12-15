# uvm_gui_desktop_var14.py

import tkinter as tk
from tkinter import ttk, messagebox

from core_runner import run_uvm_source


class UvmGuiApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("УВМ — вариант 14 (десктопный GUI)")
        self.geometry("1000x600")

        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        # Верхняя панель с кнопкой
        self.toolbar = ttk.Frame(self)
        self.btn_run = ttk.Button(
            self.toolbar,
            text="Ассемблировать и выполнить",
            command=self.on_run_clicked
        )

        # Метки
        self.editor_label = ttk.Label(self, text="Исходный код (ASM, формат: команда аргумент):")
        self.output_label = ttk.Label(self, text="Вывод (байт-код + лог + дамп памяти в CSV):")

        # Текстовые поля
        self.editor = tk.Text(self, wrap="none")
        self.output = tk.Text(self, wrap="none", state="disabled")

        # Скроллбары редактора
        self.editor_scroll_y = ttk.Scrollbar(
            self, orient="vertical", command=self.editor.yview
        )
        self.editor_scroll_x = ttk.Scrollbar(
            self, orient="horizontal", command=self.editor.xview
        )
        self.editor.configure(
            yscrollcommand=self.editor_scroll_y.set,
            xscrollcommand=self.editor_scroll_x.set,
        )

        # Скроллбары вывода
        self.output_scroll_y = ttk.Scrollbar(
            self, orient="vertical", command=self.output.yview
        )
        self.output_scroll_x = ttk.Scrollbar(
            self, orient="horizontal", command=self.output.xview
        )
        self.output.configure(
            yscrollcommand=self.output_scroll_y.set,
            xscrollcommand=self.output_scroll_x.set,
        )

        # Стартовый текст с примерами
        self.editor.insert(
            "1.0",
            "# Пример программы из спецификации (вариант 14)\n"
            "# Формат: команда пробел аргумент\n"
            "# Команды: load_const, read_value, write_value, sgn\n\n"
            "load_const 831      # A=14, B=831 → 0xFE 0x33 0x00\n"
            "read_value 97       # A=11, B=97 → 0x1B 0x06 0x00\n"
            "write_value 291     # A=7, B=291 → 0x37 0x12 0x00\n"
            "sgn 158             # A=4, B=158 → 0xE4 0x09 0x00\n\n"
            "# Пример для тестовой задачи (sgn над вектором длины 10)\n"
            "# load_const 10\n"
            "# ... программа будет дописана ...\n"
        )

    def _layout_widgets(self):
        # Настраиваем сетку
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Toolbar
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky="we")
        self.btn_run.pack(side="left", padx=5, pady=5)

        # Метки
        self.editor_label.grid(row=1, column=0, sticky="w", padx=5, pady=(5, 0))
        self.output_label.grid(row=1, column=1, sticky="w", padx=5, pady=(5, 0))

        # Редактор
        self.editor.grid(row=2, column=0, sticky="nsew", padx=(5, 0), pady=5)
        self.editor_scroll_y.grid(row=2, column=0, sticky="nse", padx=(0, 0), pady=5)
        self.editor_scroll_x.grid(row=3, column=0, sticky="we", padx=(5, 0))

        # Окно вывода
        self.output.grid(row=2, column=1, sticky="nsew", padx=(5, 5), pady=5)
        self.output_scroll_y.grid(row=2, column=1, sticky="nse", padx=(0, 5), pady=5)
        self.output_scroll_x.grid(row=3, column=1, sticky="we", padx=(5, 5))

    def on_run_clicked(self):
        source = self.editor.get("1.0", "end")

        try:
            result_text = run_uvm_source(source)
        except Exception as e:
            messagebox.showerror("Ошибка выполнения", f"{type(e).__name__}: {e}")
            return

        # Выводим результат
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", result_text)
        self.output.configure(state="disabled")


def main():
    app = UvmGuiApp()
    app.mainloop()


if __name__ == "__main__":
    main()