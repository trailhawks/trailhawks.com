"""Smoke tests for every admin view of our first-party apps.

For each model registered in the admin whose app lives in this repo (i.e. not a
third-party package under site-packages), we exercise the changelist, add, and
change views as a superuser and assert none of them return a server error.

Crucially, the changelist/change tests create a real instance with model_bakery
first, so per-row ``list_display`` callables actually run. That is what catches
bugs like ``format_html()`` being called without format args, which only blows
up when a row is rendered -- an empty changelist would pass right over it.
"""

from __future__ import annotations

import uuid

import pytest
from django.conf import settings
from django.contrib import admin
from django.db.models import CharField, SlugField
from django.urls import reverse
from model_bakery import baker
from model_bakery import generators


@pytest.fixture(autouse=True)
def _short_char_values():
    """Make model_bakery generate short CharField/SlugField values.

    By default model_bakery fills a CharField to its full ``max_length``. Some
    models derive a shorter column inside ``save()`` (e.g. Location does
    ``slug = slugify(name)`` into a 50-char SlugField), so a 250-char name
    overflows. Short values keep every model saveable.
    """

    def gen_short(max_length=8, **kwargs):
        return uuid.uuid4().hex[: min(max_length or 8, 8)]

    generators.add("django.db.models.CharField", gen_short)
    generators.add("django.db.models.SlugField", gen_short)
    try:
        yield
    finally:
        generators.user_mapping.pop(CharField, None)
        generators.user_mapping.pop(SlugField, None)


def _first_party_models():
    base = str(settings.BASE_DIR)
    models = []
    for model in admin.site._registry:
        path = getattr(model._meta.app_config, "path", "") or ""
        if path.startswith(base) and "site-packages" not in path and "/.venv/" not in path:
            models.append(model)
    return sorted(models, key=lambda m: (m._meta.app_label, m._meta.model_name))


def _model_id(model):
    return f"{model._meta.app_label}.{model._meta.model_name}"


FIRST_PARTY_MODELS = _first_party_models()


def _admin_url(model, view, *args):
    name = f"admin:{model._meta.app_label}_{model._meta.model_name}_{view}"
    return reverse(name, args=args)


def _bake(model):
    """Best-effort instance creation; skip the test if the model can't be baked."""
    try:
        return baker.make(model)
    except Exception as exc:  # noqa: BLE001 - report why baking failed, then skip
        pytest.skip(f"could not build a {_model_id(model)} instance: {exc}")


def _bake_with_children(model):
    """Bake an instance plus one object for each reverse FK pointing at it.

    Some ``list_display`` callables only render (and only blow up) when related
    rows exist -- e.g. RaceAdmin.download_csv_results renders a link only when
    ``race.result_set.exists()``. Populating reverse relations makes the
    changelist exercise those conditional branches.
    """
    obj = _bake(model)
    for rel in model._meta.related_objects:
        if not (rel.one_to_many or rel.one_to_one):
            continue
        try:
            baker.make(rel.related_model, **{rel.field.name: obj})
        except Exception:  # noqa: BLE001 - children are best-effort extra coverage
            continue
    for m2m in model._meta.many_to_many:
        try:
            getattr(obj, m2m.name).add(baker.make(m2m.related_model))
        except Exception:  # noqa: BLE001 - best-effort extra coverage
            continue
    return obj


def test_admin_registry_is_not_empty():
    # Guard against the discovery silently finding nothing (e.g. autodiscover not run).
    assert FIRST_PARTY_MODELS, "no first-party admin models were discovered"


@pytest.mark.parametrize("model", FIRST_PARTY_MODELS, ids=_model_id)
def test_admin_changelist(admin_client, model, db):
    _bake_with_children(model)  # a row + related rows so per-row columns fully render
    response = admin_client.get(_admin_url(model, "changelist"))
    assert response.status_code == 200


@pytest.mark.parametrize("model", FIRST_PARTY_MODELS, ids=_model_id)
def test_admin_add(admin_client, model, db):
    response = admin_client.get(_admin_url(model, "add"))
    # 403 is acceptable for models that intentionally forbid adding.
    assert response.status_code in (200, 403)


@pytest.mark.parametrize("model", FIRST_PARTY_MODELS, ids=_model_id)
def test_admin_change(admin_client, model, db):
    obj = _bake(model)
    response = admin_client.get(_admin_url(model, "change", obj.pk))
    assert response.status_code == 200
