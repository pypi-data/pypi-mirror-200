import uuid

from dataclasses import dataclass, field
from typing import Optional, Literal

from ..widget import Widget, AttributeNames
from .panel import PanelWidget, Panel


@dataclass
class HorizontalLayout(Panel):
    placements: dict = field(default_factory=lambda: {})
    horizontal_align: Optional[Literal["start", "center", "end"]] = "start"
    vertical_align: Optional[Literal["start", "center", "end"]] = "start"

    def place(self, widget: Widget, width: Optional[float] = None, offset: Optional[int] = None):
        """
        Place widget inside layout
        param widget: widget to place.
        param width: understood as a percentage.
        param offset: distance with the next widget.
        """
        self.widgets.append(widget)
        self.placements[widget.widget_id] = (width, offset)

    def to_dict_widget(self):
        panel_dict = {
            AttributeNames.ID.value: self.panel_id if self.panel_title else str(uuid.uuid1()),
            AttributeNames.TYPE.value: HorizontalLayout.__name__,
            AttributeNames.DRAGGABLE.value: self.draggable,
            AttributeNames.RESIZABLE.value: self.resizable,
            AttributeNames.DISABLED.value: self.disabled,
            AttributeNames.PROPERTIES.value: {}
        }

        if self.panel_title is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                "panel_title": self.panel_title
            })

        if self.horizontal_align is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.HORIZONTAL_ALIGN.value: self.horizontal_align,
            })

        if self.vertical_align is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.VERTICAL_ALIGN.value: self.vertical_align
            })

        if self.placements is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.PLACEMENTS.value: [{
                    AttributeNames.WIDGET_REF.value: key,
                    AttributeNames.WIDTH.value: width,
                    AttributeNames.OFFSET.value: offset
                } for key, (width, offset) in self.placements.items()]
            })

        if self.widgets is not None:
            widgets = [widget.to_dict_widget() for widget in self.widgets]
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.WIDGETS.value: widgets
            })

        return panel_dict


class HorizontalLayoutWidget(PanelWidget):
    """
    Creates a layout where widgets are arranged side by side horizontally.
    """

    def __init__(self,
                 panel_title: Optional[str] = None,
                 panel_id: Optional[str] = None,
                 horizontal_align: Optional[Literal["start", "center", "end"]] = "start",
                 vertical_align: Optional[Literal["start", "center", "end"]] = "start",
                 **additional):
        self._parent_class = HorizontalLayout.__name__
        super().__init__(panel_title=panel_title, panel_id=panel_id,
                         compatibility=tuple([HorizontalLayout.__name__, ]),
                         **additional)
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align
        self.placements = dict()

    def _check_placement_width(self):
        """
        Check that total width of the widgets does not go over 100, since the width is represented as a percentage.
        """
        total = 0
        for key, (width, offset) in self.placements.items():
            total += width
            if total > 100:
                raise Exception("The total width of the widgets cannot be over a 100")

    def place(self, widget: Widget, width: Optional[float] = None, offset: Optional[int] = None):
        """
        Place widget inside layout
        param widget: widget to place.
        param width: understood as a percentage.
        param offset: distance with the next widget.
        """
        super()._place(widget)
        self.placements[widget.widget_id] = (width, offset)
        if width is not None:
            self._check_placement_width()

    def to_dict_widget(self):
        panel_dict = super().to_dict_widget()
        panel_dict[AttributeNames.PROPERTIES.value].update({
            AttributeNames.HORIZONTAL_ALIGN.value: self.horizontal_align,
            AttributeNames.VERTICAL_ALIGN.value: self.vertical_align
        })
        panel_dict[AttributeNames.PROPERTIES.value].update({
            AttributeNames.PLACEMENTS.value: [{
                AttributeNames.WIDGET_REF.value: key,
                AttributeNames.WIDTH.value: width,
                AttributeNames.OFFSET.value: offset
            } for key, (width, offset) in self.placements.items()]
        })
        return panel_dict
