from pprint import pformat
from typing import List, Iterator, Optional, Union, Iterable
from urllib.parse import urljoin

from pydantic import ValidationError

from dnastack.alpha.client.ewes.models import WesServiceInfo, ExtendedRunStatus, ExtendedRunListOptions, \
    ExtendedRunListResponse, ExtendedRun, RunId, WorkbenchApiError, BatchActionResult, MinimalExtendedRun, \
    MinimalBatch, \
    BatchRunRequest, ExtendedRunRequest
from dnastack.alpha.client.workbench.base_client import BaseWorkbenchClient
from dnastack.client.base_exceptions import UnauthenticatedApiAccessError, UnauthorizedApiAccessError, ServerError
from dnastack.client.models import ServiceEndpoint
from dnastack.client.result_iterator import ResultLoader, InactiveLoaderError, ResultIterator
from dnastack.client.service_registry.models import ServiceType
from dnastack.http.session import HttpSession, HttpError


class ExtendedRunListResultLoader(ResultLoader):

    def __init__(self,
                 service_url: str,
                 http_session: HttpSession,
                 list_options: Optional[ExtendedRunListOptions] = None,
                 max_results: int = None):
        self.__http_session = http_session
        self.__service_url = service_url
        self.__list_options = list_options
        self.__max_results = int(max_results) if max_results else None
        self.__loaded_results = 0
        self.__active = True
        self.__visited_urls: List[str] = list()

        if not self.__list_options:
            self.__list_options = ExtendedRunListOptions()

    def has_more(self) -> bool:
        return self.__active

    def __generate_api_error_feedback(self, response_body) -> str:
        if self.__service_url:
            return f'Failed to load a follow-up page of the table list from {self.__service_url} ({response_body})'
        else:
            return f'Failed to load the first page of the table list from {self.__service_url} ({response_body})'

    def load(self) -> List[ExtendedRunStatus]:
        if not self.__active:
            raise InactiveLoaderError(self.__service_url)

        with self.__http_session as session:
            current_url = self.__service_url

            try:
                response = session.get(current_url, params=self.__list_options)
            except HttpError as e:
                status_code = e.response.status_code
                response_text = e.response.text

                self.__visited_urls.append(current_url)

                if status_code == 401:
                    raise UnauthenticatedApiAccessError(self.__generate_api_error_feedback(response_text))
                elif status_code == 403:
                    raise UnauthorizedApiAccessError(self.__generate_api_error_feedback(response_text))
                elif status_code >= 400:  # Catch all errors
                    raise ServerError(
                        f'Unexpected error: {response_text}',
                        status_code,
                        response_text,
                        urls=self.__visited_urls
                    )

            status_code = response.status_code
            response_text = response.text

            try:
                response_body = response.json() if response_text else dict()
            except Exception:
                self.logger.error(f'{self.__service_url}: Unexpectedly non-JSON response body from {current_url}')
                raise ServerError(
                    f'Unable to deserialize JSON from {response_text}.',
                    status_code,
                    response_text,
                    urls=self.__visited_urls
                )

            try:
                api_response = ExtendedRunListResponse(**response_body)
            except ValidationError:
                raise ServerError(
                    f'Invalid Response Body: {response_body}',
                    status_code,
                    response_text,
                    urls=self.__visited_urls
                )

            self.logger.debug(f'Response:\n{pformat(response_body, indent=2)}')

            self.__list_options.page_token = api_response.next_page_token or None
            if not self.__list_options.page_token:
                self.__active = False

            if self.__max_results and (self.__loaded_results + len(api_response.runs)) >= self.__max_results:
                self.__active = False
                num_of_loadable_results = self.__max_results - self.__loaded_results
                return api_response.runs[0:num_of_loadable_results]
            else:
                self.__loaded_results += len(api_response.runs)
                return api_response.runs


class EWesClient(BaseWorkbenchClient):

    @staticmethod
    def get_adapter_type() -> str:
        return 'ewes-service'

    @staticmethod
    def get_supported_service_types() -> List[ServiceType]:
        return [
            ServiceType(group='com.dnastack.workbench', artifact='ewes-service', version='1.0.0'),
        ]

    @classmethod
    def make(cls, endpoint: ServiceEndpoint, namespace: str):
        """Create this class with the given `endpoint` and `namespace`."""
        if not endpoint.type:
            endpoint.type = cls.get_default_service_type()
        return cls(endpoint, namespace)

    def get_service_info(self) -> WesServiceInfo:
        with self.create_http_session() as session:
            response = session.get(urljoin(self.endpoint.url, f'{self.namespace}/ga4gh/wes/v1/service-info'))
            return WesServiceInfo(**response.json())

    def list_runs(self,
                  list_options: Optional[ExtendedRunListOptions] = None,
                  max_results: int = None) -> Iterator[ExtendedRunStatus]:
        return ResultIterator(ExtendedRunListResultLoader(
            service_url=urljoin(self.endpoint.url, f'{self.namespace}/ga4gh/wes/v1/runs'),
            http_session=self.create_http_session(),
            list_options=list_options,
            max_results=max_results))

    def get_status(self, run_id: str) -> MinimalExtendedRun:
        with self.create_http_session() as session:
            response = session.get(urljoin(self.endpoint.url, f'{self.namespace}/ga4gh/wes/v1/runs/{run_id}/status'))
            return MinimalExtendedRun(**response.json())

    def get_run(self, run_id: str, include_tasks: bool = False) -> ExtendedRun:
        with self.create_http_session() as session:
            response = session.get(urljoin(self.endpoint.url, f'{self.namespace}/ga4gh/wes/v1/runs/{run_id}'
                                                              f'?exclude_tasks={not include_tasks}'))
            return ExtendedRun(**response.json())

    def cancel_run(self, run_id: str) -> Union[RunId, WorkbenchApiError]:
        with self.create_http_session() as session:
            response = session.post(urljoin(self.endpoint.url, f'{self.namespace}/ga4gh/wes/v1/runs/{run_id}/cancel'))
            return RunId(**response.json())

    def cancel_runs(self, run_ids: List[str]) -> BatchActionResult:
        with self.create_http_session() as session:
            response = session.post(urljoin(self.endpoint.url, f'{self.namespace}/ga4gh/wes/v1/runs/cancel'),
                                    json=run_ids)
            return BatchActionResult(**response.json())

    def delete_runs(self, run_ids: List[str]) -> BatchActionResult:
        with self.create_http_session() as session:
            response = session.post(urljoin(self.endpoint.url, f'{self.namespace}/ga4gh/wes/v1/runs/delete'),
                                    json=run_ids)
            return BatchActionResult(**response.json())

    def submit_run(self, data: ExtendedRunRequest) -> MinimalExtendedRun:
        with self.create_http_session() as session:
            response = session.post(urljoin(self.endpoint.url, f'{self.namespace}/ga4gh/wes/v1/runs'),
                                    json=data.dict())
        return MinimalExtendedRun(**response.json())

    def submit_batch(self, data: BatchRunRequest) -> MinimalBatch:
        with self.create_http_session() as session:
            response = session.post(urljoin(self.endpoint.url, f'{self.namespace}/ga4gh/wes/v1/batch'),
                                    json=data.dict())
        return MinimalBatch(**response.json())

    def stream_run_logs(self, log_url: str, max_bytes: Optional[int]) -> Iterable[bytes]:
        full_log_url = log_url
        if max_bytes:
            full_log_url = f'{full_log_url}&max={max_bytes}'

        with self.create_http_session() as session:
            with session.get(urljoin(self.endpoint.url, full_log_url), stream=True) as response:
                if int(response.headers['Content-Length']) == 0:
                    yield None
                    return
                for chunk in response.iter_content(chunk_size=None):
                    yield chunk
