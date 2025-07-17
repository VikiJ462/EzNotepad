import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog, QMessageBox,
    QTabWidget, QVBoxLayout, QWidget, QMenuBar, QMenu, QStyleFactory
)
from PyQt6.QtGui import (
    QAction, QTextCharFormat, QColor, QFont, QSyntaxHighlighter,
    QTextDocument, QPalette, QFontMetricsF, QTextCursor
)
from PyQt6.QtCore import Qt, QRegularExpression

# Nová třída pro QTextEdit s automatickým odsazováním
class TextEditWithAutoIndent(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Nastavení šířky tabulátoru na 4 mezery
        self.setTabStopDistance(QFontMetricsF(self.font()).horizontalAdvance(' ') * 4)

    def keyPressEvent(self, event):
        # Automatické odsazení po '{' a Enter
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            cursor = self.textCursor()
            
            # Získat text aktuálního bloku (řádku) PŘED zpracováním Enter
            current_block_text = cursor.block().text()
            
            # Vypočítat existující odsazení
            leading_whitespace = ""
            for char in current_block_text:
                if char == ' ' or char == '\t':
                    leading_whitespace += char
                else:
                    break
            
            # Necháme základní třídu zpracovat událost klávesy Enter (vloží nový řádek a posune kurzor)
            super().keyPressEvent(event) 

            # Nyní je kurzor na nově vytvořeném řádku.
            new_cursor = self.textCursor()
            
            # Vložit úvodní prázdné znaky z předchozího řádku
            new_cursor.insertText(leading_whitespace)

            # Pokud předchozí řádek končil znakem '{', přidáme další tabulátor
            if current_block_text.strip().endswith('{'):
                new_cursor.insertText('\t') # Přidat jeden další tabulátor
            
            self.setTextCursor(new_cursor)
        
        # Automatické zrušení odsazení po '}'
        elif event.text() == '}':
            cursor = self.textCursor()
            
            # Necháme základní třídu zpracovat událost klávesy '}' (vloží '}')
            super().keyPressEvent(event)

            # Po vložení '}' získáme aktualizovaný kurzor a text bloku.
            cursor = self.textCursor()
            block_text = cursor.block().text()

            # Zkontrolovat, zda je '}' prvním neprázdným znakem a zda existuje úvodní odsazení
            stripped_block_text = block_text.strip()
            if stripped_block_text.startswith('}'):
                # Vypočítat délku úvodního prázdného místa
                leading_whitespace_length = len(block_text) - len(block_text.lstrip())

                if leading_whitespace_length > 0:
                    cursor.beginEditBlock()
                    # Přesunout kurzor na začátek řádku
                    cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
                    # Smazat jeden tabulátor nebo 4 mezery.
                    if block_text.startswith('\t'):
                        cursor.deleteChar()
                    elif block_text.startswith('    '):
                        for _ in range(4):
                            cursor.deleteChar()
                    cursor.endEditBlock()
                self.setTextCursor(cursor)
        else:
            # Pro všechny ostatní klávesy necháme základní třídu, aby je zpracovala
            super().keyPressEvent(event)


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.highlightingRules = []

        # Keywords (e.g., print, if, else) - Orange
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor("#FF9900")) # Orange
        keywords = [
            "False", "None", "True", "and", "as", "assert", "async", "await",
            "break", "class", "continue", "def", "del", "elif", "else",
            "except", "finally", "for", "from", "global", "if", "import",
            "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise",
            "return", "try", "while", "with", "yield"
        ]
        self.highlightingRules.extend([(QRegularExpression(r"\b" + keyword + r"\b"), keywordFormat)
                                       for keyword in keywords])

        # Strings (e.g., "hello world", 'single quote string') - Pink
        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor("#FF69B4")) # Pink
        self.highlightingRules.append((QRegularExpression(r"\"[^\"\\]*(\\[\s\S][^\"\\]*)*\""), stringFormat))
        self.highlightingRules.append((QRegularExpression(r"\'[^\'\\]*(\\[\s\S][^\'\\]*)*\'"), stringFormat))

        # Numbers - Light Blue
        numberFormat = QTextCharFormat()
        numberFormat.setForeground(QColor("#87CEEB")) # Light Blue
        self.highlightingRules.append((QRegularExpression(r"\b[0-9]+(\.[0-9]+)?\b"), numberFormat))

        # Comments (e.g., # This is a comment) - Greenish Gray
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor("#808080")) # Gray (Dark mode friendly)
        self.highlightingRules.append((QRegularExpression(r"#.*"), commentFormat))

        # Function calls (e.g., myFunction()) - Dark Blue
        functionFormat = QTextCharFormat()
        functionFormat.setForeground(QColor("#4682B4")) # Steel Blue
        self.highlightingRules.append((QRegularExpression(r"\b[A-Za-z0-9_]+\s*\("), functionFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = pattern
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
        self.setCurrentBlockState(0)

# Třída pro zvýrazňování syntaxe C
class CHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.highlightingRules = []

        # Keywords (e.g., int, char, if, for) - Orange
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor("#FF9900")) # Orange
        keywords = [
            "auto", "break", "case", "char", "const", "continue", "default", "do",
            "double", "else", "enum", "extern", "float", "for", "goto", "if",
            "inline", "int", "long", "register", "restrict", "return", "short",
            "signed", "sizeof", "static", "struct", "switch", "typedef", "union",
            "unsigned", "void", "volatile", "while", "_Alignas", "_Alignof",
            "_Atomic", "_Bool", "_Complex", "_Generic", "_Imaginary", "_Noreturn",
            "_Static_assert", "_Thread_local"
        ]
        self.highlightingRules.extend([(QRegularExpression(r"\b" + keyword + r"\b"), keywordFormat)
                                       for keyword in keywords])

        # Data types - Teal
        dataTypeFormat = QTextCharFormat()
        dataTypeFormat.setForeground(QColor("#008080")) # Teal
        dataTypes = [
            "int", "char", "float", "double", "void", "long", "short", "signed",
            "unsigned", "struct", "union", "enum", "typedef"
        ]
        self.highlightingRules.extend([(QRegularExpression(r"\b" + dt + r"\b"), dataTypeFormat)
                                       for dt in dataTypes])

        # Preprocessor directives (e.g., #include, #define) - CornflowerBlue (světlejší)
        preprocessorFormat = QTextCharFormat()
        preprocessorFormat.setForeground(QColor("#6495ED")) # CornflowerBlue (světlejší modrá)
        self.highlightingRules.append((QRegularExpression(r"^#.*"), preprocessorFormat))

        # Strings (e.g., "hello world") - Pink
        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor("#FF69B4")) # Pink
        self.highlightingRules.append((QRegularExpression(r"\"[^\"\\]*(\\[\s\S][^\"\\]*)*\""), stringFormat))
        self.highlightingRules.append((QRegularExpression(r"\'[^\'\\]*(\\[\s\S][^\'\\]*)*\'"), stringFormat))

        # Numbers - Light Blue
        numberFormat = QTextCharFormat()
        numberFormat.setForeground(QColor("#87CEEB")) # Light Blue
        self.highlightingRules.append((QRegularExpression(r"\b[0-9]+(\.[0-9]+)?\b"), numberFormat))
        self.highlightingRules.append((QRegularExpression(r"\b0x[0-9a-fA-F]+\b"), numberFormat)) # Hex numbers

        # Comments (e.g., // single-line, /* multi-line */) - Greenish Gray
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor("#808080")) # Gray (Dark mode friendly)
        self.highlightingRules.append((QRegularExpression(r"//.*"), commentFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QColor("#808080"))
        self.commentStartExpression = QRegularExpression(r"/\*")
        self.commentEndExpression = QRegularExpression(r"\*/")

    def highlightBlock(self, text):
        # Aplikování pravidel pro jednořádkové zvýrazňování
        for pattern, format in self.highlightingRules:
            expression = pattern
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

        # Aplikování zvýrazňování víceřádkových komentářů
        self.setCurrentBlockState(0)
        startIndex = 0
        if self.previousBlockState() != 1: # 1 znamená uvnitř víceřádkového komentáře
            startIndex = self.commentStartExpression.match(text).capturedStart()
        
        while startIndex >= 0:
            match = self.commentEndExpression.match(text, startIndex)
            endIndex = match.capturedStart()
            commentLength = 0
            if endIndex == -1:
                self.setCurrentBlockState(1) # Stále uvnitř víceřádkového komentáře
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + match.capturedLength()
            
            self.setFormat(startIndex, commentLength, self.multiLineCommentFormat)
            
            startIndex = self.commentStartExpression.match(text, startIndex + commentLength).capturedStart()


class NotepadGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.languages = {
            "en": {
                "title": "Easy Notepad",
                "file_menu": "File",
                "edit_menu": "Edit",
                "language_menu": "Language",
                "theme_menu": "Theme",
                "highlight_menu": "Highlighting",
                "new_note": "New Note",
                "open_note": "Open Note",
                "save_note": "Save Note",
                "save_as": "Save As...",
                "close_tab": "Close Tab",
                "exit": "Exit",
                "python_highlight": "Python",
                "c_highlight": "C",
                "no_highlight": "None",
                "note_title": "Note Title",
                "enter_title": "Enter the title for your note:",
                "note_saved_success": "Note '{title}' saved successfully!",
                "note_closed_success": "Tab for '{title}' closed.",
                "no_note_open": "No note is currently open.",
                "save_changes_prompt": "Do you want to save changes to '{title}'?",
                "untitled": "Untitled",
                "all_files": "All Files",
                "text_files": "Text Files",
                "error": "Error",
                "warning": "Warning",
                "about": "About",
                "about_message": "Easy Notepad\nVersion 1.0\nCreated with PyQt6",
                "light_theme": "Light",
                "dark_theme": "Dark",
                "confirm_exit_app_prompt": "Are you sure you want to exit Easy Notepad?",
                "confirm_close_tab_prompt": "Are you sure you want to close '{title}'?",
            },
            "cs": {
                "title": "Snadný Poznámkový Blok",
                "file_menu": "Soubor",
                "edit_menu": "Úpravy",
                "language_menu": "Jazyk",
                "theme_menu": "Motiv",
                "highlight_menu": "Zvýrazňování Syntax",
                "new_note": "Nový Zápisek",
                "open_note": "Otevřít Zápisek",
                "save_note": "Uložit Zápisek",
                "save_as": "Uložit jako...",
                "close_tab": "Zavřít Záložku",
                "exit": "Ukončit",
                "python_highlight": "Python",
                "c_highlight": "C",
                "no_highlight": "Žádné",
                "note_title": "Název Zápisku",
                "enter_title": "Zadejte název pro váš zápisek:",
                "note_saved_success": "Zápisek '{title}' byl úspěšně uložen!",
                "note_closed_success": "Záložka pro '{title}' byla zavřena.",
                "no_note_open": "Momentálně není otevřen žádný zápisek.",
                "save_changes_prompt": "Chcete uložit změny do '{title}'?",
                "untitled": "Bezejmenný",
                "all_files": "Všechny soubory",
                "text_files": "Textové soubory",
                "error": "Chyba",
                "warning": "Upozornění",
                "about": "O aplikaci",
                "about_message": "Snadný Poznámkový Blok\nVerze 1.0\nVytvořeno pomocí PyQt6",
                "light_theme": "Tmavy",
                "dark_theme": "Světlý",
                "confirm_exit_app_prompt": "Opravdu chcete ukončit Snadný Poznámkový Blok?",
                "confirm_close_tab_prompt": "Opravdu chcete zavřít záložku '{title}'?",
            },
        }

        self.current_language = "en"
        self.current_theme = "light"
        self.highlighters = {} # Ukládání instancí zvýrazňovačů pro každou záložku

        self.init_ui()
        self.update_ui_texts()
        self.apply_theme()

    def init_ui(self):
        self.setWindowTitle(self.get_text("title"))
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.layout.addWidget(self.tab_widget)

        self.create_menu()

    def get_text(self, key):
        return self.languages[self.current_language].get(key, key)

    def update_ui_texts(self):
        self.setWindowTitle(self.get_text("title"))
        self.file_menu.setTitle(self.get_text("file_menu"))
        self.edit_menu.setTitle(self.get_text("edit_menu"))
        self.language_menu.setTitle(self.get_text("language_menu"))
        self.theme_menu.setTitle(self.get_text("theme_menu"))
        self.highlight_menu.setTitle(self.get_text("highlight_menu"))

        self.new_note_action.setText(self.get_text("new_note"))
        self.open_note_action.setText(self.get_text("open_note"))
        self.save_note_action.setText(self.get_text("save_note"))
        self.save_as_note_action.setText(self.get_text("save_as"))
        self.close_tab_action.setText(self.get_text("close_tab"))
        self.exit_action.setText(self.get_text("exit"))

        self.about_action.setText(self.get_text("about"))

        self.light_theme_action.setText(self.get_text("light_theme"))
        self.dark_theme_action.setText(self.get_text("dark_theme"))

        self.python_highlight_action.setText(self.get_text("python_highlight"))
        self.c_highlight_action.setText(self.get_text("c_highlight"))
        self.no_highlight_action.setText(self.get_text("no_highlight"))

        # Aktualizace názvů záložek, pokud jsou "Bezejmenný"
        for i in range(self.tab_widget.count()):
            tab_data = self.tab_widget.widget(i).property("tab_data")
            if tab_data and tab_data["modified"] and tab_data["path"] is None:
                self.tab_widget.setTabText(i, self.get_text("untitled") + "*")
            elif tab_data and tab_data["path"] is None:
                self.tab_widget.setTabText(i, self.get_text("untitled"))

    def create_menu(self):
        menubar = self.menuBar()

        # Menu Soubor
        self.file_menu = menubar.addMenu(self.get_text("file_menu"))
        self.new_note_action = QAction(self.get_text("new_note"), self)
        self.new_note_action.triggered.connect(self.new_note)
        self.file_menu.addAction(self.new_note_action)

        self.open_note_action = QAction(self.get_text("open_note"), self)
        self.open_note_action.triggered.connect(self.open_note)
        self.file_menu.addAction(self.open_note_action)

        self.save_note_action = QAction(self.get_text("save_note"), self)
        self.save_note_action.triggered.connect(self.save_note)
        self.file_menu.addAction(self.save_note_action)

        self.save_as_note_action = QAction(self.get_text("save_as"), self)
        self.save_as_note_action.triggered.connect(self.save_note_as)
        self.file_menu.addAction(self.save_as_note_action)

        self.file_menu.addSeparator()

        self.close_tab_action = QAction(self.get_text("close_tab"), self)
        self.close_tab_action.triggered.connect(self.close_current_tab)
        self.file_menu.addAction(self.close_tab_action)

        self.file_menu.addSeparator()

        self.exit_action = QAction(self.get_text("exit"), self)
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

        # Menu Úpravy
        self.edit_menu = menubar.addMenu(self.get_text("edit_menu"))
        self.about_action = QAction(self.get_text("about"), self)
        self.about_action.triggered.connect(self.show_about)
        self.edit_menu.addAction(self.about_action)

        # Menu Jazyk
        self.language_menu = menubar.addMenu(self.get_text("language_menu"))
        for lang_code, lang_data in self.languages.items():
            lang_action = QAction(lang_data["title"].split(" ")[-1] if " " in lang_data["title"] else lang_data["title"], self)
            lang_action.triggered.connect(lambda checked, code=lang_code: self.change_language(code))
            self.language_menu.addAction(lang_action)

        # Menu Motiv
        self.theme_menu = menubar.addMenu(self.get_text("theme_menu"))
        self.light_theme_action = QAction(self.get_text("light_theme"), self)
        self.light_theme_action.triggered.connect(lambda: self.change_theme("light"))
        self.theme_menu.addAction(self.light_theme_action)

        self.dark_theme_action = QAction(self.get_text("dark_theme"), self)
        self.dark_theme_action.triggered.connect(lambda: self.change_theme("dark"))
        self.theme_menu.addAction(self.dark_theme_action)

        # Menu Zvýrazňování Syntax
        self.highlight_menu = menubar.addMenu(self.get_text("highlight_menu"))
        self.python_highlight_action = QAction(self.get_text("python_highlight"), self)
        self.python_highlight_action.triggered.connect(lambda: self.set_syntax_highlight("python"))
        self.highlight_menu.addAction(self.python_highlight_action)

        self.c_highlight_action = QAction(self.get_text("c_highlight"), self)
        self.c_highlight_action.triggered.connect(lambda: self.set_syntax_highlight("c"))
        self.highlight_menu.addAction(self.c_highlight_action)

        self.highlight_menu.addSeparator()

        self.no_highlight_action = QAction(self.get_text("no_highlight"), self)
        self.no_highlight_action.triggered.connect(lambda: self.set_syntax_highlight(None))
        self.highlight_menu.addAction(self.no_highlight_action)

        self._apply_menu_action_style(self.current_theme == "dark")


    def _apply_menu_action_style(self, is_dark_theme):
        pass

    def get_current_text_edit(self):
        current_index = self.tab_widget.currentIndex()
        if current_index == -1:
            return None, None # Žádná záložka není otevřená
        return self.tab_widget.widget(current_index), current_index

    def new_note(self):
        self.create_new_tab()

    def create_new_tab(self, file_path=None, content=""):
        text_edit = TextEditWithAutoIndent() # Používáme novou třídu TextEditWithAutoIndent

        tab_name = self.get_text("untitled")
        if file_path:
            tab_name = os.path.basename(file_path)

        tab_index = self.tab_widget.addTab(text_edit, tab_name)
        self.tab_widget.setCurrentIndex(tab_index)
        text_edit.setText(content)
        text_edit.setFocus()

        tab_data = {
            "path": file_path,
            "modified": False,
            "highlighter": None
        }
        text_edit.setProperty("tab_data", tab_data)

        text_edit.textChanged.connect(lambda: self.on_text_change(text_edit))


    def on_text_change(self, text_edit):
        tab_data = text_edit.property("tab_data")
        if tab_data and not tab_data["modified"]:
            tab_data["modified"] = True
            current_index = self.tab_widget.indexOf(text_edit)
            current_text = self.tab_widget.tabText(current_index)
            if not current_text.endswith("*"):
                self.tab_widget.setTabText(current_index, current_text + "*")

    def open_note(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.get_text("open_note"), "",
            f"{self.get_text('text_files')} (*.txt);;{self.get_text('all_files')} (*.*)"
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.create_new_tab(file_path, content)
            except Exception as e:
                QMessageBox.critical(self, self.get_text("error"), f"Failed to open file: {e}")

    def save_note(self):
        text_edit, current_index = self.get_current_text_edit()
        if not text_edit:
            QMessageBox.information(self, self.get_text("warning"), self.get_text("no_note_open"))
            return

        tab_data = text_edit.property("tab_data")
        if tab_data["path"]:
            try:
                with open(tab_data["path"], "w", encoding="utf-8") as file:
                    file.write(text_edit.toPlainText())
                QMessageBox.information(self, self.get_text("title"), self.get_text("note_saved_success").format(title=os.path.basename(tab_data["path"])))
                tab_data["modified"] = False
                self.tab_widget.setTabText(current_index, os.path.basename(tab_data["path"]))
            except Exception as e:
                QMessageBox.critical(self, self.get_text("error"), f"Failed to save file: {e}")
        else:
            self.save_note_as()

    def save_note_as(self):
        text_edit, current_index = self.get_current_text_edit()
        if not text_edit:
            QMessageBox.information(self, self.get_text("warning"), self.get_text("no_note_open"))
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, self.get_text("save_as"), "",
            f"{self.get_text('text_files')} (*.txt);;{self.get_text('all_files')} (*.*)"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(text_edit.toPlainText())
                tab_data = text_edit.property("tab_data")
                tab_data["path"] = file_path
                tab_data["modified"] = False
                QMessageBox.information(self, self.get_text("title"), self.get_text("note_saved_success").format(title=os.path.basename(file_path)))
                self.tab_widget.setTabText(current_index, os.path.basename(file_path))
            except Exception as e:
                QMessageBox.critical(self, self.get_text("error"), f"Failed to save file: {e}")

    def close_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index == -1:
            QMessageBox.information(self, self.get_text("warning"), self.get_text("no_note_open"))
            return
        self.close_tab(current_index)

    def close_tab(self, index):
        text_edit = self.tab_widget.widget(index)
        tab_data = text_edit.property("tab_data")
        tab_title = self.tab_widget.tabText(index).rstrip('*')

        if tab_data and tab_data["modified"]:
            # Stávající dotaz na uložení změn, pokud je upraveno
            reply = QMessageBox.question(
                self, self.get_text("warning"),
                self.get_text("save_changes_prompt").format(title=tab_title),
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Save:
                self.save_note()
                if tab_data["modified"]: # Pokud se uložení nezdařilo nebo bylo zrušeno
                    return
            elif reply == QMessageBox.StandardButton.Cancel:
                return # Uživatel zrušil zavření
        else:
            # Nové potvrzení, pokud SOUBOR NENÍ upraven
            reply = QMessageBox.question(
                self, self.get_text("warning"),
                self.get_text("confirm_close_tab_prompt").format(title=tab_title),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return # Uživatel zrušil zavření

        # Pokračujte se zavřením, pokud potvrzení prošlo nebo uživatel zvolil zahodit
        self.tab_widget.removeTab(index)
        doc = text_edit.document()
        if doc in self.highlighters:
            self.highlighters[doc].setDocument(None)
            del self.highlighters[doc]
        QMessageBox.information(self, self.get_text("title"), self.get_text("note_closed_success").format(title=tab_title))


    def change_language(self, lang_code):
        self.current_language = lang_code
        self.update_ui_texts()
        self.apply_theme()

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.apply_theme()

    def apply_theme(self):
        if self.current_theme == "light":
            app.setPalette(QApplication.style().standardPalette())
            app.setStyle("")
            self.setStyleSheet("")

            for i in range(self.tab_widget.count()):
                text_edit = self.tab_widget.widget(i)
                text_edit.setStyleSheet("")

        else: # Dark theme
            app.setStyle("Fusion")
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
            dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
            dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
            dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
            dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
            dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
            dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
            dark_palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(150, 150, 150))

            dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(128, 128, 128))
            dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(128, 128, 128))
            dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, QColor(80, 80, 80))

            app.setPalette(dark_palette)

            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2b2b2b;
                }
                QMenuBar {
                    background-color: #2b2b2b;
                    color: white;
                }
                QMenuBar::item {
                    background-color: transparent;
                    color: white;
                }
                QMenuBar::item:selected {
                    background-color: #444444;
                }
                QMenu {
                    background-color: #3c3c3c;
                    color: white;
                    border: 1px solid #555555;
                }
                QMenu::item {
                    background-color: transparent;
                    color: white;
                }
                QMenu::item:selected {
                    background-color: #555555;
                }
                QTextEdit {
                    background-color: #2b2b2b;
                    color: #f0f0f0;
                    selection-background-color: #555555;
                    selection-color: #f0f0f0;
                    border: 1px solid #444444;
                }
                QTabWidget::pane {
                    border: 1px solid #444444;
                    background-color: #2b2b2b;
                }
                QTabBar::tab {
                    background: #444444;
                    color: white;
                    border: 1px solid #555555;
                    border-bottom-color: #444444;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    padding: 5px 10px;
                }
                QTabBar::tab:selected {
                    background: #2b2b2b;
                    border-color: #555555;
                    border-bottom-color: #2b2b2b;
                }
                QTabBar::tab:hover {
                    background: #555555;
                }
            """)
        self.update_ui_texts()


    def set_syntax_highlight(self, language):
        text_edit, _ = self.get_current_text_edit()
        if not text_edit:
            QMessageBox.information(self, self.get_text("warning"), self.get_text("no_note_open"))
            return

        doc = text_edit.document()
        if doc in self.highlighters:
            self.highlighters[doc].setDocument(None)
            del self.highlighters[doc]

        if language == "python":
            highlighter = PythonHighlighter(doc)
            self.highlighters[doc] = highlighter
        elif language == "c":
            highlighter = CHighlighter(doc)
            self.highlighters[doc] = highlighter
        elif language is None:
            pass

    def show_about(self):
        QMessageBox.information(self, self.get_text("about"), self.get_text("about_message"))

    def closeEvent(self, event):
        # První, dotaz na potvrzení ukončení celé aplikace
        reply = QMessageBox.question(
            self, self.get_text("warning"),
            self.get_text("confirm_exit_app_prompt"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            event.ignore()
            return

        # Následně pokračujte s kontrolou neuložených záložek
        for i in range(self.tab_widget.count()):
            text_edit = self.tab_widget.widget(i)
            tab_data = text_edit.property("tab_data")
            if tab_data and tab_data["modified"]:
                self.tab_widget.setCurrentIndex(i)
                reply = QMessageBox.question(
                    self, self.get_text("warning"),
                    self.get_text("save_changes_prompt").format(title=self.tab_widget.tabText(i).rstrip('*')),
                    QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
                )
                if reply == QMessageBox.StandardButton.Save:
                    self.save_note()
                    if tab_data["modified"]:
                        event.ignore()
                        return
                elif reply == QMessageBox.StandardButton.Cancel:
                    event.ignore()
                    return
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = NotepadGUI()
    window.show()
    sys.exit(app.exec())