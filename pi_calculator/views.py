from celery.result import AsyncResult
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from pi_calculator.tasks import compute_pi


# Create your views here.

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

        if method not in ["madhava_leibniz", "wallis"]:
            raise ValidationError({"method": "The 'method' parameter must be 'wallis' or 'madhava_leibniz'"})

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
            response["progress"] = result.info.get("progress", None)

        return Response(response)
