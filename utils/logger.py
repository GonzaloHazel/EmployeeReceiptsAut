from loguru import logger
import os

LOGS_PATH = os.getenv("LOGS_PATH", "logs")  # Valor por defecto si no está en .env
os.makedirs(LOGS_PATH, exist_ok=True)

logger.add(
    f"{LOGS_PATH}/employee_receipts.log",
    rotation="1 week",
    retention="1 month",
    compression="zip",
    level="INFO",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
)
