# SPDX-FileCopyrightText: 2023 Joni Hyttinen <joni.hyttinen@uef.fi>
#
# SPDX-License-Identifier: MIT
import csv
import logging
import time
from collections.abc import Iterator
from pathlib import Path

import numpy as np
from PySide6.QtCore import Signal

logger = logging.getLogger(__name__)

class SignalAnalyzer:
    """
    A "signal analyzer" that just generates an array of cosine function values.

    Instances of this class are intended to be run from a worker thread. Data
    is emitted through callbacks back to the parent thread.
    """

    def __init__(self):
        self.signal_path = None
        self.running = False
        self.window_size = 600 * 50000  # Let's take 10 minutes of the signal
        self.chunk_size = 500000  # ten second at a time
        self.x = 0
        self.x_array = np.zeros((self.window_size,))
        self.y_array = np.zeros_like(self.x_array) * np.nan
        self.y_max = -np.inf  # Use ridiculous values to force y-scale change
        self.y_min = np.inf

    def _read_signal(self, chunk_size: int = 1) -> Iterator[np.ndarray]:
        """
        Read the signal file in chunks of `chunk_size` rows.

        This method is a generator, and it should be called iteratively, for
        example in a `while` or a `for` loop. A generator method generates
        values as they are needed. Consequently, this method does not read
        the whole file at once, but only `count` rows that then yielded
        to the outer loop for processing. On the next loop iteration, the
        execution in this method continues after the yield statement.

        :param chunk_size: the number of rows in a chunk
        :return: a numpy array of shape (count, 2). The final array may be shorter.
        """
        if self.signal_path is None or not self.signal_path.is_file():
            # This could raise an exception, but then we would have to handle that somewhere.
            print(f"""signal path "{self.signal_path}" is not a valid file.""")
            return

        with self.signal_path.open("r") as signal_file:
            reader = csv.reader(signal_file)
            # skip column headers ("adc1", "adc2")
            next(reader)
            data = np.zeros((chunk_size, 2))
            i = 0
            for i, row in enumerate(reader):
                data[i % chunk_size] = np.array(row, np.uint16)
                if i > 0 and i % chunk_size == 0:
                    yield data
            if i % chunk_size != 0:
                yield data[: i % chunk_size]

    def _start(self, set_axis_y=None):
        """
        Tasks that should be done before starting the main loop of SignalAnalyzer.
        """
        self.running = True
        if set_axis_y:
            set_axis_y.emit(self.y_min, self.y_max)

    def stop(self):
        """
        Stops the main loop.
        """
        self.running = False

    def start(
        self,
        signal_path: Path,
        set_chart_axis_y: Signal | None = None,
        update_chart: Signal | None = None,
        progress_callback: Signal | None = None,
    ):
        """
        Starts the SignalAnalyzer main loop.

        :param signal_path: the path to the signal data file.
        :param set_chart_axis_y: Callback function to update chart y-axis.
        :param update_chart: Callback function to update a chart.
        :param progress_callback: Callback function to update progress meters.
        """

        self.signal_path = signal_path
        self._start(set_chart_axis_y)

        while self.running:
            self.x = -self.window_size

            end_time = time.time()
            for chunk in self._read_signal(self.chunk_size):
                # Record iteration start time
                start_time = time.time()
                logger.debug("Chunk read in {:.2f} ms".format((start_time - end_time) * 1000))

                # Break out from the for-loop if `self.running` has changed
                if not self.running:
                    break

                chunk_size = chunk.shape[0]  # At the end of the file, we don't know how large this is
                self.x_array = np.linspace(self.x, self.x + self.window_size - 1, self.window_size) / 50000
                self.y_array = np.roll(self.y_array, -chunk_size)  # roll `self.y_array` back by `chunk_size`
                self.y_array[-chunk_size:] = chunk[:, 1]  # replace the last `chunk_size` entries with `chunk`
                self.x += chunk_size

                # Update y-axis min/max if need be:
                self.y_min = y_min if (y_min := np.nanmin(self.y_array)) < self.y_min else self.y_min
                self.y_max = y_max if (y_max := np.nanmax(self.y_array)) > self.y_max else self.y_max

                # Uh oh, we quickly notice that plotting this many points is downright unfeasible. Let's reduce the
                # load for visualization by selecting only every 100th value in the arrays.
                vis_x = self.x_array[::100].copy()  # these array slice views seem to go missing if not copied
                vis_y = self.y_array[::100].copy()

                logger.debug("Computation done in {:.2f} ms".format((time.time() - start_time) * 1000))

                # This signal will now block the thread until chart update is finished
                if set_chart_axis_y:
                    set_chart_axis_y.emit(self.y_min, self.y_max)

                # This signal will now block the thread until chart update is finished
                if update_chart:
                    update_chart.emit(vis_x, vis_y)

                if progress_callback:
                    # This loop has no meaningful progress.
                    # Just report the current left-most x-coordinate.
                    progress_callback.emit(self.x)

                end_time = time.time()
                logger.debug("Finished iteration in {:.2f} ms".format((end_time - start_time) * 1000))

            # Stop while-loop when the file ends
            self.running = False
