log-request-id
=================

Log-Request-ID is an extension to handle request-IDs logs in popular python api frameworks.

Currently supported frameworks: flask

Requirements
------------

-  python (3.6+)

Instalation
-----------

Install using ``pip``

::

   pip install log-request-id


Usage
-----


1. Set ``LOG_REQUEST_ID_FRAMEWORK_SUPPORT`` to point to your framework of choice (section currently supported).

.. code:: txt

    LOG_REQUEST_ID_FRAMEWORK_SUPPORT=flask

2. Init request-ID handler

-  Flask, with ``log_request_id.flask.init_flask_request_id_handler``

.. code:: python

   from log_request_id import init_flask_request_id_handler

   def create_flask_app():
       app = Flask()
       init_flask_request_id_handler(app)

3. Change log format (optional)

At this stage ``request_id`` is already present in log data, request-ID will be under ``request_id`` key.

.. code:: python

   logging.basicConfig(level=logging.WARNING, format='%(filename)s:%(levelname)s:%(request_id)s - %(message)s')
   # or
   logging.getlogger().setformatter(logging.formatter("%(asctime)s:%(name)s:level=%(levelname)s:%(request_id)s - %(message)s"))


For more advanced logger configuration see `python's logging module <https://docs.python.org/3/library/logging.html>`_.

``Warning`` if you will be adding custom handler or custom logging initialization use ``log_request_id.logging.RequestIdLogRecordFactory`` or ``log_request_id.logging.RequestIdLogFilter``.
