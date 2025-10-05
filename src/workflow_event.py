from dataclasses import dataclass
from typing import Union, Optional

from src.github_api import get_delivered_version_from_build_and_push


@dataclass
class Workflow:
    id: int
    name: str
    head_branch: str
    status: str
    conclusion: str
    actor: str
    event: str
    url: str


@dataclass
class WorkflowJob:
    id: int
    name: str
    status: str
    conclusion: str
    run_id: str
    workflow_name: str


@dataclass
class WorkflowFailed:
    workflow: Workflow


@dataclass
class WorkflowSuccess:
    workflow: Workflow


@dataclass
class DeliveryJobSuccess:
    job: WorkflowJob
    tag: str


type Event = Union[
    WorkflowFailed,
    WorkflowSuccess,
    DeliveryJobSuccess,
]


def event_from_gh_event(gh_event: dict) -> Optional[Event]:
    action = gh_event["action"]
    if action != "completed":
        return None

    workflow_job = gh_event.get("workflow_job")
    if workflow_job:
        job = WorkflowJob(
            id=workflow_job["id"],
            name=workflow_job["name"],
            status=workflow_job["status"],
            conclusion=workflow_job["conclusion"],
            run_id=workflow_job["run_id"],
            workflow_name=workflow_job["workflow_name"],
        )

        if (
            job.workflow_name == "Delivery"
            and job.name == "build_and_push"
            and job.conclusion == "success"
        ):
            return DeliveryJobSuccess(
                job, get_delivered_version_from_build_and_push(job.id)
            )

        return None

    workflow_run = gh_event.get("workflow_run")
    if workflow_run:
        workflow = Workflow(
            id=workflow_run["id"],
            name=workflow_run["name"],
            head_branch=workflow_run["head_branch"],
            status=workflow_run["status"],
            conclusion=workflow_run["conclusion"],
            actor=workflow_run["triggering_actor"]["login"],
            event=workflow_run["event"],
            url=workflow_run["html_url"],
        )

        # Обработка только событий Доставки и Развертывания
        # if workflow.name != "Delivery" and workflow.name != "Deploy":
        #     return None

        if workflow.conclusion == "failure":
            return WorkflowFailed(workflow)
        elif workflow.conclusion == "success":
            return WorkflowSuccess(workflow)

        return None

    return None
