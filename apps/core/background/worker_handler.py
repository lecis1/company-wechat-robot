from apscheduler.schedulers.background import BaseScheduler
import logging

from typing import Callable, List


class BaseSchedulerHandler(object):

    def __init__(
        self,
        scheduler: BaseScheduler,
        name=None,
        trigger="date",
        trigger_args=None,
        misfire_grace_time=10
    ) -> None:
        self.scheduler = scheduler
        self.name = name
        self.trigger = trigger
        self.trigger_args = trigger_args if trigger_args else {}
        self.misfire_grace_time = misfire_grace_time
        self.logger = logging.getLogger(
            r"C:\Users\dong\Desktop\个人文件\logs\company-wecaht-robot\error.log")
        self.exception = logging.getLogger(
            r"C:\Users\dong\Desktop\个人文件\logs\company-wecaht-robot\running.log")

    def tasks(self) -> List[Callable]:
        return []

    def add_jobs(self):
        for task in self.tasks():
            if self.trigger_args is None:
                trigger_args = {}
            else:
                trigger_args = self.trigger_args
            self.scheduler.add_job(
                task,
                trigger=self.trigger,
                misfire_grace_time=self.misfire_grace_time,
                **trigger_args
            )
