import urllib

from tasksupervisor.entities.entity import FiwareEntity
from fiwareobjectconverter.object_fiware_converter import ObjectFiwareConverter


class Materialflow(FiwareEntity):
    def __init__(self):
        FiwareEntity.__init__(self)
        self.specification = ""
        self.ownerId = ""
        self.active = False

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
