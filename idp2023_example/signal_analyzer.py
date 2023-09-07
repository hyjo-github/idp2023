# SPDX-FileCopyrightText: 2023 Joni Hyttinen <joni.hyttinen@uef.fi>
#
# SPDX-License-Identifier: MIT

import time

import numpy as np
from PySide6.QtCore import Signal


class SignalAnalyzer:
    """
    A "signal analyzer" that just generates an array of cosine function values.

    Instances of this class are intended to be run from a worker thread. Data
    is emitted through callbacks back to the parent thread.
    """

    def __init__(self):
        self.running = False
        self.window_size = 1000
        self.x = 0
        self.x_array = np.zeros((self.window_size,))
        self.y_array = np.zeros_like(self.x_array)

    def _generate_data_array(self) -> None:
        self.x_array = np.linspace(self.x, self.x + 100, self.window_size)
        self.y_array = np.cos(2 * np.pi * 1 / 0.5 * self.x_array)
        self.x += 0.01

    def _start(self, set_axis_y=None):
        """
        Tasks that should be done before starting the main loop of SignalAnalyzer.
        """
        self.running = True
        if set_axis_y:
            set_axis_y.emit(-1.1, 1.1)

    def stop(self):
        """
        Stops the main loop.
        """
        self.running = False

    def start(
        self,
        set_chart_axis_y: Signal | None = None,
        update_chart: Signal | None = None,
        progress_callback: Signal | None = None,
    ):
        """
        Starts the SignalAnalyzer main loop.

        :param set_chart_axis_y: Callback function to update chart y-axis.
        :param update_chart: Callback function to update a chart.
        :param progress_callback: Callback function to update progress meters.
        """
        self._start(set_chart_axis_y)

        while self.running:
            self._generate_data_array()

            if update_chart:
                update_chart.emit(self.x_array, self.y_array)

            if progress_callback:
                # This loop has no meaningful progress.
                # Just report the current left-most x-coordinate.
                progress_callback.emit(self.x)

            # Too fast loop will flood the event queue and everything crashes
            time.sleep(0.01)
