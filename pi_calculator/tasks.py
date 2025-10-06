from celery import shared_task
from celery.app.task import Task
from pi_calculator.pi_calculation_utils import CALCULATION_METHODS


@shared_task(bind=True)
def compute_pi(self: Task, decimals, method: str):
    print(f"Starting the computation of pi with {decimals} decimals precision using {method}.")
    result = CALCULATION_METHODS[method](decimals, self)
    print(f"Finished computing!")
    return {"progress": 1.0, "result": str(result), "n": decimals}