import importscan
from pkg_resources import iter_entry_points

from usmqe.web.application.implementations.web_ui import ViaWebUI
from usmqe.web.application.implementations import TendrlImplementationContext
from usmqe.web.application.entities import EntityCollections


class Application(object):
    def __init__(self, hostname=None, path="", scheme="https", username=None, password=None):
        self.application = self
        self.hostname = hostname
        self.path = path
        self.scheme = scheme
        self.username = username
        self.password = password
        self.web_ui = ViaWebUI(owner=self)
        self.context = TendrlImplementationContext.from_instances([self.web_ui])
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
        ep.name: ep.resolve() for ep in iter_entry_points("usmqe.application_collections")
    }


from usmqe import web  # noqa

importscan.scan(web)
