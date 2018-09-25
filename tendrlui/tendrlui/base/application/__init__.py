import importscan
from pkg_resources import iter_entry_points

from tendrlui import settings
from tendrlui.base.application.implementations.web_ui import WebUI
#from tendrlui.base.application.implementations.rest_api import RESTAPI
from tendrlui.base.application.implementations import TendrluiImplementationContext
from tendrlui.base.modeling import EntityCollections


class Application(object):
    def __init__(self, hostname=None, path="", scheme="https"):
        self.application = self
        self.hostname = hostname or settings.satellite.hostname
        self.path = path
        self.scheme = scheme
        self.web_ui = WebUI(owner=self)
#        self.rest_api = RESTAPI(owner=self)
#        self.context = TendrluiImplementationContext.from_instances([self.web_ui, self.rest_api])
        self.context = TendrluiImplementationContext.from_instances([self.web_ui])
        self.collections = EntityCollections.for_application(self)

    @property
    def address(self):
        return "{}://{}/{}".format(self.scheme, self.hostname, self.path)

    @property
    def destinations(self):
        """Returns a dict of all valid destinations for a particular object"""
        return {
            impl.name: impl.navigator.list_destinations(self)
            for impl in self.application.context.implementations.values()
            if impl.navigator
        }


def load_application_collections():
    return {
        ep.name: ep.resolve() for ep in iter_entry_points("tendrlui.application_collections")
    }


from tendrlui import base  # noqa

importscan.scan(base)
