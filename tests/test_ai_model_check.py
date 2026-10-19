"""Offline validation of the configured pydantic-ai model identifier."""

import pytest

from races.checks import check_pydantic_ai_model, resolve_model


def test_model_identifier_resolves_without_prefix_leak():
    model = resolve_model()
    assert ":" not in model.model_name
    assert type(model).__name__ == "OpenAIChatModel"


def test_check_passes_for_default_model():
    assert check_pydantic_ai_model(None) == []


@pytest.mark.parametrize(
    ("identifier", "expected_ids"),
    [
        ("openai-chat:openai-chat:gpt-5.4-nano", {"ai.E001"}),
        ("openai:gpt-5.4-nano", {"ai.E002"}),
        ("openai-responses:gpt-5.4-nano", {"ai.E002"}),
        ("nonsense-provider:gpt-5.4-nano", {"ai.E003"}),
    ],
)
def test_check_flags_bad_model_identifiers(settings, identifier, expected_ids):
    settings.PYDANTIC_AI_MODEL = identifier
    assert {e.id for e in check_pydantic_ai_model(None)} == expected_ids
