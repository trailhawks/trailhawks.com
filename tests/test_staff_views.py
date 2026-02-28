from datetime import datetime, timezone as dt_timezone

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from races.models import Race
from runs.models import Run


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(username="staff", password="testpass", is_staff=True)


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(username="regular", password="testpass", is_staff=False)


@pytest.fixture
def staff_client(staff_user):
    client = Client()
    client.login(username="staff", password="testpass")
    return client


@pytest.fixture
def regular_client(regular_user):
    client = Client()
    client.login(username="regular", password="testpass")
    return client


@pytest.fixture
def race(db):
    return Race.objects.create(
        title="Test Trail Race",
        slug="test-trail-race",
        start_datetime=timezone.now(),
        active=True,
        race_type=1,
    )


@pytest.fixture
def inactive_race(db):
    return Race.objects.create(
        title="Old Race",
        slug="old-race",
        start_datetime=datetime(2020, 6, 1, tzinfo=dt_timezone.utc),
        active=False,
        race_type=1,
    )


@pytest.fixture
def run(db):
    return Run.objects.create(
        name="Monday Trail Run",
        slug="monday-trail-run",
        run_time="6:30 PM",
        details="Weekly group run",
        day_of_week=0,
        active=True,
    )


# -- Dashboard --


class TestStaffDashboard:
    def test_staff_can_access(self, staff_client):
        response = staff_client.get(reverse("staff:dashboard"))
        assert response.status_code == 200

    def test_anonymous_redirected(self, client):
        response = client.get(reverse("staff:dashboard"))
        assert response.status_code == 302

    def test_non_staff_forbidden(self, regular_client):
        response = regular_client.get(reverse("staff:dashboard"))
        assert response.status_code == 403


# -- Race CRUD --


class TestRaceList:
    def test_staff_can_access(self, staff_client, race):
        response = staff_client.get(reverse("staff:race-list"))
        assert response.status_code == 200
        assert b"Test Trail Race" in response.content

    def test_anonymous_redirected(self, client):
        response = client.get(reverse("staff:race-list"))
        assert response.status_code == 302

    def test_non_staff_forbidden(self, regular_client):
        response = regular_client.get(reverse("staff:race-list"))
        assert response.status_code == 403

    def test_search_filters_results(self, staff_client, race, inactive_race):
        response = staff_client.get(reverse("staff:race-list"), {"q": "Test Trail"})
        assert response.status_code == 200
        assert b"Test Trail Race" in response.content
        assert b"Old Race" not in response.content

    def test_search_no_results(self, staff_client, race):
        response = staff_client.get(reverse("staff:race-list"), {"q": "nonexistent"})
        assert response.status_code == 200
        assert b"No races found" in response.content

    def test_filter_by_active(self, staff_client, race, inactive_race):
        response = staff_client.get(reverse("staff:race-list"), {"active": "true"})
        assert response.status_code == 200
        assert b"Test Trail Race" in response.content
        assert b"Old Race" not in response.content

    def test_filter_by_year(self, staff_client, race, inactive_race):
        response = staff_client.get(reverse("staff:race-list"), {"year": "2020"})
        assert response.status_code == 200
        assert b"Old Race" in response.content
        assert b"Test Trail Race" not in response.content

    def test_htmx_returns_partial(self, staff_client, race):
        response = staff_client.get(
            reverse("staff:race-list"),
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        # Partial should not contain the full page layout
        assert b"<!DOCTYPE html>" not in response.content
        assert b"Test Trail Race" in response.content

    def test_context_has_row_urls(self, staff_client, race):
        response = staff_client.get(reverse("staff:race-list"))
        rows = response.context["object_rows"]
        assert len(rows) == 1
        row = rows[0]
        assert "detail_url" in row
        assert "edit_url" in row
        assert "agent_url" in row
        assert "chat_url" in row


class TestRaceDetail:
    def test_staff_can_access(self, staff_client, race):
        response = staff_client.get(reverse("staff:race-detail", kwargs={"pk": race.pk}))
        assert response.status_code == 200

    def test_anonymous_redirected(self, client, race):
        response = client.get(reverse("staff:race-detail", kwargs={"pk": race.pk}))
        assert response.status_code == 302


class TestRaceCreate:
    def test_staff_can_access_form(self, staff_client):
        response = staff_client.get(reverse("staff:race-create"))
        assert response.status_code == 200

    def test_staff_can_create(self, staff_client):
        response = staff_client.post(
            reverse("staff:race-create"),
            {
                "title": "New Race",
                "slug": "new-race",
                "start_datetime": "2026-06-01 08:00:00",
                "active": True,
                "race_type": 1,
            },
        )
        assert response.status_code == 302
        assert Race.objects.filter(title="New Race").exists()


class TestRaceUpdate:
    def test_staff_can_access_form(self, staff_client, race):
        response = staff_client.get(reverse("staff:race-update", kwargs={"pk": race.pk}))
        assert response.status_code == 200

    def test_staff_can_update(self, staff_client, race):
        response = staff_client.post(
            reverse("staff:race-update", kwargs={"pk": race.pk}),
            {
                "title": "Updated Race",
                "slug": "test-trail-race",
                "start_datetime": "2026-06-01 08:00:00",
                "active": True,
                "race_type": 1,
            },
        )
        assert response.status_code == 302
        race.refresh_from_db()
        assert race.title == "Updated Race"


# -- Run CRUD --


class TestRunList:
    def test_staff_can_access(self, staff_client, run):
        response = staff_client.get(reverse("staff:run-list"))
        assert response.status_code == 200
        assert b"Monday Trail Run" in response.content

    def test_anonymous_redirected(self, client):
        response = client.get(reverse("staff:run-list"))
        assert response.status_code == 302

    def test_non_staff_forbidden(self, regular_client):
        response = regular_client.get(reverse("staff:run-list"))
        assert response.status_code == 403

    def test_search_filters_results(self, staff_client, run):
        response = staff_client.get(reverse("staff:run-list"), {"q": "Monday"})
        assert response.status_code == 200
        assert b"Monday Trail Run" in response.content

    def test_search_no_results(self, staff_client, run):
        response = staff_client.get(reverse("staff:run-list"), {"q": "nonexistent"})
        assert response.status_code == 200
        assert b"No runs found" in response.content

    def test_filter_by_active(self, staff_client, run):
        response = staff_client.get(reverse("staff:run-list"), {"active": "true"})
        assert response.status_code == 200
        assert b"Monday Trail Run" in response.content

    def test_htmx_returns_partial(self, staff_client, run):
        response = staff_client.get(
            reverse("staff:run-list"),
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        assert b"<!DOCTYPE html>" not in response.content
        assert b"Monday Trail Run" in response.content


class TestRunDetail:
    def test_staff_can_access(self, staff_client, run):
        response = staff_client.get(reverse("staff:run-detail", kwargs={"pk": run.pk}))
        assert response.status_code == 200

    def test_anonymous_redirected(self, client, run):
        response = client.get(reverse("staff:run-detail", kwargs={"pk": run.pk}))
        assert response.status_code == 302


class TestRunCreate:
    def test_staff_can_access_form(self, staff_client):
        response = staff_client.get(reverse("staff:run-create"))
        assert response.status_code == 200

    def test_staff_can_create(self, staff_client):
        response = staff_client.post(
            reverse("staff:run-create"),
            {
                "name": "New Run",
                "slug": "new-run",
                "run_time": "7:00 AM",
                "details": "A new group run",
                "day_of_week": 2,
                "active": True,
            },
        )
        assert response.status_code == 302
        assert Run.objects.filter(name="New Run").exists()


class TestRunUpdate:
    def test_staff_can_access_form(self, staff_client, run):
        response = staff_client.get(reverse("staff:run-update", kwargs={"pk": run.pk}))
        assert response.status_code == 200

    def test_staff_can_update(self, staff_client, run):
        response = staff_client.post(
            reverse("staff:run-update", kwargs={"pk": run.pk}),
            {
                "name": "Updated Run",
                "slug": "monday-trail-run",
                "run_time": "6:30 PM",
                "details": "Updated details",
                "day_of_week": 0,
                "active": True,
            },
        )
        assert response.status_code == 302
        run.refresh_from_db()
        assert run.name == "Updated Run"
