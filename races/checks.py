import os
from unittest import mock

from django.core.checks import Error, register

from .agents import _build_model_identifier


def resolve_model():
    """Resolve the configured pydantic-ai model exactly like the app does, without any network access.

    Constructing the OpenAI provider requires an API key to be present, but no request is ever made,
    so a placeholder is supplied when the real one isn't set (e.g. in CI).
    """
    from pydantic_ai import Agent

    with mock.patch.dict(os.environ, {"OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY") or "check-only"}):
        return Agent(_build_model_identifier()).model


@register()
def check_pydantic_ai_model(app_configs, **kwargs):
    errors = []
    try:
        model = resolve_model()
    except Exception as e:
        return [Error(f"Could not resolve pydantic-ai model {_build_model_identifier()!r}: {e}", id="ai.E003")]

    name = model.model_name
    cls = type(model).__name__
    if ":" in name:
        errors.append(
            Error(
                f"Model name still contains a provider prefix: {name!r} "
                "(double-prefix / misconfigured `PYDANTIC_AI_MODEL`)",
                id="ai.E001",
            )
        )
    if cls != "OpenAIChatModel":
        errors.append(
            Error(
                f"Expected OpenAIChatModel (Chat Completions), got {cls} "
                "— check the model prefix in `PYDANTIC_AI_MODEL` (use `openai-chat:`)",
                id="ai.E002",
            )
        )
    return errors
