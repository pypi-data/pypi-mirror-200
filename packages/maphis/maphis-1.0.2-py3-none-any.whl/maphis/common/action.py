import abc
import copy
import typing

from PySide6.QtWidgets import QWidget

from maphis.common.common import Info
from maphis.common.label_image import LabelImg, RegionProperty
from maphis.common.photo import Photo
from maphis.common.regions_cache import RegionsCache
from maphis.common.state import State
from maphis.common.units import Unit, BaseUnit, SIPrefix, Value, UnitStore
from maphis.common.user_params import UserParam
from maphis.common.utils import get_dict_from_doc_str
from maphis.common.user_param import Param, IntParam


class Action:
    FOLDER = ''
    TEMPLATE = ''

    def __init__(self, info: typing.Optional[Info] = None):
        doc_dict = get_dict_from_doc_str(self.__doc__)
        self.info = Info.load_from_dict(doc_dict) if info is None else info
        self._user_params: typing.Dict[str, Param] = {}
        self._group = doc_dict['GROUP'] if 'GROUP' in doc_dict else 'General'

    @property
    def user_params(self) -> typing.List[Param]:
        return list(self._user_params.values())

    @property
    def user_params_dict(self) -> typing.Dict[str, Param]:
        return self._user_params

    @property
    def can_be_executed(self) -> typing.Tuple[bool, str]:
        return True, ''

    @property
    def group(self) -> str:
        return self._group

    def __hash__(self) -> int:
        return hash(self.info.key)

    def __eq__(self, other):
        return hash(self) == hash(other)

    @property
    def setting_widget(self) -> typing.Optional[QWidget]:
        return None

    def _setup_params(self):
        pass

    def current_settings_to_str_dict(self) -> typing.Dict[str, typing.Dict[str, str]]:
        return {
            'standard_parameters': {param_key: str(param.value) for param_key, param in self._user_params.items()},
            'custom_parameters': {}
        }

    def setup_settings_from_dict(self, _dict: typing.Dict[str, typing.Dict[str, str]]):
        standard_params: typing.Dict[str, str] = _dict['standard_parameters']
        for param_key, param_value_str in standard_params.items():
            param_obj: Param = self.user_params_dict[param_key]
            param_obj.parse(param_value_str)

    def initialize(self) -> typing.Tuple[bool, str]:
        return True, ''


class RegionComputation(Action):
    FOLDER = 'regions'
    TEMPLATE = 'region_computation_template.py'

    def __init__(self, info: typing.Optional[Info] = None):
        super(RegionComputation, self).__init__(info)
        self._region_restricted = "REGION_RESTRICTED" in self.__doc__

    @abc.abstractmethod
    def __call__(self, photo: Photo, labels: typing.Optional[typing.Set[int]] = None, storage=None) -> typing.List[LabelImg]:
        pass

    @property
    def region_restricted(self) -> bool:
        return self._region_restricted


class PropertyComputation(Action):
    FOLDER = 'properties'
    TEMPLATE = 'property_computation_template.py'

    def __init__(self, info: typing.Optional[Info] = None):
        super(PropertyComputation, self).__init__(info)
        doc_dict = get_dict_from_doc_str(self.__doc__)
        self._region_restricted = self.__doc__ is not None and "REGION_RESTRICTED" in self.__doc__
        self._units: UnitStore = UnitStore()
        self._px_unit: Unit = Unit(BaseUnit.px, prefix=SIPrefix.none, dim=1)
        self._no_unit: Unit = Unit(BaseUnit.none, prefix=SIPrefix.none, dim=0)

    @abc.abstractmethod
    def __call__(self, photo: Photo, region_labels: typing.List[int], regions_cache: RegionsCache, props: typing.List[str]) -> typing.List[RegionProperty]:
        pass

    @property
    def region_restricted(self) -> bool:
        return self._region_restricted

    @property
    @abc.abstractmethod
    def computes(self) -> typing.Dict[str, Info]:
        pass

    @abc.abstractmethod
    def example(self, prop_name: str) -> RegionProperty:
        prop = RegionProperty()
        prop.prop_comp_key = self.info.key
        prop.local_key = prop_name
        prop.info = copy.deepcopy(self.info)
        prop.settings = self.current_settings_to_str_dict()
        # prop.value = Value(0, Unit(BaseUnit.px, SIPrefix.none, dim=1))
        prop.value = Value(0, self._units.units['mm'])
        return prop

    def target_worksheet(self, prop_name: str) -> str:
        return 'common'

    @property
    @abc.abstractmethod
    def requested_props(self) -> typing.List[str]:
        return []


class GeneralAction(Action):
    FOLDER = 'general'
    TEMPLATE = 'general_action_template.py'

    def __init__(self, info: typing.Optional[Info] = None):
        super(GeneralAction, self).__init__(info)

    @abc.abstractmethod
    def __call__(self, state: State, context: 'ActionContext') -> None:
        pass
