from inkit import resources
from inkit.metaclasses import ProductMetaclass


class Folder(metaclass=ProductMetaclass):

    _main_resource = resources.FolderResource()


class Template(metaclass=ProductMetaclass):

    _main_resource = resources.TemplateResource()


class Render(metaclass=ProductMetaclass):

    _main_resource = resources.RenderResource()


class Batch(metaclass=ProductMetaclass):

    _main_resource = resources.BatchResource()


class Document(metaclass=ProductMetaclass):

    _main_resource = resources.DocumentResource()
