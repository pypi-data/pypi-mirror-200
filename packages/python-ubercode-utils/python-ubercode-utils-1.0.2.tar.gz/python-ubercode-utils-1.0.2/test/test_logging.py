import unittest
from contextlib import redirect_stdout
from io import StringIO

from ubercode.utils import logging


class TestLogging(unittest.TestCase):

    # -------- helper utilities ----------
    def test_indent_string(self):
        """ Tests the indent string helper functon """
        # test normal whitespace stripping
        original_str = "test string"
        self.assertEqual(" test string", logging.indent_string(original_str, 1), "1 indent not working")
        self.assertEqual("    test string", logging.indent_string(original_str, 1*4), "4 indent not working")

    # -------- logging class ----------
    def test_log(self):
        tlog = logging.ColorLogger("test_log")
        # default should be info
        self.assertEqual("INFO", tlog.level)
        # reset to debug for checking all helper functions
        tlog.level = "DEBUG"
        self.assertEqual("DEBUG", tlog.level)
        # assert the helper functions like .info() match the base .log() as we expect
        for log_method in logging.ColorLogger.DEFAULT_COLOR_MAP.keys():
            log_level = log_method if log_method != 'SUCCESS' else 'INFO'
            with redirect_stdout(StringIO()) as sout:
                getattr(tlog, log_method.lower())(f"test {log_method.lower()} msg")
            helper_value = sout.getvalue()
            with redirect_stdout(StringIO()) as sout:
                tlog.log(f"test {log_method.lower()} msg", log_level=log_level, color=tlog.DEFAULT_COLOR_MAP[log_method])
            log_value = sout.getvalue()
            self.assertEqual(helper_value, log_value, "helper log method doesn't equal direct log method call")
        # assert for each log level we get output for the method and above and get None for below
        for logger_level in logging.ColorLogger.LOG_LEVELS:
            # set the logger level to the current iteration
            tlog.level = logger_level
            tlog_idx = logging.ColorLogger.LOG_LEVELS.index(logger_level)
            # at this logger level we loop again expecting None if level is lower and some length if eq or higher
            for log_method in logging.ColorLogger.DEFAULT_COLOR_MAP.keys():
                log_level = log_method if log_method != 'SUCCESS' else 'INFO'
                log_idx = logging.ColorLogger.LOG_LEVELS.index(log_level)
                with redirect_stdout(StringIO()) as sout:
                    getattr(tlog, log_method.lower())(f"test {log_method.lower()} msg")
                result = sout.getvalue()
                if log_idx < tlog_idx:
                    self.assertTrue(len(result) == 0, f"expected no msg; log idx [{log_idx}] logger idx [{tlog_idx}]")
                else:
                    self.assertTrue(len(result) > 0, f"expected log msg; log idx [{log_idx}] logger idx [{tlog_idx}]")


if __name__ == '__main__':
    unittest.main()
