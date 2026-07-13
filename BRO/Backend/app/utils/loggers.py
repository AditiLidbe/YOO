import logging

logger=logging.getLogger("TASKFLOW")
logger.setLevel(logging.INFO)
file_handler=logging.FileHandler("taskflow.log")
formatter=logging.Formatter("%(asctime)s: %(levelname)s : %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
