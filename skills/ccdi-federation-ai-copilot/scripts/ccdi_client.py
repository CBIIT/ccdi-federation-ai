import json
from urllib.parse import urlencode

def live_execution_available() -> bool:
    return True


def build_request_url(base_url: str, path: str, params: dict | None = None) -> str:
    base = base_url.rstrip('/')
    route = path if path.startswith('/') else f'/{path}'
    if not params:
        return f'{base}{route}'

    return f'{base}{route}?{urlencode(params, doseq=True)}'


def read_only_get(
    base_url: str,
    path: str,
    params: dict | None = None,
    timeout_seconds: int = 30,
    max_retries: int = 0,
    urlopen=None,
) -> dict:
    """Execute a read-only GET request against the CCDI Federation API.

    Args:
        base_url: The base URL of the API (e.g. ``https://federation.ccdi.cancer.gov/api/v1/``).
        path: The API path relative to *base_url*.
        params: Optional query parameters to include in the request, such as
            endpoint-specific filters or pagination values.
        timeout_seconds: Request timeout in seconds.
        max_retries: Number of additional retry attempts on failure.
        urlopen: Injectable URL opener for testing; defaults to :func:`urllib.request.urlopen`.
    """
    if urlopen is None:
        from urllib.request import urlopen as _urlopen

        urlopen = _urlopen

    merged_params: dict = dict(params) if params else {}

    url = build_request_url(base_url, path, merged_params)
    attempts = max_retries + 1
    last_error = ''

    for _ in range(attempts):
        try:
            with urlopen(url, timeout=timeout_seconds) as response:
                payload = response.read().decode('utf-8')
                headers = dict(response.headers.items()) if hasattr(response, 'headers') else {}
                status = getattr(response, 'status', None)
                try:
                    parsed_payload = json.loads(payload)
                except json.JSONDecodeError:
                    return {
                        'ok': False,
                        'url': url,
                        'status': status,
                        'headers': headers,
                        'payload': None,
                        'errors': ['invalid_json_response'],
                    }

                return {
                    'ok': True,
                    'url': url,
                    'status': status,
                    'headers': headers,
                    'payload': parsed_payload,
                    'errors': [],
                }
        except OSError as exc:
            last_error = str(exc)

    return {
        'ok': False,
        'url': url,
        'status': None,
        'headers': {},
        'payload': None,
        'errors': [last_error] if last_error else ['unknown_error'],
    }
