"""Tests for ccdi_client.py — request_source and summarized_query parameters."""

import json
import unittest
from contextlib import contextmanager
from io import BytesIO
from urllib.parse import parse_qs, urlparse

from ccdi_client import REQUEST_SOURCE, build_request_url, read_only_get

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
# request_source
# ---------------------------------------------------------------------------

class TestRequestSourceDefault(unittest.TestCase):
    """request_source=agent_skill is appended by default."""

    def _run(self, extra_params=None):
        urlopen, captured = _make_urlopen({'data': []})
        read_only_get(BASE_URL, SUBJECT_PATH, params=extra_params, urlopen=urlopen)
        return _query_params(captured['url'])

    def test_request_source_present(self):
        qs = self._run()
        self.assertIn('request_source', qs)

    def test_request_source_value_is_agent_skill(self):
        qs = self._run()
        self.assertEqual(qs['request_source'], ['agent_skill'])

    def test_request_source_constant_equals_agent_skill(self):
        self.assertEqual(REQUEST_SOURCE, 'agent_skill')

    def test_request_source_present_alongside_other_params(self):
        qs = self._run(extra_params={'sex': 'F', 'page': '1'})
        self.assertIn('request_source', qs)
        self.assertEqual(qs['request_source'], ['agent_skill'])
        self.assertEqual(qs['sex'], ['F'])

    def test_custom_request_source(self):
        urlopen, captured = _make_urlopen({'data': []})
        read_only_get(BASE_URL, SUBJECT_PATH, urlopen=urlopen, request_source='custom_source')
        qs = _query_params(captured['url'])
        self.assertEqual(qs['request_source'], ['custom_source'])

    def test_original_params_not_mutated(self):
        original = {'sex': 'F'}
        urlopen, _ = _make_urlopen({'data': []})
        read_only_get(BASE_URL, SUBJECT_PATH, params=original, urlopen=urlopen)
        self.assertNotIn('request_source', original)

    def test_none_params_produces_request_source(self):
        """Calling with params=None still appends request_source."""
        urlopen, captured = _make_urlopen({'data': []})
        read_only_get(BASE_URL, SUBJECT_PATH, params=None, urlopen=urlopen)
        qs = _query_params(captured['url'])
        self.assertIn('request_source', qs)


# ---------------------------------------------------------------------------
# summarized_query
# ---------------------------------------------------------------------------

class TestSummarizedQuery(unittest.TestCase):
    """summarized_query is optional, included only when provided, and never contains raw prompts."""

    def test_omitted_by_default(self):
        urlopen, captured = _make_urlopen({'data': []})
        read_only_get(BASE_URL, SUBJECT_PATH, urlopen=urlopen)
        qs = _query_params(captured['url'])
        self.assertNotIn('summarized_query', qs)

    def test_included_when_provided(self):
        urlopen, captured = _make_urlopen({'data': []})
        read_only_get(
            BASE_URL, SUBJECT_PATH, urlopen=urlopen,
            summarized_query='pediatric subjects with osteosarcoma',
        )
        qs = _query_params(captured['url'])
        self.assertIn('summarized_query', qs)
        self.assertEqual(qs['summarized_query'], ['pediatric subjects with osteosarcoma'])

    def test_none_omits_param(self):
        urlopen, captured = _make_urlopen({'data': []})
        read_only_get(BASE_URL, SUBJECT_PATH, urlopen=urlopen, summarized_query=None)
        qs = _query_params(captured['url'])
        self.assertNotIn('summarized_query', qs)

    def test_sanitized_summary_no_pii(self):
        """A properly sanitized value contains no names, emails, or identifiers."""
        sanitized = 'female subjects with diagnosis osteosarcoma'
        self.assertNotIn('@', sanitized)
        self.assertNotIn('John', sanitized)

        urlopen, captured = _make_urlopen({'data': []})
        read_only_get(BASE_URL, SUBJECT_PATH, urlopen=urlopen, summarized_query=sanitized)
        qs = _query_params(captured['url'])
        self.assertEqual(qs['summarized_query'], [sanitized])

    def test_summarized_query_alongside_request_source(self):
        urlopen, captured = _make_urlopen({'data': []})
        read_only_get(
            BASE_URL, SUBJECT_PATH, urlopen=urlopen,
            summarized_query='RNA-seq samples tumor',
        )
        qs = _query_params(captured['url'])
        self.assertIn('request_source', qs)
        self.assertIn('summarized_query', qs)

    def test_summarized_query_alongside_other_params(self):
        urlopen, captured = _make_urlopen({'data': []})
        read_only_get(
            BASE_URL, SUBJECT_PATH,
            params={'sex': 'F'},
            urlopen=urlopen,
            summarized_query='female subjects',
        )
        qs = _query_params(captured['url'])
        self.assertEqual(qs['sex'], ['F'])
        self.assertEqual(qs['summarized_query'], ['female subjects'])
        self.assertEqual(qs['request_source'], ['agent_skill'])


# ---------------------------------------------------------------------------
# Return-value sanity checks
# ---------------------------------------------------------------------------

class TestReadOnlyGetReturnValue(unittest.TestCase):
    def test_successful_response_includes_url_with_request_source(self):
        urlopen, _ = _make_urlopen({'data': [{'id': '1'}]})
        result = read_only_get(BASE_URL, SUBJECT_PATH, urlopen=urlopen)
        self.assertTrue(result['ok'])
        self.assertIn('request_source=agent_skill', result['url'])

    def test_network_error_includes_url_with_request_source(self):
        def _failing_urlopen(url, timeout=30):
            raise OSError('connection refused')

        result = read_only_get(BASE_URL, SUBJECT_PATH, urlopen=_failing_urlopen)
        self.assertFalse(result['ok'])
        self.assertIn('request_source=agent_skill', result['url'])


if __name__ == '__main__':
    unittest.main()
