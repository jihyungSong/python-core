import logging

from spaceone.core import config
from spaceone.core.error import *

_LOGGER = logging.getLogger(__name__)


def _get_module(package, target):
    return __import__(f'{package}.{target}', fromlist=[f'{target}'])


class Locator(object):

    def __init__(self, transaction=None):
        self.transaction = transaction

    def get_service(self, name, metadata={}):
        package = config.get_package()
        try:
            service_module = _get_module(package, 'service')
            return getattr(service_module, name)(metadata)

        except ERROR_BASE as e:
            raise e

        except Exception as e:
            raise ERROR_LOCATOR(name=name, reason=e, _meta={'type': 'service'})

    def get_manager(self, name, **kwargs):
        package = config.get_package()
        try:
            manager_module = _get_module(package, 'manager')
            return getattr(manager_module, name)(self.transaction, **kwargs)

        except ERROR_BASE as e:
            raise e

        except Exception as e:
            raise ERROR_LOCATOR(name=name, reason=e, _meta={'type': 'manager'})

    def get_connector(self, name, **kwargs):
        package = config.get_package()
        connector_conf = config.get_handler(name)
        try:
            connector_module = _get_module(package, 'connector')
            return getattr(connector_module, name)(self.transaction, connector_conf, **kwargs)

        except ERROR_BASE as e:
            raise e

        except Exception as e:
            raise ERROR_LOCATOR(name=name, reason=e, _meta={'type': 'connector'})

    def get_info(self, name, *args, **kwargs):
        package = config.get_package()
        try:
            info_module = _get_module(package, 'info')
            return getattr(info_module, name)(*args, **kwargs)

        except ERROR_BASE as e:
            raise e

        except Exception as e:
            raise ERROR_LOCATOR(name=name, reason=e, _meta={'type': 'info'})

    def get_model(self, name):
        package = config.get_package()
        try:
            model_module = _get_module(package, 'model')
            model = getattr(model_module, name)
            model.connect()
            return model

        except ERROR_BASE as e:
            raise e

        except Exception as e:
            raise ERROR_LOCATOR(name=f'{name} Model', reason=e, _meta={'type': 'info'})
