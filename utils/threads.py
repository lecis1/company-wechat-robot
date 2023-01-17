import logging
import os
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from queue import Queue, Full
from typing import Callable, Dict, Type, Optional, Union, List
from utils.logs.logs import DebugLog, ErrorLog, InfoLog


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ThreadFactory:
    """
    线程工厂类，实现重启线程的功能
    """

    def __init__(self, cls: Type[threading.Thread], *args, **kwargs):
        self.cls = cls
        self.args = args
        self.thread: Optional[threading.Thread] = None
        self.kwargs = kwargs
        self.thread = self.cls(*self.args, **self.kwargs)

    def start(self):
        self.thread.start()

    def restart(self) -> int:
        if self.thread and not self.thread.is_alive():
            self.thread = self.cls(*self.args, **self.kwargs)
            self.thread.start()
            return 0
        return 1


class ThreadGuard(metaclass=Singleton):
    """
    线程守卫，防止重要线程崩溃，自动拉起挂掉的线程。
    ======================================
    """

    def __init__(self, sleep_time: int = 3,
                 running_log_name=None,
                 error_log_name=None,
                 logger=None,
                 error_logger=None):
        self.guard_table: Dict[str, ThreadFactory] = {}
        self.guard_thread = None
        self.sleep_time = sleep_time
        self.running_log_name = running_log_name
        self.error_log_name = error_log_name
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(self.running_log_name)
        if error_logger:
            self.error = error_logger
        else:
            self.error = logging.getLogger(self.error_log_name)
        self.pid = os.getpid()

    def set_guard_table(self, guard_table: Dict[str, ThreadFactory]):
        self.guard_table = guard_table

    def protect(self, block=False):
        if not block:
            self.guard_thread = threading.Thread(
                target=self.guard, daemon=True)
            self.guard_thread.start()
        else:
            self.guard()

    def guard(self):
        while True:
            time.sleep(self.sleep_time)
            self.logger.debug(
                DebugLog(f'''检查线程状态; 当前监控线程: {list(self.guard_table.keys())}'''))
            try:
                for name, tf in self.guard_table.items():
                    if tf and tf.restart() == 0:
                        self.logger.info(InfoLog(
                            desc=f'检测到线程未启动，自动启动线程; name: {name}; 所属进程：{self.pid}; 线程ID: {tf.thread.ident}'
                        ))
            except Exception as e:
                self.logger.error(ErrorLog(
                    f'线程守护异常；{self.guard_table}'
                ))
                self.logger.exception(e)
