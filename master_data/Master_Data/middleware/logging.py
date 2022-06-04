import json
import logging
import time

logging.basicConfig(level=logging.INFO, filename="log", encoding="utf-8")


# Custom middleware to log requests and responses
class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        response_ms = duration * 1000
        info = json.dumps({
            "source": request.META["REMOTE_ADDR"],
            "destination": request.headers["Host"],
            "method": request.method,
            "resource": request.path,
            "body": str(request.POST),
            "response_ms": str(response_ms),
            "response": str(response.data),
            "headers": dict(request.headers),
            "metadata": {str(k): str(v) for k, v in request.META.items()},
        }, indent=2)
        logging.info(info)

        return response
