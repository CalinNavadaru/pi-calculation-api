import sys
import time

from celery import shared_task
from celery.app.task import Task
from pi_calculator.pi_calculation_utils import wallis_product, madhava_leibniz_series


@shared_task(bind=True)
def compute_pi(self: Task, decimals, method: str):
    print(f"Starting the computation of pi with {decimals} decimals precision using {method}.")
    if method == "wallis":
        result = wallis_product(decimals, self)
    else:
        result = madhava_leibniz_series(decimals, self)
    print(f"Finished computing!")
    return {"progress": 1.0, "result": result}