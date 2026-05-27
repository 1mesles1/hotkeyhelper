import os
import sys
import tkinter as tk

VERSION = "0.0.1"
APP_NAME = "HotkeyHelper"
CONFIG_DIR = os.path.expanduser("~/.config/hotkeyhelper")

# Проверка флагов командной строки
if len(sys.argv) > 1:
    flag = sys.argv[1]
    if flag in ['-v', '--v']:
        print(f"{APP_NAME} version {VERSION}")
        sys.exit(0)
    elif flag in ['-h', '--h']:
        print(f"{APP_NAME} — A lightweight hotkey cheat sheet for tiling window managers.")
        print(f"\nConfiguration files are located at:\n  {CONFIG_DIR}/")
        print("\nUsage:")
        print("  hotkeyhelper          Show the GUI hotkey window")
        print("  -v, --v               Show application version")
        print("  -h, --h               Show this help message")
        sys.exit(0)

# Строгие настройки MATE Dark (делал ИИ)
DEFAULT_CONFIG = {
    "bg_color": "#2d3032",       # Темно-угольный фон окна
    "text_color": "#dfdfdf",     # Светло-серый текст описания
    "key_color": "#87a752",      # Фирменный приглушенный зеленый MATE
    "section_color": "#b4b4b4",  # Пепельный цвет для разделов
    "border_color": "#535d6c",   # Рамка вокруг самого окна подсказок
    "font_family": "Monospace",
    "key_font_size": 9,          # Размер для горячих клавиш
    "desc_font_size": 9,         # Размер для описаний
    "section_font_size": 10,     # Размер для разделов
    "title_text": "HotKeys",     # Текст настраиваемого заголовка
    "title_font_size": 7,        # Размер шрифта для заголовка
    "show_title": True,          # Включение/отключение заголовка (True/False)
    "_comments_en": {
        "bg_color": "Main window background color (HEX)",
        "text_color": "Hotkey description text color (HEX)",
        "key_color": "Hotkey text and outline border color (HEX)",
        "section_color": "Category headers [in brackets] text color (HEX)",
        "border_color": "1-pixel window outer border color (HEX)",
        "font_family": "System name of the monospace font",
        "key_font_size": "Font size for hotkeys in pixels",
        "desc_font_size": "Font size for description text in pixels",
        "section_font_size": "Font size for category headers in pixels",
        "title_text": "Inner title text centered on the top line",
        "title_font_size": "Inner title font size in pixels",
        "show_title": "Enable or disable the top inner title (true/false)"
    },
    "_comments_ru": {
        "bg_color": "Задний фон главного окна подсказок (HEX)",
        "text_color": "Цвет основного текста с описанием горячих клавиш (HEX)",
        "key_color": "Цвет текста клавиш и их скелетной рамки (HEX)",
        "section_color": "Цвет текста заголовков категорий [в скобках] (HEX)",
        "border_color": "Цвет линии рамки в 1 пиксель по контуру окна (HEX)",
        "font_family": "Системное имя моноширинного шрифта",
        "key_font_size": "Размер шрифта горячих клавиш в пикселях",
        "desc_font_size": "Размер шрифта текста описания в пикселях",
        "section_font_size": "Размер шрифта для разделов в пикселях",
        "title_text": "Текст внутреннего заголовка по центру верхней линии",
        "title_font_size": "Размер шрифта внутреннего заголовка в пикселях",
        "show_title": "Показывать верхний внутренний заголовок с линиями? (true/false)"
    }
}

# Текст подсказок по умолчанию
DEFAULT_TEXT_DATA = """[Управление окном]
Esc / Q              = Закрыть это окно подсказок
Стрелки / PgUp / PgDn = Прокрутка списка клавиш
Home / End           = В самый начало / конец списка

[Система]
Super + Shift + H    = Показать это окно (настройка i3)
"""

def load_or_create_config():
    import json
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    file_path = os.path.join(CONFIG_DIR, "config.json")
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=4)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_or_create_hotkeys():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    file_path = os.path.join(CONFIG_DIR, "hotkeys.txt")
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(DEFAULT_TEXT_DATA)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def close_app(event=None):
    root.destroy()

def scroll_up(event): canvas.yview_scroll(-2, "units")
def scroll_down(event): canvas.yview_scroll(2, "units")
def page_up(event): canvas.yview_scroll(-1, "pages")
def page_down(event): canvas.yview_scroll(1, "pages")
def go_home(event): canvas.yview_moveto(0)
def go_end(event): canvas.yview_moveto(1)

# Загрузка конфигурации и данных
config = load_or_create_config()
hotkey_lines = load_or_create_hotkeys()

# Безопасное извлечение параметров из конфига
bg_col = config.get("bg_color", DEFAULT_CONFIG["bg_color"])
txt_col = config.get("text_color", DEFAULT_CONFIG["text_color"])
key_col = config.get("key_color", DEFAULT_CONFIG["key_color"])
sec_col = config.get("section_color", DEFAULT_CONFIG["section_color"])
brd_col = config.get("border_color", DEFAULT_CONFIG["border_color"])
font_fam = config.get("font_family", DEFAULT_CONFIG["font_family"])
key_size = config.get("key_font_size", DEFAULT_CONFIG["key_font_size"])
desc_size = config.get("desc_font_size", DEFAULT_CONFIG["desc_font_size"])
sec_size = config.get("section_font_size", DEFAULT_CONFIG["section_font_size"])
t_text = config.get("title_text", DEFAULT_CONFIG["title_text"])
t_size = config.get("title_font_size", DEFAULT_CONFIG["title_font_size"])
show_title = config.get("show_title", DEFAULT_CONFIG["show_title"])


# Инициализация окна
root = tk.Tk(className='hotkeyhelper')
root.title(t_text)
root.configure(bg=bg_col)
root.wm_attributes('-type', 'dialog') 

# Главный фрейм для рамки в 1 пиксель по краю окна
main_border_frame = tk.Frame(root, bg=bg_col, highlightbackground=brd_col, highlightthickness=1)
main_border_frame.pack(fill="both", expand=True)

# --- НАЧАЛО: Внутренний кастомный заголовок с линиями ---
if show_title:
    header_frame = tk.Frame(main_border_frame, bg=bg_col)
    header_frame.pack(fill="x", padx=15, pady=(10, 5))

    # Левая линия
    left_line = tk.Frame(header_frame, bg=brd_col, height=1)
    left_line.pack(side="left", fill="x", expand=True)

    # Текст заголовка (с одним пробелом по бокам)
    title_label = tk.Label(
        header_frame, 
        text=f" {t_text} ", 
        fg=brd_col, 
        bg=bg_col, 
        font=(font_fam, t_size, "bold")
    )
    title_label.pack(side="left")

    # Правая линия
    right_line = tk.Frame(header_frame, bg=brd_col, height=1)
    right_line.pack(side="left", fill="x", expand=True)
# --- КОНЕЦ: Внутренний заголовок ---

# Холст для скроллинга
canvas = tk.Canvas(main_border_frame, bg=bg_col, bd=0, highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True, pady=(0, 10))

scrollable_frame = tk.Frame(canvas, bg=bg_col)
scrollable_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_frame_configure)

scrollable_frame.columnconfigure(0, weight=0)
scrollable_frame.columnconfigure(1, weight=0)
scrollable_frame.columnconfigure(2, weight=1)

current_row = 0
is_first_section = True

# Анализ данных для расчета выравнивания колонок
max_key_len = 0
max_chars = 0

for line in hotkey_lines:
    clean_line = line.strip()
    if not clean_line:
        continue
    if clean_line.startswith("[") and clean_line.endswith("]"):
        line_len = len(clean_line)
    elif "=" in clean_line:
        parts = clean_line.split("=", 1)
        key_part = parts[0].strip()
        desc_part = parts[1].strip()
        if len(key_part) > max_key_len:
            max_key_len = len(key_part)
        line_len = max_key_len + len(desc_part) + 4
    else:
        line_len = len(clean_line)
        
    if line_len > max_chars:
        max_chars = line_len

# Отрисовка интерфейса на основе Grid
for line in hotkey_lines:
    clean_line = line.strip()
    if not clean_line:
        continue
        
    if clean_line.startswith("[") and clean_line.endswith("]"):
        section_text = clean_line[1:-1].upper()
        top_pad = 0 if is_first_section else 15
        is_first_section = False
        
        section_label = tk.Label(
            scrollable_frame,
            text=section_text,
            fg=sec_col,
            bg=bg_col,
            font=(font_fam, sec_size, "bold"), # <-- ЗАМЕНИТЬ НА sec_size
            pady=4
        )
        section_label.grid(row=current_row, column=0, columnspan=3, sticky="w", padx=15, pady=(top_pad, 4))
        current_row += 1
        
    elif "=" in clean_line:
        parts = clean_line.split("=", 1)
        key_part = parts[0].strip()
        desc_part = parts[1].strip()
        
        # СКЕЛЕТНЫЙ СТИЛЬ
        key_frame = tk.Frame(
            scrollable_frame, 
            bg=bg_col,
            padx=7, 
            pady=2,
            highlightbackground=key_col,
            highlightthickness=1
        )
        key_frame.grid(row=current_row, column=0, sticky="w", padx=(20, 10), pady=4)
        
        key_label = tk.Label(
            key_frame,
            text=key_part,
            fg=key_col,      
            bg=bg_col,
            font=(font_fam, key_size, "bold")
        )
        key_label.pack()
        
        # Точка-разделитель
        dots_label = tk.Label(
            scrollable_frame,
            text="·",
            fg=brd_col,
            bg=bg_col,
            font=(font_fam, desc_size)
        )
        dots_label.grid(row=current_row, column=1, sticky="w", padx=3)
        
        # Текст описания
        desc_label = tk.Label(
            scrollable_frame,
            text=desc_part,
            fg=txt_col,
            bg=bg_col,
            font=(font_fam, desc_size),
            justify="left",
            anchor="w"
        )
        desc_label.grid(row=current_row, column=2, sticky="w", padx=(10, 20), pady=4)
        
        current_row += 1

root.update_idletasks()

# Рассчитываем размеры под шрифт размера 9
char_width_pixels = int(key_size * 0.66)
text_width = (max_chars * char_width_pixels) + 70

# Учитываем, что заголовок тоже требует минимальной ширины окна
min_title_width = (len(t_text) * int(t_size * 0.65)) + 100

req_width = max(scrollable_frame.winfo_reqwidth() + 12, text_width, min_title_width)
req_height = scrollable_frame.winfo_reqheight() + 55  # Добавили запас под верхний заголовок

canvas.itemconfig(scrollable_frame_id, width=req_width)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

max_width = int(screen_width * 0.5)
max_height = int(screen_height * 0.5)

final_width = min(max(req_width, 360), max_width)
final_height = min(max(req_height, 120), max_height)

x = (screen_width // 2) - (final_width // 2)
y = (screen_height // 2) - (final_height // 2)

root.geometry(f"{final_width}x{final_height}+{x}+{y}")
root.maxsize(max_width, max_height)

# Привязка клавиш управления
root.bind("<Escape>", close_app)
root.bind("<Key-q>", close_app)
root.bind("<Key-Q>", close_app)
root.bind("<Up>", scroll_up)
root.bind("<Down>", scroll_down)
root.bind("<Prior>", page_up)
root.bind("<Next>", page_down)
root.bind("<Home>", go_home)
root.bind("<End>", go_end)

if __name__ == "__main__":
    root.mainloop()

