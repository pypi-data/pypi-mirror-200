import unittest
from contextlib import redirect_stdout
from io import StringIO

from ubercode.utils import logging
from ubercode.utils import dataframe


class TestDataframe(unittest.TestCase):

    # -------- dataframe logging class ----------
    def test_log(self):
        tlog = dataframe.DataframeLogger("test_log")
        # test that we can print a string with a label instead of a dataframe
        with redirect_stdout(StringIO()) as sout:
            tlog.dataframe("Test Dataframe", "Test Label")
        log_lines = sout.getvalue()
        label_string = logging.TermColor.OKBLUE + "Test Label"
        self.assertTrue(str(log_lines).startswith(label_string))
        # always doesn't have a color so lets change the color and test for it
        with redirect_stdout(StringIO()) as sout:
            tlog.dataframe("Test Dataframe", "Test Label", color="WARN")
        log_lines = sout.getvalue()
        content_string = logging.TermColor.WARNING + "Test Dataframe"
        self.assertTrue(content_string in str(log_lines))


if __name__ == '__main__':
    unittest.main()
