import uuid
from dataclasses import dataclass
from typing import Optional, Tuple
from folium.folium import Map
from ..widget import Widget, AttributeNames, StateControl


@dataclass
class FoliumChart(StateControl):
    title: Optional[str] = None
    folium: any = None

    def to_dict_widget(self, folium_dict: dict = None):
        if folium_dict is None:
            folium_dict = {
                AttributeNames.ID.value: str(uuid.uuid1()),
                AttributeNames.TYPE.value: FoliumChart.__name__,
                AttributeNames.PROPERTIES.value: {}
            }

        if (self.title is not None):
            folium_dict[AttributeNames.PROPERTIES.value].update({
                AttributeNames.TITLE.value: self.title
            })

        if (self.folium is not None):
            if isinstance(self.folium, Map):
                folium_dict[AttributeNames.PROPERTIES.value].update({
                    AttributeNames.VALUE.value: self.folium._repr_html_()
                })

        return folium_dict


class FoliumChartWidget(Widget, FoliumChart):

    def __init__(self,
                 title: Optional[str] = None,
                 folium: Optional[any] = None,
                 **additional
                 ):
        Widget.__init__(self, 'FoliumChart', 
                        compatibility= tuple([FoliumChart.__name__, ]),
                        **additional)
        FoliumChart.__init__(self, title=title, folium=folium)
        self._parent_class = FoliumChart.__name__

    def to_dict_widget(self):
        folium_dict = Widget.to_dict_widget(self)
        folium_dict = FoliumChart.to_dict_widget(self, folium_dict)

        return folium_dict
