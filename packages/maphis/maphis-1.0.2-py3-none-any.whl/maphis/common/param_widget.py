import typing

from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QGroupBox

from maphis.common.user_param import Param, BoolParam


class ParamWidget:
    def __init__(self, params: typing.List[Param], title: str='', group_box: bool=False):
        self.params: typing.List[Param] = []
        self.widget: QWidget = QGroupBox(title) if group_box else QWidget()
        self.widget.setWindowTitle(title)
        self.widget_layout: QGridLayout = QGridLayout()
        self.param_widget_dict: typing.Dict[Param, QWidget] = {}

        for i, param in enumerate(params):
            widget = param.get_default_ui_control()
            self.param_widget_dict[param] = widget
            if isinstance(param, BoolParam):
                self.widget_layout.addWidget(widget, i, 0)
            else:
                qlabel = QLabel()
                qlabel.setText(param.name)
                self.widget_layout.addWidget(qlabel, i, 0)
                self.widget_layout.addWidget(widget, i, 1)
            # self.widget_layout.addWidget(widget)

        self.widget.setLayout(self.widget_layout)

    def destroy(self):
        self.widget.hide()
        for param, widget in self.param_widget_dict.items():
            param.unregister_widget(widget)
            widget.deleteLater()
        self.widget.deleteLater()