import unittest
from dragline.defaultsettings import LogSettings


class LogTest(unittest.TestCase):

    def test_loggers(self):
        log = LogSettings(loggers={'test': {'handlers': ['info_file']}})
        testlogger = log.getLogger('test')
        self.assertEqual(len(testlogger.handlers), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
