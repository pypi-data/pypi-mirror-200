import os
import pathlib
from typing import Optional

import PySide6.QtCore
import requests
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QProgressDialog, QMessageBox


class DownloadDialog(QObject):
    download_finished = Signal()
    download_failed = Signal()
    download_aborted = Signal()

    def __init__(self, url: str, dst: pathlib.Path, label: str='', title: str='', parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)
        self.dst = dst
        self.url = url
        self.response = requests.get(url, stream=True)
        self.size_in_bytes = int(self.response.headers.get('content-length', 0))
        self.block_size = 1024
        self.label = f'Downloading file from {self.url}' if label == '' else label
        self.title = 'Download in progress' if title == '' else title

        self.progress_dialog = QProgressDialog(labelText=self.label)
        self.progress_dialog.setWindowTitle(self.title)
        self.progress_dialog.setWindowModality(PySide6.QtCore.Qt.WindowModality.ApplicationModal)
        self.progress_dialog.setMinimum(0)
        self.progress_dialog.setMaximum(self.size_in_bytes)
        self.downloaded_bytes = 0

    def start(self) -> bool:
        self.progress_dialog.show()
        try:
            with open(self.dst, 'wb') as f:
                for data in self.response.iter_content(self.block_size):
                    self.downloaded_bytes += len(data)
                    f.write(data)
                    if self.progress_dialog.wasCanceled():
                        f.close()
                        os.remove(self.dst)
                        self.progress_dialog.close()
                        self.download_aborted.emit()
                        return False
                    self.progress_dialog.setValue(self.downloaded_bytes)
        except Exception as e:
            QMessageBox.critical(None, 'Download not finished', str(e), QMessageBox.StandardButton.Ok)
            f.close()
            os.remove(self.dst)
            return False
        self.progress_dialog.close()
        if self.downloaded_bytes == self.size_in_bytes or self.size_in_bytes == 0:
            self.download_finished.emit()
            return True
        else:
            self.download_failed.emit()
            return False
