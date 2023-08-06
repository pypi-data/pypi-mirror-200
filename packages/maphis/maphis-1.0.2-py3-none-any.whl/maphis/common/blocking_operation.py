import typing

from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QProgressDialog, QWidget

from maphis.common.photo import Photo
from maphis.common.storage import Storage


class BlockingOperation:
    def __init__(self, storage: Storage, idxs: typing.List[int], operation: typing.Callable[[Storage, int], typing.Any],
                 result_handler: typing.Callable[[Storage, int, typing.Any], None], parent: QWidget):
        self.storage = storage
        self.indexes = idxs
        self.op = operation
        self.handler = result_handler
        self.parent = parent
        self.prgr_diag = QProgressDialog('Processing', 'Cancel', 0, len(self.indexes), self.parent)
        self.prgr_diag.setWindowTitle('Operation running')  # TODO allow to customize the title
        self.prgr_diag.setWindowModality(Qt.ApplicationModal)
        self.prgr_diag.setMinimumDuration(1)
        self.prgr_diag.show()
        self.prgr_diag.setLabelText('Initializing')
        self.prgr_diag.setValue(0)
        QCoreApplication.processEvents()

    def start(self):
        for i, idx in enumerate(self.indexes):
            self.prgr_diag.setValue(i)
            photo_name = self.storage.image_names[idx]
            self.prgr_diag.setLabelText(f'Processing {photo_name}')
            QCoreApplication.processEvents()
            if self.prgr_diag.wasCanceled():
                break
            self.handler(self.storage, idx, self.op(self.storage, idx))
        self.prgr_diag.setValue(len(self.indexes))
        self.prgr_diag.close()

    def close(self):
        self.prgr_diag.close()


class ProgressReport:
    def __init__(self, count: int, title_text: str, parent: typing.Optional[QWidget] = None):
        self.dialog = QProgressDialog()
        self.dialog.setWindowTitle(title_text)
        self.count = count
        self.current_count = 0

        self.dialog.setMinimum(0)
        self.dialog.setMaximum(count-1)

        self.dialog.setValue(0)
        self.dialog.show()

    def increment(self):
        self.current_count += 1
        self.dialog.setValue(self.current_count)
        QCoreApplication.processEvents()
        if self.current_count == self.count:
            self.dialog.close()
