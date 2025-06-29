import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, simpledialog
import os

class NotepadGUI:
    def __init__(self, master):
        self.master = master
        master.title("Easy Notepad")
        master.geometry("800x600")

        self.languages = {
            "en": {
                "title": "Easy Notepad",
                "file_menu": "File",
                "edit_menu": "Edit",
                "language_menu": "Language",
                "new_note": "New Note",
                "open_note": "Open Note",
                "save_note": "Save Note",
                "save_as": "Save As...",
                "delete_note": "Delete Note",
                "exit": "Exit",
                "show_line_numbers": "Show Line Numbers",
                "hide_line_numbers": "Hide Line Numbers",
                "note_title": "Note Title",
                "enter_title": "Enter the title for your note:",
                "note_saved_success": "Note '{title}' saved successfully!",
                "note_deleted_success": "Note '{title}' deleted successfully!",
                "note_not_found": "Note not found!",
                "no_note_open": "No note is currently open.",
                "save_changes_prompt": "Do you want to save changes to the current note?",
                "untitled": "Untitled",
                "all_files": "All Files",
                "text_files": "Text Files",
                "error": "Error",
                "warning": "Warning",
                "about": "About",
                "about_message": "Easy Notepad\nVersion 1.0\nCreated with Tkinter",
            },
            "cs": {
                "title": "Snadný Poznámkový Blok",
                "file_menu": "Soubor",
                "edit_menu": "Úpravy",
                "language_menu": "Jazyk",
                "new_note": "Nový Zápisek",
                "open_note": "Otevřít Zápisek",
                "save_note": "Uložit Zápisek",
                "save_as": "Uložit jako...",
                "delete_note": "Smazat Zápisek",
                "exit": "Ukončit",
                "show_line_numbers": "Zobrazit Čísla Řádků",
                "hide_line_numbers": "Skrýt Čísla Řádků",
                "note_title": "Název Zápisku",
                "enter_title": "Zadejte název pro váš zápisek:",
                "note_saved_success": "Zápisek '{title}' byl úspěšně uložen!",
                "note_deleted_success": "Zápisek '{title}' byl úspěšně smazán!",
                "note_not_found": "Zápisek nenalezen!",
                "no_note_open": "Momentálně není otevřen žádný zápisek.",
                "save_changes_prompt": "Chcete uložit změny do aktuálního zápisku?",
                "untitled": "Bezejmenný",
                "all_files": "Všechny soubory",
                "text_files": "Textové soubory",
                "error": "Chyba",
                "warning": "Upozornění",
                "about": "O aplikaci",
                "about_message": "Snadný Poznámkový Blok\nVerze 1.0\nVytvořeno pomocí Tkinter",
            },
            "es": {
                "title": "Bloc de Notas Fácil",
                "file_menu": "Archivo",
                "edit_menu": "Editar",
                "language_menu": "Idioma",
                "new_note": "Nueva Nota",
                "open_note": "Abrir Nota",
                "save_note": "Guardar Nota",
                "save_as": "Guardar como...",
                "delete_note": "Eliminar Nota",
                "exit": "Salir",
                "show_line_numbers": "Mostrar Números de Línea",
                "hide_line_numbers": "Ocultar Números de Línea",
                "note_title": "Título de la Nota",
                "enter_title": "Ingrese el título para su nota:",
                "note_saved_success": "¡Nota '{title}' guardada exitosamente!",
                "note_deleted_success": "¡Nota '{title}' eliminada exitosamente!",
                "note_not_found": "¡Nota no encontrada!",
                "no_note_open": "Actualmente no hay ninguna nota abierta.",
                "save_changes_prompt": "¿Desea guardar los cambios en la nota actual?",
                "untitled": "Sin título",
                "all_files": "Todos los archivos",
                "text_files": "Archivos de texto",
                "error": "Error",
                "warning": "Advertencia",
                "about": "Acerca de",
                "about_message": "Bloc de Notas Fácil\nVersión 1.0\nCreado con Tkinter",
            },
            "de": {
                "title": "Einfacher Notizblock",
                "file_menu": "Datei",
                "edit_menu": "Bearbeiten",
                "language_menu": "Sprache",
                "new_note": "Neue Notiz",
                "open_note": "Notiz Öffnen",
                "save_note": "Notiz Speichern",
                "save_as": "Speichern unter...",
                "delete_note": "Notiz Löschen",
                "exit": "Beenden",
                "show_line_numbers": "Zeilennummern Anzeigen",
                "hide_line_numbers": "Zeilennummern Ausblenden",
                "note_title": "Notiztitel",
                "enter_title": "Geben Sie den Titel für Ihre Notiz ein:",
                "note_saved_success": "Notiz '{title}' erfolgreich gespeichert!",
                "note_deleted_success": "Notiz '{title}' erfolgreich gelöscht!",
                "note_not_found": "Notiz nicht gefunden!",
                "no_note_open": "Derzeit ist keine Notiz geöffnet.",
                "save_changes_prompt": "Möchten Sie die Änderungen an der aktuellen Notiz speichern?",
                "untitled": "Unbenannt",
                "all_files": "Alle Dateien",
                "text_files": "Textdateien",
                "error": "Fehler",
                "warning": "Warnung",
                "about": "Über",
                "about_message": "Einfacher Notizblock\nVersion 1.0\nErstellt mit Tkinter",
            },
            "uk": {
                "title": "Легкий Блокнот",
                "file_menu": "Файл",
                "edit_menu": "Редагувати",
                "language_menu": "Мова",
                "new_note": "Нова Нотатка",
                "open_note": "Відкрити Нотатку",
                "save_note": "Зберегти Нотатку",
                "save_as": "Зберегти як...",
                "delete_note": "Видалити Нотатку",
                "exit": "Вихід",
                "show_line_numbers": "Показати Номери Рядків",
                "hide_line_numbers": "Приховати Номери Рядків",
                "note_title": "Назва Нотатки",
                "enter_title": "Введіть назву для вашої нотатки:",
                "note_saved_success": "Нотатка '{title}' успішно збережена!",
                "note_deleted_success": "Нотатка '{title}' успішно видалена!",
                "note_not_found": "Нотатка не знайдена!",
                "no_note_open": "Наразі жодна нотатка не відкрита.",
                "save_changes_prompt": "Ви хочете зберегти зміни в поточній нотатці?",
                "untitled": "Без назви",
                "all_files": "Усі файли",
                "text_files": "Текстові файли",
                "error": "Помилка",
                "warning": "Попередження",
                "about": "Про програму",
                "about_message": "Легкий Блокнот\nВерсія 1.0\nСтворено за допомогою Tkinter",
            },
            "zh": {
                "title": "简易记事本",
                "file_menu": "文件",
                "edit_menu": "编辑",
                "language_menu": "语言",
                "new_note": "新建笔记",
                "open_note": "打开笔记",
                "save_note": "保存笔记",
                "save_as": "另存为...",
                "delete_note": "删除笔记",
                "exit": "退出",
                "show_line_numbers": "显示行号",
                "hide_line_numbers": "隐藏行号",
                "note_title": "笔记标题",
                "enter_title": "请输入笔记标题：",
                "note_saved_success": "笔记“{title}”保存成功！",
                "note_deleted_success": "笔记“{title}”删除成功！",
                "note_not_found": "未找到笔记！",
                "no_note_open": "当前没有打开的笔记。",
                "save_changes_prompt": "是否保存当前笔记的更改？",
                "untitled": "无标题",
                "all_files": "所有文件",
                "text_files": "文本文件",
                "error": "错误",
                "warning": "警告",
                "about": "关于",
                "about_message": "简易记事本\n版本 1.0\n使用 Tkinter 创建",
            },
            "ja": {
                "title": "簡易メモ帳",
                "file_menu": "ファイル",
                "edit_menu": "編集",
                "language_menu": "言語",
                "new_note": "新規メモ",
                "open_note": "メモを開く",
                "save_note": "メモを保存",
                "save_as": "名前を付けて保存...",
                "delete_note": "メモを削除",
                "exit": "終了",
                "show_line_numbers": "行番号を表示",
                "hide_line_numbers": "行番号を非表示",
                "note_title": "メモのタイトル",
                "enter_title": "メモのタイトルを入力してください：",
                "note_saved_success": "メモ「{title}」が正常に保存されました！",
                "note_deleted_success": "メモ「{title}」が正常に削除されました！",
                "note_not_found": "メモが見つかりません！",
                "no_note_open": "現在開いているメモはありません。",
                "save_changes_prompt": "現在のメモへの変更を保存しますか？",
                "untitled": "無題",
                "all_files": "すべてのファイル",
                "text_files": "テキストファイル",
                "error": "エラー",
                "warning": "警告",
                "about": "について",
                "about_message": "簡易メモ帳\nバージョン 1.0\nTkinterで作成",
            },
        }

        self.current_language = "en"
        self.current_note_path = None
        self.text_widget_modified = False

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Main frame
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        # Line numbers canvas
        self.line_numbers_canvas = tk.Canvas(self.main_frame, width=30, bg="lightgray")
        self.line_numbers_canvas.pack(side=tk.LEFT, fill=tk.Y)
        self.show_line_numbers_var = tk.BooleanVar(value=True)

        # Text area
        self.text_area = scrolledtext.ScrolledText(self.main_frame, wrap="word", undo=True)
        self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.text_area.bind("<KeyRelease>", self.on_text_change)
        self.text_area.bind("<MouseWheel>", self._scroll_text_and_lines)
        self.text_area.bind("<Button-4>", self._scroll_text_and_lines) # For Linux
        self.text_area.bind("<Button-5>", self._scroll_text_and_lines) # For Linux

        self.text_area.vbar.config(command=self._scroll_line_numbers)
        self.line_numbers_canvas.bind("<Configure>", self._redraw_line_numbers)

        self.create_menu()
        self.update_ui_texts()
        self._redraw_line_numbers()

    def get_text(self, key):
        return self.languages[self.current_language].get(key, key)

    def update_ui_texts(self):
        self.master.title(self.get_text("title"))
        self.file_menu.entryconfig(0, label=self.get_text("new_note"))
        self.file_menu.entryconfig(1, label=self.get_text("open_note"))
        self.file_menu.entryconfig(2, label=self.get_text("save_note"))
        self.file_menu.entryconfig(3, label=self.get_text("save_as"))
        self.file_menu.entryconfig(5, label=self.get_text("delete_note"))
        self.file_menu.entryconfig(7, label=self.get_text("exit"))

        self.edit_menu.entryconfig(0, label=self.get_text("show_line_numbers") if not self.show_line_numbers_var.get() else self.get_text("hide_line_numbers"))
        self.main_menu.entryconfig(1, label=self.get_text("file_menu"))
        self.main_menu.entryconfig(2, label=self.get_text("edit_menu"))
        self.main_menu.entryconfig(3, label=self.get_text("language_menu"))


    def create_menu(self):
        self.main_menu = tk.Menu(self.master)
        self.master.config(menu=self.main_menu)

        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New Note", command=self.new_note)
        self.file_menu.add_command(label="Open Note", command=self.open_note)
        self.file_menu.add_command(label="Save Note", command=self.save_note)
        self.file_menu.add_command(label="Save As...", command=self.save_note_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Delete Note", command=self.delete_note)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.on_closing)

        self.edit_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Show Line Numbers", command=self.toggle_line_numbers)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="About", command=self.show_about)


        self.language_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Language", menu=self.language_menu)
        for lang_code, lang_data in self.languages.items():
            self.language_menu.add_command(label=lang_data["title"].split(" ")[-1] if " " in lang_data["title"] else lang_data["title"], command=lambda code=lang_code: self.change_language(code))

    def on_text_change(self, event=None):
        self.text_widget_modified = True
        self._redraw_line_numbers()

    def _redraw_line_numbers(self, event=None):
        if not self.show_line_numbers_var.get():
            self.line_numbers_canvas.pack_forget()
            return
        else:
            self.line_numbers_canvas.pack(side=tk.LEFT, fill=tk.Y)

        self.line_numbers_canvas.delete("all")

        i = self.text_area.index("@0,0")
        while True:
            dline = self.text_area.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            line_num = str(int(float(i)))
            self.line_numbers_canvas.create_text(2, y, anchor="nw", text=line_num, font=("Consolas", 10))
            i = self.text_area.index("%s+1line" % i)

    def _scroll_line_numbers(self, *args):
        self.text_area.yview(*args)
        self._redraw_line_numbers()

    def _scroll_text_and_lines(self, event):
        self.text_area.yview_scroll(-1 * (event.delta // 120), "units")
        self._redraw_line_numbers()
        return "break" # Prevents default scroll behavior if needed

    def toggle_line_numbers(self):
        self.show_line_numbers_var.set(not self.show_line_numbers_var.get())
        if self.show_line_numbers_var.get():
            self.line_numbers_canvas.pack(side=tk.LEFT, fill=tk.Y)
            self._redraw_line_numbers()
            self.edit_menu.entryconfig(0, label=self.get_text("hide_line_numbers"))
        else:
            self.line_numbers_canvas.pack_forget()
            self.edit_menu.entryconfig(0, label=self.get_text("show_line_numbers"))


    def new_note(self):
        if self.text_widget_modified:
            if messagebox.askyesno(self.get_text("warning"), self.get_text("save_changes_prompt")):
                self.save_note()
        self.text_area.delete(1.0, tk.END)
        self.current_note_path = None
        self.text_widget_modified = False
        self.master.title(self.get_text("untitled") + " - " + self.get_text("title"))
        self._redraw_line_numbers()

    def open_note(self):
        if self.text_widget_modified:
            if messagebox.askyesno(self.get_text("warning"), self.get_text("save_changes_prompt")):
                self.save_note()

        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[
                (self.get_text("text_files"), "*.txt"),
                (self.get_text("all_files"), "*.*")
            ]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.current_note_path = file_path
                self.text_widget_modified = False
                self.master.title(os.path.basename(file_path) + " - " + self.get_text("title"))
                self._redraw_line_numbers()
            except Exception as e:
                messagebox.showerror(self.get_text("error"), f"Failed to open file: {e}")

    def save_note(self):
        if self.current_note_path:
            try:
                with open(self.current_note_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo(self.get_text("title"), self.get_text("note_saved_success").format(title=os.path.basename(self.current_note_path)))
                self.text_widget_modified = False
            except Exception as e:
                messagebox.showerror(self.get_text("error"), f"Failed to save file: {e}")
        else:
            self.save_note_as()

    def save_note_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                (self.get_text("text_files"), "*.txt"),
                (self.get_text("all_files"), "*.*")
            ]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.current_note_path = file_path
                messagebox.showinfo(self.get_text("title"), self.get_text("note_saved_success").format(title=os.path.basename(file_path)))
                self.text_widget_modified = False
                self.master.title(os.path.basename(file_path) + " - " + self.get_text("title"))
            except Exception as e:
                messagebox.showerror(self.get_text("error"), f"Failed to save file: {e}")

    def delete_note(self):
        if not self.current_note_path:
            messagebox.showinfo(self.get_text("warning"), self.get_text("no_note_open"))
            return

        note_title = os.path.basename(self.current_note_path)
        if messagebox.askyesno(self.get_text("warning"), f"Are you sure you want to delete '{note_title}'?"):
            try:
                os.remove(self.current_note_path)
                messagebox.showinfo(self.get_text("title"), self.get_text("note_deleted_success").format(title=note_title))
                self.new_note() # Clear the text area after deletion
            except OSError:
                messagebox.showerror(self.get_text("error"), self.get_text("note_not_found"))
            except Exception as e:
                messagebox.showerror(self.get_text("error"), f"Failed to delete note: {e}")

    def change_language(self, lang_code):
        self.current_language = lang_code
        self.update_ui_texts()
        # Update the title in case a note is open
        if self.current_note_path:
            self.master.title(os.path.basename(self.current_note_path) + " - " + self.get_text("title"))
        else:
            self.master.title(self.get_text("untitled") + " - " + self.get_text("title"))

    def show_about(self):
        messagebox.showinfo(self.get_text("about"), self.get_text("about_message"))

    def on_closing(self):
        if self.text_widget_modified:
            if messagebox.askyesno(self.get_text("warning"), self.get_text("save_changes_prompt")):
                self.save_note()
        self.master.destroy()

def main():
    root = tk.Tk()
    app = NotepadGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()