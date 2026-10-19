import os

from django.core.checks import Warning, register

from .agents import _build_model_identifier

# Providers whose API key env var is known here. Only these are resolved (with a placeholder key if the
# real one isn't set, since constructing the provider needs one; no request is ever made). Other
# providers (openrouter, deepseek, gateway/..., etc.) only get the string checks.
_PROVIDER_ENV_KEYS = {
    "openai": "OPENAI_API_KEY",
    "openai-chat": "OPENAI_API_KEY",
    "openai-responses": "OPENAI_API_KEY",
}
_OPENAI_PROVIDERS = frozenset(_PROVIDER_ENV_KEYS)
_ACCEPTED_MODEL_CLASSES = {"OpenAIChatModel", "OpenAIResponsesModel"}


def _provider_factory(provider_name):
    from pydantic_ai.providers import infer_provider
    from pydantic_ai.providers.openai import OpenAIProvider

    env_key = _PROVIDER_ENV_KEYS.get(provider_name)
    if env_key is None:
        return infer_provider(provider_name)
    return OpenAIProvider(api_key=os.environ.get(env_key) or "check-only")


def resolve_model(identifier=None):
    """Resolve a known-provider model identifier like the app does, without any network access."""
    from pydantic_ai.models import infer_model

    return infer_model(identifier or _build_model_identifier(), provider_factory=_provider_factory)


@register()
def check_pydantic_ai_model(app_configs, **kwargs):
    """Warn about a misconfigured ``PYDANTIC_AI_MODEL``.

    These are warnings, not errors, so a bad value never blocks ``migrate``, ``runserver`` or the start
    scripts. CI runs ``manage.py check --fail-level WARNING`` to still fail the build.
    """
    identifier = _build_model_identifier()
    provider, sep, name = identifier.partition(":")  # only the first colon separates provider from model
    hint = "Expected `PYDANTIC_AI_MODEL` as `provider:model_name`"

    if not sep:
        return [Warning(f"{hint}, got {identifier!r}", id="ai.W003")]

    warnings = []
    if not name:
        warnings.append(Warning(f"Model name is empty in {identifier!r}. {hint}", id="ai.W004"))
    else:
        head = name.partition(":")[0]
        if head == provider or (head in _OPENAI_PROVIDERS and provider in _OPENAI_PROVIDERS):
            warnings.append(
                Warning(
                    f"Model name {name!r} still contains a provider prefix (doubled prefix in {identifier!r}). {hint}",
                    id="ai.W001",
                )
            )
    if warnings or provider not in _PROVIDER_ENV_KEYS:
        return warnings

    try:
        model = resolve_model(identifier)
    except Exception as e:
        return [Warning(f"Could not resolve pydantic-ai model {identifier!r}: {e}", id="ai.W002")]

    cls = type(model).__name__
    if cls not in _ACCEPTED_MODEL_CLASSES:
        warnings.append(
            Warning(
                f"Expected an OpenAI chat or responses model, got {cls}; check the prefix in `PYDANTIC_AI_MODEL`",
                id="ai.W005",
            )
        )
    return warnings
