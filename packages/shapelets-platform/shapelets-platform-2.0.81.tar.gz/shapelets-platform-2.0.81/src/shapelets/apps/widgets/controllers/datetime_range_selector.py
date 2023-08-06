from __future__ import annotations

from datetime import date, datetime, time
import uuid

from dataclasses import dataclass
from typing import Dict, Optional, Union

from ..datetime_utils import _date_to_string, _transform_date_time_value
from ..widget import AttributeNames, StateControl, Widget


@dataclass
class DateRangeSelector(StateControl):
    title: Optional[str] = None
    start_datetime: Optional[Union[float, int, str, datetime, date, time]] = None
    end_datetime: Optional[Union[float, int, str, datetime, date, time]] = None
    min_datetime: Optional[Union[float, int, str, date]] = None
    max_datetime: Optional[Union[float, int, str, date]] = None
    _format: Optional[str] = None
    _start_datetime_str: Optional[str] = None
    _end_datetime_str: Optional[str] = None
    _min_datetime_str: Optional[str] = None
    _max_datetime_str: Optional[str] = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())

        if self.start_datetime is not None:
            self._start_datetime_str, self._format = _transform_date_time_value(self.start_datetime)

        if self.end_datetime is not None:
            self._end_datetime_str, self._format = _transform_date_time_value(self.end_datetime)

        if self.min_datetime is not None:
            try:
                self._min_datetime_str = _date_to_string(self.min_datetime)
            except:
                raise ValueError(f"Unexpected type {type(self.min_datetime)} for min_datetime.")

        if self.max_datetime is not None:
            try:
                self._max_datetime_str = _date_to_string(self.max_datetime)
            except:
                raise ValueError(f"Unexpected type {type(self.max_datetime)} for max_datetime.")

    def to_dict_widget(self, date_dict: Dict = None) -> Dict:
        if date_dict is None:
            date_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: DateRangeSelector.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }

        _widget_providers = []
        if self.title is not None:
            if isinstance(self.title, str):
                date_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            elif isinstance(self.title, Widget):
                target = {"id": self.title.widget_id, "target": AttributeNames.TITLE.value}
                _widget_providers.append(target)
            else:
                raise ValueError(f"Unexpected type {type(self.title)} in title")

        if self.start_datetime is not None:
            date_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.START_DATE.value: self._start_datetime_str
            })

        if self.end_datetime is not None:
            date_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.END_DATE.value: self._end_datetime_str
            })

        if self._format is not None:
            date_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.FORMAT.value: self._format
            })

        if self.min_datetime is not None:
            date_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.MIN_DATE.value: self._min_datetime_str
            })

        if self.max_datetime is not None:
            date_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.MAX_DATE.value: self._max_datetime_str
            })

        if _widget_providers:
            self.add_widget_providers(date_dict, _widget_providers)

        return date_dict


class DatetimeRangeSelectorWidget(DateRangeSelector, Widget):

    def __init__(self,
                 title: Optional[str] = None,
                 start_datetime: Optional[Union[float, int, str, datetime, date, time]] = None,
                 end_datetime: Optional[Union[float, int, str, datetime, date, time]] = None,
                 min_datetime: Optional[Union[float, int, str, date, time]] = None,
                 max_datetime: Optional[Union[float, int, str, date, time]] = None,
                 **additional):
        Widget.__init__(self,
                        DateRangeSelector.__name__,
                        compatibility=tuple(
                            [
                                DateRangeSelector.__name__,
                                float.__name__,
                                str.__name__,
                                datetime.__name__,
                                date.__name__,
                                time.__name__
                            ]
                        ),
                        **additional)
        DateRangeSelector.__init__(self,
                                   title=title,
                                   start_datetime=start_datetime,
                                   end_datetime=end_datetime,
                                   min_datetime=min_datetime,
                                   max_datetime=max_datetime)

        self._parent_class = DateRangeSelector.__name__

    def to_dict_widget(self) -> Dict:
        date_dict = Widget.to_dict_widget(self)
        date_dict = DateRangeSelector.to_dict_widget(self, date_dict)
        return date_dict
