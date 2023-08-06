import typing
from typing import Optional

import PySide6.QtCore
import PySide6.QtWidgets
from PySide6.QtWidgets import QWidget

from maphis.common.state import State
from maphis.tags.tag_chooser import TagsChooser, Tags


GroupsOfTags = typing.List[Tags]


class TagsChoosers(QWidget):
    selection_changed = PySide6.QtCore.Signal(TagsChooser)

    def __init__(self, state: State, init_count: int = 1, parent: Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowType = PySide6.QtCore.Qt.WindowType.Widget,
                 preceding_label='') -> None:
        super().__init__(parent, f)

        self.state = state
        self.preceding_label = preceding_label

        self.tag_choosers_layout = PySide6.QtWidgets.QVBoxLayout()

        self.main_layout = PySide6.QtWidgets.QVBoxLayout()

        self.main_layout.addLayout(self.tag_choosers_layout)

        self.btnAddChooser = PySide6.QtWidgets.QPushButton('+')
        self.btnAddChooser.clicked.connect(self.add_tags_chooser)

        self.main_layout.addWidget(self.btnAddChooser)
        self.main_layout.addStretch()

        for i in range(init_count):
            self.add_tags_chooser()
        self.setLayout(self.main_layout)

    def add_tags_chooser(self):
        tag_chooser = TagsChooser(self.state, self, preceding_label=self.preceding_label)
        tag_chooser.set_button_handler(lambda: self.remove_tags_chooser(tag_chooser))
        tag_chooser.selection_changed.connect(lambda _: self.selection_changed.emit(tag_chooser))
        # tag_chooser.set_button_visible(True)
        self.tag_choosers_layout.addWidget(tag_chooser)
        if self.tag_choosers_layout.count() > 1:
            for i in range(self.tag_choosers_layout.count()):
                tag_chooser: TagsChooser = self.tag_choosers_layout.itemAt(i).widget()
                tag_chooser.set_button_visible(True)
        self.selection_changed.emit(tag_chooser)

    def remove_tags_chooser(self, tag_chooser: TagsChooser):
        tag_chooser.hide()
        self.tag_choosers_layout.removeWidget(tag_chooser)
        tag_chooser.deleteLater()
        if self.tag_choosers_layout.count() == 1:
            tag_chooser: TagsChooser = self.tag_choosers_layout.itemAt(0).widget()
            tag_chooser.set_button_visible(False)
        self.selection_changed.emit(None)

    def get_all_tag_groups(self) -> GroupsOfTags:
        groups: GroupsOfTags = []
        for i in range(self.tag_choosers_layout.count()):
            tags_chooser: TagsChooser = self.tag_choosers_layout.itemAt(i).widget()
            groups.append(tags_chooser.selected_tags())
        return groups

    def __iter__(self) -> TagsChooser:
        for i in range(self.tag_choosers_layout.count()):
            tag_chooser: TagsChooser = self.tag_choosers_layout.itemAt(i).widget()
            yield tag_chooser
