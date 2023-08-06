import json
import re

from inkit.exceptions import InkitException
from inkit.extensions import base64encode


class ProductMetaclass(type):

    def __init__(cls, classname, superclasses, attr_dict):
        super().__init__(classname, superclasses, attr_dict)
        for handler in cls._main_resource.handlers:  # noqa
            setattr(cls, handler, getattr(cls._main_resource, handler))  # noqa

    def __call__(cls, *args, **kwargs):
        raise InkitException(f'Class {cls.__name__} is not instantiable')


class ResourceBuilderMetaclass(type):

    def __new__(mcs, classname, superclasses, attr_dict):
        mcs.set_methods(attr_dict)
        mcs.set_handlers(attr_dict)
        return super().__new__(mcs, classname, superclasses, attr_dict)

    @classmethod
    def set_methods(mcs, attr_dict):
        build_request_data = mcs.build_request_data_factory()
        attr_dict[build_request_data.__name__] = staticmethod(build_request_data)

    @classmethod
    def set_handlers(mcs, attr_dict):
        handlers = []
        for route in attr_dict['routes']:
            attr_dict[route.sdk_method_name] = mcs.handlers_factory(
                resource_path=route.path,
                http_method=route.http_method
            )
            handlers.append(route.sdk_method_name)
        attr_dict['handlers'] = handlers

    @staticmethod
    def handlers_factory(resource_path, http_method):
        if re.search(r'/{id}', resource_path):
            def handler(self, entity_id, **kwargs):
                request_data = self.build_request_data(
                    path=resource_path.format(id=entity_id),
                    http_method=http_method,
                    data=kwargs
                )
                return self.client.send(**request_data)
            return handler

        def handler(self, **kwargs):
            request_data = self.build_request_data(
                path=resource_path,
                http_method=http_method,
                data=kwargs
            )
            return self.client.send(**request_data)
        return handler

    @staticmethod
    def build_request_data_factory():
        def build_request_data(path, http_method, data):
            request_data = {
                'path': path,
                'http_method': http_method
            }
            if http_method.upper() in ('GET', 'DELETE') and data:
                request_data.update(params={
                    key.replace('_', '-', 1) if key.startswith('data_') else key: val
                    for key, val in data.items()
                })
            if re.search(r'(/pdf|download/\w+)$', path):
                request_data.update(
                    retry=15,
                    retry_interval=2,
                    status_forcelist=[404]
                )
            if http_method.upper() in ('POST', 'PATCH'):
                request_data.update(data=json.dumps({
                    key: base64encode(val) if key == 'file' else val
                    for key, val in data.items()
                }))
            return request_data
        return build_request_data
