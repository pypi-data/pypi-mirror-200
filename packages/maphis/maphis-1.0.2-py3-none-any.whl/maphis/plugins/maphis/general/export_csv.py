import csv
import typing
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QApplication

from maphis.common.utils import attempt_to_save_with_retries
from maphis.common.common import Info
from maphis.common.plugin import GeneralAction, ActionContext
from maphis.common.state import State
from maphis.plugins.maphis.general.common import _filter_by_NDArray, get_prop_tuple_list, \
    _group_measurements_by_sheet, _tabular_export_routine, _ndarray_export_routine, show_export_success_message


class ExportCSV(GeneralAction):
    """
    GROUP: export
    NAME: Export to CSV
    KEY: export_csv
    DESCRIPTION: Export measurements to CSV.
    """
    def __init__(self, info: Optional[Info] = None):
        super().__init__(info)

    def __call__(self, state: State, context: ActionContext) -> None:
        prop_tuple_list = get_prop_tuple_list(context)
        nd_props, other_props = _filter_by_NDArray(prop_tuple_list, context)

        file_grouped_props = _group_measurements_by_sheet(other_props, context)

        file_names: typing.List[str] = []

        for group_name, prop_list in file_grouped_props.items():
            path, _ = attempt_to_save_with_retries(write_results, 'Save as...', 'single_file', ['csv'],
                                         QApplication.activeWindow(),
                                         path=context.storage.location / f'{context.current_label_name}_results_{group_name}.csv',
                                         object=None, routine=_tabular_export_routine, prop_list=prop_list,
                                         context=context)
            # with open(context.storage.location / f'{context.current_label_name}_results_{group_name}.csv', 'w', newline='') as f:
            #     writer = csv.writer(f, dialect='excel')
            #     _tabular_export_routine(prop_list, writer.writerow, context)
            if path is not None:
                file_names.append(path.name)

        sheet_nd_props = _group_measurements_by_sheet(nd_props, context)

        for group_name, prop_list in sheet_nd_props.items():
            path, _ = attempt_to_save_with_retries(write_results, 'Save as...', 'single_file', ['csv'],
                                                   QApplication.activeWindow(),
                                                   path=context.storage.location / f'{context.current_label_name}_results_{group_name}.csv',
                                                   object=None, routine=_ndarray_export_routine, prop_list=prop_list,
                                                   context=context)
            # with open(context.storage.location / f'{context.current_label_name}_results_{group_name}.csv', 'w', newline='') as f:
            #     writer = csv.writer(f, dialect='excel')
            #     _ndarray_export_routine(prop_list, writer.writerow, context)
            if path is not None:
                file_names.append(path.name)

        # filenames = '\n'.join(file_names)
        # filenames = filenames[:-2]
        if len(file_names) > 0:
            show_export_success_message(context.storage.location, file_names, context)


def write_results(path: Path, object: typing.Any, routine, prop_list, context: ActionContext) -> Path:
    with open(path, 'w',
              newline='') as f:
        writer = csv.writer(f, dialect='excel')
        routine(prop_list, writer.writerow, context)

    return path