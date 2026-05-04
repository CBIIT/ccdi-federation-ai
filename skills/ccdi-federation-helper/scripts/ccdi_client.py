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
    timeout_seconds: int = 10,
    max_retries: int = 0,
    urlopen=None,
) -> dict:
    if urlopen is None:
        from urllib.request import urlopen as _urlopen

        urlopen = _urlopen

    url = build_request_url(base_url, path, params)
    attempts = max_retries + 1
    last_error = ''

    for _ in range(attempts):
        try:
            with urlopen(url, timeout=timeout_seconds) as response:
                payload = response.read().decode('utf-8')
                try:
                    parsed_payload = json.loads(payload)
                except json.JSONDecodeError:
                    return {
                        'ok': False,
                        'url': url,
                        'payload': None,
                        'errors': ['invalid_json_response'],
                    }

                return {
                    'ok': True,
                    'url': url,
                    'payload': parsed_payload,
                    'errors': [],
                }
        except OSError as exc:
            last_error = str(exc)

    return {
        'ok': False,
        'url': url,
        'payload': None,
        'errors': [last_error] if last_error else ['unknown_error'],
    }