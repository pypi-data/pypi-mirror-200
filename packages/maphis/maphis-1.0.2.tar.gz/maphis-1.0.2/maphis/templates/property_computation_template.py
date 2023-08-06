import abc
import typing

from maphis.common.action import PropertyComputation
from maphis.common.common import Info
from maphis.common.label_image import RegionProperty
from maphis.common.photo import Photo
from maphis.common.regions_cache import RegionsCache
from maphis.common.user_params import UserParam


class CLASS_NAME(PropertyComputation):
    """
    NAME: <NAME>
    DESCRIPTION: <DESCRIPTION>
    KEY: <KEY>
    """
    def __init__(self, info: typing.Optional[Info] = None):
        super(CLASS_NAME, self).__init__(info)

    def __call__(self, photo: Photo, region_labels: typing.List[int], regions_cache: RegionsCache) -> typing.List[RegionProperty]:
        super(CLASS_NAME, self).__call__(photo, region_labels, regions_cache)

    @property
    def user_params(self) -> typing.List[UserParam]:
        return super().user_params

    @property
    def region_restricted(self) -> bool:
        return super().region_restricted

    @property
    def computes(self) -> typing.Dict[str, Info]:
        return super().computes

    def example(self, prop_name: str) -> RegionProperty:
        pass

    def target_worksheet(self, prop_name: str) -> str:
        return super().target_worksheet(prop_name)

