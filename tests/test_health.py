"""/health/ and /version.txt under both sites' urlconfs.

The container health check curls http://localhost:8000/health/ and needs a
real 200; trailhawks.com and hawkhundred.com run the same image with
different ROOT_URLCONFs.
"""

import pytest

from config import __version__

URLCONFS = ["config.urls", "config.urls_hawkhundred"]


@pytest.mark.django_db
@pytest.mark.parametrize("urlconf", URLCONFS)
def test_health_returns_200(client, settings, urlconf):
    settings.ROOT_URLCONF = urlconf
    settings.ALLOWED_HOSTS = ["localhost"]
    settings.DEBUG = False
    response = client.get("/health/", HTTP_HOST="localhost")
    assert response.status_code == 200


@pytest.mark.parametrize("urlconf", URLCONFS)
def test_version_txt(client, settings, urlconf):
    settings.ROOT_URLCONF = urlconf
    settings.ALLOWED_HOSTS = ["localhost"]
    response = client.get("/version.txt", HTTP_HOST="localhost")
    assert response.status_code == 200
    assert response.content.decode() == __version__
