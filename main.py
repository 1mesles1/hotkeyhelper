import json
import tkinter as tk

def load_json(filename):
    """Безопасно загружает данные из JSON-файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка чтения файла {filename}: {e}")
        exit(1)

def close_app(event=None):
    """Закрывает программу."""
    root.destroy()

# Функции для прокрутки текста с клавиатуры
def scroll_up(event): text_box.yview_scroll(-1, "units")
def scroll_down(event): text_box.yview_scroll(1, "units")
def page_up(event): text_box.yview_scroll(-1, "pages")
def page_down(event): text_box.yview_scroll(1, "pages")
def go_home(event): text_box.see("1.0")
def go_end(event): text_box.see("end")

# 1. Загрузка данных
config = load_json("config.json")
hotkeys = load_json("hotkeys.json")

# Находим самую длинную строку и количество строк для правильного масштаба
max_chars = 0
total_lines = len(hotkeys)

for item in hotkeys:
    line_len = len(item['key']) + len(item['description']) + 3 # +3 для " — "
    if line_len > max_chars:
        max_chars = line_len

# 2. Создание главного окна с указанием класса для i3wm
root = tk.Tk(className='hotkeyhelper')
root.title("Hotkey Helper")
root.configure(bg=config["bg_color"])

# Говорим i3wm, что это диалоговое (плавающее) окно
root.wm_attributes('-type', 'dialog') 

# 3. Настройка текстового поля (задаем ширину в СИМВОЛАХ, а высоту в СТРОКАХ)
text_box = tk.Text(
    root, 
    bg=config["bg_color"], 
    fg=config["text_color"],
    font=(config["font_family"], config["font_size"]),
    bd=0,
    highlightthickness=0,
    padx=15,
    pady=15,
    wrap="word",
    width=max_chars + 2,   # Ширина ровно под самую длинную строку + запас
    height=total_lines     # Высота ровно по количеству строк
)
text_box.pack(expand=True, fill="both")

# Создаем "теги" для раскраски текста
text_box.tag_config("key_style", foreground=config["key_color"], font=(config["font_family"], config["font_size"], "bold"))
text_box.tag_config("desc_style", foreground=config["text_color"])

# 4. Заполнение текстом
for item in hotkeys:
    key_str = f"{item['key']}"
    desc_str = f" — {item['description']}\n"
    
    text_box.insert("end", key_str, "key_style")
    text_box.insert("end", desc_str, "desc_style")

# Делаем текст доступным только для чтения
text_box.config(state="disabled")

# 5. ОГРАНИЧЕНИЕ ДО 50% ЭКРАНА И ЦЕНТРИРОВАНИЕ
root.update_idletasks()

# Получаем размеры, которые Tkinter насчитал на основе символов и строк
req_width = root.winfo_reqwidth()
req_height = root.winfo_reqheight()

# Получаем физические размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

max_width = int(screen_width * 0.5)
max_height = int(screen_height * 0.5)

# Если окно получилось больше 50% экрана, сжимаем его до 50%
final_width = min(req_width, max_width)
final_height = min(req_height, max_height)

# Вычисляем координаты центра
x = (screen_width // 2) - (final_width // 2)
y = (screen_height // 2) - (final_height // 2)

# Применяем точную геометрию и лимиты
root.geometry(f"{final_width}x{final_height}+{x}+{y}")
root.maxsize(max_width, max_height)

# 6. Навигация и закрытие (Привязка клавиш)
root.bind("<Escape>", close_app)
root.bind("<Key-q>", close_app)
root.bind("<Key-Q>", close_app)

root.bind("<Up>", scroll_up)
root.bind("<Down>", scroll_down)
root.bind("<Prior>", page_up)     # PageUp
root.bind("<Next>", page_down)   # PageDown
root.bind("<Home>", go_home)
root.bind("<End>", go_end)

if __name__ == "__main__":
    root.mainloop()

