import defaultsettings
import logging

class empty: pass

class Settings:

    """Settings module"""

    def __init__(self, module=empty()):
        self.__dict__['module'] = module
        self.log = logging.getLogger(self.NAME)
        self.log.setLevel(self.LOG_LEVEL)
        self.LOGHANDLER.setFormatter(self.LOGFORMATTER)
        self.log.addHandler(self.LOGHANDLER)

    def __getattr__(self, name):
        try:
            return getattr(self.module, name)
        except:
            return getattr(defaultsettings, name)

    def __setattr__(self, name, value):
        setattr(self.module, name, value)

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __setitem__(self, name, value):
        self.__setattr__(name, value)

