import functools
import functools
import time
import typing
from typing import List

import PySide6
import numpy as np
from PySide6.QtCore import Qt, QCoreApplication, Signal, QModelIndex
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QTableView, QProgressDialog, QMenu, QTextEdit, QVBoxLayout, \
    QTabWidget, QTableWidget, QSizePolicy, QAbstractScrollArea, QLabel

from maphis.common.blocking_operation import ProgressReport
from maphis.common.label_hierarchy import Node
from maphis.common.label_image import RegionProperty, PropertyType, LabelImg
from maphis.common.photo import Photo, UpdateEvent, UpdateContext, LabelImageUpdateType
from maphis.common.plugin import PropertyComputation, ActionContext, GeneralAction
from maphis.common.regions_cache import RegionsCache
from maphis.common.state import State
from maphis.common.storage import Storage
from maphis.label_editor.computation_widget import ComputationWidget
from maphis.measurements_viewer.measurement_assign_dialog import MeasurementAssignDialog, \
    PropertyAssignment
from maphis.measurements_viewer.measurements_model import MeasurementsTableModel, MeasurementsTableRole
from maphis.measurements_viewer.ui_measurements_viewer import Ui_MeasurementsViewer


class MeasurementsViewer(QWidget):
    open_project_folder = Signal()
    unsaved_changes = Signal()

    def __init__(self, state: State, action_context: ActionContext, parent: typing.Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowFlags=Qt.WindowFlags()):
        super().__init__(parent, f)
        self.all_props: typing.List[typing.Tuple[str, str]] = []
        self.ui = Ui_MeasurementsViewer()
        self.ui.setupUi(self)

        self.state = state
        # self.state.storage_changed.connect(self.set_new_storage)

        self.action_context: ActionContext = action_context

        self.ui.cmbLabelImages.currentTextChanged.connect(self.show_measurements_for)

        self.ui.btnComputeMeasurements.clicked.connect(self.show_new_measurements_dialog)
        # self.ui.btnExport.clicked.connect(self.export_xlsx_results)
        self.ui.btnExport.clicked.connect(self.export_default)
        self.ui.btnRecompute.setVisible(False)
        self.ui.btnRecompute.clicked.connect(self.recompute)
        self.ui.btnDelete.clicked.connect(self.delete_measurements)

        # TODO in future, a flexible export system would be nice
        self._export_menu = QMenu()
        self._export_menu.triggered.connect(self._handle_export_action_triggered)

        for gen_action in self.action_context.general_actions.values():
            if gen_action.group != 'export':
                continue
            action = self._export_menu.addAction(gen_action.info.name)
            action.setData(gen_action)
            # self._export_menu.addAction(action)
        self._default_export_action: typing.Optional[QAction] = None
        if len(self._export_menu.actions()) > 0:
            self._default_export_action = self._export_menu.actions()[0]
        self.ui.btnExport.setText('Export measurements')
        self.ui.btnExport.setEnabled(len(self._export_menu.actions()) > 0)

        self.ui.btnExport.setMenu(self._export_menu)

        self.computation_widget = ComputationWidget(self.state, None)
        self.computation_widget.set_settings_group_shown(False)
        self.computation_widget.set_restrict_group_shown(False)
        self.computation_widget.setVisible(False)
        self.measurement_assign_dialog = MeasurementAssignDialog(self.state,
                                                                 self.computation_widget.computations_model,
                                                                 parent=self)
        self.measurement_assign_dialog.setWindowModality(Qt.ApplicationModal)
        self.measurement_assign_dialog.ui.mainLayout.addWidget(self.computation_widget)
        self.setEnabled(False)

        self.prop_table_models: typing.Dict[str, MeasurementsTableModel] = {}

        #self.ui.results_widget.setLayout(QHBoxLayout())
        self.tables: typing.List[QTableView] = []

        self.model = MeasurementsTableModel(self.state)
        self.ui.chkColorVisually.toggled.connect(self.model.display_intensity_in_color)
        self.ui.tableView.doubleClicked.connect(self._handle_index_double_clicked)
        self.nd_browser = None

        self.current_label_name: str = ''
        self.ui.cmbLabelImages.setVisible(False)
        self.ui.lblShowMeasurementsFor.setVisible(False)

    def export_default(self):
        self._handle_export_action_triggered(self._default_export_action)

    def _handle_export_action_triggered(self, action: QAction):
        self._default_export_action = action
        if action.data() is None:
            return
        gen_action: GeneralAction = action.data()
        self.action_context.current_label_name = self.current_label_name
        self.action_context.units = self.state.units
        gen_action(self.state, self.action_context)

    def set_new_storage(self, new_strg: typing.Optional[Storage], old_strg: typing.Optional[Storage]):
        self.ui.cmbLabelImages.blockSignals(True)
        if old_strg is not None:
            old_strg.update_photo.disconnect(self._handle_photo_update)
            self.ui.cmbLabelImages.clear()
        if new_strg is not None:
            new_strg.update_photo.connect(self._handle_photo_update)
            label_images = set(new_strg.label_image_names)
            label_images.remove(new_strg.default_label_image)
            label_images = list(sorted(label_images))
            label_images.insert(0, new_strg.default_label_image)
            self.ui.cmbLabelImages.blockSignals(False)
            for label_img_name in label_images:
                self.ui.cmbLabelImages.addItem(label_img_name)
            self.current_label_name = new_strg.default_label_image
            self.measurement_assign_dialog._label_tree_model.show_hierarchy_for(new_strg.default_label_image)
        self.ui.cmbLabelImages.setEnabled(self.ui.cmbLabelImages.count() > 0)
        self.ui.cmbLabelImages.setCurrentIndex(0)

    def _handle_photo_update(self, update: UpdateEvent):
        if update.update_context != UpdateContext.LabelImg:
            return
        index = self.state.image_list_model.image_paths.index(update.photo.image_path)
        if update.update_obj.update_type in {LabelImageUpdateType.PropertiesValid, LabelImageUpdateType.PropertiesInvalid}:
            self.model.headerDataChanged.emit(Qt.Orientation.Vertical, index, index)
        elif update.update_obj.update_type in {LabelImageUpdateType.PropertyUpdate, LabelImageUpdateType.PropertyRemoved, LabelImageUpdateType.PropertyAdded}:
            model_index_first = self.state.image_list_model.index(index, 0)
            model_index_last = self.state.image_list_model.index(index, self.model.columnCount() - 1)
            self.model.dataChanged.emit(model_index_first, model_index_last)

    def register_computation(self, comp: PropertyComputation):
        pass

    def show_measurements_for(self, label_image_name: str):
        self.current_label_name = label_image_name
        self.measurement_assign_dialog.current_label_name = self.current_label_name
        self.measurement_assign_dialog._label_tree_model.show_hierarchy_for(label_image_name)
        self.model.beginResetModel()
        self.model.current_label_name = self.current_label_name
        self.model.update_model()
        self.model.endResetModel()

    def compute_measurements_(self, assignments: typing.Dict[Photo, typing.List[PropertyAssignment]]):
        progress_dialog = ProgressReport(len(assignments), 'Computing properties', self)
        for photo, prop_assignments in assignments.items():
            all_labels: typing.Set[Node] = set(functools.reduce(set().union,
                                                                [assignment.regions for assignment in prop_assignments]))
            all_labels: typing.Set[int] = {region.label for region in all_labels}
            regions_cache = RegionsCache(all_labels, photo, self.current_label_name)
            for prop_assignment in prop_assignments:
                region_props: List[RegionProperty] = []
                computation = prop_assignment.computation
                computation.setup_settings_from_dict(prop_assignment.computation_settings)
                labels = [region.label for region in prop_assignment.regions]
                props_ = computation(photo, labels, regions_cache, list(prop_assignment.props))
                region_props.extend(props_)
                for prop in region_props:
                    # photo[self.state.storage.default_label_image].set_region_prop(prop.label, prop)
                    photo[self.current_label_name].set_region_prop(prop.label, prop)
            progress_dialog.increment()
        self.update_measurements_view()
        self.unsaved_changes.emit()
        self.enable_delete_recompute()

    def show_new_measurements_dialog(self):
        # print(self.state.storage.used_regions('Labels'))
        # to_compute: typing.Dict[str, typing.Set[int]] = self.measurement_assign_dialog.show_dialog()
        to_compute: typing.List[PropertyAssignment] = self.measurement_assign_dialog.show_dialog(self.state.storage.get_label_hierarchy(self.current_label_name))
        #FIXME this if is to identify when the dialog was closed by clicking on 'Cancel' but it actually does not work
        if len(to_compute) == 0:
            return

        for to_comp in to_compute:
            to_comp.props = set(to_comp.computation.requested_props)

        photo_assignments: typing.Dict[Photo, typing.List[PropertyAssignment]] = {photo: to_compute for photo in self.state.storage.images}
        self.compute_measurements_(photo_assignments)
        return

    def update_measurements_view(self):
        self.model.update_model()
        self.ui.tableView.setModel(None)
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.selectionModel().selectionChanged.connect(self.enable_delete_recompute)
        self.ui.btnExport.setEnabled(True)
        self.ui.tableView.resizeColumnsToContents()
        # self.ui.tableView.setSortingEnabled(True)
        # self.ui.tableView.sortByColumn(0, Qt.SortOrder.AscendingOrder)

    def enable_delete_recompute(self):
        enable = len(self.ui.tableView.selectedIndexes()) > 0
        self.ui.btnDelete.setEnabled(enable)
        self.ui.btnRecompute.setEnabled(enable)

    def recompute(self):
        idxs = self.ui.tableView.selectedIndexes()
        row_wise: typing.List[QModelIndex] = list(sorted(idxs, key=lambda idx: idx.row()))
        # assignments: typing.List[typing.Tuple[int, typing.Dict[str, typing.Set[int]]]] = []
        # assignments: typing.Dict[Photo, typing.Dict[Proper]]
        assignments: typing.Dict[Photo, typing.Dict[PropertyComputation, PropertyAssignment]] = {}
        # assignment: typing.Dict[str, typing.Set[int]] = {}
        photo_idx = row_wise[0].row()
        for idx in row_wise:
            photo: Photo = idx.data(MeasurementsTableRole.Photo)
            # if idx.row() != photo_idx:
            #     assignments.append((photo_idx, assignment))
            #     photo_idx = idx.row()
            #     assignment = {}
            photo_assignment: typing.Dict[PropertyComputation, PropertyAssignment] = assignments.setdefault(photo, {})
            label = self.model.data(idx, MeasurementsTableRole.Label)
            region_property: RegionProperty = idx.data(MeasurementsTableRole.RegionProperty)

            prop_comp_key = self.model.data(idx, MeasurementsTableRole.PropertyComputationKey)
            # assignment.setdefault(prop_key, set()).add(label)

            # region_property: RegionProperty = photo['Labels'].region_props[label][prop_comp_key]

            prop_comp = self.computation_widget.computations_model.computations_dict[prop_comp_key]

            prop_comp_assignment: PropertyAssignment = photo_assignment.setdefault(prop_comp, PropertyAssignment(prop_comp))
            prop_comp_assignment.props.add(idx.data(MeasurementsTableRole.LocalKey))
            prop_comp_assignment.regions.add(photo[self.current_label_name].label_hierarchy.nodes[label])
            prop_comp_assignment.computation_settings = region_property.settings
        photo_assignments: typing.Dict[Photo, typing.List[PropertyAssignment]] = {photo: list(prop_assignments.values()) for photo, prop_assignments in assignments.items()}
        # assignments.append((row_wise[-1].row(), assignment))
        self.compute_measurements_(photo_assignments)

    def compute_measurements(self, photo_assignments: typing.List[typing.Tuple[int, typing.Dict[str, typing.Set[int]]]]):
        progr_dialog = QProgressDialog(minimum=0, maximum=len(photo_assignments), parent=self)
        progr_dialog.setWindowModality(Qt.WindowModal)
        progr_dialog.setCancelButton(None)
        progr_dialog.setMinimumDuration(0)
        progr_dialog.setValue(0)
        progr_dialog.setLabelText('Preparing to compute properties...')
        progr_dialog.setWindowTitle('Computing properties')
        time.sleep(0.01)
        progr_dialog.setValue(0)
        QCoreApplication.processEvents()
        for progress_value, (i, to_compute) in enumerate(photo_assignments):
            photo = self.state.storage.get_photo_by_idx(i)
            computations = {}
            # for prop_key, labels in to_compute.items():
            #     dot_splits = prop_key.split('.')
            #     prop_name = dot_splits.pop()
            #     comp_key = '.'.join(dot_splits)
            #     prop_labels = computations.setdefault(prop_key, labels)
            #     # prop_labels[prop_name] = labels
            all_labels = set(functools.reduce(set.union, to_compute.values()))
            regs_cache = RegionsCache(all_labels, photo, self.current_label_name)
            for prop_key, prop_labels in to_compute.items():
                computation: PropertyComputation = self.computation_widget.computations_model.computations_dict[prop_key]
                progr_dialog.setLabelText(f'Computing {computation.info.name} for {photo.image_name}')
                progr_dialog.setValue(progress_value + 1)
                reg_props = computation(photo, list(prop_labels), regs_cache)
                for prop in reg_props:
                    # prop.info.key = f'{computation_key}.{prop.info.key}'
                    prop.info.key = computation.info.key
                    photo[self.current_label_name].set_region_prop(prop.label, prop)
            progr_dialog.setValue(progress_value + 1)
        progr_dialog.hide()
        self.update_measurements_view()
        self.unsaved_changes.emit()

    def _handle_index_double_clicked(self, index: QModelIndex):
        prop: typing.Optional[RegionProperty] = index.data(MeasurementsTableRole.RegionProperty)
        if prop is None:
            return
        # if prop.prop_type != PropertyType.NDArray and prop.prop_type != PropertyType.Vector:
        #     return

        if prop.prop_type == PropertyType.NDArray:
            table_widget, text = self.create_ndarray_table(prop)
        elif prop.prop_type == PropertyType.Vector:
            table_widget, text = self.create_vector_table(prop)
        else:
            return

        if self.nd_browser is not None:
            widgets: typing.List[QWidget] = []
            for i in range(self.nd_browser.count()):
                widgets.append(self.nd_browser.widget(i))
            self.nd_browser.clear()
            for w in widgets:
                w.deleteLater()
            size = self.nd_browser.size()
        else:
            self.nd_browser = QTabWidget()
            size = None

        self.nd_browser.addTab(table_widget, 'Table view')

        photo: Photo = index.data(MeasurementsTableRole.Photo)
        self.nd_browser.setWindowTitle(f'{photo.image_name} {self.state.label_hierarchy.nodes[prop.label].name}:{prop.info.name}')
        # lay = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.zoomIn(3)
        text_edit.setText(text)
        self.nd_browser.addTab(text_edit, 'Raw view')
        self.nd_browser.setWindowModality(Qt.ApplicationModal)
        self.nd_browser.show()
        if size is not None:
            self.nd_browser.resize(size)
        # self.nd_browser.res
        table_widget.adjustSize()

    def create_ndarray_table(self, prop: RegionProperty) -> typing.Tuple[QWidget, str]:

        table_widget = QWidget()
        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tables_layout = QVBoxLayout()
        table_widget.setLayout(tables_layout)

        text = ''

        np.set_printoptions(precision=3)
        for i in range(prop.num_vals):
            nd: np.ndarray = prop.value[0][i]
            if nd.ndim > 2:
                raise ValueError("Not implemented for ndim > 2")
            elif nd.ndim == 1:
                nd = np.array(nd)
            table = QTableWidget()
            table.setRowCount(nd.shape[0])
            table.setColumnCount(nd.shape[1])
            table.setHorizontalHeaderLabels(prop.col_names)
            table.setVerticalHeaderLabels(prop.row_names)

            for r in range(nd.shape[0]):
                for c in range(nd.shape[1]):
                    titem = QTableWidgetItem(f'{nd[r, c]:.3f}')
                    table.setItem(r, c, titem)
            tables_layout.addWidget(QLabel(prop.val_names[i]))
            tables_layout.addWidget(table)
            tables_layout.addSpacing(32)
            table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            # table.adjustSize()

            text += f'\n{prop.val_names[i]}\n'
            text += str(prop.value[0][i])
            text += '\n'

        return table_widget, text

    def create_vector_table(self, prop: RegionProperty) -> typing.Tuple[QWidget, str]:
        widget = QWidget()
        layout = QVBoxLayout()

        widget.setLayout(layout)

        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        table_widget = QTableWidget(1, prop.num_vals)
        layout.addWidget(table_widget)

        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        table_widget.setVerticalHeaderLabels([prop.info.name])
        table_widget.setHorizontalHeaderLabels(prop.val_names)

        for i in range(prop.num_vals):
            table_item = QTableWidgetItem(f'{prop.value[0][i]:.2f}')
            table_widget.setItem(0, i, table_item)

        return widget, ', '.join([str(v) for v in prop.value[0]])

    def delete_measurements(self):
        indexes: typing.List[QModelIndex] = self.ui.tableView.selectedIndexes()
        self.state.storage.update_photo.disconnect(self._handle_photo_update)
        self.model.beginResetModel()
        for idx in indexes:
            photo: Photo = idx.data(MeasurementsTableRole.Photo)
            if photo is None:
                continue
            # TODO remove harcoded 'Labels'
            # label_img: LabelImg = photo['Labels']
            label_img: LabelImg = photo[self.current_label_name]
            prop: typing.Optional[RegionProperty] = idx.data(MeasurementsTableRole.RegionProperty)
            if prop is None:
                continue
            label_img.remove_property(prop.label, prop.prop_key)
        self.model.endResetModel()
        self.update_measurements_view()
        self.state.storage.update_photo.connect(self._handle_photo_update)
