import asyncio
import sys
import unittest
from unittest.mock import MagicMock

from fastapi import FastAPI, Request
from starlette.datastructures import MutableHeaders
from starlette.responses import Response
from starlette.testclient import TestClient
from starlette.types import Receive, Scope, Send

sys.path.append("../../")
sys.path.append("../src")
sys.path.append("../src/longsight")

from instrumentation import (
    AWSCorrelationIdMiddleware,
    CorrelationIDFilter,
    Instrumentation,
    LoggerRouteHandler,
    instrument,
    instrument_with_aws,
)

app = FastAPI()
app.add_middleware(AWSCorrelationIdMiddleware)
app.router.route_class = LoggerRouteHandler


@app.get("/dummy_route")
@instrument()
async def dummy_route(request: Request, instrumentation=None):
    return {"success": True}


class TestAWSCorrelationIdMiddleware(unittest.TestCase):
    def setUp(self) -> None:
        self.scope = {"type": "http", "headers": {}}
        self.receive: Receive = MagicMock()
        self.send: Send = MagicMock()

    async def mock_app(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        pass

    def test_aws_correlation_id_middleware(self):
        aws_middleware = AWSCorrelationIdMiddleware(self.mock_app)

        async def run_test():
            await aws_middleware(self.scope, self.receive, self.send)

        asyncio.run(run_test())

        headers = MutableHeaders(scope=self.scope)
        self.assertIsNotNone(headers.get("X-Request-ID"))


class TestInstrumentation(unittest.TestCase):
    def test_instrumentation_context_manager(self):
        request = MagicMock()
        with Instrumentation(request=request) as instr:
            self.assertIsNotNone(instr.logger)
            self.assertIsNotNone(instr.metrics)

    def test_instrumentation_error_handling(self):
        request = MagicMock()
        with self.assertRaises(ValueError):
            with self.assertLogs(level="ERROR") as log_cm:
                with Instrumentation(request=request) as instr:
                    raise ValueError("Test error")

        self.assertIn(
            "Request shutdown with error: Test error", log_cm.output[0]
        )


class TestInstrumentDecorator(unittest.TestCase):
    def test_instrument_decorator(self):
        with TestClient(app) as client:
            response = client.get("/dummy_route")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"success": True})


class TestInstrumentWithAWSDecorator(unittest.TestCase):
    def test_instrument_with_aws(self):
        @app.get("/test_aws")
        @instrument_with_aws(bucket="test_bucket")
        async def test_route(request: Request, instrumentation=None):
            self.assertIsNotNone(instrumentation)
            self.assertIsNotNone(instrumentation.aws_connector)

            return Response(status_code=200)

        with TestClient(app) as client:
            # Make a request to the test route
            response = client.get("/test_aws")

            # Assert that the response status code is 200
            self.assertEqual(response.status_code, 200)


class TestCorrelationIDFilter(unittest.TestCase):
    def setUp(self):
        self.request = MagicMock()
        self.request.state = MagicMock()
        self.request.state.correlation_id = "test_correlation_id"

    def test_correlation_id_filter(self):
        correlation_id_filter = CorrelationIDFilter(self.request)
        log_record = MagicMock()

        result = correlation_id_filter.filter(log_record)

        self.assertEqual(log_record.correlation_id, "test_correlation_id")
        self.assertTrue(result)
