from typing import Any, Dict
from django.apps import AppConfig
from dataclasses import dataclass


@dataclass()
class WorkerConfig:
    name: str  # 名称
    handler: Any  # 处理类
    trigger: str = None
    trigger_args: Dict = None
    guard: bool = False


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name: str = 'apps.core'
    default = True
    dependencies = None
