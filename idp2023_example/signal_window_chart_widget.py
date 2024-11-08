# SPDX-FileCopyrightText: 2023 Joni Hyttinen <joni.hyttinen@uef.fi>
#
# SPDX-License-Identifier: MIT

# A signal widget for showing n points of a signal.
#
# Based on matplotlib documentation [1]
#
# [1] https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_qt_sgskip.html
import logging
import time

import numpy as np
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout
# The documentation imports FigureCanvas directly, but PyCharm does not like that since FigureCanvas is created on
# runtime in matplotlib.backends.backend_qtagg module. Therefore PyCharm does not see this identifier and marks it as
# a programming error.
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

logger = logging.getLogger(__name__)
logging.getLogger("matplotlib").setLevel(logging.INFO)  # matplotlib has a lot of DEBUG-messages.

class SignalWindowChartWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(NavigationToolbar(self._canvas, self))
        self.layout.addWidget(self._canvas)

        self._ax = self._canvas.figure.subplots()

        self.setLayout(self.layout)

    @Slot(float, float)
    def set_axis_y(self, min_y: float, max_y: float):
        if np.isfinite(min_y) and np.isfinite(max_y):
            self._ax.set_ylim(min_y, max_y)

    @Slot(np.ndarray, np.ndarray)
    def replace_array(self, x: np.ndarray, y: np.ndarray, do_not_try_fix_what_is_not_broken: bool = False):
        start_time = time.time()

        self._ax.cla()
        self._ax.plot(x, y)
        self._ax.set_xlim(x.min(), x.max())
        self._canvas.draw()

        end_time = time.time()
        logger.debug("Finished updating chart in {:.2f} ms".format((end_time - start_time) * 1000))
