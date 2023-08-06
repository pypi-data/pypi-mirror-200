from __future__ import annotations

import uuid

from dataclasses import dataclass, field
from typing import Literal, Optional, Tuple, Union

from ..widget import Widget, AttributeNames, StateControl
from .panel import PanelWidget, Panel


@dataclass
class TabsLayout(Panel):
    tabs: Optional[Tuple[str, StateControl]] = field(default_factory=lambda: [])
    position: Optional[Literal["top", "bottom" "left", "right"]] = "bottom"

    def add_tab(self, tab_title: str, component: StateControl) -> TabsLayout:
        if self.tabs is None:
            element = tab_title, component
            self.tabs = [element]
        else:
            my_list = list(self.tabs)
            element = tab_title, component
            my_list.append(element)
            self.tabs = tuple(my_list)

        return self

    def remove_tab(self, index: Union[str, int]) -> TabsLayout:
        my_list = list(self.tabs)

        try:
            if isinstance(index, str):
                index = self.get_index(index)
                my_list.pop(index)
            elif isinstance(index, int):
                my_list.pop(index)
            else:
                raise ValueError(f"Error {TabsLayout.__name__}: wrong format for param index")
        except:
            raise ValueError(f"Error {TabsLayout.__name__}: wrong value for param index")

        self.tabs = tuple(my_list)
        return self

    def get_index(self, name: str) -> int:
        my_list = list(self.tabs)

        try:
            enum_list = [(i, x) for i, x in enumerate(my_list, 0)]
            i_list = [t[0] for t in enum_list if (t[1][0] == name)]
            return i_list[0]
        except:
            raise ValueError(f"Error {TabsLayout.__name__}: wrong value for string index")

    def to_dict_widget(self, panel_dict: dict = None):
        if panel_dict is None:
            panel_dict = {
                AttributeNames.ID.value: self.panel_id if self.panel_title else str(uuid.uuid1()),
                AttributeNames.TYPE.value: TabsLayout.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }

        if self.panel_title is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                "panel_title": self.panel_title
            })

        if self.tabs is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TABS.value: [{"title": tab[0], "component": tab[1].to_dict_widget()} for tab in self.tabs]
            })

        if self.position is not None:
            panel_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.POSITION.value: self.position
            })

        return panel_dict


class TabsLayoutWidget(PanelWidget, TabsLayout):
    """
    Creates a layout that provides a horizontal layout to display tabs.
    """

    def __init__(self,
                 panel_title: Optional[str] = None,
                 panel_id: Optional[str] = None,
                 tabs: Optional[Tuple[str, StateControl]] = [],
                 position: Optional[Literal["top", "bottom" "left", "right"]] = "bottom",
                 **additional):
        self._parent_class = TabsLayout.__name__
        PanelWidget.__init__(self, panel_title=panel_title, panel_id=panel_id, 
                             compatibility =  tuple([TabsLayout.__name__,]),
                             **additional)
        TabsLayout.__init__(self, tabs=tabs, position=position)
        self.placements = dict()

    # def place(self, widget: Widget, tab_title: str = None):
    #     super()._place(widget)

    def to_dict_widget(self):
        panel_dict = Widget.to_dict_widget(self)
        panel_dict = TabsLayout.to_dict_widget(self, panel_dict)
        return panel_dict
