from __future__ import annotations

import pandas as pd
import numpy as np
import shapelets as sh
import uuid

from typing import Union, Optional, Tuple
from dataclasses import dataclass

from ..widget import AttributeNames, Widget, StateControl
from ..util import _to_utf64_arrow_buffer



@dataclass
class Table(StateControl):
    data: Optional[Union[pd.DataFrame, sh.DataSet]] = None
    rows_per_page: Optional[int] = None
    tools_visible: Optional[bool] = None

    def __post_init__(self):
        if not hasattr(self, "widget_id"):
            self.widget_id = str(uuid.uuid1())

    def replace_widget(self, new_widget: Table):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.data = new_widget.data
        self.rows_per_page = new_widget.rows_per_page
        self.tools_visible = new_widget.tools_visible

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.data is not None:
            return self.data
        return None


    def from_dataframe(self, data: pd.DataFrame) -> Table:
        self.data = data
        return self

    def to_dataframe(self) -> pd.DataFrame:
        dataframe = self.data
        return dataframe

    def from_dataset(self, data: sh.DataSet) -> Table:
        self.data = data
        return self

    def to_dataset(self) -> sh.DataSet:
        dataset = self.data
        return dataset

    def from_list(self, lista: list) -> Table:
        self.data = lista
        return self

    def to_list(self) -> list:
        lista = self.data.values.tolist() if self.data is not None else []
        return lista

    def to_utf64_arrow_buffer(self) -> str:
        return _to_utf64_arrow_buffer(data=self.data, preserve_index=False)

    def to_dict_widget(self, table_dict: dict = None):
        if table_dict is None:
            table_dict = {
                AttributeNames.ID.value: self.widget_id,
                AttributeNames.TYPE.value: Table.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        if self.data is not None:
            if isinstance(self.data, (pd.DataFrame, sh.DataSet)):
                arrow_data = self.to_utf64_arrow_buffer()
                table_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.DATA.value: arrow_data,
                })
            else:
                raise ValueError("Data type not supported")

        if self.rows_per_page is not None:
            if isinstance(self.rows_per_page, int):
                table_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.ROWS_PER_PAGE.value: self.rows_per_page
                })

        if self.tools_visible is not None:
            if isinstance(self.tools_visible, int):
                table_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TOOLS_VISIBLE.value: self.tools_visible
                })

        return table_dict


class TableWidget(Table, Widget):

    def __init__(self,
                 data: Optional[Union[pd.DataFrame, sh.DataSet]] = None,
                 rows_per_page: Optional[int] = None,
                 tools_visible: Optional[bool] = None,
                 **additional):
        Widget.__init__(self, Table.__name__,
                        compatibility=tuple(
                            [pd.DataFrame.__name__, np.ndarray.__name__, list.__name__, Table.__name__]),
                        **additional)
        Table.__init__(self, data=data, rows_per_page=rows_per_page, tools_visible=tools_visible)
        self._parent_class = Table.__name__
        self._compatibility: Tuple = (pd.DataFrame.__name__,
                                      np.ndarray.__name__,
                                      list.__name__,
                                      Table.__name__,
                                      sh.DataSet.__name__)

    def to_dict_widget(self):
        table_dict = Widget.to_dict_widget(self)
        table_dict = Table.to_dict_widget(self, table_dict)
        return table_dict
