import logging
import time
from multiprocessing import Process

from django.conf import settings
from utils.logs.logs import InfoLog

from .worker import Worker


class BackgroundManager(object):
    """
    管理后台进程
    """

    def __init__(self):
        self.processes = {}
        self.logger = logging.getLogger(settings.RUNNING_LOG_NAME)
        self.error = logging.getLogger(settings.ERROR_LOG_NAME)

    def start_worker_process(self):
        w = Worker()
        self.processes["worker"] = {
            "target": w.start,
            "process": Process(target=w.start)
        }

    def guard(self):
        while True:
            for name, config in self.processes.items():
                if not config["process"].is_alive():
                    p = Process(target=config["target"])
                    config["process"] = p
                    p.start()
                    self.logger.info(InfoLog(f"检测到{name}进程未启动; 自动启动进程"))
            time.sleep(3)

    def start(self):
        self.start_worker_process()
        self.guard()
