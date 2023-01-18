from django.apps import AppConfig
from apps.core.apps import WorkerConfig


class WeatherForecastConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.weather_forecast'
    default = True
    app_url_conf = "apps.plugins.dpiv6.urls"
    websocket_message_router = "apps.plugins.dpiv6.websocket_messages"
    workers = [
        WorkerConfig(
            name="weather-forecast",
            handler="apps.weather_forecast.worker_handlers.WeatherForecastHandler",
            trigger="cron",
            trigger_args={"hour": "19", "minute": "30", "second": "0"},
        ),
    ]
