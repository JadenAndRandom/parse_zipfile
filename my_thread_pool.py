
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtCore import QObject, pyqtSignal


class MyThreadPool(QObject):
    finished = pyqtSignal(object)

    def __init__(self, parent=None, max_workers=None):
        super().__init__(parent)
        self._executor = ThreadPoolExecutor(max_workers)

    @property
    def executor(self):
        return self._executor

    def submit(self, fn, *args, **kwargs):
        future = self.executor.submit(fn, *args, **kwargs)
        future.add_done_callback(self._internal_done_callback)

    def _internal_done_callback(self, future):
        data = future.result()
        self.finished.emit(data)
