import copy
import typing
from typing import Callable, Any

from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QValidator
from PySide6.QtWidgets import QWidget, QLineEdit, QSpinBox, QCheckBox, QHBoxLayout, QLabel


class Param(QObject):
    value_changed = Signal(object)

    def __init__(self):
        super().__init__()
        self.name: str = ''
        self.key: str = ''
        self.description: str = ''
        self._type = None
        self.widgets: typing.List[QWidget] = []
        self.value: typing.Any = None
        self._param_widget: typing.Optional[QWidget] = None

    def register_widget(self, widg: QWidget):
        pass

    def unregister_widget(self, widg: QWidget):
        pass

    def set_value(self, val: typing.Any):
        pass

    def get_default_ui_control(self) -> QWidget:
        pass

    def __hash__(self) -> int:
        return hash(self.key)

    def parse(self, val: str):
        pass


class StringParam(Param):

    def __init__(self):
        super().__init__()
        self.value = ''
        self.widgets: typing.List[QLineEdit] = []
        self.validator: typing.Optional[QValidator] = None
        self.parser: typing.Optional[Callable[[str], Any]] = None

    def set_validator(self, validator: typing.Optional[QValidator]):
        self.validator = validator
        for ledit in self.widgets:
            ledit.setValidator(self.validator)

    def set_parser(self, parser: typing.Callable[[str], typing.Any]):
        self.parser = parser

    def get_text_field(self) -> QLineEdit:
        ledit = QLineEdit()
        ledit.setText(self.value)
        if self.validator is not None:
            ledit.setValidator(self.validator)
        ledit.setObjectName(self.key)

        # container = QWidget()
        # layout = QHBoxLayout()
        # layout.addWidget(QLabel(self.name))
        # layout.addWidget(ledit)
        # container.setLayout(layout)

        def handle_text_changed(new_text: str):
            self.value = new_text
            for widget in self.widgets:
                if id(widget) == id(ledit):
                    continue
                widget.blockSignals(True)
                widget.setText(new_text)
                widget.blockSignals(False)
            self.value_changed.emit(self.value)
        ledit.textChanged.connect(handle_text_changed)
        self.widgets.append(ledit)
        return ledit

    def get_default_ui_control(self) -> QLineEdit:
        if self._param_widget is None:
            self._param_widget = self.get_text_field()
        return self._param_widget

    def parse(self, val: str):
        self.value = val
        for widget in self.widgets:
            widget.blockSignals(True)
            widget.setText(self.value)
            widget.blockSignals(False)
        self.value_changed.emit(self.value)


class IntParam(Param):

    def __init__(self):
        super().__init__()
        self.widgets: typing.List[QSpinBox] = []
        self.value = 0
        self.increment_step: int = 1
        self.min_value: typing.Optional[int] = None
        self.max_value: typing.Optional[int] = None

    def get_spinbox(self) -> QSpinBox:
        spbox = QSpinBox()
        if self.min_value is not None:
            spbox.setMinimum(self.min_value)
        if self.max_value is not None:
            spbox.setMaximum(self.max_value)
        spbox.setValue(self.value)
        spbox.setSingleStep(self.increment_step)
        spbox.setObjectName(self.key)

        # container = QWidget()
        # layout = QHBoxLayout()
        # layout.addWidget(QLabel(self.name))
        # layout.addWidget(spbox)
        # container.setLayout(layout)

        def handle_value_changed(val: int):
            self.value = val
            for widget in self.widgets:
                if id(widget) == id(spbox):
                    continue
                widget.blockSignals(True)
                widget.setValue(self.value)
                widget.blockSignals(False)
            self.value_changed.emit(self.value)
        spbox.valueChanged.connect(handle_value_changed)
        self.widgets.append(spbox)
        return spbox

    def get_default_ui_control(self) -> QSpinBox:
        if self._param_widget is None:
            self._param_widget = self.get_spinbox()
        return self._param_widget

    def set_value(self, val: int):
        if self.min_value <= val <= self.max_value:
            self.value = val
            for widg in self.widgets:
                widget: QSpinBox = widg
                widget.blockSignals(True)
                widget.setValue(val)
                widget.blockSignals(False)
            self.value_changed.emit(val)

    def parse(self, val: str):
        try:
            int_val = int(val)
            self.value = int_val
            for widget in self.widgets:
                widget.blockSignals(True)
                widget.setValue(self.value)
                widget.blockSignals(False)
            self.value_changed.emit(self.value)
        except ValueError:
            print(f"Cannot convert {val} to integer number.")


class BoolParam(Param):

    def __init__(self):
        super().__init__()
        self.value = True
        self.widgets: typing.List[QCheckBox] = []

    def get_checkbox(self) -> QCheckBox:
        chkbox = QCheckBox()
        chkbox.setChecked(self.value)
        chkbox.setObjectName(self.key)

        def handle_state_changed(state: int):
            self.value = state == Qt.CheckState.Checked.value
            for widget in self.widgets:
                if id(widget) == id(chkbox):
                    continue
                widget.blockSignals(True)
                widget.setChecked(self.value)
                widget.blockSignals(False)
            self.value_changed.emit(self.value)
        chkbox.setText(self.name)
        chkbox.stateChanged.connect(handle_state_changed)
        self.widgets.append(chkbox)
        return chkbox

    def get_default_ui_control(self) -> QCheckBox:
        if self._param_widget is None:
            self._param_widget = self.get_checkbox()
        return self._param_widget

    def parse(self, val: str):
        if val.lower() == 'true':
            self.value = True
        elif val.lower() == 'false':
            self.value = False
        else:
            raise ValueError(f'Cannot convert {val} into a boolean value.')
        for widget in self.widgets:
            widget.blockSignals(True)
            widget.setChecked(self.value)
            widget.blockSignals(False)


class ParamBuilder:
    def __init__(self):
        self.param: Param = Param()

    def name(self, name: str) -> 'ParamBuilder':
        self.param.name = name
        return self

    def key(self, key: str) -> 'ParamBuilder':
        self.param.key = key
        return self

    def description(self, desc: str) -> 'ParamBuilder':
        self.param.description = desc
        return self

    def string_param(self) -> 'StringParamBuilder':
        str_param_builder = StringParamBuilder()
        self.__copy_param(self.param, str_param_builder.param)
        return str_param_builder

    def int_param(self) -> 'IntParamBuilder':
        int_param_builder = IntParamBuilder()
        self.__copy_param(self.param, int_param_builder.param)
        return int_param_builder

    def bool_param(self) -> 'BoolParamBuilder':
        bool_param_builder = BoolParamBuilder()
        self.__copy_param(self.param, bool_param_builder.param)
        return bool_param_builder

    def __copy_param(self, src: Param, dst: Param):
        dst.name = src.name
        dst.key = src.key
        dst.description = src.description

    def build(self) -> Param:
        return self.param


class StringParamBuilder(ParamBuilder):
    def __init__(self):
        super().__init__()
        self.param: StringParam = StringParam()

    def default_value(self, val: str) -> 'StringParamBuilder':
        self.param.value = val
        return self

    def validator(self, validator: typing.Optional[QValidator]) -> 'StringParamBuilder':
        self.param.validator = validator
        return self

    def build(self) -> StringParam:
        return self.param


class IntParamBuilder(ParamBuilder):
    def __init__(self):
        super().__init__()
        self.param: IntParam = IntParam()
        self.param.value = 0

    def default_value(self, val: int) -> 'IntParamBuilder':
        self.param.value = val
        return self

    def min_value(self, val: typing.Optional[int]) -> 'IntParamBuilder':
        self.param.min_value = val
        return self

    def max_value(self, val: typing.Optional[int]) -> 'IntParamBuilder':
        self.param.max_value = val
        return self

    def build(self) -> IntParam:
        return self.param


class BoolParamBuilder(ParamBuilder):
    def __init__(self):
        super().__init__()
        self.param: BoolParam = BoolParam()
        self.param.value = True

    def true(self) -> 'BoolParamBuilder':
        self.param.value = True
        return self

    def false(self) -> 'BoolParamBuilder':
        self.param.value = False
        return self

    def build(self) -> BoolParam:
        return self.param
