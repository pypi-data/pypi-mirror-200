import pytest

try:
    from django.conf import settings
except ImportError:
    pytest.skip()

from django.http import HttpResponse, HttpResponseRedirect
from django.test import RequestFactory

from unpoly.contrib.django import UnpolyMiddleware

settings.configure()


def get_response(request):
    return HttpResponse("")


@pytest.fixture
def mw():
    return UnpolyMiddleware(get_response)


@pytest.fixture
def factory():
    return RequestFactory()


def test_django_middleware_headers(mw, factory):
    req = factory.get("/test", HTTP_X_UP_VERSION="2.2.1")
    response = mw(req)
    assert response.headers["X-Up-Method"] == "GET"
    assert "X-Up-Location" not in response.headers


def test_django_up_cookie(mw, factory):
    # Setting the cookie
    req = factory.post("/test")
    response = mw(req)
    assert response.cookies["_up_method"].value == "POST"

    # Deleting the cookie if set
    req = factory.get("/test", HTTP_COOKIE="_up_method=POST", HTTP_X_UP_VERSION="2.2.1")
    response = mw(req)
    assert response.cookies["_up_method"].value == ""

    # Not doing anything
    req = factory.get("/test", HTTP_X_UP_VERSION="2.2.1")
    response = mw(req)
    assert "_up_method" not in response.cookies


def test_django_redirect_up_params(factory):
    def get_response(request):
        request.up.set_title("Testing")
        return HttpResponseRedirect("/redirect?test=abc")

    mw = UnpolyMiddleware(get_response)

    req = factory.get("/test", HTTP_X_UP_VERSION="2.2.1")
    response = mw(req)
    assert response.headers["Location"] == "/redirect?test=abc&_up_title=Testing"
