from __future__ import annotations

import calendar
import numpy as np
import pandas as pd
import time
import uuid
import warnings

from dataclasses import dataclass, field
from datetime import date, datetime

from typing import List, Optional, Tuple, Union

from ..widget import AttributeNames, StateControl, Widget
from ..contexts import FilteringContext, TemporalContext
from ..util import _to_utf64_arrow_buffer
from ....model import Sequence
from .... import DataSet


@dataclass
class View:
    """
    Highlight a section of a Linechart.
    """
    start: Optional[Union[int, str, datetime]] = None
    end: Optional[Union[int, str, datetime]] = None

    def _adjust_view_type(self):
        """
        View values come in different types. Adjust those values to a common type so the UI can plot them.
        """
        if isinstance(self.start, datetime):
            # We need nanoseconds
            try:
                # Might fail in Windows
                self.start = int(self.start.timestamp() * 10 ** 9)
            except:
                self.start = calendar.timegm(self.start.timetuple()) * 10 ** 9
        elif isinstance(self.start, date):
            self.start = int(time.mktime(self.start.timetuple()) * 10 ** 9)
        elif isinstance(self.start, str):
            self.start = int(datetime.strptime(self.start, '%Y-%m-%d').timestamp() * 10 ** 9)

        if isinstance(self.end, datetime):
            try:
                # Might fail in Windows
                self.end = int(self.end.timestamp() * 10 ** 9)
            except:
                self.end = calendar.timegm(self.end.timetuple()) * 10 ** 9
        elif isinstance(self.end, date):
            self.end = int(time.mktime(self.end.timetuple()) * 10 ** 9)
        elif isinstance(self.end, str):
            self.end = int(datetime.strptime(self.end, '%Y-%m-%d').timestamp() * 10 ** 9)

    def to_dict(self):
        self._adjust_view_type()
        return {
            AttributeNames.BEGIN.value: str(self.start),
            AttributeNames.END.value: str(self.end)
        }


LineChartValueType = Union[
    List[int],
    List[float],
    List[str],
    np.ndarray,
    pd.DataFrame,
    pd.Series,
    DataSet
]


@dataclass
class LineChart(StateControl):
    data: Optional[LineChartValueType] = None
    title: Optional[str] = None
    views: Optional[List[View]] = field(default_factory=lambda: [])
    temporal_context: Optional[TemporalContext] = None
    filtering_context: Optional[FilteringContext] = None
    multi_line_chart: Optional[bool] = True
    multi_lane: Optional[bool] = True
    _plots: List = field(default_factory=lambda: [])
    _is_type = None

    def __post_init__(self):
        # A subtype to differentiate between sequences or y_axis/x_axis. Requested by UI.
        self.linechart_sub_type = None
        self.sequence = None
        self.y_axis = None
        self.x_axis = None
        if isinstance(self.data, Sequence):
            self.linechart_sub_type = f"{AttributeNames.SEQUENCE.value.capitalize()}"
            self.sequence = self.data
        elif isinstance(self.data, List):
            self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
            self.y_axis = self.data
        elif isinstance(self.data, np.ndarray):
            self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
            self.y_axis = self.data
        elif isinstance(self.data, pd.Series):
            self.linechart_sub_type = f"Arrow"
            self._plot_dataframe(data=self.data.to_frame())
        elif isinstance(self.data, pd.DataFrame):
            self.linechart_sub_type = f"Arrow"
            self._plot_dataframe(data=self.data)
        elif isinstance(self.data, DataSet):
            self.linechart_sub_type = f"Arrow"
            df_from_dataset = self.data.to_pandas()
            if 'index' in df_from_dataset:
                df_from_dataset.set_index('index', inplace=True)
            self._plot_dataframe(data=df_from_dataset)
        elif self.data is None:
            self.linechart_sub_type = "Empty"

        # Adjust Views
        if len(self.views) > 0:
            for index, view in enumerate(self.views):
                self.views[index] = self._adjust_views(view)

    @staticmethod
    def _extract_starts_and_every_from_index(dataframe: pd.DataFrame) -> Tuple[int, int]:
        indices = dataframe.index.values
        # The timestamp is stored as nanoseconds from epoch. Get it as an int64 and convert it to ms
        starts = int(indices[0].astype('uint64') / 1e6)
        every = int((indices[1] - indices[0]).astype("timedelta64[ms]") / np.timedelta64(1, 'ms'))
        return starts, every

    def _plot_dataframe(self, data: pd.DataFrame):
        df_clean = data.select_dtypes(include='number')
        df_clean.dropna(inplace=True)
        if not self.multi_line_chart:
            df_clean = df_clean.iloc[:, [0]]

        if isinstance(df_clean.index, pd.DatetimeIndex):
            starts, every = self._extract_starts_and_every_from_index(df_clean)
            df_clean.reset_index(drop=True)
        elif isinstance(df_clean.index, pd.RangeIndex):
            starts = df_clean.index.start
            every = df_clean.index.step
            df_clean.reset_index(drop=True)
        else:
            warnings.warn("Dataframe index type not allow. Will try to reset index")
            df_clean.reset_index(inplace=True, drop=True)
            starts = df_clean.index.start
            every = df_clean.index.step

        self._plots.append({
            AttributeNames.ARROW_DATA.value: self.to_utf64_arrow_buffer(df_clean),
            AttributeNames.START.value: starts,
            AttributeNames.EVERY.value: every,
            AttributeNames.LENGTH.value: len(df_clean.index)
        })

    def replace_widget(self, new_widget: LineChart):
        """
        Replace the current values of the widget for the values of a similar widget type.
        """
        self.data = new_widget.data
        self.title = new_widget.title
        self.views = new_widget.views
        self.temporal_context = new_widget.temporal_context
        self.filtering_context = new_widget.filtering_context
        self.multi_line_chart = new_widget.multi_line_chart
        self.multi_lane = new_widget.multi_lane
        self.linechart_sub_type = new_widget.linechart_sub_type
        self._plots = new_widget._plots
        self._is_type = new_widget._is_type

    def get_current_value(self):
        """
        Return the current value of the widget. Return None is the widget value is not set.
        """
        if self.data is not None:
            return self.data
        return None

    # TODO Adjust LineChart Type
    def from_sequences(self, sequences: List[Sequence]) -> LineChart:
        self.linechart_sub_type = f"{AttributeNames.SEQUENCE.value.capitalize()}"
        self.data = sequences
        return self

    def from_sequence(self, sequence: Sequence) -> LineChart:
        self.linechart_sub_type = f"{AttributeNames.SEQUENCE.value.capitalize()}"
        self.data = sequence
        return self

    def to_sequence(self) -> Sequence:
        return self.sequence

    def from_views(self, views: List[View]) -> LineChart:
        self.views = views
        return self

    def from_view(self, view: View) -> LineChart:
        self.views.append(view)
        return self

    def to_views(self) -> List[View]:
        return self.views

    def from_dataframe(self, dataframe: pd.DataFrame) -> LineChart:
        # TODO: save dataframe/transform
        self.data = dataframe
        return self

    def to_dataframe(self) -> pd.DataFrame:
        # TODO: transform sequence to dataframe
        return self.sequence

    def from_ndarray(self, ndarray: np.ndarray) -> LineChart:
        # TODO: save ndarray/transform
        self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
        self.data = ndarray
        return self

    def to_ndarray(self) -> np.ndarray:
        # TODO: transform sequence to ndarray
        return self.sequence

    def from_series(self, series: pd.Series):
        self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
        self.data = series

    def to_series(self) -> np.ndarray:
        # TODO: transform sequence to Series
        return self.data

    def from_list(self, lst: list) -> LineChart:
        self.linechart_sub_type = f"{LineChart.__name__}"
        self.data = lst
        return self

    def to_list(self) -> pd.DataFrame:
        return self.y_axis

    def plot(self,
             y_axis: Union[List[int], List[float], np.ndarray, pd.Series] = None,
             x_axis: Union[List[int], List[float], List[str], np.ndarray] = None,
             sequence: Union[List[Sequence], Sequence] = None,
             label: str = None,
             lane_index: int = 0):
        # TODO: I want to complety modify or remove this function. Doesn't make sense to have a function with some many
        # isInstances once we are already checking that in previous functions.
        plot_dict = {}

        plot_dict.update({AttributeNames.LANE_INDEX.value: lane_index})

        if sequence is not None:
            # Adjust subtype for UI
            self.linechart_sub_type = f"{AttributeNames.SEQUENCE.value.capitalize()}"
            # list of sequences
            if isinstance(sequence, List) and all([isinstance(seq, Sequence) for seq in sequence]):
                for seq in sequence:
                    if isinstance(seq, Sequence):
                        plot_dict_array = dict()
                        plot_dict_array.update({
                            AttributeNames.LANE_INDEX.value: lane_index,
                            AttributeNames.SEQUENCE_ID.value: seq.sequence_id
                        })
                        self._plots.append(plot_dict_array)
                    else:
                        raise ValueError(f"Unexpected type {type(seq)}")
                    # elif isinstance(seq, SequenceSelector):
                    #     seq_node = dict()
                    #     seq_node.update({
                    #         AttributeNames.LANE_INDEX.value: lane_index,
                    #         AttributeNames.WIDGET_REF.value: seq.widget_id
                    #     })
                    #     self._plots.append(seq_node)

            # if isinstance(sequence, SequenceSelector) or isinstance(sequence, CollectionSelector):
            #     if self.sequence:
            #         self._plots.append({AttributeNames.WIDGET_REF.value: sequence.widget_id})

            # a single sequence
            if isinstance(sequence, Sequence):
                plot_dict.update({
                    AttributeNames.SEQUENCE_ID.value: sequence.sequence_id
                })
                self._plots.append(plot_dict)

        # Handle arrays: y-axis
        # TODO: save array and send ID
        if y_axis is not None:
            self.linechart_sub_type = f"{AttributeNames.NUMPY_ARRAY.value.capitalize()}"
            if isinstance(y_axis, np.ndarray):
                plot_dict.update({AttributeNames.Y_AXIS.value: y_axis.tolist()})
            elif isinstance(y_axis, List):
                plot_dict.update({AttributeNames.Y_AXIS.value: y_axis})
            elif isinstance(y_axis, pd.Series):
                plot_dict.update({AttributeNames.Y_AXIS.value: y_axis.values.tolist()})

        # Handle arrays: x-axis
        # TODO: save array and send ID
        if x_axis is not None:
            if isinstance(x_axis, np.ndarray):
                is_type = ''
                if ('<i' in x_axis.dtype.str) or ('<f' in x_axis.dtype.str):
                    is_type = 'number'
                elif '<U' in x_axis.dtype.str:
                    is_type = 'string'
                if self._is_type is None:
                    self._is_type = is_type
                if self._is_type is not None and self._is_type is not is_type:
                    raise Exception("invalid mix of types in x axis")

                plot_dict.update({AttributeNames.X_AXIS.value: "nd_array_id"})

            elif isinstance(x_axis, List):
                is_type = ""
                if all([isinstance(item, str) for item in x_axis]):
                    is_type = 'string'
                elif all([(isinstance(item, float) or isinstance(item, int)) for item in x_axis]):
                    is_type = 'number'

                if self._is_type is None:
                    self._is_type = is_type

                if self._is_type is not None and self._is_type is not is_type:
                    raise Exception("invalid mix of types in x axis")

                plot_dict.update({AttributeNames.X_AXIS.value: x_axis})
            elif isinstance(x_axis, pd.RangeIndex):
                plot_dict.update({AttributeNames.X_AXIS.value: x_axis.tolist()})
            elif isinstance(x_axis, pd.DatetimeIndex):
                #     plot_dict.update({AttributeNames.X_AXIS.value: pd.Series(x_axis.format()).tolist()})
                plot_dict.update({AttributeNames.X_AXIS.value: x_axis.astype(np.int64).tolist()})

        if label is not None:
            if sequence:
                plot_dict.update({AttributeNames.LABEL.value: sequence})
            if isinstance(label, str):
                plot_dict.update({
                    AttributeNames.LABEL.value: label
                })
        if self.sequence is None:
            self._plots.append(plot_dict)

    def to_dict_widget(self, line_chart_dict: dict = None):
        if line_chart_dict is None:
            line_chart_dict = {
                AttributeNames.ID.value: str(uuid.uuid1()),
                AttributeNames.TYPE.value: LineChart.__name__,
                AttributeNames.DRAGGABLE.value: self.draggable,
                AttributeNames.RESIZABLE.value: self.resizable,
                AttributeNames.DISABLED.value: self.disabled,
                AttributeNames.PROPERTIES.value: {}
            }
        if self.title is not None:
            if isinstance(self.title, str):
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.TITLE.value: self.title
                })
            else:
                raise ValueError(f"Unexpected type {type(self.title)} in title")

        if self.views:
            if isinstance(self.views, List) and all(isinstance(view, View) for view in self.views):
                view_list = [view.to_dict() for view in self.views]
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VIEWS.value: view_list
                })
            elif isinstance(self.views, List):
                # For now, try to get begin and end
                view_list = [{
                    AttributeNames.BEGIN.value: str(view[0]),
                    AttributeNames.END.value: str(view[1])
                } for view in self.views]
                line_chart_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VIEWS.value: view_list
                })

        if len(self._plots) > 0:
            line_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.PLOTS.value: self._plots
            })

        if self.linechart_sub_type:
            line_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TYPE.value: self.linechart_sub_type
            })

        if self.multi_lane is not None:
            line_chart_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.MULTI_LANE.value: self.multi_lane
            })

        return line_chart_dict

    @staticmethod
    def to_utf64_arrow_buffer(data: pd.DataFrame) -> str:
        return _to_utf64_arrow_buffer(data=data, preserve_index=False)

    def _adjust_views(self, view) -> View:
        """
        Views can be created with integers. When a view receives integers, the start and end indicate the index of the dataframe.
        param view: View to adjust.
        returns same View if modification is not needed, or a modified View with the correct index from the dataframe as start and end.
        """
        if isinstance(view.start, int) and isinstance(view.end, int):
            view.start = self.data.index[view.start]
            view.end = self.data.index[view.end]
        return view


class LineChartWidget(Widget, LineChart):
    def __init__(self,
                 data: Optional[LineChartValueType] = None,
                 title: Optional[str] = None,
                 views: Optional[List[View]] = [],
                 temporal_context: Optional[TemporalContext] = None,
                 filtering_context: Optional[FilteringContext] = None,
                 multi_line_chart: Optional[bool] = True,
                 multi_lane: Optional[bool] = True,
                 **additional):

        # define TYPE
        widget_type = LineChart.__name__
        Widget.__init__(self, widget_type,
                        compatibility=tuple(
                            [str.__name__, int.__name__, float.__name__, LineChart.__name__, Sequence.__name__,
                             View.__name__, "List[View]", "List[Sequence]", pd.DataFrame.__name__,
                             list.__name__, np.ndarray.__name__, pd.Series.__name__]),
                        **additional)
        LineChart.__init__(
            self,
            data=data,
            title=title,
            views=views,
            temporal_context=temporal_context,
            filtering_context=filtering_context,
            multi_line_chart=multi_line_chart,
            multi_lane=multi_lane
        )
        self._parent_class = LineChart.__name__

        temporal_context_id = None
        if self.temporal_context:
            temporal_context_id = self.temporal_context.context_id
            self.temporal_context.widgets.append(self.widget_id)
        filtering_context_id = None
        if self.filtering_context:
            filtering_context_id = filtering_context.context_id
            filtering_context.output_widgets.append(self.widget_id)
        self.temporal_context = temporal_context_id
        self.filtering_context = filtering_context_id

    def to_dict_widget(self):
        line_chart_dict = Widget.to_dict_widget(self)
        line_chart_dict = LineChart.to_dict_widget(self, line_chart_dict)
        return line_chart_dict
