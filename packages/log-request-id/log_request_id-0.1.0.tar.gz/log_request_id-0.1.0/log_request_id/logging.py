import logging
from .request_id import DEFAULT_REQUEST_ID_OBJECT_NAME, current_request_id


class RequestIdLogRecordFactory:
    """wrapper around default logging factory, adding request_id info to extra"""

    def __init__(self, **extra_log_record_kwargs):
        self.extra_log_record_kwargs = extra_log_record_kwargs
        self.old_factory = logging.getLogRecordFactory()

    def __call__(self, *args, **kwargs):
        """create record with added extra attribute"""
        log_record = self.old_factory(*args, **kwargs)

        if self.extra_log_record_kwargs:
            for key, value in self.extra_log_record_kwargs.items():
                setattr(log_record, key, value)

        setattr(log_record, DEFAULT_REQUEST_ID_OBJECT_NAME, current_request_id())

        return log_record


class RequestIdLogFilter(logging.Filter):
    """wrapper around default logging Filter, adding request_id info to `log_record`"""

    def filter(self, log_record):
        """add request_id to log_record under DEFAULT_REQUEST_ID_OBJECT_NAME"""

        setattr(log_record, DEFAULT_REQUEST_ID_OBJECT_NAME, current_request_id())
        return log_record
