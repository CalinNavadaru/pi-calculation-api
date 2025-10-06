import math
from decimal import Decimal, getcontext
from typing import Callable, Dict

from celery.app.task import Task


def madhava_leibniz_series(decimals: int, task: Task) -> float:
    print("madhava")
    pi = 0.0
    prev_pi = -2.0
    error = 10 ** (-decimals)
    k = 0
    max_steps = 10 ** (decimals + 1)

    while abs(pi - prev_pi) >= error:
        prev_pi = pi
        term = 4 * ((-1) ** k) / (2 * k + 1)
        pi += term
        k += 1

        if k % 10 == 0:
            task.update_state(
                state="PROGRESS",
                meta={
                    'progress': round(min(k / max_steps, 1.0), 2)
                }
            )

    task.update_state(state="PROGRESS", meta={'progress': 1.00})
    return round(pi, decimals)


def wallis_product(decimals: int, task: Task) -> float:
    print("wallis")
    pi = 1.0
    error = 10 ** (-decimals)
    max_steps = 10 ** (decimals + 1)

    k = 1
    while abs(2 * pi - math.pi) >= error:
        term = (4 * (k ** 2)) / (4 * (k ** 2) - 1)
        pi *= term
        k += 1

        if k % 10 == 0:
            task.update_state(
                state="PROGRESS",
                meta={
                    'progress': round(min(k / max_steps, 1.0), 2)
                }
            )

    task.update_state(state="PROGRESS", meta={'progress': 1.00})
    return round(2 * pi, decimals)


def pi_gauss_legendre(decimals: int, task: Task):
    print("gauss")
    getcontext().prec = decimals + 10

    a = Decimal(1)
    b = Decimal(1) / Decimal(2).sqrt()
    t = Decimal(1) / Decimal(4)
    p = Decimal(1)

    max_iterations = math.ceil(math.log2(decimals * 3.32192809489)) # log_2(10) approximately equal to 3.32192809489

    for i in range(max_iterations):
        a_next = (a + b) / 2
        b = (a * b).sqrt()
        t -= p * (a - a_next) ** 2
        a = a_next
        p *= 2

        task.update_state(
            state='PROGRESS',
            meta={'progress': round((i + 1) / max_iterations, 2)}
        )

    pi = (a + b) ** 2 / (4 * t)
    return round(pi, decimals)


CALCULATION_METHODS = {"madhava_leibniz": madhava_leibniz_series, "wallis": wallis_product, "gauss": pi_gauss_legendre}
CALCULATION_METHODS: Dict[str, Callable[[int, Task], None]]
