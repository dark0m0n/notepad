import sys
import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QInputDialog, QMessageBox, QLineEdit
from PyQt6.QtGui import QAction, QKeySequence, QTextCursor, QTextOption, QFont, QFontDatabase

from pathlib import Path

from datetime import datetime, date


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.window = Widgets()
        self.window.resize(900, 500)
        self.window.show()
        self.fname_adr = None
        self.last_search_text = ""


class Widgets(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Untitled: Notepad')
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        menu = self.menuBar()

        # File menu
        file_menu = menu.addMenu('&File')

        # New button
        file_menu_new = QAction('&New', self)
        file_menu_new.setShortcut(QKeySequence('Ctrl+N'))
        file_menu_new.triggered.connect(self.new_file)
        file_menu.addAction(file_menu_new)

        # Open button
        file_menu_open = QAction('&Open...', self)
        file_menu_open.setShortcut(QKeySequence('Ctrl+O'))
        file_menu_open.triggered.connect(self.open_file)
        file_menu.addAction(file_menu_open)

        # Save button
        file_menu_save = QAction('&Save', self)
        file_menu_save.setShortcut(QKeySequence('Ctrl+S'))
        file_menu_save.triggered.connect(self.save_file)
        file_menu.addAction(file_menu_save)

        # Save as button
        file_menu_save_as = QAction('Save &As...', self)
        file_menu_save_as.setShortcut('Ctrl+Shift+S')
        file_menu_save_as.triggered.connect(self.save_as_file)
        file_menu.addAction(file_menu_save_as)

        file_menu.addSeparator()

        # Exit button
        file_menu_exit = QAction('E&xit', self)
        file_menu_exit.setShortcut(QKeySequence.StandardKey.Quit)
        file_menu_exit.triggered.connect(self.close)
        file_menu.addAction(file_menu_exit)

        # Edit menu
        edit_menu = menu.addMenu('&Edit')

        # Undo button
        edit_menu_undo = QAction('&Undo', self)
        edit_menu_undo.setShortcut(QKeySequence.StandardKey.Undo)
        edit_menu_undo.triggered.connect(self.undo)
        edit_menu.addAction(edit_menu_undo)

        edit_menu.addSeparator()

        # Cut button
        edit_menu_cut = QAction('&Cut', self)
        edit_menu_cut.setShortcut(QKeySequence.StandardKey.Cut)
        edit_menu_cut.triggered.connect(self.cut)
        edit_menu.addAction(edit_menu_cut)

        # Copy button
        edit_menu_copy = QAction('&Copy', self)
        edit_menu_copy.setShortcut(QKeySequence.StandardKey.Copy)
        edit_menu_copy.triggered.connect(self.copy)
        edit_menu.addAction(edit_menu_copy)

        # Paste button
        edit_menu_paste = QAction('&Paste', self)
        edit_menu_paste.setShortcut(QKeySequence.StandardKey.Paste)
        edit_menu_paste.triggered.connect(self.paste)
        edit_menu.addAction(edit_menu_paste)

        # Delete button
        edit_menu_delete = QAction('&Delete', self)
        edit_menu_delete.setShortcut(QKeySequence.StandardKey.Delete)
        edit_menu_delete.triggered.connect(self.delete)
        edit_menu.addAction(edit_menu_delete)

        edit_menu.addSeparator()

        # Find button
        edit_menu_find = QAction('&Find...', self)
        edit_menu_find.setShortcut(QKeySequence.StandardKey.Find)
        edit_menu_find.triggered.connect(self.find_text)
        edit_menu.addAction(edit_menu_find)

        # Find next button
        edit_menu_find_next = QAction('&Find Next', self)
        edit_menu_find_next.setShortcut(QKeySequence.StandardKey.FindNext)
        edit_menu_find_next.triggered.connect(self.find_next)
        edit_menu.addAction(edit_menu_find_next)

        # Replace button
        edit_menu_replace = QAction('&Replace', self)
        edit_menu_replace.setShortcut(QKeySequence.StandardKey.Replace)
        edit_menu_replace.triggered.connect(self.replace)
        edit_menu.addAction(edit_menu_replace)

        # Go to button
        edit_menu_go_to = QAction('&Go To...', self)
        edit_menu_go_to.setShortcut('Ctrl+G')
        edit_menu_go_to.triggered.connect(self.go_to)
        edit_menu.addAction(edit_menu_go_to)

        edit_menu.addSeparator()

        # Select all button
        edit_menu_select_all = QAction('&Select All', self)
        edit_menu_select_all.setShortcut(QKeySequence.StandardKey.SelectAll)
        edit_menu_select_all.triggered.connect(self.select_all)
        edit_menu.addAction(edit_menu_select_all)

        # Time/Date button
        edit_menu_time_date = QAction('&Time/Date', self)
        edit_menu_time_date.setShortcut('F5')
        edit_menu_time_date.triggered.connect(self.time_date)
        edit_menu.addAction(edit_menu_time_date)

        # Format menu
        format_menu = menu.addMenu('&Format')

        # Word wrap button
        format_menu_word_wrap = QAction('Word &Wrap', self)
        format_menu_word_wrap.setCheckable(True)
        format_menu_word_wrap.triggered.connect(self.word_wrap)
        format_menu.addAction(format_menu_word_wrap)

        format_menu_font = QAction('&Font...', self)
        format_menu_font.triggered.connect(self.choose_font)
        format_menu.addAction(format_menu_font)

        # View menu
        view_menu = menu.addMenu("&View")

        # Zoom submenu
        zoom_submenu = view_menu.addMenu('&Zoom')

        # Zoom in button
        zoom_submenu_zoom_in = QAction('Zoom &In', self)
        zoom_submenu_zoom_in.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_submenu_zoom_in.triggered.connect(self.zoom_in)
        zoom_submenu.addAction(zoom_submenu_zoom_in)

        # Zoom out button
        zoom_submenu_zoom_out = QAction('Zoom &Out', self)
        zoom_submenu_zoom_out.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_submenu_zoom_out.triggered.connect(self.zoom_out)
        zoom_submenu.addAction(zoom_submenu_zoom_out)

    # File menu functions

    def new_file(self):
        """Create a new clean file
        """

        self.setWindowTitle('Untitled: Notepad')
        self.fname_adr = None
        self.textEdit.clear()

    def open_file(self):
        """Open file
        """

        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
        self.fname_adr = fname[0]

        if fname[0]:
            with open(fname[0], 'r', encoding='utf-8') as file:
                data = file.read()
                self.textEdit.setText(data)
                self.setWindowTitle(
                    str(os.path.basename(fname[0])) + ": Notepad")

    def save_file(self):
        """Save data in current file
        """

        filepath = os.path.join(os.path.dirname(
            self.fname_adr), str(os.path.basename(self.fname_adr)))

        with open(filepath, 'w') as file:
            file.write(self.textEdit.toPlainText())

    def save_as_file(self):
        """Create file and save data in this file
        """

        home_dir = str(Path.home())
        fname = QFileDialog.getSaveFileName(
            self, "Save file", home_dir, "Text files (*.txt)")

        self.setWindowTitle(str(os.path.basename(fname[0])) + ": Notepad")
        self.fname_adr = fname[0]

        if fname[0]:
            with open(fname[0], 'w') as file:
                file.write(self.textEdit.toPlainText())

    # Edit menu functions

    def undo(self):
        """Undo the text
        """

        self.textEdit.document().undo()

    def cut(self):
        """Cut the text
        """

        self.textEdit.cut()

    def copy(self):
        """Copy the text
        """

        self.textEdit.copy()

    def paste(self):
        """Paste copied text
        """

        self.textEdit.paste()

    def delete(self):
        """Delete character after cursor
        """

        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            cursor.deleteChar()
        else:
            cursor.deleteChar()
            cursor.setPosition(cursor.position()-1,
                               QTextCursor.MoveMode.MoveAnchor)

    def find_text(self):
        """Find input text in the text
        """

        search_text, ok = QInputDialog.getText(
            self, "Find Text", "Enter the text to find:")
        if ok and search_text:
            cursor = self.textEdit.document().find(search_text)
            if cursor.isNull():
                QMessageBox.information(
                    self, 'Notepad', f'"{search_text}" not found')
            else:
                self.textEdit.setTextCursor(cursor)
                self.textEdit.setFocus()
                self.last_search_text = search_text

    def find_next(self):
        """Show next found text
        """

        cursor = self.textEdit.document().find(
            self.last_search_text, self.textEdit.textCursor().position())
        if cursor.isNull():
            QMessageBox.information(
                self, 'Notepad', f'"{self.last_search_text}" not found')
        else:
            self.textEdit.setTextCursor(cursor)
            self.textEdit.setFocus()

    def replace(self):
        """Find text and replace it on input text
        """

        text, ok = QInputDialog.getText(
            self, "Find and replace", "Enter text to find:", QLineEdit.EchoMode.Normal, "")
        if ok and text:
            replace_text, ok = QInputDialog.getText(
                self, "Find and replace", "Enter text to replace:", QLineEdit.EchoMode.Normal, "")
            if ok and replace_text:
                cursor = self.textEdit.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.Start)
                while cursor.hasSelection():
                    cursor.clearSelection()
                    cursor.movePosition(
                        QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)
                if cursor.movePosition(QTextCursor.MoveOperation.NextWord, QTextCursor.MoveMode.KeepAnchor):
                    if cursor.selectedText() == text:
                        cursor.insertText(replace_text)
                        while cursor.movePosition(QTextCursor.MoveOperation.NextWord, QTextCursor.MoveMode.KeepAnchor):
                            if cursor.selectedText() == text:
                                cursor.insertText(replace_text)

    def go_to(self):
        """Move cursor to entered line
        """

        num, ok = QInputDialog.getInt(self, 'Move to line', 'Number of line:')
        if ok and num:
            cursor = self.textEdit.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            cursor.movePosition(QTextCursor.MoveOperation.Down,
                                QTextCursor.MoveMode.MoveAnchor, num-1)
            self.textEdit.setTextCursor(cursor)

    def select_all(self):
        """Select all text
        """

        self.textEdit.selectAll()

    def time_date(self):
        """Write time and date
        """

        now = datetime.now()
        today = date.today()
        self.textEdit.append(
            f'{now.hour}:{now.minute} {today.strftime("%d.%m.%Y")}')

    # Format menu functions

    def word_wrap(self, check):
        """Turn on ot turn off word wrap
        """

        if check == True:
            self.textEdit.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        else:
            self.textEdit.setWordWrapMode(QTextOption.WrapMode.WordWrap)

    def choose_font(self):
        """Set font size
        """

        num, ok = QInputDialog.getInt(self, 'Font Size', 'Font size:')
        if num and ok:
            default_font = QFontDatabase.systemFont(
                QFontDatabase.SystemFont.GeneralFont)
            self.textEdit.setFont(QFont(default_font.family(), num))

    # View menu functions

    def zoom_in(self):
        """Zoom in window
        """

        self.textEdit.zoomIn()

    def zoom_out(self):
        """Zoom out window
        """

        self.textEdit.zoomOut()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
