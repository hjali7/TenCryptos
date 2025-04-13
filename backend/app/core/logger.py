import logging

LOG_FILE_PATH = "logs/app.log"

# ساخت لاگر اصلی
logger = logging.getLogger("tencryptos")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(formatter)

# اضافه شدن به لاگر
logger.addHandler(file_handler)
