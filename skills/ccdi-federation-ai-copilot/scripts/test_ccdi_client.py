"""Tests for ccdi_client.py."""

import json
import unittest
from io import BytesIO
from urllib.parse import parse_qs, urlparse

from ccdi_client import build_request_url, read_only_get

BASE_URL = 'https://federation-stage.ccdi.cancer.gov/api/v1/'
SUBJECT_PATH = '/subject'


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class _FakeResponse:
    """Minimal file-like object that mimics :class:`http.client.HTTPResponse`."""

    def __init__(self, body: dict, status: int = 200):
        self._data = BytesIO(json.dumps(body).encode())
        self.status = status
        self.headers = {}

    def read(self) -> bytes:
        return self._data.read()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass


def _make_urlopen(body: dict, status: int = 200):
    """Return a fake *urlopen* that captures the requested URL and returns *body*."""
    captured = {}

    def _urlopen(url, **kwargs):
        captured['url'] = url
        return _FakeResponse(body, status)

    return _urlopen, captured


def _query_params(url: str) -> dict:
    """Parse query string from *url* into a ``{key: [value, …]}`` dict."""
    return parse_qs(urlparse(url).query)


# ---------------------------------------------------------------------------
# build_request_url
# ---------------------------------------------------------------------------

class TestBuildRequestUrl(unittest.TestCase):
    def test_no_params(self):
        url = build_request_url(BASE_URL, SUBJECT_PATH)
        self.assertEqual(url, 'https://federation-stage.ccdi.cancer.gov/api/v1/subject')

    def test_with_params(self):
        url = build_request_url(BASE_URL, SUBJECT_PATH, {'sex': 'F'})
        self.assertIn('sex=F', url)

    def test_trailing_slash_stripped(self):
        url = build_request_url('https://example.com/api/v1/', '/subject')
        self.assertTrue(url.startswith('https://example.com/api/v1/subject'))


# ---------------------------------------------------------------------------
# read_only_get request params
# ---------------------------------------------------------------------------

class TestReadOnlyGetRequestParams(unittest.TestCase):
    def test_none_params_produces_no_query_string(self):
        urlopen, captured = _make_urlopen({'data': []})
        read_only_get(BASE_URL, SUBJECT_PATH, params=None, urlopen=urlopen)
        self.assertEqual(captured['url'], 'https://federation-stage.ccdi.cancer.gov/api/v1/subject')

    def test_original_params_not_mutated(self):
        original = {'sex': 'F'}
        urlopen, _ = _make_urlopen({'data': []})
        read_only_get(BASE_URL, SUBJECT_PATH, params=original, urlopen=urlopen)
        self.assertEqual(original, {'sex': 'F'})

    def test_supplied_params_are_sent(self):
        urlopen, captured = _make_urlopen({'data': []})
        read_only_get(BASE_URL, SUBJECT_PATH, params={'sex': 'F', 'page': '1'}, urlopen=urlopen)
        qs = _query_params(captured['url'])
        self.assertEqual(qs['sex'], ['F'])
        self.assertEqual(qs['page'], ['1'])


# ---------------------------------------------------------------------------
# Return-value sanity checks
# ---------------------------------------------------------------------------

class TestReadOnlyGetReturnValue(unittest.TestCase):
    def test_successful_response_includes_request_url(self):
        urlopen, _ = _make_urlopen({'data': [{'id': '1'}]})
        result = read_only_get(BASE_URL, SUBJECT_PATH, urlopen=urlopen)
        self.assertTrue(result['ok'])
        self.assertEqual(result['url'], 'https://federation-stage.ccdi.cancer.gov/api/v1/subject')

    def test_network_error_includes_request_url(self):
        def _failing_urlopen(url, timeout=30):
            raise OSError('connection refused')

        result = read_only_get(BASE_URL, SUBJECT_PATH, urlopen=_failing_urlopen)
        self.assertFalse(result['ok'])
        self.assertEqual(result['url'], 'https://federation-stage.ccdi.cancer.gov/api/v1/subject')


if __name__ == '__main__':
    unittest.main()
