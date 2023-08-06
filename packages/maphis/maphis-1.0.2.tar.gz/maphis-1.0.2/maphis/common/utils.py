import dataclasses
import os
import shutil
import subprocess
import typing
from copy import deepcopy
from pathlib import Path
import importlib.resources
import platform

import cv2
import numpy as np
import openpyxl
from PySide6.QtCore import Qt, QPoint, QMimeDatabase
from PySide6.QtGui import QImage, QCursor
from PySide6.QtWidgets import QFileDialog, QWidget, QMessageBox, QApplication, QPushButton
import pytesseract

from maphis import MAPHIS_PATH
from maphis.common.download import DownloadDialog
from maphis.common.units import Value, Unit, BaseUnit, CompoundUnit, SIPrefix


def create_file_dialog(root_folder: Path, title: str, mode: QFileDialog.FileMode,
                       extensions: typing.Optional[typing.List[str]], parent: QWidget) -> QFileDialog:
    file_dialog = QFileDialog(parent)
    file_dialog.setDirectory(str(root_folder))
    file_dialog.setFileMode(mode)
    file_dialog.setWindowTitle(title)
    file_dialog.setWindowModality(Qt.WindowModality.WindowModal)
    if extensions is not None:
        mime_db = QMimeDatabase()
        mime_types = [mime_db.mimeTypesForFileName(f'file.{ext}') for ext in extensions]
        filter_strings = [mime_type[0].filterString() for mime_type in mime_types if len(mime_type) > 0]
        file_dialog.setNameFilters(filter_strings)
    return file_dialog


def choose_folder(parent: QWidget, title = "Open folder", path: typing.Optional[Path] = None) -> typing.Optional[Path]:
    file_dialog = QFileDialog(parent)
    if path is not None:
        file_dialog.setDirectory(str(path))
    file_dialog.setFileMode(QFileDialog.FileMode.Directory)
    file_dialog.setWindowTitle(title)
    file_dialog.setWindowModality(Qt.WindowModal)
    if file_dialog.exec_():
        file_path = Path(file_dialog.selectedFiles()[0])
        return file_path
    return None


def let_user_open_path(root_folder: Path=Path.home(), title: str='Open',
                       mode: typing.Union[typing.Literal['single_file'], typing.Literal['files'], typing.Literal['directory']]='files',
                       extensions: typing.Optional[typing.List[str]]=None,
                       parent: typing.Optional[QWidget]=None) -> typing.List[Path]:
    if mode == 'single_file':
        file_mode = QFileDialog.FileMode.ExistingFile
    elif mode == 'files':
        file_mode = QFileDialog.FileMode.ExistingFiles
    else:
        file_mode = QFileDialog.FileMode.Directory
    file_dialog = create_file_dialog(root_folder, title, file_mode, extensions, parent)
    file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)

    if file_dialog.exec_():
        return [Path(selected_file) for selected_file in file_dialog.selectedFiles()]
    return []


def let_user_save_path(root_folder: Path=Path.home(), title: str='Save as',
                       mode: typing.Union[typing.Literal['single_file'], typing.Literal['directory']]='single_file',
                       extensions: typing.Optional[typing.List[str]]=None,
                       parent: typing.Optional[QWidget]=None) -> typing.Optional[Path]:
    if mode == 'single_file':
        file_mode = QFileDialog.FileMode.AnyFile
    else:
        file_mode = QFileDialog.FileMode.Directory

    file_dialog = create_file_dialog(root_folder, title, file_mode, extensions, parent)
    file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)

    if file_dialog.exec_():
        if len(file_dialog.selectedFiles()) > 0:
            return Path(file_dialog.selectedFiles()[0])
    return None


def get_dict_from_doc_str(doc_str: str) -> typing.Dict[str, str]:
    lines = [line for line in doc_str.splitlines() if len(line) > 0 and not line.isspace()]

    splits = [line.split(':') for line in lines]
    splits = [split for split in splits if len(split) == 2]

    return {split[0].strip(): split[1].strip() for split in splits}


def is_valid_annotation_project(path: Path, req_folders: typing.List[str]) -> bool:
    return all([(path / folder).exists() for folder in req_folders])


def get_scale_marker_roi(img: np.ndarray) -> typing.Tuple[np.ndarray, typing.Tuple[int, int, int, int]]:
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    gray_ = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)))

    _, th = cv2.threshold(gray_, 245, 255, cv2.THRESH_BINARY)

    closed = cv2.morphologyEx(th, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15)))
    closed = cv2.morphologyEx(closed, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15)))

    N, label_img, stats, centroids = cv2.connectedComponentsWithStats(closed, None, None, None, 4)

    ratios: typing.List[float] = []

    for i in range(N):
        l, t, w, h = stats[i, [cv2.CC_STAT_LEFT, cv2.CC_STAT_TOP, cv2.CC_STAT_WIDTH, cv2.CC_STAT_HEIGHT]]
        if int(l)+int(w) > closed.shape[1] or int(t)+int(h) > closed.shape[0]:
            ratios.append(-42)
            continue
        nonzeros = np.count_nonzero(th[t:t+h, l:l+w])
        bbox_area = w * h
        ratios.append(nonzeros / bbox_area)

    idxs = np.argsort(ratios)
    largest_idx = idxs[-1]

    top, left, height, width = stats[largest_idx, [cv2.CC_STAT_TOP, cv2.CC_STAT_LEFT, cv2.CC_STAT_HEIGHT, cv2.CC_STAT_WIDTH]]

    return gray[top:top+height, left:left+width], (left, top, width, height)


def get_scale_line_ends(scale_marker: np.ndarray) -> typing.Tuple[int, int, int, int]:
    roi = scale_marker
    height, width = scale_marker.shape[0], scale_marker.shape[1]
    inv_roi = 255 - roi
    _, inv_roi = cv2.threshold(inv_roi, 245, 255, cv2.THRESH_BINARY)

    if height > width:
        print('height > width')
        only_line = cv2.morphologyEx(inv_roi, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15)),
                                     borderType=cv2.BORDER_CONSTANT, borderValue=0)

        nonzero = np.nonzero(only_line)

        if len(nonzero[0]) == 0:
            return -1, 0, 0, 0

        p1_y, p1_x = np.min(nonzero[0]), np.min(nonzero[1])
        p2_y = np.max(nonzero[0])
        p2_x = p1_x
    else:
        print('width > height')
        only_line = cv2.morphologyEx(inv_roi, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1)),
                                     borderType=cv2.BORDER_CONSTANT, borderValue=0)

        nonzero = np.nonzero(only_line)

        if len(nonzero[0]) == 0:
            print("Scale line not found")
            return -1, -1, -1, -1

        p1_y, p1_x = np.min(nonzero[0]), np.min(nonzero[1])
        p2_x = np.max(nonzero[1])
        p2_y = p1_y

    return p1_x, p1_y, p2_x, p2_y


def get_reference_length(img: np.ndarray) -> typing.Tuple[str, np.ndarray]:
    tesseract_bin_path = MAPHIS_PATH / 'bin' / 'Tesseract-OCR' / 'tesseract.exe'
    try:
        if platform.system() == 'Windows':
            if not check_if_tesseract_present():
                raise pytesseract.TesseractNotFoundError
                # return '', img
            pytesseract.pytesseract.tesseract_cmd = str(tesseract_bin_path)
        rot = img
        for i in range(4):
            rot = cv2.rotate(rot, cv2.ROTATE_90_CLOCKWISE)
            text = pytesseract.image_to_string(rot)
            if len(text) == 0:
                continue
            if text[0].isdigit() and rot.shape[1] >= rot.shape[0]:
                return text, rot
    except pytesseract.TesseractNotFoundError:
        if platform.system() == 'Windows':
            text = f'Could not locate and download Tesseract OCR. Please download the binary version of Tesseract OCR and install it in the location {tesseract_bin_path}.'
        else:
            text = 'Please install Tesseract OCR.'
        QMessageBox.warning(QApplication.activeWindow(), "Tesseract OCR not found", text, QMessageBox.StandardButton.Ok)
    return '', img


def vector_to_img(vec: typing.Union[np.ndarray, typing.List[float]], size: typing.Tuple[int, int]) -> np.ndarray:
    vec_min, vec_max = np.min(vec), np.max(vec)

    if isinstance(vec, list):
        vec = np.array(vec)

    stretched = (size[1] - 1) - np.round((size[1] - 1) * ((vec - vec_min) / (vec_max - vec_min + 1e-6))).astype(np.uint16)

    img = 255 * np.ones(size[::-1], np.uint8)
    step = round(size[0] / len(vec))

    for i in range(1, len(vec)):
        img = cv2.line(img, (step * (i-1), stretched[i-1]), (step * i, stretched[i]), 0, 1)

    return img


def vector_to_img2(vec: typing.Union[np.ndarray, typing.List[float]], size: typing.Tuple[int, int]) -> np.ndarray:
    vec_min, vec_max = np.min(vec), np.max(vec)

    vec_min = round(vec_min)
    vec_max = round(vec_max + 0.5)

    if isinstance(vec, list):
        vec = np.array(vec)

    stretched = (size[1] - 1) - np.round((size[1] - 1) * ((vec - vec_min) / (vec_max - vec_min + 1e-6))).astype(np.uint16)

    height = vec_max - vec_min

    # img = 255 * np.ones(size[::-1], np.uint8)
    img = 255 * np.ones((height, 256))
    step = round(256 / len(vec))

    for i in range(1, len(vec)):
        img = cv2.line(img, (step * (i-1), round(vec[i-1])), (step * i, round(vec[i])), 0, 1)

    return img


def is_cursor_inside(widget: QWidget) -> bool:
    rect = widget.rect()
    rect.moveTo(widget.mapToGlobal(QPoint(0, 0)))
    return rect.contains(QCursor.pos())


@dataclasses.dataclass
class ScaleLineInfo:
    p1: typing.Tuple[int, int]
    p2: typing.Tuple[int, int]
    length: Value

    def __repr__(self) -> str:
        return f'ScaleLineInfo(p1={repr(self.p1)}, p2={repr(self.p2)}, length={repr(self.length)})'

    def rotate(self, ccw: bool, origin: typing.Tuple[int, int]):
        p1_c = complex(self.p1[0] - origin[0], self.p1[1] - origin[1])
        p2_c = complex(self.p2[0] - origin[0], self.p2[1] - origin[1])

        p1_c = p1_c * complex(0, -1 if ccw else 1)
        p2_c = p2_c * complex(0, -1 if ccw else 1)

        p1 = (round(p1_c.real), round(p1_c.imag))
        p1 = (p1[0] + origin[1], p1[1] + origin[0])

        p2 = (round(p2_c.real), round(p2_c.imag))
        p2 = (p2[0] + origin[1], p2[1] + origin[0])

        self.p1 = p1
        self.p2 = p2

    def scale(self, f: float, o: typing.Tuple[int, int]):
        p1_ = (f * (self.p1[0] - o[0]), f * (self.p1[1] - o[1]))
        p2_ = (f * (self.p2[0] - o[0]), f * (self.p2[1] - o[1]))

        self.p1 = (round(p1_[0] + f * o[0]), round(p1_[1] + f * o[1]))
        self.p2 = (round(p2_[0] + f * o[0]), round(p2_[1] + f * o[1]))


@dataclasses.dataclass
class ScaleSetting:
    reference_length: typing.Optional[Value] = None
    scale: typing.Optional[Value] = None
    scale_line: typing.Optional[ScaleLineInfo] = None
    scale_marker_bbox: typing.Optional[typing.Tuple[int, int, int, int]] = None
    scale_marker_img: typing.Optional[QImage] = None

    @classmethod
    def from_dict(cls, obj_dict: typing.Dict[str, typing.Any]) -> 'ScaleSetting':
        if (maybe_ref_l := obj_dict.get('reference_length')) is not None:
            ref_l = eval(maybe_ref_l)
        else:
            ref_l = None

        if (maybe_scale := obj_dict.get('scale')) is not None:
            scale = eval(maybe_scale)
        else:
            scale = None

        if (maybe_scale_line := obj_dict.get('scale_line')) is not None:
            scale_line = eval(maybe_scale_line)
        else:
            scale_line = None

        if (maybe_bbox := obj_dict.get('scale_marker_bbox')) is not None:
            scale_marker_bbox = eval(maybe_bbox)
        else:
            scale_marker_bbox = None

        return ScaleSetting(reference_length=ref_l,
                            scale=scale,
                            scale_line=scale_line,
                            scale_marker_bbox=scale_marker_bbox)

    def scale_by_factor(self, fac: float, o: typing.Tuple[int, int]):
        if self.scale is not None:
            self.scale.value *= fac
        if self.scale_line is not None:
            self.scale_line.scale(fac, o)

    def __deepcopy__(self, memodict={}):
        sc_setting = ScaleSetting(reference_length=deepcopy(self.reference_length),
                                  scale=deepcopy(self.scale),
                                  scale_line=deepcopy(self.scale_line),
                                  scale_marker_bbox=deepcopy(self.scale_marker_bbox),
                                  scale_marker_img=self.scale_marker_img)
        return sc_setting


def open_with_default_app(path: Path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])


def check_if_tesseract_present() -> bool:
    bin_path = MAPHIS_PATH / 'bin'
    tess_path = bin_path / 'Tesseract-OCR'
    if not tess_path.exists():
        download_path = bin_path / 'tesseract.zip'
        download = DownloadDialog("https://gitlab.fi.muni.cz/xmraz3/maphis_pekar_segmentation/-/raw/main/Tesseract-OCR.zip",
                                  download_path, label='Downloading Tesseract OCR engine.',
                                  title="First-time initialization")

        if not download.start():
            return False
        shutil.unpack_archive(download_path, download_path.parent)
        os.remove(download_path)
        return True
    else:
        return True


def attempt_to_save_with_retries(save_function: typing.Callable[[Path, typing.Any], typing.Any],
                                 title, mode, extensions, parent, **kwargs) -> typing.Tuple[typing.Optional[Path], typing.Any]:
    if 'path' not in kwargs:
        kwargs['path'] = let_user_save_path(Path.home(), title, mode, extensions, parent)
    if kwargs['path'] is None:
        return None, None
    results_saved_or_cancelled = False

    while not results_saved_or_cancelled:
        try:
            func_ret_val = save_function(**kwargs)
            results_saved_or_cancelled = True
            # show_success_info_dialog(path)
            return kwargs['path'], func_ret_val
        except PermissionError:
            path = show_error_and_ask_for_other_path(kwargs['path'], title, mode, extensions, parent)
            if path is None:
                results_saved_or_cancelled = True
            else:
                kwargs['path'] = path
    return None, None


def show_success_info_dialog(output_path: Path):
    diag_box = QMessageBox(QMessageBox.Icon.Information, "Saving complete",
                       f"The file is stored in {output_path}. Do you wish to open the folder?",
                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                       QApplication.activeWindow())
    diag_box.button(QMessageBox.StandardButton.Yes).clicked.connect(diag_box.accept)
    diag_box.button(QMessageBox.StandardButton.No).clicked.connect(diag_box.reject)

    if diag_box.exec_() == QMessageBox.DialogCode.Accepted:
        open_with_default_app(output_path.parent)
    diag_box.close()
    diag_box.deleteLater()


def show_error_and_ask_for_other_path(old_path: Path, title, mode, extensions, parent) -> typing.Optional[Path]:
    diag = QMessageBox(parent)
    diag.setWindowTitle('Cannot save the results')
    diag.setText(
        f"The file {old_path} cannot be used for saving (maybe it's opened in another program).")
    diag.addButton(QMessageBox.StandardButton.Cancel)
    diag.addButton(QMessageBox.StandardButton.Open)
    button: QPushButton = diag.button(QMessageBox.StandardButton.Open)
    button.clicked.connect(diag.accept)
    button.setText('Save as...')

    if diag.exec_() == QMessageBox.DialogCode.Accepted:
        return let_user_save_path(old_path.parent, title, mode, extensions, parent)
    return None


def save_text(path: Path, text: str):
    with open(path, 'w') as f:
        f.write(text)


def catch_exception_and_show_messagebox(title: str, text: str, msg_icon: QMessageBox.Icon, print_exception: bool=False):
    def msg_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                ret = func(*args, **kwargs)
                return ret
            except Exception as e:
                diag = QMessageBox(msg_icon, title.format_map(kwargs),
                                   text.format_map(kwargs),
                                   QMessageBox.StandardButton.Close, parent=QApplication.activeWindow())
                if print_exception:
                    diag.setDetailedText(str(e))
                diag.exec_()
            return None
        return wrapper
    return msg_decorator