# SPDX-FileCopyrightText: 2023 Joni Hyttinen <joni.hyttinen@uef.fi>
#
# SPDX-License-Identifier: MIT

# https://doc.qt.io/qtforpython-6/tutorials/index.html
# https://doc.qt.io/qtforpython-6/tutorials/expenses/expenses.html

import sys

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow, QApplication

from idp2023_example.signal_app_widget import SignalAppWidget


class SignalAppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.file_menu = self.menuBar().addMenu("&File")
        file_open_action = self.file_menu.addAction("Open", self.file_open_action)
        file_open_action.setShortcut("Ctrl+O")

        file_quit_action = self.file_menu.addAction("Quit", self.close)
        file_quit_action.setShortcut("Ctrl+Q")

        self.signal_app_widget = SignalAppWidget()
        self.setCentralWidget(self.signal_app_widget)
        self.setWindowTitle("Signal app template")

    def closeEvent(self, event: QCloseEvent) -> None:
        self.signal_app_widget.stop_signal_analyser()

    def file_open_action(self):
        pass


def run():
    app = QApplication([])

    main_window = SignalAppMainWindow()
    main_window.resize(1024, 768)
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
