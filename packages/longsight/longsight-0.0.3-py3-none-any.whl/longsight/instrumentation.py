import functools
import logging
from contextlib import AbstractContextManager
from contextvars import ContextVar
from logging import LogRecord
from types import TracebackType
from typing import Callable
from typing import Optional
from typing import Type
from uuid import uuid4


from aws_lambda_powertools import Logger, Metrics, Tracer, single_metric
from aws_lambda_powertools.metrics import MetricUnit
from fastapi import Request
from fastapi.routing import APIRoute
from starlette.datastructures import MutableHeaders
from starlette.responses import Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from claws import aws_utils

correlation_id: ContextVar[Optional[str]] = ContextVar(
    "correlation_id", default=None
)

logger: Logger = Logger()
metrics: Metrics = Metrics(namespace="default")


class LoggerRouteHandler(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def route_handler(request: Request) -> Response:
            ctx = {
                "path": request.url.path,
                "route": self.path,
                "method": request.method,
            }
            logger.append_keys(fastapi=ctx)

            with single_metric(
                name="RequestCount",
                unit=MetricUnit.Count,
                value=1,
                namespace=metrics.namespace,
            ) as metric:
                metric.add_dimension(
                    name="route", value=f"{request.method} {self.path}"
                )

            return await original_route_handler(request)

        return route_handler


class CorrelationIdFilter(logging.Filter):
    """Logging filter to attach correlation IDs to log records"""

    def __init__(
        self,
        name: str = "",
        uuid_length: Optional[int] = None,
        default_value: Optional[str] = None,
    ):
        super().__init__(name=name)
        self.uuid_length = uuid_length
        self.default_value = default_value

    def filter(self, record: "LogRecord") -> bool:
        """
        Attach a correlation ID to the log record.
        """
        record.correlation_id = correlation_id.get(self.default_value)
        return True


class AWSCorrelationIdMiddleware:
    def __init__(
        self,
        app: "ASGIApp",
        header_name: str = "X-Request-ID",
    ):
        self.app = app
        self.header_name = header_name

    async def __call__(
        self, scope: "Scope", receive: "Receive", send: "Send"
    ) -> None:
        """
        Load request ID from headers if present. Generate one otherwise.
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        aws_context = scope.get("aws.context")
        id_value = None

        if hasattr(aws_context, "aws_request_id"):
            id_value = aws_context.aws_request_id

        headers = MutableHeaders(scope=scope)

        if not id_value:
            # Load request ID from the request headers
            header_value = headers.get(self.header_name.lower())

            if not header_value:
                id_value = uuid4().hex
            else:
                id_value = header_value

        headers[self.header_name] = id_value

        correlation_id.set(id_value)

        async def handle_outgoing_request(message: "Message") -> None:
            if (
                message["type"] == "http.response.start"
                and correlation_id.get()
            ):
                headers = MutableHeaders(scope=message)
                headers.append(self.header_name, correlation_id.get())

            await send(message)

        await self.app(scope, receive, handle_outgoing_request)
        return


def instrument_with_aws(bucket: str):
    """
    This is a decorator that will instrument a FastAPI route and provide AWS.
    :param bucket: the bucket for the AWSClient to use.
    :return: the wrapped function
    """

    def wrap(f):
        @functools.wraps(f)
        async def wrapped_f(*args, **kwargs):
            from claws import aws_utils

            # create the boto3 objects
            aws_connector = aws_utils.AWSConnector(bucket=bucket)

            fastapi_request = kwargs.get("request", None)
            fastapi_app = fastapi_request.app if fastapi_request else None

            aws_context = (
                fastapi_request.scope.get("aws.context", {})
                if fastapi_request
                else {}
            )

            with Instrumentation(
                aws_connector=aws_connector,
                fastapi_app=fastapi_app,
                request=fastapi_request,
            ) as metric_logger:
                if hasattr(aws_context, "aws_request_id"):
                    metric_logger.logger.info(
                        f"Set correlation ID to AWS "
                        f"requestId: {aws_context.aws_request_id}"
                    )

                kwargs["instrumentation"] = metric_logger
                return await f(*args, **kwargs)

        return wrapped_f

    return wrap


def instrument():
    """
    This is a decorator that will instrument a FastAPI route.
    :return: the wrapped function
    """

    def wrap(f):
        @functools.wraps(f)
        async def wrapped_f(*args, **kwargs):
            fastapi_request = kwargs.get("request", None)
            fastapi_app = fastapi_request.app if fastapi_request else None

            aws_context = (
                fastapi_request.scope.get("aws.context", {})
                if fastapi_request
                else {}
            )

            with Instrumentation(
                aws_connector=None,
                fastapi_app=fastapi_app,
                request=fastapi_request,
            ) as metric_logger:
                if hasattr(aws_context, "aws_request_id"):
                    metric_logger.logger.info(
                        f"Set correlation ID to AWS "
                        f"requestId: {aws_context.aws_request_id}"
                    )

                kwargs["instrumentation"] = metric_logger
                return await f(*args, **kwargs)

        return wrapped_f

    return wrap


class Instrumentation(AbstractContextManager):
    """
    A context manager that provides instrumentation on AWS CloudWatch.
    """

    def __exit__(
        self,
        __exc_type: Type[BaseException],
        __exc_value: BaseException,
        __traceback: TracebackType,
    ) -> bool:
        if __exc_value:
            self.logger.error(f"Request shutdown with error: {__exc_value}.")
            raise __exc_value

        return True

    def __init__(
        self,
        aws_connector: aws_utils.AWSConnector = None,
        namespace: str = "LabsAPI",
        fastapi_app=None,
        request: Request = None,
    ):
        metrics.namespace = namespace
        self._aws_connector = aws_connector
        self._namespace = namespace
        self._app = fastapi_app

        self._logger: Logger = logger
        self._metrics: Metrics = metrics
        self._tracer: Tracer = Tracer()

        self._logger.addFilter(CorrelationIdFilter())

        if self._aws_connector:
            self._aws_connector.instrumentation = self

        self.request_id = None
        self._request = request

    @property
    def logger(self):
        return self._logger

    @property
    def aws_connector(self) -> aws_utils.AWSConnector:
        return self._aws_connector

    @aws_connector.setter
    def aws_connector(self, value):
        self._aws_connector = value
        self._aws_connector.instrumentation = self

    @property
    def metrics(self):
        return self._metrics

    @property
    def namespace(self):
        return self._namespace


class CorrelationIDFilter(logging.Filter):
    """
    This class acts as a context filter for logs. This adds the Correlation ID
    to log entries.
    """

    def __init__(self, request: Request):
        super().__init__()
        self._request = request

    def filter(self, record):
        try:
            record.correlation_id = self._request.state.correlation_id
        except:
            record.correlation_id = None
        return True
