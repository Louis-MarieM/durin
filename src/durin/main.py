from durin.config.logger import logger

def run():
    logger.info("Hello from etl-pipeline !")
    logger.debug("Debug log from etl-pipeline !")
    logger.info("Breakpoint from etl-pipeline !")
    logger.info("Goodbye from etl-pipeline !")

def function_to_test():
    return "ok"
