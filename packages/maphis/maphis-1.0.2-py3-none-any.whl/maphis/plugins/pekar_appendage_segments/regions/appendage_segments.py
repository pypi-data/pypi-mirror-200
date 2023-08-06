import arthseg

from maphis.common.photo import Photo, LabelImg
from maphis.common.plugin import RegionComputation
from typing import Set, Optional


class AppendageSegments(RegionComputation):
    """
    NAME: Appendages segmentation
    DESCRIPTION: Labels appendages into smaller parts based on geodetic distance from body.
    """

    def __init__(self) -> None:
        RegionComputation.__init__(self, None)

    def __call__(
        self, photo: Photo, labels: Optional[Set[int]] = None
    ) -> Set[LabelImg]:
        copy = photo['Labels'].clone()
        label_hierarchy = copy.label_hierarchy

        leg_labels = {
            label_hierarchy.label('1:2:1:0'): [
                label_hierarchy.label('1:2:1:1'),
                label_hierarchy.label('1:2:1:2'),
                label_hierarchy.label('1:2:1:3'),
            ],
            label_hierarchy.label('1:2:2:0'): [
                label_hierarchy.label('1:2:2:1'),
                label_hierarchy.label('1:2:2:2'),
                label_hierarchy.label('1:2:2:3'),
            ],
            label_hierarchy.label('1:2:3:0'): [
                label_hierarchy.label('1:2:3:1'),
                label_hierarchy.label('1:2:3:2'),
                label_hierarchy.label('1:2:3:3'),
            ],
            label_hierarchy.label('1:2:4:0'): [
                label_hierarchy.label('1:2:4:1'),
                label_hierarchy.label('1:2:4:2'),
                label_hierarchy.label('1:2:4:3'),
            ],
            label_hierarchy.label('1:2:5:0'): [
                label_hierarchy.label('1:2:5:1'),
                label_hierarchy.label('1:2:5:2'),
                label_hierarchy.label('1:2:5:3'),
            ],
            label_hierarchy.label('1:2:6:0'): [
                label_hierarchy.label('1:2:6:1'),
                label_hierarchy.label('1:2:6:2'),
                label_hierarchy.label('1:2:6:3'),
            ],
            label_hierarchy.label('1:2:7:0'): [
                label_hierarchy.label('1:2:7:1'),
                label_hierarchy.label('1:2:7:2'),
                label_hierarchy.label('1:2:7:3'),
            ],
            label_hierarchy.label('1:2:8:0'): [
                label_hierarchy.label('1:2:8:1'),
                label_hierarchy.label('1:2:8:2'),
                label_hierarchy.label('1:2:8:3'),
            ],
        }

        body_labels = {
            label_hierarchy.label('1:1:1:0'),
            label_hierarchy.label('1:1:2:0'),
        }
        back_label = label_hierarchy.label('1:1:3:0')

        copy.label_image = arthseg.leg_segments(
            copy.label_image,
            labels=leg_labels,
            body_labels=body_labels,
            alternative_labels={back_label},
        )

        return [copy]
