import os
from typing import Any

import httpx
from chaoslib.types import Configuration, Experiment, Journal, Secrets
from logzero import logger

from chaosreliably.controls import find_extension_by_name

__all__ = ["after_experiment_control"]
OPENAI_URL = "https://api.openai.com/v1/chat/completions"


def after_experiment_control(
    context: Experiment,
    state: Journal,
    openai_model: str = "gpt-3.5-turbo",
    configuration: Configuration = None,
    secrets: Secrets = None,
    **kwargs: Any,
) -> None:
    extension = find_extension_by_name(context, "chatgpt")
    if not extension:
        return None

    secrets = secrets or {}
    openapi_secrets = secrets.get("openai", {})

    org = openapi_secrets.get("org") or os.getenv("OPENAI_ORG")
    if not org:
        logger.warning("Cannot call OpenAPI: missing org")
        return None

    key = openapi_secrets.get("key") or os.getenv("OPENAI_API_KEY")
    if not key:
        logger.warning("Cannot call OpenAPI: missing secret key")
        return None

    logger.debug(
        f"Asking OpenAPI for chat completions using model '{openai_model}'"
    )

    messages = extension.get("messages", [])
    try:
        r = httpx.post(
            OPENAI_URL,
            timeout=60,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
                "OpenAI-Organization": org,
            },
            json={
                "model": openai_model,
                "temperature": 0.2,
                "messages": messages,
            },
        )
    except httpx.ReadTimeout:
        logger.debug("OpenAI took too long to respond unfortunately")
    else:
        if r.status_code == 200:
            extension["results"] = r.json()
