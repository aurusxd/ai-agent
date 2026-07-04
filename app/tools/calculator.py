from app.services.logger import log


def calc(expression: str):
    log.info(f"Зашел в calculator: {expression}")
    return eval(expression)
