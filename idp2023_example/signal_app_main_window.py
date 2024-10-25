# SPDX-FileCopyrightText: 2023 Joni Hyttinen <joni.hyttinen@uef.fi>
#
# SPDX-License-Identifier: MIT

# https://doc.qt.io/qtforpython-6/tutorials/index.html
# https://doc.qt.io/qtforpython-6/tutorials/expenses/expenses.html

import sys
from pathlib import Path
import logging

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow

from idp2023_example.signal_app_widget import SignalAppWidget

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SignalAppMainWindow(QMainWindow):
    last_dir = Path.home()  # Keep track of the last opened directory
    selected_filter = None

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
        event.accept()
        logger.debug("Closing application.")

    def file_open_action(self):
        signal_path, self.selected_filter = QFileDialog.getOpenFileName(
            self,
            self.tr("Open Industrial Project signal file"),
            str(self.last_dir),  # ok, Qt seems to like path strings
            self.tr("Signal files (*.csv)"),
            self.selected_filter,
        )
        signal_path = Path(signal_path)  # but I like pathlib.Path
        self.last_dir = signal_path.parent
        self.signal_app_widget.set_signal_path(signal_path)
        logger.debug("Opened file '{}'".format(signal_path))


def run():
    app = QApplication([])

    main_window = SignalAppMainWindow()
    main_window.resize(1024, 768)
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
