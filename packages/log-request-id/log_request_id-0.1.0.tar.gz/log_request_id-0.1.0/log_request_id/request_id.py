import uuid
import functools
import os

DEFAULT_REQUEST_ID_OBJECT_NAME: str = os.getenv('DEFAULT_REQUEST_ID_OBJECT_NAME', default='request_id')
REQUEST_ID_CONTEXT_GETTERS = []


def current_request_id():
    for request_id_context_getter in REQUEST_ID_CONTEXT_GETTERS:
        request_id = request_id_context_getter()

        if request_id is not None:
            return request_id


def register_context_getter(skip=False):
    @functools.wraps
    def _wrap(getter):
        if getter in REQUEST_ID_CONTEXT_GETTERS and not skip:
            REQUEST_ID_CONTEXT_GETTERS.append(getter)

        return getter

    return _wrap


def default_request_id_generator():
    return str(uuid.uuid4())
