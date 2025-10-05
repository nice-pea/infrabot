import hashlib
import hmac

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
