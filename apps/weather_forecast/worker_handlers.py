import requests
from apps.core.background.worker_handler import BaseSchedulerHandler, BaseScheduler

import json


class WeatherForecastHandler(BaseSchedulerHandler):

    def __init__(
        self,
        scheduler: BaseScheduler,
        name=None,
        trigger="date",
        trigger_args=None,
        misfire_grace_time=10,
    ) -> None:
        super().__init__(scheduler, name, trigger, trigger_args, misfire_grace_time)
        self.city_data_info = r"C:\Users\dong\Desktop\个人文件\个人应用\company_wecaht_robot\data\city_data_info.json"
        self.city_code_info = r"C:\Users\dong\Desktop\个人文件\个人应用\company_wecaht_robot\data\city_code.json"

    def tasks(self):
        return [self.weather_forecast]

    def weather_forecast(self):
        root_url = "http://t.weather.itboy.net/api/weather/city/"
        city_code = self.get_city_code()

        weather_data_url = root_url+city_code
        city_info = self.get_city_info(weather_data_url)
        send_info = ""
        if city_info:
            send_info = self.fomrat_info(city_info)
        if send_info:

    def get_city_code(self):
        try:
            with open(self.city_code_info, 'r') as f:
                content = json.loads(f.read())
                return content
        except:
            return "101270101"

    def get_city_info(self, url):
        response = requests.get(url=url,
                                verify=False, stream=True, timeout=60)

        if response.status_code == 200:
            with open(self.city_data_info, "w", encoding="utf8") as f:
                f.write(response.text)

            message = json.loads(response.text)
            return message
        else:
            print("获取城市天气数据失败，请检查")
            return

    def fomrat_info(infos):
        send_info = ""
        info_template = "{datetime} {weekday}; 天气: {type}; 温度: {low}~{high} ℃; 日出: {sunrise}, 日落: {sunset}; 温馨提示: {notice}"
        for info in info.get("data", {}).get("forcast", []):
            datetime = info.get("ymd")
            weekday = info.get("week")
            type = info.get("type")
            high = info.get("high")
            low = info.get("low")
            sunrise = info.get("sunrise")
            sunset = info.get("sunset")
            notice = info.get("notice")
            format_info = info_template.format(
                datetime=datetime,
                weekday=weekday,
                type=type,
                low=low,
                high=high,
                sunrise=sunrise,
                sunset=sunset,
                notice=notice
            )
            send_info += format_info + "\n"
        if send_info:
            send_info = "未来15天天气情况:\n" + send_info
        return send_info
