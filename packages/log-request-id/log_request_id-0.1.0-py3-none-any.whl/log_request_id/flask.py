import os
from typing import Optional
from .request_id import DEFAULT_REQUEST_ID_OBJECT_NAME, default_request_id_generator, register_context_getter


@register_context_getter(skip=os.getenv('LOG_REQUEST_ID_FRAMEWORK_SUPPORT') == 'flask')
def get_flask_context_request_id(request_id_object_name=None):
    from flask import g, has_request_context

    request_id_object_name = request_id_object_name or DEFAULT_REQUEST_ID_OBJECT_NAME
    return g.get(request_id_object_name, None) if has_request_context() else None


def init_flask_request_id_handler(app, request_id_object_name: Optional[str] = None, request_id_generator=None):
    app.before_request(lambda : propagate_flask_request_id(request_id_object_name, request_id_generator))


def propagate_flask_request_id(request_id = None, request_id_object_name: Optional[str] = None, request_id_generator=None):
    from flask import g, has_request_context

    request_id_generator = request_id_generator or default_request_id_generator
    request_id_object_name = request_id_object_name or DEFAULT_REQUEST_ID_OBJECT_NAME
    request_id = request_id or request_id_generator()

    if has_request_context() and g.get(request_id_object_name) is None:
        setattr(g, request_id_object_name, request_id_generator())


def suppress_flask_request_id(request_id_object_name: Optional[str] = None):
    from flask import g, has_request_context
    request_id_object_name = request_id_object_name or DEFAULT_REQUEST_ID_OBJECT_NAME

    if has_request_context():
        g.pop(request_id_object_name, None)
