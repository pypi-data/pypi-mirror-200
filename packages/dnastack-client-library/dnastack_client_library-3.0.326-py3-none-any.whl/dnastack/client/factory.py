from typing import Optional, Iterable, List, Type, Callable, Union, Dict

from dnastack.client.base_client import BaseServiceClient
from dnastack.client.constants import DATA_SERVICE_CLIENT_CLASSES, SERVICE_CLIENT_CLASS
from dnastack.client.models import ServiceEndpoint
from dnastack.common.events import Event, EventHandler


class UnsupportedServiceTypeError(RuntimeError):
    """ Raised when the given client class is not supported """

    def __init__(self, endpoint: ServiceEndpoint):
        super().__init__(f'{endpoint.id}: {endpoint.type.group}:{endpoint.type.artifact}:{endpoint.type.version} '
                         'is not supported')


def create(endpoint: ServiceEndpoint,
           additional_service_client_classes: Iterable[Type[BaseServiceClient]] = None) -> SERVICE_CLIENT_CLASS:
    supported_service_client_classes = list(DATA_SERVICE_CLIENT_CLASSES)
    if additional_service_client_classes:
        supported_service_client_classes.extend(additional_service_client_classes)
    for cls in supported_service_client_classes:
        if endpoint.type in cls.get_supported_service_types():
            return cls.make(endpoint)
    raise UnsupportedServiceTypeError(endpoint)


class EndpointRepository:
    def __init__(self,
                 endpoints: Iterable[ServiceEndpoint],
                 cacheable=True,
                 additional_service_client_classes: Iterable[Type[BaseServiceClient]] = None,
                 default_event_interceptors: Optional[Dict[str, Union[EventHandler, Callable[[Event], None]]]] = None):
        self.__cacheable = cacheable
        self.__endpoints = self.__set_endpoints(endpoints)
        self.__additional_service_client_classes = additional_service_client_classes
        self.__default_event_interceptors = default_event_interceptors or dict()

    def set_default_event_interceptors(self, interceptors: Dict[str, Union[EventHandler, Callable[[Event], None]]]):
        self.__default_event_interceptors.update(interceptors)
        for t in self.__default_event_interceptors:
            if self.__default_event_interceptors[t] is None:
                del self.__default_event_interceptors[t]

    def all(self) -> List[ServiceEndpoint]:
        return self.__endpoints

    def get(self, id: str) -> Optional[SERVICE_CLIENT_CLASS]:
        for endpoint in self.__endpoints:
            if endpoint.id == id:
                client: BaseServiceClient = create(endpoint, self.__additional_service_client_classes)
                for event_type, event_handler in self.__default_event_interceptors.items():
                    client.events.on(event_type, event_handler)
                return client
        return None

    def __set_endpoints(self, endpoints: Iterable[ServiceEndpoint]):
        return (
            [e for e in endpoints]
            if (self.__cacheable and not isinstance(endpoints, list))
            else endpoints
        )
