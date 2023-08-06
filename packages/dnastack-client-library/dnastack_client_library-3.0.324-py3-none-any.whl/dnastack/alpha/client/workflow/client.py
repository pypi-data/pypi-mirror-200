from typing import List
from urllib.parse import urljoin

from dnastack.alpha.client.workflow.models import WorkflowDescriptor, WorkflowListResult, Workflow, WorkflowCreate, \
    WorkflowVersionCreate, WorkflowVersion
from dnastack.alpha.client.workbench.base_client import BaseWorkbenchClient
from dnastack.client.models import ServiceEndpoint
from dnastack.client.service_registry.models import ServiceType


class WorkflowClient(BaseWorkbenchClient):

    @staticmethod
    def get_adapter_type() -> str:
        return 'workflow-service'

    @staticmethod
    def get_supported_service_types() -> List[ServiceType]:
        return [
            ServiceType(group='com.dnastack.workbench', artifact='workflow-service', version='1.0.0'),
        ]

    @classmethod
    def make(cls, endpoint: ServiceEndpoint, namespace: str):
        """Create this class with the given `endpoint` and `namespace`."""
        if not endpoint.type:
            endpoint.type = cls.get_default_service_type()
        return cls(endpoint, namespace)

    def get_json_schema(self, workflow_id: str, version_id: str) -> WorkflowDescriptor:
        with self.create_http_session() as session:
            response = session.get(
                urljoin(self.endpoint.url, f'{self.namespace}/workflows/{workflow_id}/versions/{version_id}/describe'))
        return WorkflowDescriptor(**response.json())

    def list_workflows(self) -> WorkflowListResult:
        with self.create_http_session() as session:
            response = session.get(
                urljoin(self.endpoint.url, f'{self.namespace}/workflows'))
        return WorkflowListResult(**response.json())

    def get_workflow(self, workflow_id: str) -> Workflow:
        with self.create_http_session() as session:
            response = session.get(
                urljoin(self.endpoint.url, f'{self.namespace}/workflows/{workflow_id}'))
        return Workflow(**response.json())

    def create_workflow(self, workflow_create_request: WorkflowCreate) -> Workflow:
        with self.create_http_session() as session:
            response = session.post(
                urljoin(self.endpoint.url, f'{self.namespace}/workflows'), json=workflow_create_request.dict())
        return Workflow(**response.json())

    def create_version(self, workflow_id: str, workflow_version_create_request: WorkflowVersionCreate) -> WorkflowVersion:
        with self.create_http_session() as session:
            response = session.post(
                urljoin(self.endpoint.url, f'{self.namespace}/workflows/{workflow_id}/versions'),
                json=workflow_version_create_request.dict())
        return WorkflowVersion(**response.json())
