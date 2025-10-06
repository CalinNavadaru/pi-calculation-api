import math

from celery.app.task import Task


def madhava_leibniz_series(decimals: int, task: Task) -> float:
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
                    'progress': round(min(k / max_steps, 1.0), 3)
                }
            )


    task.update_state(state="PROGRESS", meta={'progress': 1.00})
    return round(pi, decimals)


def wallis_product(decimals: int, task: Task) -> float:
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
                    'progress': round(min(k / max_steps, 1.0), 3)
                }
            )

    task.update_state(state="PROGRESS", meta={'progress': 1.00})
    return round(2 * pi, decimals)
