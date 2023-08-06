import json
import pathlib
import typing
from enum import IntEnum
from functools import partial
from typing import Optional

import PySide6
from PySide6.QtCore import Qt, QItemSelection, QModelIndex, QItemSelectionModel, Signal, QUrl, QObject
from PySide6.QtGui import QIcon, QPixmap, QColor, QBrush
from PySide6.QtWidgets import QDialog, QTreeWidgetItem, QTreeWidget, QAbstractItemView, QDialogButtonBox, QVBoxLayout, \
    QWidget, QGroupBox, QFileDialog, QMessageBox

from maphis.common.utils import let_user_save_path, attempt_to_save_with_retries, save_text, let_user_open_path, \
    catch_exception_and_show_messagebox
from maphis.common.common import Info
from maphis.common.label_hierarchy import Node, LabelHierarchy
from maphis.common.label_tree_model import LabelTreeModel, LabelTreeMode
from maphis.common.plugin import PropertyComputation
from maphis.common.state import State
from maphis.common.user_params import UserParam, UserParamWidgetBinding, create_params_widget
from maphis.measurements_viewer.ui_measurement_assign_dialog import Ui_MeasurementAssignDialog
from maphis.plugin_manager_ import RegionCompsListModel
from maphis.color_tolerance_dialog import ColorToleranceDialog
from maphis.plugin_manager.plugin_store import PluginStore


class AssignmentTreeDataRole(IntEnum):
    ComputationKey = Qt.UserRole,
    ComputationObject = Qt.UserRole + 1,
    ParentKey = Qt.UserRole + 2,
    LabelNode = Qt.UserRole + 3,
    IsLeaf = Qt.UserRole + 4


class MeasurementTreeDataRoles(IntEnum):
    ComputationKey = Qt.UserRole,
    ComputationObject = Qt.UserRole + 1,


class PropertyAssignment(QObject):
    regions_added = Signal(PropertyComputation, set)
    regions_removed = Signal(PropertyComputation, set)

    def __init__(self, prop_comp: PropertyComputation, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)
        self.computation: PropertyComputation = prop_comp
        self.regions: typing.Set[Node] = set()
        self.props: typing.Set[str] = set()
        self._settings: typing.Dict[str, typing.Dict[str, str]] = {}

    def __contains__(self, label_node: Node) -> bool:
        return label_node in self.regions

    def add_regions(self, regions: typing.Set[Node]):
        to_add = regions.difference(self.regions)
        self.regions = self.regions.union(to_add)
        self.regions_added.emit(self.computation, to_add)

    def remove_regions(self, regions: typing.Set[Node]):
        to_remove = self.regions.intersection(regions)
        self.regions = self.regions.difference(to_remove)
        self.regions_removed.emit(self.computation, to_remove)

    @property
    def computation_settings(self) -> typing.Dict[str, typing.Dict[str, str]]:
        if len(self._settings) == 0:
            return self.computation.current_settings_to_str_dict()
        return self._settings

    @computation_settings.setter
    def computation_settings(self, settings: typing.Dict[str, typing.Dict[str, str]]):
        self._settings = settings

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'computation_key': self.computation.info.key,
            'regions': [node.label for node in self.regions],
            'settings': self.computation.current_settings_to_str_dict(),
            'requested_properties': self.computation.requested_props
        }

    @staticmethod
    def from_dict(_dict: typing.Dict[str, typing.Any], lab_hierarchy: LabelHierarchy) -> 'PropertyAssignment':
        store = PluginStore.instance()
        prop_comps = store.all_property_computations
        # TODO remove this if eventually
        if (prop_key := _dict['computation_key']).startswith('arthropod_describer.'):
            _, suffix = prop_key.split('arthropod_describer.')
            prop_key = f'maphis.{suffix}'
        prop_comp = [prop_comp for prop_comp in prop_comps if prop_comp.info.key == prop_key]
        if len(prop_comp) == 0:
            # TODO or raise an exception
            return None
        prop_assig = PropertyAssignment(prop_comp[0])
        prop_assig.regions = set(lab_hierarchy.nodes[label] for label in _dict['regions'])
        prop_assig.properties = _dict['requested_properties']

        return prop_assig


class MeasurementAssignDialog(QDialog):
    compute_measurements = Signal(dict)

    def __init__(self, state: State, comp_model: RegionCompsListModel, parent: typing.Optional[PySide6.QtWidgets.QWidget] = None,
                 f: Qt.WindowFlags = Qt.WindowFlags()):
        super().__init__(parent, f)
        self.ui = Ui_MeasurementAssignDialog()
        self.ui.setupUi(self)
        self.ui.labelTree.setSelectionMode(QAbstractItemView.MultiSelection)
        # self.ui.btnAssign.clicked.connect(self.assign_measurements)
        self.ui.btnAssign.clicked.connect(self.create_new_assignments_from_selection)

        self.ui.assignmentTree.itemSelectionChanged.connect(self.assignment_selection_changed)
        self.ui.assignmentTree.clicked.connect(tree_item_double_click_handler(self.ui.assignmentTree))
        self.ui.assignmentTree.selectionModel().selectionChanged.connect(self.deselect_ancestors_of_leaves)

        self.ui.measurementTree.itemSelectionChanged.connect(self.measurement_selection_changed)

        self.ui.btnLabelSelectAll.clicked.connect(self.ui.labelTree.selectAll)
        self.ui.btnLabelDeselectAll.clicked.connect(self.ui.labelTree.clearSelection)

        self.ui.btnMeasSelectAll.clicked.connect(self.ui.measurementTree.selectAll)
        self.ui.btnMeasDeselectAll.clicked.connect(self.ui.measurementTree.clearSelection)

        self.ui.btnAssignmentSelectAll.clicked.connect(self.ui.assignmentTree.selectAll)
        self.ui.btnAssignmentDeselectAll.clicked.connect(self.ui.assignmentTree.clearSelection)

        self.ui.btnAssignmentRemove.clicked.connect(self.remove_assignment_by_selection)

        self.ui.btnDemoSelectColorAndTolerance.hide()
        self.ui.btnDemoSelectColorAndTolerance.clicked.connect(self.demo_select_color_and_tolerance)

        self.ui.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)

        self.ui.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.accept)

        self.state = state
        self._label_tree_model = LabelTreeModel(self.state, LabelTreeMode.Choosing)
        self.ui.labelTree.setModel(self._label_tree_model)
        self.ui.labelTree.selectionModel().selectionChanged.connect(self.label_selection_changed)
        self.ui.labelTree.setStyleSheet('QTreeView::item:disabled {color: #c0c0c0;}')

        self.comps_model = comp_model

        # self.measurement_items: typing.List[QTreeWidgetItem] = []

        self.label_items: typing.Dict[int, QTreeWidgetItem] = {}

        # self.assignments: typing.Dict[str, typing.Set[int]] = {}
        # self.assignments: typing.Dict[str, typing.Set[int]] = {}
        self.assignment_items: typing.List[QTreeWidgetItem] = []
        # self.assignment_prop_items: typing.Dict[str, QTreeWidgetItem] = {}
        self.assignment_label_items: typing.Dict[Node, QTreeWidgetItem] = {}

        self.property_assignments: typing.Dict[PropertyComputation, PropertyAssignment] = {}

        self._setup_demo_color_tolerance_dialog()

        self.settings_layout = QVBoxLayout()
        self.ui.scrollAreaWidgetContents.setLayout(self.settings_layout)
        # self.param_settings_for_props: typing.Dict[str, typing.List[UserParam]] = {}
        self.param_bindings_for_props: typing.Dict[PropertyComputation, UserParamWidgetBinding] = {}
        self.param_widgets_for_props: typing.Dict[PropertyComputation, QWidget] = {}

        self.current_label_name: str = ''

        self.ui.btnSaveConfiguration.clicked.connect(self._save_current_assignment)
        self.ui.btnLoadConfiguration.clicked.connect(self._load_assignments)

    def _save_current_assignment(self):
        save_path = let_user_save_path(extensions=['json'], parent=self)
        if save_path is None:
            return
        assignments_json = [prop_assignment.to_dict() for prop_assignment in self.property_assignments.values() if len(prop_assignment.regions)]

        config_str = json.dumps(assignments_json, indent=2)
        attempt_to_save_with_retries(save_text, title='Save configuration as...', mode='single_file', path=save_path, extensions=['json'], parent=self, text=config_str)

    def _load_assignments(self):
        # result: typing.Tuple[QUrl, typing.Any] = QFileDialog.getOpenFileUrl(self, 'Open configuration as...')
        # if result[0].isEmpty():
        #     return
        load_path = let_user_open_path(pathlib.Path.home(), title='Open configuration file',
                                       mode='single_file', extensions=['json'], parent=self)
        if len(load_path) == 0:
            return
        load_path = load_path[0]
        self.try_to_load_assignments_from(load_path=load_path)

    @catch_exception_and_show_messagebox('Loading configuration file failed',
                                         'Could not load configuration from {load_path}',
                                         QMessageBox.Icon.Critical, print_exception=True)
    def try_to_load_assignments_from(self, load_path: pathlib.Path):
        with open(load_path) as f:
            assignments_dicts = json.load(f)
        # TODO clear current assignments
        for assignment_dict in assignments_dicts:
            _prop_assignment: PropertyAssignment = PropertyAssignment.from_dict(assignment_dict, self.state.storage.get_label_hierarchy('Labels'))
            prop_assignment = self.property_assignments[_prop_assignment.computation]
            prop_assignment.add_regions(_prop_assignment.regions)
            # TODO laod also property settings
            prop_assignment.computation.setup_settings_from_dict(assignment_dict['settings'])

    def _populate_label_tree(self):
        self.ui.labelTree.clear()
        hierarchy = self.state.storage.get_label_hierarchy(self.current_label_name)
        colormap = hierarchy.colormap
        codes = [hierarchy.code(label) for label in hierarchy.labels]
        codes.sort()
        parent = self.ui.labelTree
        sibling = None
        stack = []
        depth = -1
        used_labels = self.state.storage.used_regions(self.current_label_name)
        print(used_labels)
        for code in codes[1:]:
            label = hierarchy.label(code)
            code_depth = hierarchy.get_level(hierarchy.label(code))
            if code_depth > depth:
                if depth >= 0:
                    stack.append(parent)
                parent = parent if sibling is None else sibling
                depth = code_depth
                sibling = None
            elif code_depth < depth:
                pop_count = depth - code_depth
                if pop_count > 1:
                    for _ in range(pop_count - 1):
                        sibling = stack.pop()
                else:
                    sibling = parent
                parent = stack.pop()
                depth = code_depth
            twidget = QTreeWidgetItem(parent, after=sibling)
            twidget.setExpanded(True)
            label = hierarchy.label(code)
            label_node = hierarchy.nodes[label]
            twidget.setText(0, label_node.name)
            twidget.setData(0, Qt.UserRole, label)
            pixmap = QPixmap(24, 24)
            pixmap.fill(QColor.fromRgb(*colormap[label]))
            icon = QIcon(pixmap)
            twidget.setIcon(0, icon)
            self.label_items[label] = twidget
            if label in used_labels or any(map(partial(hierarchy.is_ancestor_of, label), used_labels)):
                twidget.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            else:
                twidget.setFlags(Qt.ItemIsEnabled)
                twidget.setForeground(0, QBrush(QColor.fromRgb(120, 120, 120)))
            sibling = twidget
        self.ui.labelTree.addTopLevelItem(stack[2])
        self.ui.labelTree.doubleClicked.connect(tree_item_double_click_handler(self.ui.labelTree))

    def _populate_measurement_comps_tree(self):
        prop_comps: typing.List[PropertyComputation] = self.comps_model.region_comps
        self.ui.measurementTree.clear()
        group_items: typing.Dict[str, QTreeWidgetItem] = {}

        self.property_assignments.clear()

        for prop_comp in prop_comps:
            self.property_assignments[prop_comp] = PropertyAssignment(prop_comp)
            prop_assig = self.property_assignments[prop_comp]
            prop_assig.regions_added.connect(self._add_regions_to_property_computation)
            prop_assig.regions_removed.connect(self._remove_regions_from_property_computation)
            if prop_comp.group not in group_items:
                group_item = QTreeWidgetItem(self.ui.measurementTree)
                group_item.setText(0, prop_comp.group)
                group_item.setFlags(Qt.ItemIsEnabled)
                group_items[prop_comp.group] = group_item
            parent = group_items[prop_comp.group]
            # parent = QTreeWidgetItem(self.ui.measurementTree)
            # parent.setText(0, prop_comp.info.name)
            # parent.setData(0, Qt.UserRole, prop_comp.info.key)
            # parent.setFlags(Qt.ItemIsEnabled)
            for prop in prop_comp.computes.values():
                kid = QTreeWidgetItem(parent)
                kid.setText(0, prop.name)
                kid.setToolTip(0, prop.description)
                kid.setData(0, MeasurementTreeDataRoles.ComputationKey, prop_comp.info.key)
                kid.setData(0, MeasurementTreeDataRoles.ComputationObject, prop_comp)
                parent.addChild(kid)
        self.ui.measurementTree.expandAll()
        self.ui.measurementTree.doubleClicked.connect(tree_item_double_click_handler(self.ui.measurementTree))

    # def _populate_assignment_tree(self):
    #     self.ui.assignmentTree.clear()
    #     top_level = []
    #     prop_comps: typing.List[PropertyComputation] = self.comps_model.region_comps
    #     for prop_comp in prop_comps:
    #         twidget = QTreeWidgetItem(self.ui.assignmentTree)
    #         twidget.setText(0, prop_comp.info.name)
    #         twidget.setData(0, AssignmentTreeDataRole.ComputationKey, prop_comp.info.key)
    #         twidget.setData(0, AssignmentTreeDataRole.ComputationObject, prop_comp)
    #         twidget.setData(0, AssignmentTreeDataRole.IsLeaf, False)
    #         twidget.setFlags(Qt.ItemIsEnabled)
    #         top_level.append(twidget)
    #         twidget.setHidden(True)
    #         twidget.setExpanded(True)
    #         props: typing.List[Info] = list(prop_comp.computes.values())
    #         for prop in props:
    #             absolute_key = f'{prop_comp.info.key}.{prop.key}'
    #             self.assignments[absolute_key] = set()
    #             kid = QTreeWidgetItem()
    #             kid.setText(0, prop.name)
    #             kid.setToolTip(0, prop.description)
    #             kid.setData(0, ABS_KEY_ROLE, absolute_key)
    #             kid.setData(0, LEAF_ITEM_ROLE, False)
    #             kid.setExpanded(True)
    #             kid.setHidden(True)
    #             kid.setFlags(Qt.ItemIsEnabled)
    #             twidget.addChild(kid)
    #             self.assignment_prop_items[absolute_key] = kid
    #     self.ui.assignmentTree.addTopLevelItems(top_level)
    #     self.assignment_items = top_level

    def _add_regions_to_property_computation(self, computation: PropertyComputation, regions: typing.Set[Node]):
        for node in regions:
            if node not in self.assignment_label_items:
                label_item = QTreeWidgetItem()
                label_item.setText(0, node.name)
                pixmap = QPixmap(32, 32)
                pixmap.fill(QColor(*node.color))
                label_item.setIcon(0, QIcon(pixmap))
                label_item.setData(0, AssignmentTreeDataRole.LabelNode, node)
                label_item.setData(0, AssignmentTreeDataRole.IsLeaf, False)
                self.ui.assignmentTree.addTopLevelItem(label_item)
                self.assignment_label_items[node] = label_item
            label_tree_item: QTreeWidgetItem = self.assignment_label_items[node]
            if computation.setting_widget is not None and computation not in self.param_widgets_for_props:
                grp_box = QGroupBox(computation.info.name)
                grp_box.setLayout(QVBoxLayout())
                grp_box.layout().addWidget(computation.setting_widget)
                self.param_widgets_for_props[computation] = grp_box
                self.settings_layout.addWidget(grp_box)
            prop_key = computation.info.key
            twidget = QTreeWidgetItem()
            twidget.setText(0, computation.info.name)
            twidget.setData(0, AssignmentTreeDataRole.ComputationKey, prop_key)
            twidget.setData(0, AssignmentTreeDataRole.ComputationObject, computation)
            twidget.setData(0, AssignmentTreeDataRole.LabelNode, node)
            twidget.setData(0, AssignmentTreeDataRole.IsLeaf, True)
            label_tree_item.addChild(twidget)
            label_tree_item.setExpanded(True)
            label_tree_item.setHidden(label_tree_item.childCount() == 0)

        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply).setEnabled(any(
            [len(prop_assignment.regions) > 0 for prop_assignment in self.property_assignments.values()])
        )

    def _remove_regions_from_property_computation(self, comp: PropertyComputation, regions: typing.Set[Node]):
        for node in regions:
            node_tree_item: QTreeWidgetItem = self.assignment_label_items[node]
            computation_items: typing.List[QTreeWidgetItem] = [node_tree_item.child(i) for i in range(node_tree_item.childCount())]

            computation_item: QTreeWidgetItem = [item for item in computation_items if item.data(0, AssignmentTreeDataRole.ComputationObject) == comp][0]

            node_tree_item.removeChild(computation_item)

            if len(self.property_assignments[comp].regions) == 0:
                if comp in self.param_widgets_for_props:
                    widget = self.param_widgets_for_props[comp]
                    widget.hide()
                    self.settings_layout.removeWidget(widget)
                    # TODO if uncommented RuntimeError: Internal C++ object (PySide6.QtWidgets.QWidget) already deleted. is raised
                    # widget.layout().removeWidget(comp.setting_widget)
                    # widget.deleteLater()
                    del self.param_widgets_for_props[comp]
                    # TODO UserParamBinding is not used anymore
                    # del self.param_bindings_for_props[computation]
            node_tree_item.setHidden(node_tree_item.childCount() == 0)

        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply).setEnabled(any(
            [len(prop_assignment.regions) > 0 for prop_assignment in self.property_assignments.values()])
        )

    def remove_assignment_by_selection(self):
        items: typing.List[QTreeWidgetItem] = self.ui.assignmentTree.selectedItems()
        leaves: typing.List[QTreeWidgetItem] = [item for item in items if item.data(0, AssignmentTreeDataRole.IsLeaf)]

        for leaf in leaves:
            computation: PropertyComputation = leaf.data(0, AssignmentTreeDataRole.ComputationObject)
            node: Node = leaf.data(0, AssignmentTreeDataRole.LabelNode)

            assignment: PropertyAssignment = self.property_assignments[computation]
            assignment.remove_regions({node})

    # def show_dialog(self) -> typing.Dict[str, typing.Set[int]]:
    def show_dialog(self, label_hierarchy: LabelHierarchy) -> typing.List[PropertyAssignment]:
        # self._populate_label_tree()
        self._populate_measurement_comps_tree()
        # self._populate_assignment_tree()
        self._label_tree_model = LabelTreeModel(self.state, LabelTreeMode.Choosing)
        self._label_tree_model.set_hierarchy(label_hierarchy)
        self.ui.labelTree.setModel(self._label_tree_model)
        self.ui.labelTree.expandAll()
        self.ui.labelTree.selectionModel().selectionChanged.connect(self.label_selection_changed)
        # if self.exec_() == QDialog.Accepted:
        #     pass
        #     #self.compute_measurements.emit(self.assignments)
        #     #computations = {}
        #     #for prop_path, labels in self.assignments.items():
        #     #    dot_splits = prop_path.split('.')
        #     #    prop_name = dot_splits.pop()
        #     #    comp_key = '.'.join(dot_splits)
        #     #    prop_labels = computations.setdefault(comp_key, {})
        #     #    prop_labels[prop_name] = labels
        #     #for computation_key, prop_labels in computations.items():
        #     #    print(f'{computation_key} will compute {prop_labels}')
        #     #for i in range(self.state.storage.image_count):
        #     #    photo = self.state.storage.get_photo_by_idx(i)
        #     #    for computation_key, prop_labels in computations.items():
        #     #        computation: PropertyComputation = self.comps_model.computations_dict[computation_key]
        #     #        reg_props = computation(photo, prop_labels)
        #     #        for prop in reg_props:
        #     #            prop.info.key = f'{computation_key}.{prop.info.key}'
        #     #            photo['Labels'].set_region_prop(prop.label, prop)
        # else:
        dialog_code = self.exec_()
        prop_assignments = [prop_assignment for prop_assignment in self.property_assignments.values() if len(prop_assignment.regions) > 0]
        self.assignment_label_items.clear()
        # self.assignments.clear()
        for comp, widget in self.param_widgets_for_props.items():
            widget.hide()
            self.settings_layout.removeWidget(widget)
        self.param_widgets_for_props.clear()
        if dialog_code == QDialog.Rejected:
            prop_assignments.clear()
        self.ui.assignmentTree.clear()
        self.property_assignments.clear()
        # for comp, sett_widget in self.param_widgets_for_props.items():
        #     self.ui.settingsScrollArea.layout().removeWidget(sett_widget)
        # self.param_widgets_for_props.clear()
        self.ui.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)
        return prop_assignments

    def create_new_assignments_from_selection(self):
        selected_label_idxs: typing.List[QModelIndex] = self.ui.labelTree.selectedIndexes()
        selected_property_idxs: typing.List[QModelIndex] = self.ui.measurementTree.selectedIndexes()

        nodes: typing.Set[Node] = {idx.internalPointer() for idx in selected_label_idxs if idx.isValid()}
        for prop_idx in selected_property_idxs:
            computation: PropertyComputation = prop_idx.data(MeasurementTreeDataRoles.ComputationObject)
            property_assignment: PropertyAssignment = self.property_assignments[computation]
            property_assignment.add_regions(nodes)

    def assign_measurements(self):
        # to each label in `label_selection` assigns all props in `prop_selection` and stores the assignments
        # in `self.assignments` and also in the QTreeView self.ui.measurementTree

        label_selection: typing.List[QModelIndex] = self.ui.labelTree.selectedIndexes()
        prop_selection: typing.List[QModelIndex] = self.ui.measurementTree.selectedIndexes()

        for label_index in label_selection:
            if not label_index.isValid():
                continue
            label_node: Node = label_index.internalPointer()
            if label_node not in self.assignment_label_items:
                label_item = QTreeWidgetItem()
                label_item.setText(0, label_node.name)
                pixmap = QPixmap(32, 32)
                pixmap.fill(QColor(*label_node.color))
                label_item.setIcon(0, QIcon(pixmap))
                label_item.setData(0, AssignmentTreeDataRole.LabelNode, label_node)
                label_item.setData(0, AssignmentTreeDataRole.IsLeaf, False)
                self.ui.assignmentTree.addTopLevelItem(label_item)
                self.assignment_label_items[label_node] = label_item
            label_tree_item: QTreeWidgetItem = self.assignment_label_items[label_node]
            for prop_idx in prop_selection:
                prop_key = prop_idx.data(MeasurementTreeDataRoles.ComputationKey)
                computation: PropertyComputation = prop_idx.data(MeasurementTreeDataRoles.ComputationObject)
                if computation.setting_widget is not None and computation not in self.param_widgets_for_props:
                    grp_box = QGroupBox(computation.info.name)
                    grp_box.setLayout(QVBoxLayout())
                    grp_box.layout().addWidget(computation.setting_widget)
                    self.param_widgets_for_props[computation] = grp_box
                    self.settings_layout.addWidget(grp_box)
                # elif computation not in self.param_widgets_for_props and len(computation.user_params) > 0:
                #     widget = create_params_widget(computation.user_params, self.state)
                #     binding = UserParamWidgetBinding(self.state)
                #     binding.bind(computation.user_params, widget)
                #     group = QGroupBox()
                #     group.setTitle(computation.info.name)
                #     layout = QVBoxLayout()
                #     layout.addWidget(widget)
                #     group.setLayout(layout)
                #     self.param_widgets_for_props[computation] = group
                #     self.param_bindings_for_props[computation] = binding
                #     self.settings_layout.addWidget(group)
                if label_node not in self.property_assignments[computation]:
                    self.property_assignments[computation].regions.add(label_node)
                    twidget = QTreeWidgetItem()
                    twidget.setText(0, computation.info.name)
                    twidget.setData(0, AssignmentTreeDataRole.ComputationKey, prop_key)
                    twidget.setData(0, AssignmentTreeDataRole.ComputationObject, computation)
                    twidget.setData(0, AssignmentTreeDataRole.LabelNode, label_node)
                    twidget.setData(0, AssignmentTreeDataRole.IsLeaf, True)
                    label_tree_item.addChild(twidget)
            label_tree_item.setExpanded(True)
            label_tree_item.setHidden(label_tree_item.childCount() == 0)

        self.ui.buttonBox.button(QDialogButtonBox.Apply).setEnabled(any(
            [len(prop_assignment.regions) > 0 for prop_assignment in self.property_assignments.values()])
        )

    def label_selection_changed(self, sel, des):
        self.enable_assign_button()

    def measurement_selection_changed(self):
        self.enable_assign_button()

    def assignment_selection_changed(self):
        self.ui.btnAssignmentRemove.setEnabled(len(self.ui.assignmentTree.selectedIndexes()) > 0)

    def enable_assign_button(self):
        self.ui.btnAssign.setEnabled(len(self.ui.labelTree.selectedIndexes()) > 0 and
                                     len(self.ui.measurementTree.selectedIndexes()) > 0)

    def remove_assignments(self):
        items: typing.List[QTreeWidgetItem] = self.ui.assignmentTree.selectedItems()

        leaves: typing.List[QTreeWidgetItem] = [item for item in items if item.data(0, AssignmentTreeDataRole.IsLeaf)]

        for leaf in leaves:
            key = leaf.data(0, AssignmentTreeDataRole.ComputationKey)
            computation = leaf.data(0, AssignmentTreeDataRole.ComputationObject)
            leaf.parent().removeChild(leaf)
            label_node: Node = leaf.data(0, AssignmentTreeDataRole.LabelNode)
            self.property_assignments[computation].regions.remove(label_node)
            if len(self.property_assignments[computation].regions) == 0:
                if computation in self.param_widgets_for_props:
                    widget = self.param_widgets_for_props[computation]
                    widget.hide()
                    self.settings_layout.removeWidget(widget)
                    # TODO if uncommented RuntimeError: Internal C++ object (PySide6.QtWidgets.QWidget) already deleted. is raised
                    # widget.deleteLater()
                    del self.param_widgets_for_props[computation]
                    # TODO UserParamBinding is not used anymore
                    # del self.param_bindings_for_props[computation]
            self.ui.assignmentTree.removeItemWidget(leaf, 0)

        for node in self.assignment_label_items.values():
            if node.childCount() == 0:
                node.setHidden(True)
        for node in self.assignment_items:
            node.setHidden(all([node.child(i).isHidden() for i in range(node.childCount())]))

        self.ui.buttonBox.button(QDialogButtonBox.Apply).setEnabled(any(
            [len(prop_assignment.regions) > 0 for prop_assignment in self.property_assignments.values()])
        )
        # self.ui.assignmentTree.update()

    def deselect_ancestors_of_leaves(self, selected: QItemSelection, deselected: QItemSelection):
        for index in deselected.indexes():
            # if index.child(0, 0).isValid():
            if index.model().index(0, 0, index).isValid():
                continue
            parent = index.parent()
            while parent.isValid():
                self.ui.assignmentTree.selectionModel().select(parent, QItemSelectionModel.Deselect)
                parent = parent.parent()

    def _setup_demo_color_tolerance_dialog(self):
        self._color_tolerance_dialog = ColorToleranceDialog(self.state)
        self._color_tolerance_dialog.hide()

    def demo_select_color_and_tolerance(self):
        self._color_tolerance_dialog.get_color_and_tolerances()


def tree_item_double_click_handler(tree_widget: QTreeWidget):
    def select_subtree(index: QModelIndex):
        print(id(tree_widget))
        # if not index.child(0, 0).isValid():
        if not index.model().index(0, 0, index).isValid():
            return
        stack = [index]
        while len(stack) > 0:
            idx = stack.pop()
            if idx.isValid():
                # curr_idx = idx.child(0, 0)
                curr_idx = idx.model().index(0, 0, idx)
                child_idx = 0
                indexes_to_select = []
                while curr_idx.isValid():
                    indexes_to_select.append(curr_idx)
                    stack.append(curr_idx)
                    child_idx += 1
                    # curr_idx = idx.child(child_idx, 0)
                    curr_idx = idx.model().index(child_idx, 0, idx)
                if len(indexes_to_select) > 0:
                    tree_widget.selectionModel().select(QItemSelection(indexes_to_select[0], indexes_to_select[-1]),
                                                        QItemSelectionModel.Select)
    return select_subtree


def visit_subtree(root: QTreeWidgetItem):
    stack = [root]
    while len(stack) > 0:
        item = stack.pop()
        for i in range(len(item.childCount())):
            stack.append(item.child(i))
        yield item
    yield None
