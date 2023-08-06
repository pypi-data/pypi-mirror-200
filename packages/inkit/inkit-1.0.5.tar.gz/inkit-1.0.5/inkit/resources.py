from inkit.client import Client
from inkit.metaclasses import ResourceBuilderMetaclass
from inkit.router import Router


client = Client()


class FolderResource(metaclass=ResourceBuilderMetaclass):

    routes = Router.get_routes('folder')
    client = client


class TemplateResource(metaclass=ResourceBuilderMetaclass):

    routes = Router.get_routes('template')
    client = client


class RenderResource(metaclass=ResourceBuilderMetaclass):

    routes = Router.get_routes('render')
    client = client


class BatchResource(metaclass=ResourceBuilderMetaclass):

    routes = Router.get_routes('batch')
    client = client


class DocumentResource(metaclass=ResourceBuilderMetaclass):

    routes = Router.get_routes('document')
    client = client
