'''from nailgun import entities, config
from tendrlui.base.application.implementations import TendrluiImplementationContext, Implementation


class RESTAPI(Implementation):
    """REST API implementation using nailgun"""

    register_method_for = TendrluiImplementationContext.external_for
    name = "RESTAPI"
    entities = entities
    config = config'''
