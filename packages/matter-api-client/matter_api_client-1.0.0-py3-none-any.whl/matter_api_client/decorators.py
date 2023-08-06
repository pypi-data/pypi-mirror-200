import logging

import itertools
import time
from functools import wraps

from .exceptions import APIClientError


def retry_if_failed(method, delays=(0, 1, 5)):
    @wraps(method)
    def _impl(*args, **kwargs):
        for delay in itertools.chain(delays, [None]):
            try:
                result = method(*args, **kwargs)
            except APIClientError as ex:
                operation_successful = False
                needs_retry = True
                exc = ex
            else:
                operation_successful = True
                needs_retry = False

            if not needs_retry or delay is None:
                if not operation_successful:
                    raise exc
                return result
            else:
                logging.warning(f"Lost connection to API. Retrying in {delay} seconds...")
                time.sleep(delay)

    return _impl
