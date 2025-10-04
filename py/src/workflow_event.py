class Workflow:
    def __init__(
        self, workflow_id, name, head_branch, status, conclusion, actor, event, url
    ):
        self.workflow_id = workflow_id
        self.name = name
        self.head_branch = head_branch
        self.status = status
        self.conclusion = conclusion
        self.actor = actor
        self.event = event
        self.url = url


class WorkflowFailed:
    def __init__(self, workflow, reason):
        self.workflow = workflow
        self.reason = reason


class WorkflowSuccess:
    def __init__(self, workflow):
        self.workflow = workflow


class DeliverySuccess:
    def __init__(self, workflow):
        self.workflow = workflow


def event_from_workflow_run(workflow_run: dict) -> object | None:
    if (
        workflow_run["status"] != "completed"
        and workflow_run["conclusion"] != "success"
        and workflow_run["conclusion"] != "failed"
    ):
        return None
