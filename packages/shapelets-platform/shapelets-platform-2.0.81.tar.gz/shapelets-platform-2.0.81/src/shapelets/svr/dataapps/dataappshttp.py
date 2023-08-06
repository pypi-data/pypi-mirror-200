# Copyright (c) 2022 Shapelets.io
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import json
import os
from decimal import Decimal

from blacksheep import FromJSON, WebSocket
from blacksheep.server.controllers import ApiController, get, post, delete, ws, file
from requests import Session
from typing import List, Optional

from .dataapps_ws import DataAppChangeListeners
from .idataappsservice import IDataAppsService
from ..docs import docs
from ..model.dataapps import DataAppProfile


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


class DataAppsHttpServer(ApiController):
    def __init__(self, svr: IDataAppsService) -> None:
        self._svr = svr
        super().__init__()
        self.dataapp_change_listeners = DataAppChangeListeners()

    @classmethod
    def route(cls) -> Optional[str]:
        return '/api/dataapps'

    @ws("/ws")
    async def ws(self, websocket: WebSocket):
        await websocket.accept()
        try:
            msg = await websocket.receive_text()
            self.dataapp_change_listeners.add(msg, websocket)
            while True:
                msg = await websocket.receive_text()
        except Exception as e:
            print(e)
        finally:
            self.dataapp_change_listeners.remove(websocket)

    @get("/")
    async def dataapp_list(self) -> List[DataAppProfile]:
        return self._svr.get_all()

    @post("/")
    async def create(self, attributes: FromJSON[DataAppProfile]) -> DataAppProfile:
        dataapp_attributes = DataAppProfile(name=attributes.value.name,
                                            major=attributes.value.major,
                                            minor=attributes.value.minor,
                                            description=attributes.value.description,
                                            specId=attributes.value.specId,
                                            tags=attributes.value.tags)
        data_app = self._svr.create(dataapp_attributes)
        await self.dataapp_change_listeners.notify(data_app.name, data_app.major, data_app.minor, False)
        return data_app

    @get("/{id}")
    async def get_dataapp(self, dataAppName: str) -> DataAppProfile:
        return self._svr.get_dataapp(dataAppName)

    @delete("/")
    async def delete_all(self) -> bool:
        return self._svr.delete_all()

    @delete("/{id}/{major}/{minor}")
    async def delete(self, dataAppName: str, major: int, minor: int) -> bool:
        delete = self._svr.delete_dataapp(dataAppName, major, minor)
        await self.dataapp_change_listeners.notify(dataAppName, major, minor, False)
        return delete

    @get("/{id}/privileges")
    async def get_dataapp_privileges(self, dataapp_id: int) -> List[DataAppProfile]:
        return self._svr.get_dataapp_privileges(dataapp_id)

    @get("/{id}/versions")
    async def get_dataapp_versions(self, dataAppName: str) -> List[float]:
        return json.dumps(self._svr.get_dataapp_versions(dataAppName), cls=DecimalEncoder)

    @get("spec/{specId}")
    async def get_dataapp_spec(self, specId: str) -> file:
        shapelets_dir = os.path.expanduser('~/.shapelets')
        data_apps_store = os.path.join(shapelets_dir, 'dataAppsStore')
        spec_path = os.path.join(data_apps_store, f"{specId}.json")
        return file(spec_path, "text/json")

    @get("/{id}/{major}/{minor}")
    async def get_dataapp_by_version(self, dataAppName: str, major: int, minor: int) -> DataAppProfile:
        return self._svr.get_dataapp_by_version(dataAppName, major, minor)

    @get("/{id}/lastVersion")
    async def get_dataapp_last_version(self, dataAppName: str) -> float:
        return self._svr.get_dataapp_last_version(dataAppName)

    @get("/{id}/tags")
    async def get_dataapp_tags(self, dataAppName: str) -> List[str]:
        return self._svr.get_dataapp_tags(dataAppName)


class DataAppsHttpProxy(IDataAppsService):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> List[DataAppProfile]:
        return self.session.get('/api/dataapps/')

    def create(self, dataapp) -> DataAppProfile:
        payload = DataAppProfile(name=dataapp.name,
                                 major=dataapp.version[0] if dataapp.version else None,
                                 minor=dataapp.version[1] if dataapp.version else None,
                                 description=dataapp.description,
                                 specId=dataapp.to_json(),
                                 tags=dataapp.tags)
        return self.session.post('/api/dataapps/', json=json.loads(payload.json()))

    def get_dataapp(self, dataAppName: str) -> DataAppProfile:
        return self.session.get('/api/dataapps/', params=[("dataAppName", dataAppName)])

    def delete_dataapp(self, dataAppName: str, version: float):
        self.session.delete('/api/dataapps/{id}/{version}', params=[("dataAppName", dataAppName), ("version", version)])

    def delete_all(self) -> bool:
        self.session.delete('/api/dataapps/')
        return True

    def get_dataapp_privileges(self, dataAppName: str) -> List[DataAppProfile]:
        pass

    def get_dataapp_versions(self, dataAppName: str) -> List[float]:
        return self.session.get('/api/{id}/versions', params=[("dataAppName", dataAppName)])

    def get_dataapp_by_version(self, dataAppName: str, version: float) -> List[float]:
        return self.session.get('/api/{id}/{version}', params=[("dataAppName", dataAppName), ("version", version)])

    def get_dataapp_last_version(self, dataAppName: str) -> float:
        return self.session.get('/api/{id}/lastVersion', params=[("dataAppName", dataAppName)])

    def get_dataapp_tags(self, dataAppName: str) -> List[str]:
        return self.session.get('/api/{id}/tags', params=[("dataAppName", dataAppName)])
