from typing import Optional

from maphis.common.common import Info
from maphis.common.plugin import Plugin


class UNetPlugin(Plugin):
    """
    NAME: UNet Pekar
    DESCRIPTION: Labels semantic parts in an image with UNet.
    """

    def __init__(self, info: Optional[Info] = None) -> None:
        super().__init__(info)
