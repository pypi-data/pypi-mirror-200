from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any

from pydantic import BaseModel

from dnastack.client.service_registry.models import Service


class WesServiceInfo(Service):
    workflow_type_versions: Optional[Dict]
    supported_wes_versions: Optional[List[str]]
    supported_filesystem_protocols: Optional[List[str]]
    workflow_engine_versions: Optional[Dict]
    default_workflow_engine_parameters: Optional[List[Dict]]
    system_state_counts: Optional[Dict]
    auth_instructions_url: Optional[str]
    tags: Optional[Dict]


class Pagination(BaseModel):
    next_page_url: Optional[str]
    total_elements: Optional[int]


class ExtendedRunStatus(BaseModel):
    batch_id: Optional[str]
    run_id: str
    batch_index: Optional[int]
    state: str
    start_time: datetime
    end_time: Optional[datetime]
    submitted_by: Optional[str]
    workflow_url: Optional[str]
    workflow_name: Optional[str]
    workflow_version: Optional[str]
    workflow_authors: Optional[List[str]]
    workflow_type: Optional[str]
    workflow_type_version: Optional[str]
    workflow_params: Optional[Dict]
    tags: Optional[Dict]
    workflow_engine_parameters: Optional[Dict]


class ExtendedRunListResponse(BaseModel):
    runs: List[ExtendedRunStatus]
    pagination: Optional[Pagination]
    next_page_token: Optional[str]


class ExtendedRunListOptions(BaseModel):
    page_token: Optional[str]
    page: Optional[int]
    page_size: Optional[int]
    expand: Optional[bool]
    until: Optional[str]
    since: Optional[str]
    search: Optional[str]
    order: Optional[str]
    direction: Optional[str]
    batchId: Optional[str]
    state: Optional[List[str]]
    engineId: Optional[str]
    submittedBy: Optional[str]
    workflowName: Optional[str]
    workflowVersion: Optional[str]
    workflowUrl: Optional[str]
    workflowType: Optional[str]
    workflowTypeVersion: Optional[str]


class ExtendedRunRequest(BaseModel):
    workflow_url: Optional[str]
    batch_index: Optional[int]
    workflow_name: Optional[str]
    workflow_version: Optional[str]
    workflow_authors: Optional[List[str]]
    workflow_type: Optional[str]
    workflow_type_version: Optional[str]
    workflow_id: Optional[str]
    workflow_version_id: Optional[str]
    submitted_by: Optional[str]
    workflow_params: Optional[Dict]
    tags: Optional[Dict]
    workflow_engine_parameters: Optional[Dict]


class Log(BaseModel):
    name: str
    pretty_name: Optional[str]
    cmd: Optional[Any]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    stdout: Optional[str]
    stderr: Optional[str]
    exit_code: Optional[int]
    state: Optional[str]


class ExtendedRun(BaseModel):
    batch_id: Optional[str]
    run_id: str
    external_id: Optional[str]
    engine_id: Optional[str]
    request: Optional[ExtendedRunRequest]
    state: Optional[str]
    run_log: Optional[Log]
    task_logs: Optional[List[Log]]
    task_logs_url: Optional[str]
    outputs: Optional[Dict]


class MinimalExtendedRun(BaseModel):
    run_id: str
    state: str


class MinimalExtendedRunWithInputs(BaseModel):
    run_id: str
    inputs: Optional[Dict]


class MinimalExtendedRunWithOutputs(BaseModel):
    run_id: str
    outputs: Optional[Dict]


class BatchRunRequest(BaseModel):
    workflow_url: str
    workflow_type: Optional[str]
    workflow_type_version: Optional[str]
    engine_id: Optional[str]
    default_workflow_params: Optional[Dict]
    default_workflow_engine_parameters: Optional[Dict]
    default_tags: Optional[Dict]
    run_requests: Optional[List[ExtendedRunRequest]]


class MinimalBatch(BaseModel):
    batch_id: str
    runs: List[MinimalExtendedRun]


class RunId(BaseModel):
    run_id: str
    state: Optional[str]


class WorkbenchApiError(BaseModel):
    timestamp: str
    msg: str
    error_code: int
    trace_id: str


class BatchActionResult(BaseModel):
    run_ids_with_success: Optional[List[str]]
    run_ids_with_failure: Optional[List[str]]


class LogType(str, Enum):
    stdout = 'stdout',
    stderr = 'stderr',
