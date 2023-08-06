from __future__ import annotations

import uuid

from dataclasses import dataclass
from typing import List, Literal, Optional, Union

from ..widget import AttributeNames, StateControl, Widget


@dataclass
class RadioGroup(StateControl):
    options: Optional[List[Union[int, float, str, any]]] = None
    title: Optional[str] = None
    label_by: Optional[str] = None
    value_by: Optional[str] = None
    value: Optional[List[Union[int, float, str, any]]] = None
    style: Literal["radio", "button"] = None
    allow_multi_selection: Optional[bool] = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())
        # Check value is inside options
        self._check_value()

        if isinstance(self.options, list) and all((isinstance(x, dict)) for x in self.options):
            if self.label_by is None:
                raise Exception("You must indicate the label_by property")
            if self.value_by is None:
                raise Exception("You must indicate the value_by property")

    def replace_widget(self, new_widget: RadioGroup):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.options = new_widget.options
        self.title = new_widget.title
        self.label_by = new_widget.label_by
        self.value_by = new_widget.value_by
        self.value = new_widget.value
        self.allow_multi_selection = new_widget.allow_multi_selection

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.value is not None:
            return self.value
        return None

    def from_string(self, string: str) -> RadioGroup:
        self.value = [string]
        return self

    def to_string(self) -> str:
        return str(self.value[0])

    def from_int(self, number: int) -> RadioGroup:
        self.value = [number]
        self._check_value()
        return self

    def to_int(self) -> int:
        return int(self.value)

    def from_float(self, number: float) -> RadioGroup:
        self.value = [number]
        self._check_value()
        return self

    def to_float(self) -> float:
        return float(self.value[0])

    def from_list(self, input_list: List) -> RadioGroup:
        self.value = input_list
        self.allow_multi_selection = True
        self._check_value()
        return self

    def to_list(self) -> List:
        return list(self.value)

    def _check_value(self):
        if self.value and self.options:
            if isinstance(self.value, list):
                for item in self.value:
                    if item not in self.options:
                        raise Exception(f"Value {self.value} must be in Options: {self.options}.")
            else:
                # Check when value is not a list.
                if self.value not in self.options:
                    raise Exception(f"Value {self.value} must be in Options: {self.options}.")

    def to_dict_widget(self, radio_dict: dict = None):
        if radio_dict is None:
            radio_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: RadioGroup.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        # Widget providers are used when the value of a different widget must be set inside an attribute.
        _widget_providers = []

        if self.options is not None:
            if isinstance(self.options, Widget):
                target = {"id": self.options.widget_id, "target": AttributeNames.OPTIONS.value}
                _widget_providers.append(target)
            else:
                radio_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.OPTIONS.value: self.options,
                })

        if self.title is not None:
            if isinstance(self.title, str):
                radio_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title,
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Error Widget {self.widget_type}: Title value should be a string or another widget")

        if self.label_by is not None:
            if isinstance(self.label_by, (str, int)):
                radio_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.LABEL_BY.value: self.label_by,
                })
            elif isinstance(self.label_by, Widget):
                target = {"id": self.label_by.widget_id, "target": AttributeNames.LABEL_BY.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Label_by value should be a string, int or another widget")

        if self.value_by is not None:
            if isinstance(self.value_by, (str, int)):
                radio_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE_BY.value: self.value_by,
                })
            elif isinstance(self.value_by, Widget):
                target = {"id": self.value_by.widget_id, "target": AttributeNames.VALUE_BY.value}
                _widget_providers.append(target)
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: Value_by value should be a string, int or another widget")

        if self.value is not None:
            if isinstance(self.value, Widget):
                target = {"id": self.value.widget_id, "target": AttributeNames.VALUE.value}
                _widget_providers.append(target)
            else:
                radio_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.value,
                })

        if self.style is not None:
            radio_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TYPE.value: self.style,
            })

        if self.allow_multi_selection is not None:
            if isinstance(self.allow_multi_selection, bool):
                radio_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.ALLOW_MULTI_SELECTION.value: self.allow_multi_selection,
                })
            else:
                raise ValueError(
                    f"Error Widget {self.widget_type}: allow_multi_selection value should be a string or another widget")

        if _widget_providers:
            self.add_widget_providers(radio_dict, _widget_providers)

        return radio_dict


class RadioGroupWidget(Widget, RadioGroup):

    def __init__(self,
                 options: List = None,
                 title: str = None,
                 label_by: str = None,
                 value_by: str = None,
                 value: Union[int, float, str, any] = None,
                 style: Literal["radio", "button"] = None,
                 allow_multi_selection: Optional[bool] = None,
                 **additional):
        Widget.__init__(self, RadioGroup.__name__,
                        compatibility=tuple([str.__name__, int.__name__, float.__name__, list.__name__,
                                             List._name, RadioGroup.__name__]),
                        **additional)
        RadioGroup.__init__(self,
                            options=options,
                            title=title,
                            label_by=label_by,
                            value_by=value_by,
                            value=value,
                            style=style,
                            allow_multi_selection=allow_multi_selection)
        self._parent_class = self.widget_type = RadioGroup.__name__

    def to_dict_widget(self):
        radio_dict = Widget.to_dict_widget(self)
        radio_dict = RadioGroup.to_dict_widget(self, radio_dict)
        return radio_dict
