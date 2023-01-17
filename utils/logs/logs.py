from . import colors


class CommonLog:

    def __init__(self, desc, level='INFO', color=True, details=None):
        self.desc = desc
        self.color = color
        self.level = level.upper()
        self.details = details

    def get_string_wrapper(self):
        level_map = {
            'INFO': colors.ok_wrapper,
            'ERROR': colors.fail_wrapper,
            'WARNING': colors.warning_wrapper,
            'DEBUG': colors.debug_wrapper
        }

        return level_map[self.level]

    def build_log_string(self):
        log_strings = [f'描述: {self.desc};']
        if self.details:
            for key, value in self.details.items():
                log_strings.append(f'{key}: {value};')

        return ' '.join(log_strings)

    def __str__(self):
        wrapper = self.get_string_wrapper()
        return wrapper(self.build_log_string())


class InfoLog(CommonLog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = 'INFO'


class WarningLog(CommonLog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = 'WARNING'


class ErrorLog(CommonLog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = 'ERROR'


class DebugLog(CommonLog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = 'DEBUG'
