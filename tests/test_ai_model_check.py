"""Offline validation of the configured pydantic-ai model identifier."""

import pytest

from races.checks import check_pydantic_ai_model, resolve_model

SETTINGS_DEFAULT = "openai-responses:gpt-5.6-luna"


def ids(settings, identifier):
    settings.PYDANTIC_AI_MODEL = identifier
    return {w.id for w in check_pydantic_ai_model(None)}


def test_check_passes_for_configured_model():
    assert check_pydantic_ai_model(None) == []


def test_settings_default_is_accepted(settings):
    assert ids(settings, SETTINGS_DEFAULT) == set()


def test_settings_default_is_responses_model():
    from config import settings as project_settings

    # The default (when PYDANTIC_AI_MODEL isn't set in the environment) stays on the Responses API.
    assert 'default="openai-responses:' in open(project_settings.__file__).read()
    assert type(resolve_model(SETTINGS_DEFAULT)).__name__ == "OpenAIResponsesModel"


@pytest.mark.parametrize(
    "identifier",
    [
        "openai-chat:gpt-5.4-nano",
        "openai-responses:gpt-5.4-nano",
        "openai:gpt-5.4-nano",
        # colons inside the model name are fine; only the first colon splits provider from model
        "openai-chat:meta-llama/llama-3:free",
        "openai-chat:anthropic.claude-v1:0",
        # providers not in _PROVIDER_ENV_KEYS aren't resolved, so a missing key doesn't warn
        "openrouter:meta-llama/llama-3:free",
        "deepseek:deepseek-chat",
        "grok:grok-4",
        "gateway/openai:gpt-5",
    ],
)
def test_check_accepts_valid_identifiers(settings, identifier):
    assert ids(settings, identifier) == set()


@pytest.mark.parametrize(
    ("identifier", "expected_ids"),
    [
        ("openai-chat:openai-chat:gpt-5.4-nano", {"ai.W001"}),
        ("openai-responses:openai-chat:gpt-5.4-nano", {"ai.W001"}),
        ("ollama:ollama:llama3", {"ai.W001"}),
        ("openai-chat:", {"ai.W004"}),
        ("ollama:", {"ai.W004"}),
        ("gpt-5.4-nano", {"ai.W003"}),
        ("", {"ai.W003"}),
        ("nonsense-provider:gpt-5.4-nano", set()),
    ],
)
def test_check_flags_bad_identifiers(settings, identifier, expected_ids):
    assert ids(settings, identifier) == expected_ids


def test_check_only_warns_never_errors(settings):
    from django.core.checks import Warning

    settings.PYDANTIC_AI_MODEL = "openai-chat:openai-chat:x"
    assert all(type(w) is Warning for w in check_pydantic_ai_model(None))


def test_check_does_not_touch_process_environment(settings, monkeypatch):
    import os

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    settings.PYDANTIC_AI_MODEL = SETTINGS_DEFAULT
    assert check_pydantic_ai_model(None) == []
    assert "OPENAI_API_KEY" not in os.environ
