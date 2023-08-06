import typing
from typing import Optional

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QListWidget, QLabel, QSizePolicy, \
    QGroupBox

from maphis.common.state import State
from maphis.tags.tag_chooser import TagsChooser, Tags
from maphis.tags.tags_choosers import TagsChoosers, GroupsOfTags


class TagMappingWidget(QGroupBox):
    remove_this = Signal(QWidget)
    mapping_changed = Signal(list, list)
    complete_status_changed = Signal(bool)

    def __init__(self, state: State, parent: Optional[QWidget] = None,
                 f: Qt.WindowType = Qt.WindowType.Widget) -> None:
        super().__init__(parent)
        self._state = state
        self._setup_ui()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)

    def _setup_ui(self):
        self.setTitle('')
        self.main_layout: QVBoxLayout = QVBoxLayout()

        self._tag_map_widget = QWidget()
        self.tag_lists_layout: QHBoxLayout = QHBoxLayout()

        self._tag_map_widget.setLayout(self.tag_lists_layout)

        self.source_tags = TagsChooser(self._state, self, preceding_label='Median\nprofile of')
        # self.source_tags.selection_changed.connect(lambda _: self.relay_mapping())
        self.source_tags.selection_changed.connect(lambda _: self.complete_status_changed.emit(self.is_complete))

        self.tags_choosers: TagsChoosers = TagsChoosers(self._state, preceding_label='median\nprofile of')
        # self.tags_choosers.selection_changed.connect(lambda _: self.relay_mapping())
        self.tags_choosers.selection_changed.connect(lambda _: self.complete_status_changed.emit(self.is_complete))
        self.lblMapTo = QLabel("will be registered to the\nmedian of the following:")

        self.tag_lists_layout.addWidget(self.source_tags)
        self.tag_lists_layout.addWidget(self.lblMapTo)
        self.tag_lists_layout.addWidget(self.tags_choosers)

        self.main_layout.addWidget(self._tag_map_widget)

        self.btnRemoveThisWidget = QPushButton("x")
        self.btnRemoveThisWidget.clicked.connect(lambda: self.remove_this.emit(self))
        self.main_layout.addWidget(self.btnRemoveThisWidget)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def enable_remove_button(self, enable: bool):
        self.btnRemoveThisWidget.setEnabled(enable)
        self.btnRemoveThisWidget.setVisible(enable)

    def get_mapping(self) -> typing.Tuple[Tags, GroupsOfTags]:
        return self.source_tags.selected_tags(), self.tags_choosers.get_all_tag_groups()

    def set_mapping(self, mapping: typing.Tuple[Tags, GroupsOfTags]):
        self.source_tags.clear_tags()
        self.source_tags.set_selected_tags(mapping[0])

        for i, tags in enumerate(mapping[1]):
            if i >= self.tags_choosers.tag_choosers_layout.count():
                self.tags_choosers.add_tags_chooser()
            tag_chooser: TagsChooser = self.tags_choosers.tag_choosers_layout.itemAt(i).widget()
            tag_chooser.set_selected_tags(tags)

    def relay_mapping(self):
        self.mapping_changed.emit(self.source_tags.selected_tags(), self.tags_choosers.get_all_tag_groups())

    @property
    def is_complete(self) -> bool:
        return len(self.source_tags.selected_tags()) > 0 and all([len(sel_tags) > 0 for sel_tags in self.tags_choosers.get_all_tag_groups()])

    @property
    def is_complete_and_matches_photos(self) -> bool:
        return self.is_complete and self.source_tags.matching_photos_count > 0 and all([tag_chooser.matching_photos_count > 0 for tag_chooser in self.tags_choosers])
