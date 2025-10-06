from celery.result import AsyncResult
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from pi_calculator.pi_calculation_utils import CALCULATION_METHODS
from pi_calculator.tasks import compute_pi


class CalculatePiView(APIView):

    def get(self, request: Request):
        decimals = request.query_params.get('n')
        method = request.query_params.get('method')
        if decimals is None:
            raise ValidationError({"n": "The 'n' parameter is required."})

        if method is None:
            raise ValidationError({"method": "The 'method' parameter is required."})

        try:
            decimals = int(decimals)
            if decimals <= 0:
                raise ValueError
        except ValueError:
            raise ValidationError({"n": "The 'n' parameter must be a positive integer."})

        if method not in CALCULATION_METHODS:
            raise ValidationError({"method": f"The 'method' parameter must be {CALCULATION_METHODS.keys()}; Provided value: {method}"})

        cached_value = cache.get("n")
        if cached_value:
            return Response({"result": cached_value})
        async_result = compute_pi.delay(decimals, method)

        return Response({"id_task": async_result.id})


class CheckProgressView(APIView):

    def get(self, request: Request):
        task_id = request.query_params.get("task_id")

        if task_id is None:
            raise ValidationError({"task_id": "The 'task_id' parameter is required."})

        result = AsyncResult(task_id)
        response = {
            "task_id": task_id,
            "status": result.status,
            "progress": None,
            "result": None
        }

        if result.status == 'PENDING':
            response["message"] = "Task ID not found or not started yet."

        elif result.state == 'PROGRESS':
            response["progress"] = result.info.get("progress", None)

        elif result.state == 'SUCCESS':
            response["result"] = result.result.get("result", None)
            cache.set("n", response["result"], 30)
            response["progress"] = result.info.get("progress", None)

        return Response(response)
