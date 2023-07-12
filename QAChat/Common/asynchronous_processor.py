# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Palarus

import threading
import queue
import time


class AsynchronousProcessor:
    def __init__(self, func):
        self.func = func
        self.input_queue = queue.Queue(maxsize=1)
        self.output_queue = queue.Queue()
        self.stopped = threading.Event()
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def _worker(self):
        """
        The worker function that continuously retrieves values from the input queue,
        applies the function on them, and puts the results in the output queue.
        """
        while not self.stopped.is_set() or not self.input_queue.empty():
            try:
                value = self.input_queue.get(block=True, timeout=0.1)
                if value is not None:
                    result = self.func(value)
                    self.output_queue.put(result)
            except queue.Empty:
                continue

    def add(self, value):
        """
        Adds a value to the input queue for processing.
        If the input queue is not empty, it removes the existing value before adding the new value.

        :param value: a value to be added to the input queue for processing
        """
        while not self.input_queue.empty():
            try:
                self.input_queue.get(block=False)
            except queue.Empty:
                continue
        self.input_queue.put(value)

    def end(self):
        """
        Stops the processing of new inputs and waits for the worker thread to finish processing existing inputs.
        """
        self.stopped.set()
        self.worker_thread.join()

    def stream(self):
        """
        A generator that yields results from the output queue as they become available.
        It continues yielding results as long as the worker thread is alive or there are results in the output queue.
        """
        while self.worker_thread.is_alive() or not self.output_queue.empty():
            try:
                yield self.output_queue.get(block=True, timeout=0.1)
            except queue.Empty:
                continue


if __name__ == "__main__":

    def process(x):
        time.sleep(x)
        print("Process {}".format(x), flush=True)
        return x

    def add_values(processor):
        print("Add values", flush=True)
        processor.add(1)
        time.sleep(0.5)
        processor.add(3)
        time.sleep(1)
        processor.add(4)
        processor.add(5)
        processor.end()

    processor = AsynchronousProcessor(process)

    threading.Thread(target=add_values, args=(processor,)).start()
    for x in processor.stream():
        print(x)
    print("Finished", flush=True)
