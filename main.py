from libs.log import init_logger

if __name__ == "__main__":
    logger = init_logger(service="json_log")
    logger.info("xxxxx, abc:%s", 15, extra={"task_id": 15})
    try:
        15/0
    except Exception, ex:
        logger.error(ex, exc_info=True)


