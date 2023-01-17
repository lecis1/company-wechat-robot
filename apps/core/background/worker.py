import logging
from django.apps import apps
from typing import List
import threading

from apps.core.apps import WorkerConfig
from apps.core.background.worker_handler import BaseSchedulerHandler
from django.utils.module_loading import import_string
from utils.threads import ThreadFactory, ThreadGuard


from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BlockingScheduler


class Worker:
    def __init__(self, worker_names=None):
        self.logger = logging.getLogger(
            r"C:\Users\dong\Desktop\个人文件\logs\company-wecaht-robot\error.log")
        self.error = logging.getLogger(
            r"C:\Users\dong\Desktop\个人文件\logs\company-wecaht-robot\running.log")
        self.guard = None
        self.guard_table = {}
        self.scheduler = None
        self.worker_names = worker_names
        self.all = []

    def load_workers(self):
        for app in apps.get_app_configs():
            app_workers: List[WorkerConfig] = getattr(app, "workers", None)
            if app_workers is None:
                continue
            for worker in app_workers:
                self.add_worker(app, worker)

    def add_worker(self, app, worker: WorkerConfig):
        worker_name = f"{app.name}__{worker.name}"
        if worker_name in self.all:
            raise Exception(f"worker name冲突; {worker_name}")
        if self.worker_names is not None and worker.name not in self.worker_names:
            return

        try:
            handler_cls = import_string(worker.handler)
        except Exception as e:
            self.logger.error(
                "%s: load %s failed; error: %s",
                app, worker.name, str(e)
            )
            return
        if worker.guard:
            handler = handler_cls()
            self.guard_table[worker_name] = ThreadFactory(
                cls=threading.Tread, target=handler, args=()
            )
        else:
            handler: BaseSchedulerHandler = handler_cls(
                scheduler=self.scheduler,
                name=worker.name,
                trigger=worker.trigger,
                trigger_args=worker.trigger_args,
                misfire_grace_time=10)
            handler.add_jobs()
        self.all.append(f"{app.name}__{worker.name}")
        self.logger.info(
            "加载worker, handler: %s; trigger: %s, trigger_args: %s",
            worker.handler,
            worker.trigger,
            worker.trigger_args
        )

    def start(self):
        self.scheduler = BlockingScheduler(
            executors={
                "default": ThreadPoolExecutor(50)
            },
            job_defaults={
                "misfire_grace_time": 10,
                "max_instances": 50
            }
        )
        self.guard = ThreadGuard(logger=self.logger, error_logger=self.error)
        self.load_workers()
        self.guard.set_guard_table(self.guard_table)
        self.guard.protect()
        self.scheduler.start()
