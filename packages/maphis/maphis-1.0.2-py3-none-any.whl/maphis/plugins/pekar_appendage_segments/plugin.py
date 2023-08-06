from typing import Optional

from maphis.common.common import Info
from maphis.common.plugin import Plugin


class AppendageSegmentsPlugin(Plugin):
    """
    NAME: AppendageSegments Pekar
    DESCRIPTION: Labels appendages into smaller parts based on geodetic distance from body.
    """

    def __init__(self, info: Optional[Info] = None) -> None:
        super().__init__(info)
