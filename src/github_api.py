import hashlib
import hmac
import re

import httpx

from src.config import Config


def verify_signature(payload: str, secret: str, signature: str) -> bool:
    """Проверяет подпись от GitHub."""
    hmac_obj = hmac.new(secret.encode(), payload.encode(), hashlib.sha256)
    digest = hmac_obj.hexdigest()
    expected_signature = f"sha256={digest}"
    return hmac.compare_digest(expected_signature, signature)


def deploy_workflow_dispatch(ref: str):
    httpx.post(
        url=f"https://api.github.com/repos/{Config.gh_owner}/{Config.gh_repo}/actions/workflows/{Config.gh_workflow_deploy}/dispatches",
        data={"ref": ref},
        headers={
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {Config.gh_token}",
        },
    )


def get_delivered_version_from_build_and_push(job_id: int) -> str | None:
    response = httpx.get(
        url=f"https://api.github.com/repos/{Config.gh_owner}/{Config.gh_repo}/actions/jobs/{job_id}/logs",
        headers={
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {Config.gh_token}",
        },
    )
    response.raise_for_status()

    logs_text = response.text

    # Ищем с конца логов
    for line in reversed(logs_text.splitlines()):
        if "VERSION=" in line:
            match = re.search(r'VERSION="([^"]+)"', line)
            if match:
                return match.group(1)

    return None
