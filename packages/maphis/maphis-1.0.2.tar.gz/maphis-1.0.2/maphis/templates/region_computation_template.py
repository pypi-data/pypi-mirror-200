import abc
import typing

from maphis.common.action import RegionComputation
from maphis.common.common import Info
from maphis.common.label_image import LabelImg
from maphis.common.photo import Photo


class CLASS_NAME(RegionComputation):
    """
    NAME: <NAME>
    DESCRIPTION: <DESCRIPTION>
    KEY: <KEY>
    """
    def __init__(self, info: typing.Optional[Info] = None):
        super(CLASS_NAME, self).__init__(info)

    def __call__(self, photo: Photo, labels: typing.Optional[typing.Set[int]] = None, storage=None) -> typing.List[LabelImg]:
        super(CLASS_NAME, self).__call__(photo, labels, storage)

    @property
    def region_restricted(self) -> bool:
        return super().region_restricted
