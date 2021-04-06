import urllib

from tasksupervisor.entities.entity import FiwareEntity
from fiwareobjectconverter.object_fiware_converter import ObjectFiwareConverter
from tasksupervisor.api import materialflow

class Materialflow(FiwareEntity):
    def __init__(self):
        FiwareEntity.__init__(self)
        self.specification = ""
        self.ownerId = ""
        self.active = False

    def to_api_object(self):
        api_materialflow = materialflow.Materialflow()
        api_materialflow.id = self.id
        api_materialflow.specification = self.specification
        api_materialflow.owner_id = self.ownerId
        api_materialflow.active = self.active

        return api_materialflow

    @classmethod
    def CreateObjectFromJson(cls, _my_json):
        ts = Materialflow()
        try:
            ObjectFiwareConverter.fiware2Obj(_my_json, ts, setAttr=True)
            ts.specification = urllib.parse.unquote_plus(ts.specification)
            ts.specification = ts.specification.replace("\r\n", "\n")
        except Exception:
            return None
        return ts
